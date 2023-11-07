from fastapi import FastAPI
import requests
import json
import pandas as pd
import requests
from flatten_json import flatten
from pickle import load

features_json_file = "all_features.json"
model_file = "RF_model.sav"

app = FastAPI()

# ----------------------------------------------------------------------------------------
# Real data transaction prediction
# Tx hash for prediction: 4f4ddca2436e5c3f9ecda31a2d1d3209d3f1658e5845bf5d6dfb46c0dc6f1a4b
# ----------------------------------------------------------------------------------------

def get_tx_data (hash):
    try:
        response = requests.get(f"https://blockchain.info/rawtx/{hash}")
        tx_json = response.json()
        return tx_json
    except Exception:
        print("Failed to get the Tx data")

def preprocess_tx (tx):
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
        if not isinstance(value, str):
            tx_without_strings[key] = value
        # remove lists, since there seems to be some empty [] in there
        if isinstance(value, list):
            tx_without_strings[key] = 0
    
    # Add missing features
    with open(features_json_file, "r") as f:
        json_features = f.read()
    features = json.loads(json_features)

    for feature in features:
        if feature not in tx_without_strings and feature != 'elliptic_label':
        # if feature not in tx_without_strings:
            tx_without_strings[feature] = 0

    # Remove if it has additional features
    # union = set(features) | set(tx_without_strings.keys())
    # for feature in features:
    #     if key not in union:
    #         del tx_without_strings[key]

    scaler = load(open('scaler.pkl', 'rb'))
    df = pd.DataFrame([tx_without_strings])
    tx = scaler.transform(df)

    return (tx)


@app.get("/transaction/")
async def transaction_legality(txHash: str = None):
    if not txHash:
        return {"No txHash"}
    tx = get_tx_data(txHash)
    tx = preprocess_tx(tx)

    model_RF = load(open(model_file, 'rb'))
    y = model_RF.predict(tx)[0]

    if y == 1:
        predicted = True
    if y == 0:
        predicted = False

    return {"txHash": txHash, "isLegal": predicted}
