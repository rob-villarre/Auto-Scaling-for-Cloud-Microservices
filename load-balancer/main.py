import time
import requests
import yaml
import docker
import argparse
import plotext as plt


import plotext as plt

replica_data = {"time": [], "replicas": []}


def show_plot():
    plt.date_form("M:S")
    
    replicas = replica_data["replicas"]
    times = plt.datetimes_to_string(replica_data["time"])

    plt.plot(times, replicas)
    plt.theme("dark")
    plt.xlim(times[0])
    plt.ylim(config["min_replicas"], config["max_replicas"])
    plt.interactive(True)
    yticks = [i for i in range(config["min_replicas"], config["max_replicas"] + 1)]
    ylabels = [
        str(i) for i in range(config["min_replicas"], config["max_replicas"] + 1)
    ]
    plt.yticks(yticks, ylabels)
    plt.yfrequency(config["max_replicas"])

    plt.xfrequency(len(times))

    plt.title("Number of Replicas Over Time")
    plt.xlabel("Time")
    plt.ylabel(f"Replica Count: {dockerapi.replicas()}")
    plt.clear_terminal()
    plt.show()


parser = argparse.ArgumentParser(description="Choose state of scaling for load balancing.")
parser.add_argument(
    "--scale",
    choices=["on", "off"],
    default="on",
    help="Control auto-scaling (deafult: on)",
)
args = parser.parse_args()

class Docker:
    def __init__(self, client, service_name):
        self.client = client
        self.service = client.services.list(filters={"name": service_name})[0]

    def scale(self, replicas):

        self.service.scale(replicas)
        while True:

            # if service finished scaling
            if self.replicas() == replicas:
                break
            time.sleep(1)

    # returns current number of replicas
    def replicas(self):
        # reload service attrs from docker server
        self.service.reload()
        return self.service.attrs["Spec"]["Mode"]["Replicated"]["Replicas"]


class ResponseTimeList:
    def __init__(self, max_size):
        self.max_size = max_size
        self.list = []

    # will delete oldest entry to maintain max_size length
    def append(self, time):
        self.list.append(time)
        if len(self.list) > self.max_size:
            self.list.pop(0)

    def average(self):
        return sum(self.list) / len(self.list)


config = yaml.safe_load(open("./config.yml"))

client = docker.from_env()
dockerapi = Docker(client, config["service_name"])

class LoadBalancer:
    def __init__(self, config, dockerapi):
        self.config = config
        self.dockerapi = dockerapi
        self.response_times = ResponseTimeList(self.config['time_array_length'])
        # it will monitor response times for that many intervals before scaling again.
        self.monitor_periods = self.config['monitor_periods']
        self.timed_out = False

    def get_response_time(self):
        response_time = None
        try:
            t0 = time.time()
            requests.get(
                f"http://{self.config['host']}",
                timeout=(self.config["upper_threshold"] * 2),
            )
            t1 = time.time()
            # response_time = response.elapsed.total_seconds()
            response_time = t1 - t0
            self.timed_out = False
            return response_time
        except requests.exceptions.Timeout as timeout:
            # setting to *2 to increase number of replicants to scale by
            response_time = self.config["upper_threshold"] * 2
            self.timed_out = True
            return response_time
        except requests.exceptions.RequestException as e:
            return None

    def percentile_response_time(self, percentile):
        if len(self.response_times.list) == 0:
            return None
        return np.percentile(self.response_times.list, percentile)
    
    def scale_up(self, average_response_time):
        if (
            average_response_time >= self.config["upper_threshold"]
            and self.dockerapi.replicas() < self.config["max_replicas"]
        ):
            # Scale up by rounded value of (average_response_time / upper_threshold_value) instances
            replicas = self.dockerapi.replicas() + round(
                average_response_time / self.config["upper_threshold"]
            )
            # Cannot scale up past set maximum number of replicas
            if replicas > self.config["max_replicas"]:
                replicas = self.config["max_replicas"]

            # Scale up
            self.dockerapi.scale(replicas)

            self.monitor_periods = self.config['monitor_periods']

            # print(f"Service scaled up to {dockerapi.replicas()} replicas")

    def scale_down(self, average_response_time):
        if (
            average_response_time <= self.config["lower_threshold"]
            and self.dockerapi.replicas() > self.config["min_replicas"]
        ):
            # Scale down by rounded value of (lower_threshold_value / average_response_time) instances
            replicas = self.dockerapi.replicas() - round(
                self.config["lower_threshold"] / average_response_time
            )
            # Cannot scale down past set minimum number of replicas
            if replicas < self.config["min_replicas"]:
                replicas = self.config["min_replicas"]

            # Scale down
            self.dockerapi.scale(replicas)

            self.monitor_periods = self.config['monitor_periods']

            # print(f"Service scaled down to {dockerapi.replicas()} replicas")

    def load_balancer(self):
        response_time = self.get_response_time()


        if response_time is None:
            return

        # print(f"Response time: {response_time} seconds")
        self.response_times.append(response_time)

        metric_response_time = self.response_times.average()
        # print(f"Average response time is: {metric_response_time} seconds")

        if self.monitor_periods == 0:
            if args.scale == "on":
                self.scale_up(metric_response_time)
                self.scale_down(metric_response_time)
        else:
            self.monitor_periods -= 1
            

    def run(self):
        while True:
            lb.load_balancer()
            replica_data["time"].append(plt.today_datetime())
            replica_data["replicas"].append(dockerapi.replicas())
            show_plot()

            if self.timed_out is False and self.monitor_periods == 0:
                time.sleep(config["poll_interval"])
            else:
                time.sleep(1)

if __name__ == "__main__":
    lb = LoadBalancer(config, dockerapi)
    lb.run()

