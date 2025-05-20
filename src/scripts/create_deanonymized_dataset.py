import pandas as pd
import requests
import json
import argparse
import os
from flatten_json import flatten
from utils import logInfo

script_dir = os.path.dirname(__file__)


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument(
        "-n",
        "--limitUnknown",
        help="Number of unknown transactions to get from API",
        type=int,
        default=1000,
    )
    parser.add_argument(
        "-l",
        "--limitTransactions",
        help="Number of good and bad transactions to get from API",
        type=int,
    )
    parser.add_argument(
        "-s",
        "--skipAPIFetch",
        help="Skip API fetching, only flatten",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-t",
        "--trimJson",
        help="Trim json to not include inputs and outputs",
        action="store_true",
        default=False,
    )

    # Parse arguments
    args = parser.parse_args()

    return args


def getRealTransactionData(limitUnknown: int, limitTransactions: int, trimJson: bool):
    """
    Fetches and processes real transaction data from data files using API.
    This function performs the following steps:
    1. Reads dataset files containing transaction classes and deanonymized results.
    2. Merges the datasets on the transaction ID.
    3. Labels transactions as good, bad, or unknown (according to ).
    4. Fetches legal, illegal and unknown transaction data from the blockchain.info API.
    5. Writes the fetched transaction data to JSON files.
    """

    logInfo(f"Reading dataset files")

    classes = pd.read_csv(
        os.path.join(script_dir, "../elliptic_bitcoin_dataset/elliptic_txs_classes.csv")
    )
    deanonym = pd.read_csv(
        os.path.join(script_dir, "../elliptic_bitcoin_dataset/deanonymized_result.csv")
    )

    df = classes.merge(deanonym, on=["txId"])

    labeled_txs = df
    labeled_txs.loc[labeled_txs["class"] == "unknown", "class"] = "3"
    labeled_txs.head()

    good_txs = labeled_txs[labeled_txs["class"] == "2"]
    bad_txs = labeled_txs[labeled_txs["class"] == "1"]
    unknown_txs = labeled_txs[labeled_txs["class"] == "3"]

    logInfo(f"good_tx_list length: {len(good_txs)}")
    logInfo(f"bad_tx_list length: {len(bad_txs)}")
    logInfo(f"unknown_txs_list length: {len(unknown_txs)}")
    logInfo(f"Total length: {len(labeled_txs)}")

    if not os.path.exists(os.path.join(script_dir, "../pretrain/elliptic_txs.json")):
        json_list = []
        txs_failed_list = []

        logInfo(f"Getting legal transaction data from API")

        # legal transactions
        n = limitTransactions if limitTransactions else len(good_txs)
        for i in range(n):
            logInfo(f"Legal txs [{i}/{n}]", end="\r")
            try:
                response = requests.get(
                    f"https://blockchain.info/rawtx/{good_txs['transaction'].iloc[i]}"
                )
                tx_json = response.json()
                tx_json["elliptic_label"] = good_txs["class"].iloc[i]
                if trimJson:
                    drop_inputs_outputs(tx_json)
                json_list.append(tx_json)
            except Exception:
                txs_failed_list.append(good_txs["transaction"].iloc[i])

        logInfo(f"Finished getting legal transactions")

        logInfo(f"Getting illegal transaction data from API")

        # illegal transactions
        n = limitTransactions if limitTransactions else len(bad_txs)
        for i in range(n):
            logInfo(f"Illegal txs [{i}/{n}]", end="\r")
            try:
                response = requests.get(
                    f"https://blockchain.info/rawtx/{bad_txs['transaction'].iloc[i]}"
                )
                tx_json = response.json()
                tx_json["elliptic_label"] = bad_txs["class"].iloc[i]
                if trimJson:
                    drop_inputs_outputs(tx_json)
                json_list.append(tx_json)
            except Exception:
                txs_failed_list.append(bad_txs["transaction"].iloc[i])

        logInfo(f"Finished getting illegal transactions, writing to file...")

        os.makedirs(os.path.join(script_dir, "../pretrain"), exist_ok=True)
        with open(os.path.join(script_dir, "../pretrain/elliptic_txs.json"), "w") as f:
            f.writelines(json.dumps(json_list))

        with open(os.path.join(script_dir, "../pretrain/failed_txs.json"), "w") as f:
            f.writelines(txs_failed_list)
    else:
        logInfo("File elliptic_txs.json already exists. Skipping data fetching.")

    if not os.path.exists(os.path.join(script_dir, "../pretrain/unknown_raw_txs.json")):
        logInfo(f"Getting {limitUnknown} unknown transaction data from API")
        json_list_unknown = []
        txs_failed_list = []
        # unknown transactions
        for i in range(limitUnknown):
            try:
                logInfo(f"Unknown txs [{i}/{limitUnknown}]", end="\r")
                response = requests.get(
                    f"https://blockchain.info/rawtx/{unknown_txs['transaction'].iloc[i]}"
                )
                tx_json = response.json()
                if trimJson:
                    drop_inputs_outputs(tx_json)
                json_list_unknown.append(tx_json)
            except Exception:
                txs_failed_list.append(unknown_txs["transaction"].iloc[i])

        logInfo(f"Finished getting unknown transactions, writing to file...")

        with open(
            os.path.join(script_dir, "../pretrain/unknown_raw_txs.json"), "w"
        ) as f:
            f.writelines(json.dumps(json_list_unknown))

        with open(os.path.join(script_dir, "../pretrain/failed_txs.json"), "w") as f:
            f.writelines(txs_failed_list)
    else:
        logInfo("File unknown_raw_txs.json already exists. Skipping data fetching.")

def drop_inputs_outputs(tx):
    if "inputs" in tx:
        del tx["inputs"]
    if "out" in tx:
        del tx["out"]
    if "ver" in tx:
        del tx["ver"]
    if "tx_index" in tx:
        del tx["tx_index"]
    if "double_spend" in tx:
        del tx["double_spend"]


def flatten_txs():
    """
    This function reads transaction data from 'elliptic_txs.json', flattens each transaction,
    and writes the flattened transactions to 'flat_txs.json'.
    The function performs the following steps:
    1. Opens and reads the JSON file containing transaction data.
    2. Flattens each transaction using the `flatten` function.
    3. Writes the flattened transactions to a new JSON file.
    """
    if not os.path.exists(os.path.join(script_dir, "../pretrain/flat_txs.json")):

        f = open(os.path.join(script_dir, "../pretrain/elliptic_txs.json"))
        data = json.load(f)
        flat_txs = []

        logInfo(f"Flattening transaction data")
        for tx in data:
            flat_tx = flatten(tx)
            flat_txs.append(flat_tx)

        with open(os.path.join(script_dir, "../pretrain/flat_txs.json"), "w") as f:
            json.dump(flat_txs, f, indent=2)
    else:
        logInfo("File flat_txs.json already exists. Skipping data flattening.")


if __name__ == "__main__":
    # Parse the arguments
    args = parseArguments()

    # Get real transaction data
    if not args.skipAPIFetch:
        getRealTransactionData(args.limitUnknown, args.limitTransactions, args.trimJson)
    else:
        logInfo("Skipping API real data fetching.")

    # Flatten transactions
    flatten_txs()
