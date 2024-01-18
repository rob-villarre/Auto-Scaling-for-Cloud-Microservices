import time
import schedule
import requests
import yaml
import docker

class Docker:
    def __init__(self, client, service_name):
        self.client = client
        self.service = client.services.list(filters={"name": service_name})[0]
    
    def scale(self, replicas):

        if (replicas >= config['max_replicas'] or replicas <= config['min_replicas']):
            return

        self.service.scale(replicas)
        while True:
            # reload service attrs from docker server
            self.service.reload()
            # if service finished scaling
            if self.replicas() == replicas:
                break
            time.sleep(1)

    # returns current number of replicas
    def replicas(self):
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

def load_balancer():
    try:
        # TODO: change timeout to better value?
        t0 = time.time()
        response = requests.get(f"http://{config['host']}")
        t1 = time.time()
        # response_time = response.elapsed.total_seconds()
        response_time = t1 - t0
        print(f"Response time: {response_time} seconds")
        RESPONSE_TIMES.append(response_time)
        
        average_response_time = RESPONSE_TIMES.average()
        print(RESPONSE_TIMES.list)
        print(
            f"Average response time is: {average_response_time} seconds"
        )

        # start scaling once response times array is full
        if len(RESPONSE_TIMES.list) < RESPONSE_TIMES.max_size:
            return

        if average_response_time > config['upper_threshold']:
            dockerapi.scale(min(dockerapi.replicas() + config['scale_step'], config['max_replicas']))
            print(f"Service scaled up to {dockerapi.replicas()} replicas")
            time.sleep(5)
        
        if average_response_time < config['lower_threshold']:
            dockerapi.scale(max(dockerapi.replicas() - config['scale_step'], config['min_replicas']))
            print(f"Service scaled down to {dockerapi.replicas()} replicas")
            time.sleep(5)

    # TODO handle timeout
    except requests.exceptions.Timeout as timeout:
        print(timeout)
    # TODO handle all other exceptions
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == "__main__":
    schedule.every(config['poll_interval']).seconds.do(load_balancer)

    while True:
        schedule.run_pending()
        time.sleep(1)

