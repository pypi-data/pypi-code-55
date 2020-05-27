LOG_FORMAT = '%(asctime)s [%(levelname)s] %(funcName)s (%(filename)s:%(lineno)d) %(message)s'
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8080

# To have extended stats, by origin IP, based on the logs.
# https://developers.cloudflare.com/logs/logpull-api/requesting-logs/
DEFAULT_LOGS_FETCH = True
DEFAULT_LOGS_COUNT = 10000
DEFAULT_LOGS_SAMPLE = 0.1
# Time range in seconds for the logs
# Adjust with your scrape_interval
DEFAULT_LOGS_RANGE = 60
DEFAULT_GET_ORIGIN_IP_PTR = True
DNS_PTR_CACHE = 1024
