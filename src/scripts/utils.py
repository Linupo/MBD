from datetime import datetime

RANDOM_STATE = 99
TRAIN_TEST_SPLIT = 0.2

BEST_RF_PARAMS = {
    "max_depth": 12,
    "max_features": 1000,
    "min_samples_split": 12,
    "n_estimators": 100,
}

BEST_TREE_PARAMS = {
    "max_depth": 12,
    "max_features": 1000,
    "min_samples_split": 12,
}


def logError(message: str, end="\n"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} [ERROR]: {message}", end=end)


def logInfo(message: str, end="\n"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} [INFO]: {message}", end=end)
