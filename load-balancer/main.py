import time
from datetime import timedelta

import docker

client = docker.from_env()

import requests

RESPONSE_TIMES = []
REQUESTS_PER_MINUTE = 6

# Acceptable response time
# Upper: 1.5 seconds
# Lower: 1.0 seconds

UPPER = 1.5
LOWER = 1.0

if __name__ == "__main__":
    start_time = time.time()

    # webapp_service = client.services.list(filters={"name": "app_name_web"})[0]

    # replicas = webapp_service.attrs['Spec']['Mode']['Replicated']['Replicas']

    # print(replicas)

    for _ in range(REQUESTS_PER_MINUTE):
        response = requests.get("http://10.2.9.11:8000", timeout=3)
        # delta = timedelta(hours=2, minutes=30, seconds=45)
        elapsed_seconds = response.elapsed.total_seconds()

        print(f"Response time: {elapsed_seconds} seconds")
        RESPONSE_TIMES.append(elapsed_seconds)
        time.sleep(10)
    average_response_time = sum(RESPONSE_TIMES) / len(RESPONSE_TIMES)
    print(
        f"Average response time for {REQUESTS_PER_MINUTE} requests is: {average_response_time} seconds"
    )
