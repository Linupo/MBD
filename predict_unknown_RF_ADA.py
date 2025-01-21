import csv
import json
from multiprocessing.pool import ThreadPool as Pool
import pandas as pd
from predict_transaction import get_tx_data, predict
from pickle import load

scaler = load(open("scaler.pkl", 'rb'))

with open("unknown_raw_txs.json", 'r') as j:
     contents = json.loads(j.read())

def check_predictions(_model_RF, _model_ADA, trainPortion):
    predictions = {}

    for idx, tx in enumerate(contents):
        if idx == 1000:
            break
        print (f"predicting {idx}")
        predictions[tx["hash"]] = (predict(tx["hash"], scaler, _model_RF, rawTx=tx), predict(tx["hash"], scaler, _model_ADA, rawTx=tx))

    with open(f"predictions_comparison_{trainPortion}_{100-trainPortion}.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['txHash', 'predictionRF', 'predictionADA'])
        for hash in predictions.keys():
            writer.writerow([hash, predictions[hash][0], predictions[hash][1]])


model_RF = load(open("models/RF_model_20_80.sav", 'rb'))
model_ADA = load(open("models/ADA_model_20_80.sav", 'rb'))
check_predictions(model_RF, model_ADA, 80)

model_RF = load(open("models/RF_model_25_75.sav", 'rb'))
model_ADA = load(open("models/ADA_model_25_75.sav", 'rb'))
check_predictions(model_RF, model_ADA, 75)

model_RF = load(open("models/RF_model_30_70.sav", 'rb'))
model_ADA = load(open("models/ADA_model_30_70.sav", 'rb'))
check_predictions(model_RF, model_ADA, 70)

print ("done")