from datetime import datetime


def logError(message, end="\n"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} [ERROR]: {message}", end=end)


def logInfo(message, end="\n"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} [INFO]: {message}", end=end)
