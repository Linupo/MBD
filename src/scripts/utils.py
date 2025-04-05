from datetime import datetime

RANDOM_STATE = 99
TRAIN_TEST_SPLIT = 0.2

def logError(message: str, end="\n"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} [ERROR]: {message}", end=end)


def logInfo(message: str, end="\n"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} [INFO]: {message}", end=end)
