import pandas as pd

predictions_mine = pd.read_csv("predictions_mine.csv")
predictions_elliptic = pd.read_csv("predicted_unknown.csv")
predictions_elliptic = predictions_elliptic.loc[predictions_elliptic["txHash"].isin(predictions_mine["txHash"])]

# General info
print(f"[Mine] Predicted legal transactions {len(predictions_mine.loc[predictions_mine['prediction'] == True])}")
print(f"[Mine] Predicted illegal transactions {len(predictions_mine.loc[predictions_mine['prediction'] == False])}")

print(f"[Elliptic] Predicted legal transactions {len(predictions_elliptic.loc[predictions_elliptic['prediction'] == 0])}")
print(f"[Elliptic] Predicted illegal transactions {len(predictions_elliptic.loc[predictions_elliptic['prediction'] == 1])}")

predictions_mine_map = {}
predictions_elliptic_map = {}

for idx in range(len(predictions_mine)):
    predictions_mine_map[predictions_mine['txHash'][idx]] = 0 if predictions_mine['prediction'][idx] else 1
for idx in range(len(predictions_elliptic)):
    predictions_elliptic_map[predictions_elliptic['txHash'][idx]] = predictions_elliptic['prediction'][idx]

count = 0
for txHash in predictions_mine_map.keys():
    if predictions_mine_map[txHash] == predictions_elliptic_map[txHash]:
        count += 1

print(f"Percent of same predictions {count/len(predictions_mine_map.keys())}")
