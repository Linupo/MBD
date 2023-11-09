import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from pickle import dump

# 1st normalization try, will not work since we need the scaler to scale the real data
# def normalize_data_and_write_to_json(json_file_path, normalized_json_file_path):
#   df = pd.read_json(json_file_path)
#   normalized_df=(df-df.min())/(df.max()-df.min())
#   # normalized_df=(df-df.mean())/df.std()
#   normalized_df.to_json(normalized_json_file_path)


# Crashes the laptop with the full dataset
def normalize_data_and_write_to_json(json_file_path, normalized_json_file_path):
  df = pd.read_json(json_file_path)

  y = df['elliptic_label']
  X = df.drop(columns=['elliptic_label']) # ismetam nereikalingus

  # df_scaled = pd.DataFrame(scaler.fit_transform(X),columns = df.columns)

  scaler = StandardScaler()
  df_scaled = pd.DataFrame(scaler.fit_transform(X),columns = X.columns)

  # save the scaler
  dump(scaler, open('scaler.pkl', 'wb'))

  df_scaled['elliptic_label'] = y
  df_scaled.to_json(normalized_json_file_path)

if __name__ == "__main__":
  json_file_path = "subset_pretrained_flat_txs.json"
  normalized_json_file_path = "subset_normalized_json_file_with_scaler.json"

  normalize_data_and_write_to_json(json_file_path, normalized_json_file_path)