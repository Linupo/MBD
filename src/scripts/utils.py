from datetime import datetime


def logError(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} [ERROR]: {message}")


def logInfo(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} [INFO]: {message}")
