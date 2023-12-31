# Forensics tool that predicts bitcoin transaction legality using AI

## Building the model

The model will be build using the following datasets to train the model:

- [Elliptic data set](https://www.kaggle.com/datasets/ellipticco/elliptic-data-set)
- [Deanonymized 99.5 pct of Elliptic dataset](https://www.kaggle.com/datasets/ellipticco/elliptic-data-set/discussion/117862)

These datasets are not stored inside the repository so first step would be to download them and place them in the repository root, inside a folder named `Elliptic_bitcoin_dataset`. After you've done so the file structure should look like this:

```c#
📁 MBD
├── API.py // runs the API after the
├── Example.ipynb // contains an example on how to train models on anonymized data
├── Example_visual.ipynb //contains an example on how to visualize the data
├── create_deanonymized_dataset.ipynb // sends a series of requests to aquire real data from deanonymized dataset exposed hashes
├── flatten.ipynb // flattens the real transaction data
├── normalize.py // normilizes the data and creates a scaler
├── pretraining.py // prepares the data for normalizing
├── RF_on_real_data.py // trains model on real data after pretraining and normalization
└──📁 Elliptic_bitcoin_dataset
	├── deanonymized_result.csv //contains deanonymized map of transactions
	├── elliptic_txs_classes.csv
	├── elliptic_txs_edgelist.csv
	└── elliptic_txs_features.csv
```

### Getting real transaction data

First thing to do is to run `create_deanonymized_dataset.ipynb` it should create a file: `elliptic_txs_json.json`. It does so by using an https://blockchain.info/rawtx API to get transaction data.

> NOTE: in the code the variables named tx refer to transaction

### Flattening the nested arrays

After the `elliptic_txs_json.json` is created you must run the `flatten.ipynb`, this script flattens all the nested arrays and dictionaries of the json and dumps it into `flat_txs.json` file.

### Pretraining

Then we do the pretraining (run `pretraining.py`), it does multiple things:

- Creates a subset of 200 (since it's easier to create a model trained on 200 observations, as if we used all of the labeled observations the process would take multiple hours). This number can be changed.
- Changes the type of `elliptic_label` feature from string to int.
- Removes all string type features (only numeric features are used for training)
- Adds missing features. All of the transactions have different lengths of features so in order to fix that we find all the unique features then iterate over all the objects and see which ones are missing, add them with a value of 0. This step also creates a file named `all_features.json` that has a list of all the unique features the dataset has.
- Convert boolean attribute values into binary type (0 and 1).
- After all of the above steps are completed it dumps the modified dataset into `subset_pretrained_flat_txs.json`

### Normalization

The script `normalize.py` does 2 things:

1. Creates a `subset_normalized_json_file_with_scaler.json` dataset by normalizing the `subset_pretrained_flat_txs.json`
2. Creates a scaler `scaler.pkl`. This scaler will be used once we try to feed real-life transaction data to the model

### Training the random forest model

`RF_on_real_data.py` script splits the 200 observations into test (25%) and train (75%) subsets, trains a random forest classifier, prints the accuracy of the model and dumps the model into `RF_model.sav`.

### Running the API

To run the API enter the following line in repository root terminal:

```shell
uvicorn API:app --reload
```

This will start the api on http://127.0.0.1:8000. Right now it has one endpoint:

```
http://127.0.0.1:8000/transaction/?txHash=4f4ddca2436e5c3f9ecda31a2d1d3209d3f1658e5845bf5d6dfb46c0dc6f1a4b
```

Where the txHash can be changed into any bitcoin transaction hash. The API endpoint queries real raw data of the transaction, prepares it for the scaler that was saved before, scales the raw data, loads the model and predicts what the legality of the transaction could be. The response looks like this:

```json
{
  "txHash": "4f4ddca2436e5c3f9ecda31a2d1d3209d3f1658e5845bf5d6dfb46c0dc6f1a4b",
  "isLegal": true
}
```

### Running the t3 app

To run the web application execute the following command:

```
npm install
npm run dev
```
