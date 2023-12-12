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

X = df.drop(columns=['elliptic_label']) # delete unused
y = df['elliptic_label']

# legal = 2, illegal = 1

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=15)

# -----------------------------------------
# Random Forest
# -----------------------------------------

model_RF = RandomForestClassifier().fit(X_train.values,y_train.values)
y_preds_RF = model_RF.predict(X_test.values)

accuracy_RF = accuracy_score(y_test, y_preds_RF)
print("Accuracy:", accuracy_RF)

cm = confusion_matrix(y_test, y_preds_RF)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()
plt.title("Random Forest confusion matrix")
# plt.show()

# -----------------------------------------
# ADABoost
# -----------------------------------------

model_AdaBoost = AdaBoostClassifier().fit(X_train.values,y_train.values)
y_preds_ADA = model_AdaBoost.predict(X_test.values)
accuracy_ADA = accuracy_score(y_test, y_preds_ADA)
print("Accuracy:", accuracy_ADA)

cm = confusion_matrix(y_test, y_preds_ADA)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()
plt.title("ADABoost confusion matrix")
# plt.show()

# -----------------------------------------
# XGBoost
# -----------------------------------------

le = LabelEncoder()
y_train = le.fit_transform(y_train)
y_test = le.fit_transform(y_test)
model_XGBoost = XGBClassifier().fit(X_train,y_train)

y_preds_XGB = model_XGBoost.predict(X_test)
accuracy_XGB = accuracy_score(y_test, y_preds_XGB)
print("Accuracy:", accuracy_XGB)

cm = confusion_matrix(y_test, y_preds_XGB)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()
plt.title("XGBoost confusion matrix")
# plt.show()

# Save model to file
filename = 'RF_model.sav'
dump(model_AdaBoost, open(filename, 'wb'))