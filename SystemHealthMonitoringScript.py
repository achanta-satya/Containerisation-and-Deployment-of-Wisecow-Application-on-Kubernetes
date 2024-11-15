import psutil
import time

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80

# Function to check system health
def check_system_health():
    cpu_usage = psutil.cpu_percent(interval=1)  # Check CPU usage
    if cpu_usage > CPU_THRESHOLD:
        print(f"ALERT: CPU Usage is high: {cpu_usage}%")

    memory = psutil.virtual_memory()  # Check memory usage
    if memory.percent > MEMORY_THRESHOLD:
        print(f"ALERT: Memory Usage is high: {memory.percent}%")

    disk = psutil.disk_usage('/')   # Check disk space usage
    if disk.percent > DISK_THRESHOLD:
        print(f"ALERT: Disk Space Usage is high: {disk.percent}%")

    print(f"\nRunning processes:")       # Check running processes
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, CPU Usage: {proc.info['cpu_percent']}%")


if __name__ == "__main__":
    while True:
        print("\nChecking system health...")
        check_system_health()
        time.sleep(10)  # Check every 10 seconds
