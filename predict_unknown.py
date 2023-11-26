import csv
from multiprocessing.pool import ThreadPool as Pool
import pandas as pd
from predict_transaction import get_tx_data, predict
from pickle import load

model_file = "RF_model.sav"
scaler_file = "scaler.pkl"
model_RF = load(open(model_file, 'rb'))
scaler = load(open(scaler_file, 'rb'))

# define worker function before a Pool is instantiated
def worker(hash):
    try:
        predictions[hash] = predict(hash, scaler, model_RF)
    except:
        print('error with item')

pool = Pool(5)

deanonym = pd.read_csv("predicted_unknown.csv")
predictions = {}
count = len(deanonym)

for idx, txHash in enumerate(deanonym["txHash"]):
    print (f"predicting {idx}/{count}")
    if (idx == 1000):
        break
    pool.apply_async(worker, (txHash,))

print ("closing pool")
pool.close()
pool.join()

with open('predictions_comparison.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['txHash', 'prediction'])
    for hash in predictions.keys():
        writer.writerow([hash, predictions[hash]])
print ("done")