import json
import logging
import os
import time
from datetime import datetime


def get_user_ip(request):
    return request.META.get("REMOTE_ADDR")


# Get the current directory of the Django app
current_directory = os.path.dirname(os.path.abspath(__file__))
# Construct the log file path in the current directory
LOG_FILE_PATH = os.path.join(current_directory, "log_file.json")
print("LOG FILE PATH:", LOG_FILE_PATH)


class JsonFileHandler(logging.FileHandler):
    def emit(self, record):
        log_entry = self.format(record)
        try:
            log_data = json.loads(log_entry)
        except json.JSONDecodeError:
            log_data = {"message": log_entry}
        with open(self.baseFilename, "a", encoding=self.encoding) as f:
            json.dump(log_data, f)
            f.write("\n")


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
        self.setup_logger()

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        self.log_request(request, response, end_time - start_time)

        return response

    def log_request(self, request, response, elapsed_time):
        self.logger.info(
            json.dumps(
                {
                    "date": datetime.now().isoformat(),
                    "path": request.path,
                    "method": request.method,
                    "status_code": response.status_code,
                    "user": (
                        request.user.username
                        if request.user.is_authenticated
                        else "Anonymous"
                    ),
                    "user_ip": get_user_ip(request),
                    "elapsed_time": f"{elapsed_time:.6f} seconds",
                }
            )
        )

    def setup_logger(self):
        if not os.path.exists(os.path.dirname(LOG_FILE_PATH)):
            os.makedirs(os.path.dirname(LOG_FILE_PATH))
        handler = JsonFileHandler(LOG_FILE_PATH)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
