
import requests
import concurrent.futures
import time
import os
import pandas as pd
import csv

PATH = os.getcwd() + "/consul_latency_graphing/"


#average key per second 
def write_to_csv(threads, latency):
        
    csvPath = PATH + "Request_Latency.csv"
    if not os.path.exists(csvPath):
        with open (csvPath, 'w', newline = "", encoding='utf-8') as writeHeader:
            writer = csv.writer(writeHeader)
            writer.writerow(["Threads", "Latency"])
        writeHeader.close()
    
    with open (csvPath, 'a', newline = "", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([threads, latency])
    file.close()
        

def put_key(url, threads):

	header = {'content-type':'application/json', "Accept-Charset":"UTF-8"}
	
	num_idx = url.rfind("_") + 1
	payload = url[num_idx:]
	start = time.perf_counter()
	response = requests.put(url, data = payload, headers=header)
	#print(response.content)
	if response.status_code in [200, 201]:
		end = time.perf_counter()
		write_to_csv(threads, end - start)
		#print("Successfully wrote value to Consul KV store!")
	else:
    		print(f"Error writing value to Consul KV store: {response.text}")

 
def main():
	thread_counts = [20, 40, 60, 80, 100]
	consul = "http://localhost:8500/v1/kv/key"
	# pandas df [thread count, total_time]
	throughput = pd.DataFrame(columns =["Thread Count", "Total Time"])

	for threads in thread_counts:
		print("Thread count {0}".format(threads))
		start = time.perf_counter()
		with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
			futures = []
			for i in range(100000): # 100k
				cur_url = "{0}-{1}_{2}".format(consul, threads, i)
				futures.append(executor.submit(put_key, url=cur_url, threads = threads))
				#print("Appended - {}".format(i))	
			
		end = time.perf_counter()
				
		print(f'Total time elapsed: {end-start:0.2f} seconds')	
		data = pd.DataFrame([{"Thread Count": threads, "Total Time" : (end - start)}])
		throughput = pd.concat([throughput, data], axis=0, ignore_index=True)

	throughput.to_csv(PATH + "Threads_Total_Time.csv", encoding='utf-8', index=False)
	
main()

