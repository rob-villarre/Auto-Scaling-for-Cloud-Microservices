# ECE-422-Auto-Scaling-for-Cloud-Microservices

## Notes

- Initially configured for env running on Python 3.8

## Running Instructions

- Install Docker

```
sudo apt-get install python3-docker
```

- Create and activate virtual environment

```
virtualenv venv --python=python3.8
source venv/bin/activate
```

- Install dependencies

```
pip install -r requirements.txt
```

- Run the main.py file with the following instruction where on allows scaling and off does not allow scaling:

```
sudo python3 main.py --scale <on/off>
```

While the file main.py is running, run locust to obtain the graph by typing in terminal:

```
locust
```

Locust asks for the host `http://localhost:8000/` but the Locust client itself runs on `http://localhost:8089/` in a browser.
