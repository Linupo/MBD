import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import learning_curve

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

logInfo(f"X count {len(X)}")
logInfo(f"Creating random forest learning curve graph")
model = RandomForestClassifier(random_state=42)

train_sizes, train_scores, test_scores = learning_curve(
    model,
    X,
    y,
    train_sizes=np.linspace(0.1, 1.0, 10),
    cv=5,
    scoring="accuracy",
)

train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_mean, label="Training score", color="blue", marker="o")
plt.fill_between(
    train_sizes,
    train_mean - train_std,
    train_mean + train_std,
    alpha=0.15,
    color="blue",
)
plt.plot(
    train_sizes, test_mean, label="Cross-validation score", color="green", marker="o"
)
plt.fill_between(
    train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.15, color="green"
)
plt.title("Learning Curve")
plt.xlabel("Training Set Size")
plt.ylabel("Score (Accuracy)")
plt.legend(loc="best")
plt.grid(True)
plt.savefig(os.path.join(script_dir, f"../plots/RF_learning_curve.jpg"))
