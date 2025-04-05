import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc


from train_models import remove_dataframe_features_with_all_null_values
from utils import RANDOM_STATE, TRAIN_TEST_SPLIT, logInfo

script_dir = os.path.dirname(__file__)

rf_params = {
    "max_depth": 10,
}

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
model = RandomForestClassifier(**rf_params)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TRAIN_TEST_SPLIT, random_state=RANDOM_STATE)

# Train the model
model = RandomForestClassifier(**rf_params)
model.fit(X_train, y_train)

# Get probabilities for the test data
y_probs = model.predict_proba(X_test)[:, 1]

# Calculate the ROC curve and AUC
fpr, tpr, thresholds = roc_curve(y_test, y_probs, pos_label=2)
roc_auc = auc(fpr, tpr)

# Plot the ROC curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label='ROC curve (AUC = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--') # Random classifier line
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.show()

print(f"AUC: {roc_auc}")