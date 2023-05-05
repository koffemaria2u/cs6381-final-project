import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm
import os
import pandas as pd

dirPath = os.getcwd() # + "\\consul_latency_graphing\\"

etcd_latency = pd.read_csv(dirPath + "/etcd/results_data/etcd_Request_Latency.csv")
etcd_throughput = pd.read_csv(dirPath + "/etcd/results_data/etcd_Threads_Total_Time.csv")
consul_latency = pd.read_csv(dirPath + "/Consul/Results_Graphs/Request_Latency.csv")
consul_throughput = pd.read_csv(dirPath + "/Consul/Results_Graphs/Threads_Total_Time.csv")

threads = [20, 40, 60, 80, 100]

consuls_color = (198 / 255, 42 / 255, 113 / 255)
etcd_color = (65 / 255, 158 / 255, 218 / 255)

plt.rcParams["figure.figsize"] = [10, 5]
plt.rcParams["figure.autolayout"] = True


def latency_info_per_thread(latency_df, tech_name):
    for thread_Ct in threads:
        byThreadDF = latency_df.loc[latency_df["Threads"] == thread_Ct]

        print("\n{0} Thread Count: {1}".format(tech_name, thread_Ct))
        print(byThreadDF["Latency"].describe())


def average_latency_per_request(etcd_latency_df, consul_latency_df):
    # setup subplots
    fig, axes = plt.subplots(2, 1, figsize=(8, 6))
    fig.suptitle("Average Latency Times for Key/Value Creation")

    # etcd subplots
    etcd_df_by_threads = etcd_latency_df.groupby('Threads', as_index=False)["Latency"].mean()
    axes[0].plot(threads, etcd_df_by_threads["Latency"], color=etcd_color, label="etcd", marker="o")
    axes[0].title.set_text("etcd")
    axes[0].set_xlabel("Concurrent Clients")
    axes[0].set_ylabel("Latency (s)")
    axes[0].legend(loc="upper left")

    # consul subplots
    consul_df_by_threads = consul_latency_df.groupby('Threads', as_index=False)["Latency"].mean()
    axes[1].plot(threads, consul_df_by_threads["Latency"], color=consuls_color, label="Consul", marker="o")
    axes[1].title.set_text("Consul")
    axes[1].set_xlabel("Concurrent Clients")
    axes[1].set_ylabel("Latency (s)")
    axes[1].legend(loc="upper left")

    fig.tight_layout()
    plt.legend()
    plt.savefig(dirPath + "/etcd/results_graphs/subplot_combined_Average_KV_Latency.jpg")
    plt.show()


def box_plot_summary(latency_df, tech_name, color):
    plt.rcParams["figure.figsize"] = [6, 6]
    plt.rcParams["figure.autolayout"] = True
    flier_props = {'marker': '.', "markeredgecolor": color, 'markersize': 5, 'markerfacecolor': color}
    median_props = {"color": color}
    latency_df.boxplot(column="Latency", by="Threads", boxprops={"color": 'black', "linewidth": 1.2},
                    flierprops=flier_props, medianprops=median_props)
    # plt.xticks(threads)
    plt.title("Latency Distribution by Number of Concurrent Clients")
    plt.xlabel("Concurrent Clients")
    plt.ylabel("Latency (s)")
    plt.suptitle('')
    plt.savefig(dirPath + f"/etcd/results_graphs/{tech_name}_KV_Latency_Distribution.jpg")
    plt.show()


def throughput_graph(throughput_df_etcd, throughput_df_consul):
    # setup subplot
    fig, axes = plt.subplots(2, 1, figsize=(8, 6))
    fig.suptitle("Key/Value Creation Throughput - 100,000 KV created")

    # etcd subplots
    throughput_df_etcd["KV/Sec"] = 100000 / throughput_df_etcd["Round_Trip"]
    axes[0].plot(throughput_df_etcd["Thread_Count"], throughput_df_etcd["KV/Sec"],
                 color=etcd_color, label="etcd", marker="o")
    axes[0].title.set_text("etcd")
    axes[0].set_xlabel("Concurrent Clients")
    axes[0].set_ylabel("Average KV Creation per Second")
    axes[0].legend(loc="upper left")

    # consul subplots
    throughput_df_consul["KV/Sec"] = 100000 / throughput_df_consul["Round_Trip"]
    axes[1].plot(throughput_df_consul["Thread_Count"], throughput_df_consul["KV/Sec"],
                 color=consuls_color, label="Consul", marker="o")
    axes[1].title.set_text("Consul")
    axes[1].set_xlabel("Concurrent Clients")
    axes[1].set_ylabel("Average KV Creation per Second")
    axes[1].legend(loc="upper left")

    fig.tight_layout()
    plt.legend()
    plt.savefig(dirPath + "/etcd/results_graphs/subplot_combined_KV_Throughput.jpg")
    plt.show()


if __name__ == "__main__":
    latency_info_per_thread(latency_df=etcd_latency, tech_name="etcd")
    latency_info_per_thread(latency_df=consul_latency, tech_name="Consul")
    average_latency_per_request(etcd_latency_df=etcd_latency, consul_latency_df=consul_latency)
    box_plot_summary(latency_df=etcd_latency, tech_name="etcd", color=etcd_color)
    box_plot_summary(latency_df=consul_latency, tech_name="consul", color=consuls_color)
    throughput_graph(throughput_df_etcd=etcd_throughput, throughput_df_consul=consul_throughput)
