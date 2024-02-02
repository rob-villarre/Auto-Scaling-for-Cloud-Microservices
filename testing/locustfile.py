from locust import HttpUser, TaskSet, task, constant_throughput
from locust import LoadTestShape

class UserTasks(TaskSet):
  @task
  def get_root(self):
    self.client.get("http://localhost:8000")


class WebsiteUser(HttpUser):
  wait_time = constant_throughput(0.5)
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
    {"duration": 1*120, "users": 5, "spawn_rate": 1},
    {"duration": 2*120, "users": 10, "spawn_rate": 1},
    {"duration": 3*120, "users": 20, "spawn_rate": 1},
    {"duration": 4*120, "users": 10, "spawn_rate": 1},
    {"duration": 5*120, "users": 5, "spawn_rate": 1},
  ]

  def tick(self):
    run_time = self.get_run_time()

    for stage in self.stages:
      if run_time < stage["duration"]:
        tick_data = (stage["users"], stage["spawn_rate"])
        return tick_data

    return None
  

# from locust import HttpUser, TaskSet, task, between
# import time

# class MyTaskSet(TaskSet):
#     @task
#     def my_task(self):
#         # Your task logic goes here
#         self.client.get("http://localhost:8000/")

# class MyUser(HttpUser):
#     tasks = [MyTaskSet]
#     wait_time = between(1, 2)  # Adjust as needed
#     current_rate = 1  # Initial requests per second
#     duration = 10  # Duration in minutes for doubling/halving requests
#     halving_counter = 0  # Counter for halving iterations

#     def on_start(self):
#         for _ in range(self.duration):
#             self.user.tasks[0].my_task()
#             time.sleep(60)  # Wait for one minute
#             self.adjust_task_rate(double=True)

#         while self.halving_counter < 10:
#             self.user.tasks[0].my_task()
#             time.sleep(60)  # Wait for one minute
#             self.adjust_task_rate(double=False)
#             self.halving_counter += 1

#         # Restart the test after 10 halving iterations
#         self.halving_counter = 0
#         self.on_start()

#     def adjust_task_rate(self, double=True):
#         if double:
#             # Double the rate
#             self.current_rate *= 2
#         else:
#             # Halve the rate
#             self.current_rate /= 2

#         # Adjust wait time and target_user_count
#         self.user.wait_time = between(1/self.current_rate, 2/self.current_rate)
#         self.environment.runner.target_user_count = self.current_rate

# # Example: locust -f yourfile.py --host=http://your-website.com
