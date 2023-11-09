import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from pickle import dump
from sklearn.metrics import confusion_matrix

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

model_RF = RandomForestClassifier().fit(X_train.values,y_train.values)
y_preds = model_RF.predict(X_test.values)

accuracy = accuracy_score(y_test, y_preds)
print("Accuracy:", accuracy)

cm = confusion_matrix(y_test, y_preds)
print(cm)

filename = 'RF_model.sav'
dump(model_RF, open(filename, 'wb'))