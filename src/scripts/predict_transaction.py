import argparse
import json
import os
import pickle
import pandas as pd
import requests
from flatten_json import flatten
from utils import logInfo

# ----------------------------------------------------------------------------------------
# Real data transaction prediction
# Tx hash for prediction: 4f4ddca2436e5c3f9ecda31a2d1d3209d3f1658e5845bf5d6dfb46c0dc6f1a4b
# Known bad tx: 48cc5af8141a7be7b396029e5093a9f0fe78ea03076ebd4bc805bd977e93fbcc
# ----------------------------------------------------------------------------------------

script_dir = os.path.dirname(__file__)
features_json_file = os.path.join(script_dir, "../pretrain/all_features.json")
XG_labe_encoder = os.path.join(script_dir, "../models/XGLabelEncoder.pkl")


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "hash",
        help="Hash of the transaction to predict",
    )

    # Parse arguments
    args = parser.parse_args()

    return args


def predict(
    txHash, scaler, model, rawTx=None, preprocessed_tx=None, XGBoost=False
) -> bool:
    if rawTx is None and preprocessed_tx is None:
        rawTx = get_tx_data(txHash)

    if preprocessed_tx is None:
        tx = preprocess_tx(rawTx, scaler)
    else:
        tx = preprocessed_tx

    if XGBoost:
        y = model.predict(tx)
        le = pickle.load(open(XG_labe_encoder, "rb"))
        y = 0 if le.inverse_transform(y)[0] == 2 else 1
    else:
        y = model.predict(tx)[0]

    predicted = True
    if y == 1:
        predicted = False
    return predicted


def get_tx_data(hash):
    try:
        response = requests.get(f"https://blockchain.info/rawtx/{hash}")
        tx_json = response.json()
        return tx_json
    except Exception:
        logInfo("Failed to get the Tx data from blockchain.info API")


def get_wallet_data(addr):
    try:
        response = requests.get(f"https://blockchain.info/rawaddr/{addr}")
        wallet_json = response.json()
        return wallet_json
    except Exception:
        logInfo("Failed to get the wallet data from blockchain.info API")


def preprocess_tx(tx, scaler):
    # flatten
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
        if feature not in tx_without_strings and feature != "elliptic_label":
            tx_without_strings[feature] = 0

    # Remove if it has additional features
    new_tx = {}
    for key, value in tx_without_strings.items():
        if key in features:
            new_tx[key] = value

    df = pd.DataFrame([new_tx])
    tx = scaler.transform(df)

    return tx


if __name__ == "__main__":
    # Parse the arguments
    args = parseArguments()

    script_dir = os.path.dirname(__file__)

    model_file = os.path.join(script_dir, "../models/RF_model.sav")
    scaler_file = os.path.join(script_dir, "../models/scaler.pkl")
    model_RF = pickle.load(open(model_file, "rb"))
    scaler = pickle.load(open(scaler_file, "rb"))

    logInfo(f"Transaction legal: {predict(args.hash, scaler, model_RF)}")
