import axios from "axios";
import cluster from "cluster";
import os from "os";
import { performance } from "perf_hooks";

const totalCpu = os.cpus().length;
const ENABLE_CLUSTERING = true;
const ENABLE_LOGGING = false;
const RUN_SEQUENTIAL = false;
const RUN_CONCURRENT = true;

async function sequential_latency_benchmark(requestCount = 1000) {
  let failureCount = 0;
  let successCount = 0;
  const latency = [];

  for (let iteration = 1; iteration <= 1000; iteration++) {
    const start = performance.now();
    try {
      const result = await axios.get("https://whoami.demo-lab.dev");
      if (result.status == 200) {
        successCount++;
      } else {
        failureCount++;
      }
    } catch (err) {
      failureCount++;
    }
    const stop = performance.now();
    latency.push(stop - start);
  }

  const maxLatency = Math.max(...latency);
  const minLatency = Math.min(...latency);

  const sum = latency.reduce((a, b) => a + b, 0);
  const avgLatency = (sum / latency.length) || 0;

  return {
    requestCount,
    successCount,
    failureCount,
    minLatency,
    maxLatency,
    avgLatency,
  }
}

async function concurrent_latency_benchmark(requestCount = 1000) {
  let failureCount = 0;
  let successCount = 0;
  const promises = [];

  const start = performance.now();
  for (let iteration = 1; iteration <= 1000; iteration++) {
    promises.push(axios.get("https://whoami.demo-lab.dev"));
  }
  const settled = await Promise.allSettled(promises);
  const stop = performance.now();
  const latency = (stop - start);
  
  settled.forEach(result => {
    if (result.status == "fulfilled" && result.value.status == 200) {
      successCount++;
    } else {
      failureCount++;
    }
  })

  return {
    requestCount,
    successCount,
    failureCount,
    latency,
  }
}

function log_sequential_benchmark_results(results = {}, name = "") {
  const {
    requestCount,
    successCount,
    failureCount,
    minLatency,
    maxLatency,
    avgLatency,
  } = results;

  if (name) {
    console.log(`\nResults for ${name}`)
  }

  console.log("Requests");
  console.log("---------------");
  console.log(`Total: ${requestCount}`)
  console.log(`Success: ${successCount}`);
  console.log(`Failure: ${failureCount}\n`);

  console.log("Latency");
  console.log("---------------");
  console.log(`Min: ${minLatency}`);
  console.log(`Max: ${maxLatency}`);
  console.log(`Avg: ${avgLatency}\n`);
}

async function run_sequential_benchmark() {
  const start = performance.now();
  if (ENABLE_CLUSTERING) {
    if (cluster.isPrimary) {
      console.log("Running multi-threaded sequential benchmark...");
      console.log(`Number of threads is ${totalCpu}`);
      console.log(`Master ${process.pid} is running`);
    
      for (let i=0; i<totalCpu; i++){
        cluster.fork();
      }

      let finishedCount = 0;
      cluster.on("exit", (worker, code, signal) => {
        finishedCount++;
        if (finishedCount == totalCpu) {
          const stop = performance.now();
          console.log(`Total Time - ${stop-start} ms`)
        }
      })
    } else {
      console.log(`Worker ${process.pid} running benchmark...`);
      const results = await sequential_latency_benchmark();
      log_sequential_benchmark_results(results, process.pid);
      process.exit();
    }
  } else {
    console.log("Running single-thread benchmark...\n\n");
    const results = await sequential_latency_benchmark();
    log_sequential_benchmark_results(results);
    const stop = performance.now();
    console.log(`Total Time - ${stop-start} ms`)
  }
}

async function run_concurrent_benchmark() {
  const start = performance.now();
  if (ENABLE_CLUSTERING) {
    if (cluster.isPrimary) {
      console.log("Running multi-threaded concurrent benchmark...");
      console.log(`Number of threads is ${totalCpu}`);
      console.log(`Master ${process.pid} is running`);
    
      for (let i=0; i<totalCpu; i++){
        cluster.fork();
      }

      let finishedCount = 0;
      cluster.on("exit", (worker, code, signal) => {
        finishedCount++;
        if (finishedCount == totalCpu) {
          const stop = performance.now();
          console.log(`Total Time - ${stop-start} ms`)
        }
      })
    } else {
      console.log(`Worker ${process.pid} running benchmark...`);
      const results = await concurrent_latency_benchmark();
      console.log(process.pid, results)
      process.exit();
    }
  } else {
    console.log("Running single-thread concurrent benchmark...\n\n");
    const results = await concurrent_latency_benchmark();
    console.log(results);
    const stop = performance.now();
    console.log(`Total Time - ${stop-start} ms`)
  }
}

if (RUN_SEQUENTIAL) {
  await run_sequential_benchmark();
}

if (RUN_CONCURRENT) { 
  await run_concurrent_benchmark();
}
