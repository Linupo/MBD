import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from pickle import dump
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


def remove_dataframe_features_with_all_null_values(dataframe):
    null_columns = dataframe.columns[dataframe.isnull().all()]
    dataframe.drop(null_columns, axis=1, inplace=True)
    return dataframe


df = pd.read_json("subset_normalized_json_file_with_scaler.json")
df = remove_dataframe_features_with_all_null_values(df)

X = df.drop(columns=["elliptic_label"])  # delete unused
y = df["elliptic_label"]

train_test_ratio = "70/30"

# legal = 2, illegal = 1

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=15
)

# -----------------------------------------
# Random Forest
# -----------------------------------------

model_RF = RandomForestClassifier().fit(X_train.values, y_train.values)
y_preds_RF = model_RF.predict(X_test.values)

accuracy_RF = accuracy_score(y_test, y_preds_RF)
print("Accuracy:", accuracy_RF)

cm = confusion_matrix(y_test, y_preds_RF)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()
plt.title(f"Random Forest confusion matrix {train_test_ratio}")
plt.savefig("plots/RF_CF_70-30.jpg")

# -----------------------------------------
# ADABoost
# -----------------------------------------

model_AdaBoost = AdaBoostClassifier().fit(X_train.values, y_train.values)
y_preds_ADA = model_AdaBoost.predict(X_test.values)
accuracy_ADA = accuracy_score(y_test, y_preds_ADA)
print("Accuracy:", accuracy_ADA)

cm = confusion_matrix(y_test, y_preds_ADA)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()
plt.title(f"ADABoost confusion matrix {train_test_ratio}")
plt.savefig("plots/ADA_CF_70-30.jpg")

# -----------------------------------------
# XGBoost
# -----------------------------------------

le = LabelEncoder()
y_train = le.fit_transform(y_train)
y_test = le.fit_transform(y_test)
model_XGBoost = XGBClassifier().fit(X_train, y_train)

y_preds_XGB = model_XGBoost.predict(X_test)
accuracy_XGB = accuracy_score(y_test, y_preds_XGB)
print("Accuracy:", accuracy_XGB)

cm = confusion_matrix(y_test, y_preds_XGB)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()
plt.title(f"XGBoost confusion matrix {train_test_ratio}")
plt.savefig("plots/XG_CF_70-30.jpg")

# Save LabelEncoder
dump(le, open("models/XGLabelEncoder.pkl", "wb"))
# Save models to file
dump(model_RF, open("models/RF_model.sav", "wb"))
dump(model_AdaBoost, open("models/ADA_model.sav", "wb"))
dump(model_XGBoost, open("models/XG_model.sav", "wb"))
