import os
import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.model_selection import GridSearchCV, train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

from train_models import remove_dataframe_features_with_all_null_values
from utils import RANDOM_STATE, TRAIN_TEST_SPLIT, logInfo

script_dir = os.path.dirname(__file__)

logInfo(f"Reading dataset files")

df = pd.read_json(
    os.path.join(
        script_dir, "..", "pretrain", "subset_normalized_json_file_with_scaler.json"
    )
)
df = remove_dataframe_features_with_all_null_values(df)

X = df.drop(columns=["elliptic_label"])  # delete unused
y = df["elliptic_label"]

xgb = XGBClassifier()

# Parameter grid for hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 1]
}

grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, cv=2, scoring='accuracy', verbose=1)

le = LabelEncoder()
y = y.apply(lambda x: 0 if x == 2 else 1 )
y = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TRAIN_TEST_SPLIT, random_state=RANDOM_STATE)
grid_search.fit(X_train, y_train)

# Print the best parameters and accuracy
logInfo("Best Parameters:", grid_search.best_params_)
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
logInfo("Test Accuracy:", accuracy_score(y_test, y_pred))