# Forensics tool that predicts bitcoin transaction legality using AI

## Building the model

The model will be build using the following datasets to train the model:

- [Elliptic data set](https://www.kaggle.com/datasets/ellipticco/elliptic-data-set)
- [Deanonymized 99.5 pct of Elliptic dataset](https://www.kaggle.com/datasets/ellipticco/elliptic-data-set/discussion/117862)

These datasets are not stored inside the repository so first step would be to download them and place them in the repository root, inside a folder named `Elliptic_bitcoin_dataset`. After you've done so the file structure should look like this:

```c#
📁 MBD
├── README.MD
└──📁 src
	├──📁 frontend
	├──📁 elliptic_bitcoin_dataset
	|	├── deanonymized_result.csv //contains deanonymized map of transactions
	|	├── elliptic_txs_classes.csv
	|	├── elliptic_txs_edgelist.csv
	|	└── elliptic_txs_features.csv
	└──📁 scripts
		├── API.py // runs the API after the
		├── bitcoin_graph2.py
		├── comparison.py
		├── create_deanonymized_dataset.py // sends a series of requests to aquire real data from deanonymized dataset exposed hashes
		├── Example_visual.ipynb //contains an example on how to visualize the data
		├── Example.ipynb // contains an example on how to train models on anonymized data
		├── normalize.py // normilizes the data and creates a scaler
		├── predict_transaction.py // predicts transaction from hash
		├── predict_unknown_RF_ADA.py
		├── predict_unknown_XGBoost.py
		├── pretraining.py // prepares the data for normalizing
		├── train_models.py // trains model on real data after pretraining and normalization
		├── utils.py // python utilities (e.g. nice logging)
		├── visualize_transaction.ipynb // visualisation
		└── Visuals.ipynb // visualisation

```

### Getting real transaction data

First thing to do is to run `src/scripts/create_deanonymized_dataset.py` it should create a file: `src/pretrain/elliptic_txs.json`. It does so by using an https://blockchain.info/rawtx API to get transaction data. This also flattens the transactions and writes them to a file in `src/pretrain/flat_txs.json`

> NOTE: in the code the variables named tx refer to transaction
> NOTE: Getting real transactions for the first time take time (~1h)

### Pretraining

Then we do the pretraining (run `src/scripts/pretraining.py`), it does multiple things:

- Creates a subset of 1000 (since it's easier to create a model trained on 1000 observations, as if we used all of the labeled observations the process would take multiple hours). This number can be changed by passing `-s` parameter to the script.
- Changes the type of `elliptic_label` feature from string to int.
- Removes all string type features (only numeric features are used for training)
- Adds missing features. All of the transactions have different lengths of features so in order to fix that we find all the unique features then iterate over all the objects and see which ones are missing, add them with a value of 0. This step also creates a file named `src/pretrain/all_features.json` that has a list of all the unique features the dataset has.
- Convert boolean attribute values into binary type (0 and 1).
- After all of the above steps are completed it dumps the modified dataset into `src/pretrain/subset_pretrained_flat_txs.json`

### Normalization

The script `src/scripts/normalize.py` does 2 things:

1. Creates `src/pretrain/subset_normalized_json_file_with_scaler.json` dataset by normalizing `src/pretrain/subset_pretrained_flat_txs.json`
2. Creates a scaler `src/models/scaler.pkl`. This scaler will be used once we try to feed real-life transaction data to the model

### Training the random forest model

`src/scripts/train_models.py` script trains a random forest, ADABoost, XGBoost classifiers, prints the accuracy of the models and dumps the models into `src/models/<ModelName>.sav` (the name is different for different test / train splits and different classifiers).

### Predicting transaction using CLI

Running `python .\src\scripts\predict_transaction.py 48cc5af8141a7be7b396029e5093a9f0fe78ea03076ebd4bc805bd977e93fbcc` will log if the transaction hash provided is legal or not.

### Visuals

To visualise the trees run python notebook `tree_visuals.ipynb`

## Running the API

### Getting Started with API

Running the API requires all the above steps to be completed. To run the API enter the following line in repository root terminal:

```shell
cd src/scripts/
uvicorn API:app --reload
```

This will start the api on http://127.0.0.1:8000.

### API EndPoints

```
http://127.0.0.1:8000/transaction/?txHash=4f4ddca2436e5c3f9ecda31a2d1d3209d3f1658e5845bf5d6dfb46c0dc6f1a4b
```

Where the txHash can be changed into any bitcoin transaction hash. The API endpoint queries real raw data of the transaction, prepares it for the scaler that was saved before, scales the raw data, loads the model and predicts what the legality of the transaction could be. The response looks like this:

```json
{
  "txHash": "4f4ddca2436e5c3f9ecda31a2d1d3209d3f1658e5845bf5d6dfb46c0dc6f1a4b",
  "isLegal": true,
  "rawTx": {
	...
  }
}
```

## Running the t3 app

To run the web application execute the following command:

```shell
cd src/frontend/
npm install
npm run dev
```
