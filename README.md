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
- Run using 95th percentile metric
```
sudo python3 main.py --metric p95
```
Or using average of runtime
```
sudo python3 main.py --metric average
```
While the file main.py is running, run locust to obtain the graph by typing in terminal:
```
locust
```