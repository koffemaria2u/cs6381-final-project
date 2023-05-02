import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm
import os
import pandas as pd

dirPath =  os.getcwd() + "\\consul_latency_graphing\\"

latency = pd.read_csv(dirPath + "Request_Latency.csv")
throughput = pd.read_csv(dirPath + "Threads_Total_Time.csv")

threads = [20, 40, 60, 80, 100]

consuls_color = (198/255, 42/255, 113/255)

plt.rcParams["figure.figsize"] = [10, 5]
plt.rcParams["figure.autolayout"] = True

def latency_info_per_thread():
     for thread_Ct in threads:
        byThreadDF = latency.loc[latency["Threads"] == thread_Ct]

        print("\nThread Count: {0}".format(thread_Ct))
        print(byThreadDF["Latency"].describe())


def average_latency_per_request(): 
    byThreads_df = latency.groupby('Threads', as_index=False)["Latency"].mean()
    plt.plot(threads, byThreads_df["Latency"], color = consuls_color, label="Consul", marker = "o")

    plt.xticks(threads)
    plt.title("Average Latency Times for Key/Value Creation")
    plt.xlabel("Concurrent Clients")
    plt.ylabel("Latency (s)")
    plt.legend()
    plt.savefig(dirPath + "Average_KV_Latency.jpg")
    plt.show()
    
def box_plot_summary():
    plt.rcParams["figure.figsize"] = [6, 6]
    plt.rcParams["figure.autolayout"] = True
    flier_props = {'marker': '.', "markeredgecolor": consuls_color, 'markersize': 5, 'markerfacecolor': consuls_color}
    median_props = {"color":consuls_color}
    latency.boxplot(column="Latency", by="Threads", boxprops={"color":'black', "linewidth":1.2}, flierprops=flier_props, medianprops=median_props)
    # plt.xticks(threads)
    plt.title("Latency Distribution by Number of Concurrent Clients")
    plt.xlabel("Concurrent Clients")
    plt.ylabel("Latency (s)")
    plt.suptitle('')
    plt.savefig(dirPath + "KV_Latency_Distribution.jpg")
    plt.show()


def throughput_graph():
    throughput["KV/Sec"] = 100000 / throughput["Round_Trip"]
    plt.plot(throughput["Thread_Count"], throughput["KV/Sec"], color = consuls_color, label="Consul", marker = "o")

    plt.xticks(throughput["Thread_Count"])
    plt.title("Key/Value Creation Throughput - 100,000 KV created")
    plt.xlabel("Concurrent Clients")
    plt.ylabel("Average KV Creation per Second")
    plt.legend()
    plt.savefig(dirPath + "KV_Throughput.jpg")
    plt.show()


latency_info_per_thread()
average_latency_per_request()
box_plot_summary()
throughput_graph()