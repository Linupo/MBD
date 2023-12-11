import csv
from multiprocessing.pool import ThreadPool as Pool
import pandas as pd
from predict_transaction import get_tx_data, predict
from pickle import load

model_file = "RF_model.sav"
scaler_file = "scaler.pkl"
model_RF = load(open(model_file, 'rb'))
scaler = load(open(scaler_file, 'rb'))


deanonym = pd.read_csv("predicted_unknown.csv")
predicted = pd.read_csv("predictions_comparison2.csv")
predictions = {}

for idx, txHash in enumerate(deanonym["txHash"]):
    if (len(predictions) + len(predicted) == 10000):
        break
    if txHash not in predicted["txHash"].tolist():
        print (f"predicting {idx}")
        predictions[txHash] = predict(txHash, scaler, model_RF)


with open('predictions_comparison.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['txHash', 'prediction'])
    for hash in predictions.keys():
        writer.writerow([hash, predictions[hash]])
    for idx in range(len(predicted)):
        writer.writerow([predicted["txHash"][idx], predicted["prediction"][idx]])
print ("done")