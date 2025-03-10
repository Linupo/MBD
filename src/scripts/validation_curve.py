import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import validation_curve

from train_models import remove_dataframe_features_with_all_null_values
from utils import logInfo

script_dir = os.path.dirname(__file__)


logInfo(f"Reading subset_normalized_json_file_with_scaler.json")
df = pd.read_json(
    os.path.join(
        script_dir, "..", "pretrain", "subset_normalized_json_file_with_scaler.json"
    )
)
df = remove_dataframe_features_with_all_null_values(df)

X = df.drop(columns=["elliptic_label"])  # delete unused
y = df["elliptic_label"]

model = RandomForestClassifier(random_state=42)
param_name = "max_features"  # other possible values: max_depth, min_samples_split, min_samples_leaf, max_features, n_estimators
param_range = np.arange(10, 5000, 1000)

logInfo(f"Creating validation curve for Random Forest ({param_name})")
train_scores, test_scores = validation_curve(
    model,
    X,
    y,
    param_name=param_name,
    param_range=param_range,
    cv=5,
    scoring="accuracy",
    # n_jobs=-1,
)

train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

plt.figure(figsize=(10, 6))
plt.plot(param_range, train_mean, label="Training score", color="blue", marker="o")
plt.fill_between(
    param_range,
    train_mean - train_std,
    train_mean + train_std,
    alpha=0.15,
    color="blue",
)
plt.plot(
    param_range, test_mean, label="Cross-validation score", color="green", marker="o"
)
plt.fill_between(
    param_range, test_mean - test_std, test_mean + test_std, alpha=0.15, color="green"
)
plt.title(f"Validation Curve for Random Forest ({param_name})")
plt.xlabel(param_name)
plt.ylabel("Score (Accuracy)")
plt.legend(loc="best")
plt.grid(True)
plt.savefig(os.path.join(script_dir, f"../plots/RF_validation_curve.jpg"))
