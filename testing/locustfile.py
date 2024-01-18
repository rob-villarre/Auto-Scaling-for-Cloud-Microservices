from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        # http://10.2.9.11:8000 
        self.client.get("http://localhost:8000")