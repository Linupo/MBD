import { useState } from "react";
import { getRequest } from "~/api/network";

interface transactionResponse {
  txHash: string;
  isLegal: boolean;
}

const transactionRequest = (hash: string) =>
  getRequest({
    path: `transaction/?txHash=${hash}`,
  });

export default function TransactionLegalityCheck() {
  const [isLegal, setIsLegal] = useState<boolean>();
  const [txHash, setTxHash] = useState<string>("");

  const fetchData = async () => {
    await transactionRequest(txHash).then((data: transactionResponse) => {
      // console.log(data.isLegal);
      setIsLegal(data.isLegal);
      console.log(data);
    });
  };

  const checkIfLegal = () => {
    fetchData().catch(console.error);
  };
  return (
    <div className="flex-center p flex justify-center pt-6 text-lg text-white">
      <div className="w-4 flex-auto p-4 text-right font-mono">
        Enter transaction hash:
      </div>
      <input
        className="block w-4 flex-auto rounded-lg border p-2.5 font-mono font-sans text-lg text-cyan-900 placeholder-cyan-700 focus:border-cyan-500 focus:ring-cyan-500 dark:border-cyan-500 dark:bg-gray-700 dark:text-cyan-400 dark:placeholder-cyan-500"
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
  );
}
