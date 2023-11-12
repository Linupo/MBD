from fastapi import FastAPI
import requests
import json
import pandas as pd
import requests
from flatten_json import flatten
from pickle import load
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:3000",
]

features_json_file = "all_features.json"
model_file = "RF_model.sav"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_RF = load(open(model_file, 'rb'))
scaler = load(open('scaler.pkl', 'rb'))


# ----------------------------------------------------------------------------------------
# Real data transaction prediction
# Tx hash for prediction: 4f4ddca2436e5c3f9ecda31a2d1d3209d3f1658e5845bf5d6dfb46c0dc6f1a4b
# Known bad tx: 48cc5af8141a7be7b396029e5093a9f0fe78ea03076ebd4bc805bd977e93fbcc
# ----------------------------------------------------------------------------------------

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
            tx_without_strings[feature] = 0

    # Remove if it has additional features
    new_tx = {}
    for key, value in tx_without_strings.items():
        if key in features:
            new_tx[key] = value

    df = pd.DataFrame([new_tx])
    tx = scaler.transform(df)

    return (tx)

@app.get("/transaction/")
async def transaction_legality(txHash: str = None):
    if not txHash:
        return {"No txHash"}
    tx = get_tx_data(txHash)
    tx = preprocess_tx(tx)

    y = model_RF.predict(tx)[0]

    predicted = True
    if y == 1:
        predicted = False

    return {"txHash": txHash, "isLegal": predicted}

@app.get("/wallet/")
async def wallet_legality(walletAddr: str = None):
    if not walletAddr:
        return {"No walletAddr"}
    wallet = get_wallet_data(walletAddr)

    result = []
    for wallet_tx in wallet['txs']:
        tx = preprocess_tx(wallet_tx)
        y = model_RF.predict(tx)[0]

        predicted = True
        if y == 1:
            predicted = False

        result.append(
            {
                "txHash": wallet_tx['hash'],
                "isLegal": predicted
            }
        )

    return result
