import concurrent.futures
import time
from etcd3gw.client import Etcd3Client
import logging
import os
import csv
import pandas as pd

try:
    # Python 3.8 : time.clock was deprecated and removed.
    from time import perf_counter as clock
except ImportError:
    from time import clock

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EtcdClient")
PATH = os.getcwd()


def write_to_csv(threads, latency):
    csvPath = PATH + "/etcd_Request_Latency.csv"
    if not os.path.exists(csvPath):
        with open(csvPath, 'w', newline="", encoding='utf-8') as writeHeader:
            writer = csv.writer(writeHeader)
            writer.writerow(["Threads", "Latency"])
        writeHeader.close()

    with open(csvPath, 'a', newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([threads, latency])
    file.close()


def run_test(etcd_client, i, threads):
    key = f"key_{i}"
    value = f"value_{i}"

    start = time.perf_counter()
    ret_bool = etcd_client.put(key, value)
    if ret_bool:
        logger.info(f"insert key {key}, val {value}")
        end = time.perf_counter()
        write_to_csv(threads, end - start)


def main():
    thread_counts = [20,
                     40, 60, 80, 100
                     ]
    throughput_df = pd.DataFrame(columns=["Thread Count", "Total Time"])
    num_requests = 100000

    etcd_client = Etcd3Client()
    # conduct test
    program_start_time = time.perf_counter()
    for threads in thread_counts:
        logger.info("Thread count %s" % threads)
        start_time = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for i in range(num_requests):
                futures.append(executor.submit(run_test, i=i, etcd_client=etcd_client, threads=threads))

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(f"Elapsed time: {elapsed_time:0.2f} seconds")
        data_results = pd.DataFrame([{"Thread Count": threads, "Total Time": elapsed_time}])
        throughput_df = pd.concat([throughput_df, data_results], axis=0, ignore_index=True)

        throughput = (threads * num_requests) / elapsed_time
        logger.info(f"Throughput: {throughput:0.2f} requests per second")

    throughput_df.to_csv(PATH + "/etcd_Threads_Total_Time.csv", encoding='utf-8', index=False)
    program_end_time = time.perf_counter()
    program_elapsed_time = program_end_time - program_start_time
    logger.info(f"Test successful total runtime {program_elapsed_time}, closing program...")


if __name__ == "__main__":
    main()
