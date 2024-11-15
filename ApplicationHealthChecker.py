import requests
import time

# URL to monitor
APP_URL = 'https://Accuknox.com'  # Replace with the application's URL
CHECK_INTERVAL = 60  # Time in seconds between checks

def check_application_health(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Application is UP! Status Code: {response.status_code}")
        else:
            print(f"Application is DOWN! Status Code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error checking application status: {e}")
        print("Application is DOWN!")

if __name__ == "__main__":
    while True:
        print("\nChecking application health...")
        check_application_health(APP_URL)
        time.sleep(CHECK_INTERVAL)
