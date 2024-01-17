import requests

if __name__ == "__main__":
    response = requests.get("10.2.9.11:8000", timeout=3)
    print(response.elapsed.total_seconds)
