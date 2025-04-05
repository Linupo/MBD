import os
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from pickle import dump
from utils import RANDOM_STATE, TRAIN_TEST_SPLIT, logInfo

script_dir = os.path.dirname(__file__)


# Crashes the laptop with the full dataset
def normalize_data_and_write_to_json(
    json_file_path: str,
    normalized_full_json_file_path: str,
) -> None:
    """
    Normalize the data from a JSON file and write the normalized data to another JSON file.
    This function removes the 'elliptic_label' column for normalization, scales the remaining features,
    and then writes the normalized dataset to a new JSON file, while also saving the scaler.
    The 'elliptic_label' column is added back to the normalized dataset before writing.
    """
    logInfo(f"Reading {json_file_path}")
    df = pd.read_json(json_file_path)

    logInfo(f"Removing columns unused when training")
    y = df["elliptic_label"]
    X = df.drop(
        columns=["elliptic_label", "time", "block_index", "block_height", "lock_time"]
    )  # Removing unused

    # legal = 2, illegal = 1

    X_train, _, _, _ = train_test_split(
        X,
        y,
        test_size=TRAIN_TEST_SPLIT,
        # The same random state should be used for all splits to ensure reproducibility
        random_state=RANDOM_STATE,
    )

    logInfo(f"Creating scaler")
    scaler = StandardScaler()
    # Fit the scaler only on train data, to avoid data leakage
    scaler.fit(X_train)


    full_df_scaled = pd.DataFrame(scaler.transform(X), columns=X_train.columns)


    with open(os.path.join(script_dir, "../pretrain", "all_features.json"), "w") as f:
        f.write(json.dumps(list(X_train.columns)))

    # save the scaler
    dump(scaler, open(os.path.join(script_dir, "../models", "scaler.pkl"), "wb"))

    logInfo(f"Writing normalized full dataset to {normalized_full_json_file_path}")
    full_df_scaled["elliptic_label"] = y
    full_df_scaled.to_json(normalized_full_json_file_path)


if __name__ == "__main__":
    json_file_path = os.path.abspath(
        os.path.join(script_dir, "../pretrain", "subset_pretrained_flat_txs.json")
    )

    normalized_full_json_file_path = os.path.abspath(
        os.path.join(
            script_dir,
            "../pretrain",
            "subset_normalized_json_file_with_scaler.json",
        )
    )

    normalize_data_and_write_to_json(
        json_file_path, normalized_full_json_file_path
    )
