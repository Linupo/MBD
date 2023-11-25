from fastapi import FastAPI
from pickle import load
from fastapi.middleware.cors import CORSMiddleware
from predict_transaction import get_tx_data, get_wallet_data, predict, preprocess_tx

origins = [
    "http://localhost",
    "http://localhost:3000",
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_file = "RF_model.sav"
scaler_file = "scaler.pkl"
model_RF = load(open(model_file, 'rb'))
scaler = load(open(scaler_file, 'rb'))

@app.get("/transaction/")
async def transaction_legality(txHash: str = None):
    if not txHash:
        return {"No txHash"}
    rawTx = get_tx_data(txHash)
    predicted = predict(txHash, scaler, model_RF)

    return {"txHash": txHash, "isLegal": predicted, "rawTx": rawTx}

@app.get("/wallet/")
async def wallet_legality(walletAddr: str = None):
    if not walletAddr:
        return {"No walletAddr"}
    wallet = get_wallet_data(walletAddr)

    result = []
    for wallet_tx in wallet['txs']:
        tx = preprocess_tx(wallet_tx, scaler)
        y = model_RF.predict(tx)[0]

        predicted = True
        if y == 1:
            predicted = False

        result.append(
            {
                "isLegal": predicted,
                "rawTx": wallet_tx
            }
        )

    return result
