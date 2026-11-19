import time
import urllib.request
import urllib.error
import os

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://frontend:8080"
)

print(f"Client connecting to {FRONTEND_URL}")

while True:
    try:
        with urllib.request.urlopen(FRONTEND_URL, timeout=5) as response:
            print("Frontend response:", response.read().decode())

    except Exception as error:
        print("Connection failed:", error)

    time.sleep(10)
