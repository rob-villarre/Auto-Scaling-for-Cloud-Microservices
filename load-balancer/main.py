import time
import schedule
import requests
import yaml
import docker
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Choose the metric for load balancing.')
parser.add_argument('--metric', choices=['average', 'p95'], default='average',
                help='The metric to use for load balancing (default: average)')
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
        return self.service.attrs['Spec']['Mode']['Replicated']['Replicas']

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
dockerapi = Docker(client, config['service_name'])

RESPONSE_TIMES = ResponseTimeList(max_size=config['time_array_length'])

def get_response_time():
    response_time = None
    try:
        # TODO: change timeout to better value?
        t0 = time.time()
        requests.get(f"http://{config['host']}", timeout=(config['upper_threshold'] * 2))
        t1 = time.time()
        # response_time = response.elapsed.total_seconds()
        response_time = t1 - t0
        return response_time 
    # TODO handle timeout
    except requests.exceptions.Timeout as timeout:
        response_time = config['upper_threshold'] * 2
        return response_time    
    # TODO handle all other exceptions
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def scale_up(average_response_time):
    if average_response_time >= config['upper_threshold']:
         # Scale up by rounded value of (average_response_time / upper_threshold_value) instances
        replicas = dockerapi.replicas() + round(average_response_time / config['upper_threshold'])
        # Cannot scale up past set maximum number of replicas
        if replicas > config['max_replicas']:
            replicas = config['max_replicas']

        # Scale up
        dockerapi.scale(replicas)
        # Sleep to allow changes to rebalance
        time.sleep(config['rebalance_await_time'] * round(average_response_time / config['upper_threshold']))

        print(f"Service scaled up to {dockerapi.replicas()} replicas")

def scale_down(average_response_time):
    if average_response_time <= config['lower_threshold']:
        # Scale down by rounded value of (lower_threshold_value / average_response_time) instances
        replicas = dockerapi.replicas() - round(config['lower_threshold'] / average_response_time)
        # Cannot scale down past set minimum number of replicas
        if replicas < config['min_replicas']:
            replicas = config['min_replicas']

        # Scale down
        dockerapi.scale(replicas)
        # Sleep to allow changes to rebalance
        time.sleep(config['rebalance_await_time'] * round(config['lower_threshold']/average_response_time))
        
        print(f"Service scaled down to {dockerapi.replicas()} replicas")
            

def percentile_response_time(percentile):
    if len(RESPONSE_TIMES.list) == 0:
        return None
    return np.percentile(RESPONSE_TIMES.list, percentile)

def load_balancer():
    response_time = get_response_time()
    
    print(f"Response time: {response_time} seconds")
    RESPONSE_TIMES.append(response_time)

    if args.metric == 'average':
        metric_response_time = RESPONSE_TIMES.average()
        print(f"Average response time is: {metric_response_time} seconds")
    else:
        metric_response_time = percentile_response_time(95)
        print(f"P95 response time is: {metric_response_time} seconds")

    scale_up(metric_response_time)
    scale_down(metric_response_time)

if __name__ == "__main__":
    schedule.every(config['poll_interval']).seconds.do(load_balancer)

    while True:
        schedule.run_pending()
        time.sleep(1)

