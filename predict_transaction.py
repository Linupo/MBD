import json
import pandas as pd
import requests
from flatten_json import flatten
# ----------------------------------------------------------------------------------------
# Real data transaction prediction
# Tx hash for prediction: 4f4ddca2436e5c3f9ecda31a2d1d3209d3f1658e5845bf5d6dfb46c0dc6f1a4b
# Known bad tx: 48cc5af8141a7be7b396029e5093a9f0fe78ea03076ebd4bc805bd977e93fbcc
# ----------------------------------------------------------------------------------------

features_json_file = "all_features.json"

def predict(txHash, scaler, model):
    rawTx = get_tx_data(txHash)
    tx = preprocess_tx(rawTx, scaler)

    y = model.predict(tx)[0]

    predicted = True
    if y == 1:
        predicted = False
    return predicted

def get_tx_data (hash):
    try:
        response = requests.get(f"https://blockchain.info/rawtx/{hash}")
        tx_json = response.json()
        return tx_json
    except Exception:
        print("Failed to get the Tx data")

def get_wallet_data (addr):
    try:
        response = requests.get(f"https://blockchain.info/rawaddr/{addr}")
        wallet_json = response.json()
        return wallet_json
    except Exception:
        print("Failed to get the wallet data")

def preprocess_tx (tx, scaler):
    #flatten
    tx = flatten(tx)

    # Make bool binary
    for key, value in tx.items():
      if isinstance(value, bool):
        value = int(value)
      tx[key] = value

    # Remove string features
    tx_without_strings = {}
    for key, value in tx.items():
        if isinstance(value, int) or isinstance(value, float):
            tx_without_strings[key] = value

    # Add missing features
    with open(features_json_file, "r") as f:
        json_features = f.read()
    features = json.loads(json_features)

    for feature in features:
        if feature not in tx_without_strings and feature != 'elliptic_label':
            tx_without_strings[feature] = 0

    # Remove if it has additional features
    new_tx = {}
    for key, value in tx_without_strings.items():
        if key in features:
            new_tx[key] = value

    df = pd.DataFrame([new_tx])
    tx = scaler.transform(df)

    return (tx)