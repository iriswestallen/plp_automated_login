import os
import requests
import logging
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get credentials from environment variables
EMAIL = os.getenv("PLP_EMAIL")
PASSWORD = os.getenv("PLP_PASSWORD")

LOGIN_URL = "https://api.lms.v2.powerlearnprojectafrica.org/gateway/api/auth/login/student"

def login(email, password):
    """Authenticate and return the token"""
    payload = {"email": email, "password": password}
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://academy.powerlearnprojectafrica.org",
        "Referer": "https://academy.powerlearnprojectafrica.org/",
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.post(LOGIN_URL, json=payload, headers=headers)
        response.raise_for_status()
        logging.info("[✔] Login Successful!")
    except requests.exceptions.RequestException as e:
        logging.error("[❌] Login failed: %s", e)

def rapid_fire_login(iterations=100000, threads=5, delay=0.004):
    """Runs login in multiple threads for maximum speed with delay"""
    def worker():
        for _ in range(iterations // threads):
            login(EMAIL, PASSWORD)
            time.sleep(delay)

    thread_list = [threading.Thread(target=worker) for _ in range(threads)]

    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    rapid_fire_login(iterations=100000, threads=5, delay=0.004)
