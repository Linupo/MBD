import { useState } from "react";
import { getRequest } from "~/api/network";
import TransactionGraph from "./transactionGraph";

interface transactionResponse {
  txHash: string;
  isLegal: boolean;
  rawTx: any;
}

const transactionRequest = (hash: string) =>
  getRequest({
    path: `transaction/?txHash=${hash}`,
  });

export default function TransactionLegalityCheck() {
  const [isLegal, setIsLegal] = useState<boolean>();
  const [txHash, setTxHash] = useState<string>("");
  const [rawTxData, setRawTxData] = useState();

  const fetchData = async () => {
    await transactionRequest(txHash).then((data: transactionResponse) => {
      // console.log(data.isLegal);
      setIsLegal(data.isLegal);
      setRawTxData(data.rawTx);
    });
  };

  const checkIfLegal = () => {
    fetchData().catch(console.error);
  };
  return (
    <div>
      <div className="flex-center p flex justify-center pt-6 text-lg text-white">
        <div className="w-4 flex-auto p-4 text-right font-mono">
          Enter transaction hash:
        </div>
        <input
          className={
            isLegal
              ? "block w-4 flex-auto rounded-lg border p-2.5 font-mono font-sans text-lg text-green-900 placeholder-green-700 focus:border-green-500 focus:ring-green-500 dark:border-green-500 dark:bg-gray-700 dark:text-green-400 dark:placeholder-green-500"
              : isLegal == false
              ? "block w-4 flex-auto rounded-lg border p-2.5 font-mono font-sans text-lg text-red-900 placeholder-red-700 focus:border-red-500 focus:ring-red-500 dark:border-red-500 dark:bg-gray-700 dark:text-red-400 dark:placeholder-red-500"
              : "block w-4 flex-auto rounded-lg border p-2.5 font-mono font-sans text-lg text-cyan-900 placeholder-cyan-700 focus:border-cyan-500 focus:ring-cyan-500 dark:border-cyan-500 dark:bg-gray-700 dark:text-cyan-400 dark:placeholder-cyan-500"
          }
          type="text"
          value={txHash}
          onChange={(e) => setTxHash(e.target.value)}
        />
        <div className="w-4 flex-auto p-1">
          <button
            className=" rounded border-b-4 border-cyan-700 bg-cyan-500 px-4 py-2 text-left font-mono text-lg font-bold duration-150 hover:border-cyan-500 hover:bg-cyan-400"
            onClick={checkIfLegal}
          >
            Check if legal
          </button>
        </div>
      </div>
      {rawTxData && <TransactionGraph rawTx={rawTxData} />}
    </div>
  );
}
