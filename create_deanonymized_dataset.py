import pandas as pd 
import requests
import json
import argparse
import os


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-n", "--limitUnknown", help="Number of unknown transactions to get from API", type=int, default=1000)

    # Parse arguments
    args = parser.parse_args()

    return args


def getRealTransactionData(limitUnknown: int):
    """
    Fetches and processes real transaction data from data files using API.
    This function performs the following steps:
    1. Reads dataset files containing transaction classes and deanonymized results.
    2. Merges the datasets on the transaction ID.
    3. Labels transactions as good, bad, or unknown (according to ).
    4. Fetches legal, illegal and unknown transaction data from the blockchain.info API.
    5. Writes the fetched transaction data to JSON files.
    """

    print(f"-----------------------------------------")
    print(f"Reading dataset files")
    print(f"-----------------------------------------")

    classes = pd.read_csv('elliptic_bitcoin_dataset/elliptic_txs_classes.csv')
    deanonym = pd.read_csv("elliptic_bitcoin_dataset/deanonymized_result.csv")

    df=classes.merge(deanonym, on=["txId"])

    labeled_txs = df
    labeled_txs.loc[labeled_txs["class"]=="unknown", "class"] = "3"
    labeled_txs.head()

    good_txs = labeled_txs[labeled_txs['class'] == "2"]
    bad_txs = labeled_txs[labeled_txs['class'] == "1"]
    unknown_txs = labeled_txs[labeled_txs['class'] == "3"]

    print(f"good_tx_list length: {len(good_txs)}")
    print(f"bad_tx_list length: {len(bad_txs)}")
    print(f"unknown_txs_list length: {len(unknown_txs)}")
    print(f"Total length: {len(labeled_txs)}")


    if not os.path.exists("pretrain/elliptic_txs.json"):
        json_list = []
        txs_failed_list = []

        print(f"-----------------------------------------")
        print(f"Getting legal transaction data from API")
        print(f"-----------------------------------------")
        # legal transactions
        for i in range(len(good_txs)):
            print(f"Legal txs [{i}/{len(good_txs)}]", end='\r')
            try:
                response = requests.get(f"https://blockchain.info/rawtx/{good_txs['transaction'].iloc[i]}")
                tx_json = response.json()
                tx_json["elliptic_label"] = good_txs['class'].iloc[i]
                json_list.append(tx_json)
            except Exception:
                txs_failed_list.append(good_txs['transaction'].iloc[i])

        print(f"Finished getting legal transactions")

        print(f"-----------------------------------------")
        print(f"Getting illegal transaction data from API")
        print(f"-----------------------------------------")
        # illegal transactions
        for i in range(len(bad_txs)):
            print(f"Illegal txs [{i}/{len(bad_txs)}]", end='\r')
            try:
                response = requests.get(f"https://blockchain.info/rawtx/{bad_txs['transaction'].iloc[i]}")
                tx_json = response.json()
                tx_json["elliptic_label"] = bad_txs['class'].iloc[i]
                json_list.append(tx_json)
            except Exception:
                txs_failed_list.append(bad_txs['transaction'].iloc[i])

        print(f"Finished getting illegal transactions")

        print(f"-----------------------------------------")
        print(f"Writing to file")
        print(f"-----------------------------------------")
        os.makedirs("pretrain", exist_ok=True)
        with open("pretrain/elliptic_txs.json", "w") as f:
            f.writelines(json.dumps(json_list))

        with open("pretrain/failed_txs.json", "w") as f:
            f.writelines(txs_failed_list)
    else:
        print("File pretrain/elliptic_txs.json already exists. Skipping data fetching.")

    print(f"-----------------------------------------")
    print(f"Getting unknown transaction data from API")
    print(f"-----------------------------------------")

    json_list_unknown = []
    txs_failed_list = []
    # legal transactions
    for i in range(limitUnknown):
        try:
            print(f"Unknown txs [{i}/{limitUnknown}]", end='\r')
            response = requests.get(f"https://blockchain.info/rawtx/{unknown_txs['transaction'].iloc[i]}")
            tx_json = response.json()
            json_list_unknown.append(tx_json)
        except Exception:
            txs_failed_list.append(unknown_txs['transaction'].iloc[i])

    print(f"Finished getting unknown transactions")

    print(f"-----------------------------------------")
    print(f"Writing to file")
    print(f"-----------------------------------------")

    with open("pretrain/unknown_raw_txs.json", "w") as f:
        f.writelines(json.dumps(json_list_unknown))

    with open("pretrain/failed_txs.json", "w") as f:
        f.writelines(txs_failed_list)

if __name__ == '__main__':
    # Parse the arguments
    args = parseArguments()

    # Get real transaction data
    getRealTransactionData(args.limitUnknown)
