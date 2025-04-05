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
from utils import RANDOM_STATE, TRAIN_TEST_SPLIT, logInfo
import shap

script_dir = os.path.dirname(__file__)

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--maxFeatures",
        help="The number of features to consider when looking for the best split for random forest",
        type=int,
    )

    parser.add_argument(
        "--maxDepth",
        help="The maximum depth of the tree",
        type=int,
    )

    # Parse arguments
    args = parser.parse_args()

    return args


def remove_dataframe_features_with_all_null_values(dataframe):
    logInfo("Removing features with all null values")
    null_columns = dataframe.columns[dataframe.isnull().all()]
    dataframe.drop(null_columns, axis=1, inplace=True)
    return dataframe


def train_random_forests(args):
    logInfo(f"Reading subset_normalized_json_file_with_scaler.json")
    df = pd.read_json(
        os.path.join(
            script_dir, "..", "pretrain", "subset_normalized_json_file_with_scaler.json"
        )
    )
    df = remove_dataframe_features_with_all_null_values(df)

    X = df.drop(columns=["elliptic_label"])  # delete unused
    y = df["elliptic_label"]

    train_test_ratio = f"{int((1-TRAIN_TEST_SPLIT)*100)}-{int(TRAIN_TEST_SPLIT*100)}"

    # legal = 2, illegal = 1

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TRAIN_TEST_SPLIT, random_state=RANDOM_STATE
    )

    # -----------------------------------------
    # Random Forest
    # -----------------------------------------
    logInfo(f"Training random forest")

    rf_params = {
        "max_features": args.maxFeatures if args.maxFeatures else None,
        "max_depth": args.maxDepth if args.maxDepth else None,
    }

    model_RF = RandomForestClassifier(**rf_params).fit(
        X_train.values,
        y_train.values,
    )
    y_preds_RF = model_RF.predict(X_test.values)

    accuracy_RF = accuracy_score(y_test, y_preds_RF)
    logInfo(f"Accuracy: {accuracy_RF}")

    logInfo(f"Saving Random Forest confusion matrix to RF_CF_{train_test_ratio}.jpg")
    cm = confusion_matrix(y_test, y_preds_RF)
    ConfusionMatrixDisplay(confusion_matrix=cm).plot()
    plt.title(f"Random Forest confusion matrix {train_test_ratio}")
    plt.savefig(os.path.join(script_dir, f"../plots/RF_CF_{train_test_ratio}.jpg"))

    # Check for overfitting
    logInfo(f"Checking for Random Forest overfitting")
    y_preds_RF = model_RF.predict(X_train.values)
    accuracy_RF = accuracy_score(y_train, y_preds_RF)
    logInfo(f"Accuracy: {accuracy_RF}")

    logInfo(
        f"Saving Random Forest confusion matrix to RF_CF_train_{train_test_ratio}.jpg"
    )
    cm = confusion_matrix(y_train, y_preds_RF)
    ConfusionMatrixDisplay(confusion_matrix=cm).plot()
    plt.title(f"Training dataset Random Forest confusion matrix {train_test_ratio}")
    plt.savefig(
        os.path.join(script_dir, f"../plots/RF_CF_train_{train_test_ratio}.jpg")
    )

    logInfo(f"Getting RF feature importances")
    # Get feature importances
    importances = model_RF.feature_importances_

    # Create a Pandas Series for easier handling and sorting
    feature_importances = pd.Series(
        importances, index=[f"{X.columns[i]}" for i in range(X.shape[1])]
    )

    # Get the top 10 most important features
    top_10_features = feature_importances.nlargest(10)

    # Plot the top 10 features
    plt.figure(figsize=(12, 8))  # Adjust figure size as needed
    top_10_features.plot(kind="barh")
    plt.title("Top 10 Feature Importances")
    plt.xlabel("Features")
    plt.ylabel("Importance")
    plt.yticks(fontsize=8)
    plt.savefig(
        os.path.join(script_dir, f"../plots/RF_Importances_{train_test_ratio}.jpg")
    )

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

    # Check for overfitting
    logInfo(f"Checking for ADABoost overfitting")
    y_preds_ADA = model_AdaBoost.predict(X_train.values)
    accuracy_ADA = accuracy_score(y_train, y_preds_ADA)
    logInfo(f"Accuracy: {accuracy_ADA}")

    logInfo(f"Saving ADABoost confusion matrix to ADA_CF_train_{train_test_ratio}.jpg")
    cm = confusion_matrix(y_train, y_preds_ADA)
    ConfusionMatrixDisplay(confusion_matrix=cm).plot()
    plt.title(f"Training dataset ADABoost confusion matrix {train_test_ratio}")
    plt.savefig(
        os.path.join(script_dir, f"../plots/ADA_CF_train_{train_test_ratio}.jpg")
    )

    logInfo(f"Getting ADABoost feature importances")
    # Get feature importances
    importances = model_AdaBoost.feature_importances_

    # Create a Pandas Series for easier handling and sorting
    feature_importances = pd.Series(
        importances, index=[f"{X.columns[i]}" for i in range(X.shape[1])]
    )

    # Get the top 10 most important features
    top_10_features = feature_importances.nlargest(10)

    # Plot the top 10 features
    plt.figure(figsize=(12, 8))  # Adjust figure size as needed
    top_10_features.plot(kind="barh")
    plt.title("Top 10 Feature Importances")
    plt.xlabel("Features")
    plt.ylabel("Importance")
    plt.yticks(fontsize=8)
    plt.savefig(
        os.path.join(script_dir, f"../plots/ADA_Importances_{train_test_ratio}.jpg")
    )

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

    # Check for overfitting
    logInfo(f"Checking for XGBoost overfitting")
    y_preds_XGB = model_XGBoost.predict(X_train.values)
    accuracy_XGB = accuracy_score(y_train, y_preds_XGB)
    logInfo(f"Accuracy: {accuracy_XGB}")

    logInfo(f"Saving XGBoost confusion matrix to XGB_CF_train_{train_test_ratio}.jpg")
    cm = confusion_matrix(y_train, y_preds_XGB)
    ConfusionMatrixDisplay(confusion_matrix=cm).plot()
    plt.title(f"Training dataset XGBoost confusion matrix {train_test_ratio}")
    plt.savefig(
        os.path.join(script_dir, f"../plots/XGB_CF_train_{train_test_ratio}.jpg")
    )

    logInfo(f"Getting XGBoost feature importances")
    # Get feature importances
    importances = model_XGBoost.feature_importances_

    # Create a Pandas Series for easier handling and sorting
    feature_importances = pd.Series(
        importances, index=[f"{X.columns[i]}" for i in range(X.shape[1])]
    )

    # Get the top 10 most important features
    top_10_features = feature_importances.nlargest(10)

    # Plot the top 10 features
    plt.figure(figsize=(12, 8))  # Adjust figure size as needed
    top_10_features.plot(kind="barh")
    plt.title("Top 10 Feature Importances")
    plt.xlabel("Features")
    plt.ylabel("Importance")
    plt.yticks(fontsize=8)
    plt.savefig(
        os.path.join(script_dir, f"../plots/XG_Importances_{train_test_ratio}.jpg")
    )

    # -----------------------------------------
    # Save models to files
    # -----------------------------------------
    logInfo(f"Saving models to files")
    # Save LabelEncoder
    dump(le, open(os.path.join(script_dir, "../models/XGLabelEncoder.pkl"), "wb"))
    # Save models to file
    dump(model_RF, open(os.path.join(script_dir, "../models/RF_model.sav"), "wb"))
    dump(
        model_AdaBoost, open(os.path.join(script_dir, "../models/ADA_model.sav"), "wb")
    )
    dump(model_XGBoost, open(os.path.join(script_dir, "../models/XG_model.sav"), "wb"))

    # -----------------------------------------
    # SHAP analysis
    # -----------------------------------------
    logInfo(f"Starting SHAP analysis")
    explainer = shap.TreeExplainer(model_RF)
    shap_values = explainer.shap_values(X)
    shap.initjs()
    shap.summary_plot(shap_values[:, :, 0], X, show=False)
    plt.savefig(
        os.path.join(script_dir, f"../plots/RF_summary_plot.png"), bbox_inches="tight"
    )
    plt.close()
    shap.plots.violin(shap_values[:, :, 0], features=X.columns, show=False)
    plt.savefig(
        os.path.join(script_dir, f"../plots/RF_violin_features.png"),
        bbox_inches="tight",
    )


if __name__ == "__main__":
    # Parse the arguments
    args = parseArguments()
    train_random_forests(args)
