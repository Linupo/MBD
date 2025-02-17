import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from pickle import dump
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from utils import logInfo

script_dir = os.path.dirname(__file__)


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument(
        "-t",
        "--testSize",
        help="Test split size (e.g. if you specify 0.5, the split for test / train will be 50/50), default is 0.3",
        type=float,
        default=0.3,
    )

    # Parse arguments
    args = parser.parse_args()

    return args


def remove_dataframe_features_with_all_null_values(dataframe):
    logInfo("Removing features with all null values")
    null_columns = dataframe.columns[dataframe.isnull().all()]
    dataframe.drop(null_columns, axis=1, inplace=True)
    return dataframe


def train_random_forests(test_size: float):
    logInfo(f"Reading subset_normalized_json_file_with_scaler.json")
    df = pd.read_json(
        os.path.join(
            script_dir, "..", "pretrain", "subset_normalized_json_file_with_scaler.json"
        )
    )
    df = remove_dataframe_features_with_all_null_values(df)

    X = df.drop(columns=["elliptic_label"])  # delete unused
    y = df["elliptic_label"]

    train_test_ratio = f"{int((1-test_size)*100)}-{int(test_size*100)}"

    # legal = 2, illegal = 1

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=15
    )

    # -----------------------------------------
    # Random Forest
    # -----------------------------------------
    logInfo(f"Training random forest")
    model_RF = RandomForestClassifier().fit(X_train.values, y_train.values)
    y_preds_RF = model_RF.predict(X_test.values)

    accuracy_RF = accuracy_score(y_test, y_preds_RF)
    logInfo(f"Accuracy: {accuracy_RF}")

    logInfo(f"Saving Random Forest confusion matrix to RF_CF_{train_test_ratio}.jpg")
    cm = confusion_matrix(y_test, y_preds_RF)
    ConfusionMatrixDisplay(confusion_matrix=cm).plot()
    plt.title(f"Random Forest confusion matrix {train_test_ratio}")
    plt.savefig(os.path.join(script_dir, f"../plots/RF_CF_{train_test_ratio}.jpg"))

    # -----------------------------------------
    # ADABoost
    # -----------------------------------------
    logInfo(f"Training ADABoost")
    model_AdaBoost = AdaBoostClassifier().fit(X_train.values, y_train.values)
    y_preds_ADA = model_AdaBoost.predict(X_test.values)
    accuracy_ADA = accuracy_score(y_test, y_preds_ADA)
    logInfo(f"Accuracy: {accuracy_ADA}")

    logInfo(f"Saving ADABoost confusion matrix to ADA_CF_{train_test_ratio}.jpg")
    cm = confusion_matrix(y_test, y_preds_ADA)
    ConfusionMatrixDisplay(confusion_matrix=cm).plot()
    plt.title(f"ADABoost confusion matrix {train_test_ratio}")
    plt.savefig(os.path.join(script_dir, f"../plots/ADA_CF_{train_test_ratio}.jpg"))

    # -----------------------------------------
    # XGBoost
    # -----------------------------------------
    logInfo(f"Training XGBoost")
    le = LabelEncoder()
    y_train = le.fit_transform(y_train)
    y_test = le.fit_transform(y_test)
    model_XGBoost = XGBClassifier().fit(X_train, y_train)

    y_preds_XGB = model_XGBoost.predict(X_test)
    accuracy_XGB = accuracy_score(y_test, y_preds_XGB)
    logInfo(f"Accuracy: {accuracy_XGB}")

    logInfo(f"Saving XGBoost confusion matrix to XG_CF_{train_test_ratio}.jpg")
    cm = confusion_matrix(y_test, y_preds_XGB)
    ConfusionMatrixDisplay(confusion_matrix=cm).plot()
    plt.title(f"XGBoost confusion matrix {train_test_ratio}")
    plt.savefig(os.path.join(script_dir, f"../plots/XG_CF_{train_test_ratio}.jpg"))

    logInfo(f"Saving models to files")
    # Save LabelEncoder
    dump(le, open(os.path.join(script_dir, "../models/XGLabelEncoder.pkl"), "wb"))
    # Save models to file
    dump(model_RF, open(os.path.join(script_dir, "../models/RF_model.sav"), "wb"))
    dump(
        model_AdaBoost, open(os.path.join(script_dir, "../models/ADA_model.sav"), "wb")
    )
    dump(model_XGBoost, open(os.path.join(script_dir, "../models/XG_model.sav"), "wb"))


if __name__ == "__main__":
    # Parse the arguments
    args = parseArguments()
    train_random_forests(args.testSize)
