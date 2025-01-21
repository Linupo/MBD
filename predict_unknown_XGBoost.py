import csv
import json
from multiprocessing.pool import ThreadPool as Pool
import pandas as pd
from predict_transaction import get_tx_data, predict, preprocess_tx
from pickle import load

scaler = load(open("scaler.pkl", 'rb'))

with open("unknown_raw_txs.json", 'r') as j:
     contents = json.loads(j.read())

def check_predictions(_model_XG_80_20, _model_XG_75_25, _model_XG_70_30):
    predictions_80 = {}
    predictions_75 = {}
    predictions_70 = {}

    for idx, tx in enumerate(contents):
        if idx == 1000:
            break
        processed_tx = preprocess_tx(tx, scaler)
        prediction_80 = predict(tx["hash"], scaler, _model_XG_80_20, preprocessed_tx=processed_tx, XGBoost=True)
        prediction_75 = predict(tx["hash"], scaler, _model_XG_75_25, preprocessed_tx=processed_tx, XGBoost=True)
        prediction_70 = predict(tx["hash"], scaler, _model_XG_70_30, preprocessed_tx=processed_tx, XGBoost=True)
        print (f"{idx} : {prediction_80} {prediction_75} {prediction_70}")
        predictions_80[tx["hash"]] = prediction_80
        predictions_75[tx["hash"]] = prediction_75
        predictions_70[tx["hash"]] = prediction_70

    with open(f"comparison/XG_80_20.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['txHash', 'predictionRF'])
        for hash in predictions_80.keys():
            writer.writerow([hash, predictions_80[hash]])

    with open(f"comparison/XG_75_25.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['txHash', 'predictionRF'])
        for hash in predictions_75.keys():
            writer.writerow([hash, predictions_75[hash]])

    with open(f"comparison/XG_70_30.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['txHash', 'predictionRF'])
        for hash in predictions_70.keys():
            writer.writerow([hash, predictions_70[hash]])

model_XG_80 = load(open("models/XG_model_20_80.sav", 'rb'))
model_XG_75 = load(open("models/XG_model_25_75.sav", 'rb'))
model_XG_70 = load(open("models/XG_model_30_70.sav", 'rb'))
check_predictions(model_XG_80, model_XG_75, model_XG_70)