import re
from collections import Counter

# Path to the log file
log_file_path = '/var/log/apache2/access.log'

# Regular expression for Apache/Nginx log format (adjust if necessary)
log_pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[.*\] ".*" (?P<status_code>\d{3}) .* "(?P<requested_url>.*)"'

def analyze_log_file(file_path):
    ip_counter = Counter()
    url_counter = Counter()
    error_count = 0

    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(log_pattern, line)
            if match:
                ip = match.group('ip')
                status_code = int(match.group('status_code'))
                requested_url = match.group('requested_url')

                ip_counter[ip] += 1         #count IP & URL
                url_counter[requested_url] += 1

                if status_code == 404:      #count 404 error
                    error_count += 1

    print(f"\nTotal 404 Errors: {error_count}")        # Display analysis results
    print("\nMost Requested URLs:")
    for url, count in url_counter.most_common(5):
        print(f"{url}: {count} times")

    print("\nTop 5 IP Addresses with Most Requests:")
    for ip, count in ip_counter.most_common(5):
        print(f"{ip}: {count} requests")

# Main function
if __name__ == "__main__":
    analyze_log_file(log_file_path)
