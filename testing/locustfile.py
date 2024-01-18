from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape

class UserTasks(TaskSet):
  @task
  def get_root(self):
    self.client.get("/")


class WebsiteUser(HttpUser):
  wait_time = constant(0.5)
  tasks = [UserTasks]

# https://github.com/locustio/locust/blob/master/examples/custom_shape/stages.py
class WaveShape(LoadTestShape):
  """
  A simply load test shape class that has different user and spawn_rate at
  different stages.

  Keyword arguments:

      stages -- A list of dicts, each representing a stage with the following keys:
          duration -- When this many seconds pass the test is advanced to the next stage
          users -- Total user count
          spawn_rate -- Number of users to start/stop per second
          stop -- A boolean that can stop that test at a specific stage

      stop_at_end -- Can be set to stop once all stages have run.
  """

  stages = [
    {"duration": 100, "users": 10, "spawn_rate": 10},
    {"duration": 200, "users": 100, "spawn_rate": 50},
    {"duration": 300, "users": 1000, "spawn_rate": 100},
    {"duration": 400, "users": 100, "spawn_rate": 50},
    {"duration": 500, "users": 10, "spawn_rate": 10},
  ]

  def tick(self):
    run_time = self.get_run_time()

    for stage in self.stages:
      if run_time < stage["duration"]:
        tick_data = (stage["users"], stage["spawn_rate"])
        return tick_data

    return None