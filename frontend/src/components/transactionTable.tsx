import { useState } from "react";
import { getRequest } from "~/api/network";

interface transactionResponse {
  txHash: string;
  isLegal: boolean;
}

const walletTransactionsRequest = (hash: string) =>
  getRequest({
    path: `wallet/?walletAddr=${hash}`,
  });

export default function TransactionTable() {
  const [transactions, setTransactions] = useState<transactionResponse[]>();
  const [walletAddr, setWalletAddr] = useState<string>("");

  const fetchData = async () => {
    await walletTransactionsRequest(walletAddr).then(
      (data: transactionResponse[]) => {
        setTransactions(data);
        console.log(data);
      },
    );
  };

  const checkIfWalletTxsLegal = () => {
    fetchData().catch(console.error);
  };

  return (
    <div className="font-mono text-white">
      <div className="flex-center flex justify-center pt-6 text-lg">
        <div className="w-4 flex-auto p-4 text-right">Input wallet address</div>
        <input
          className="block w-4 flex-auto rounded-lg border p-2.5 font-sans text-lg placeholder-cyan-700 focus:border-cyan-500 focus:ring-cyan-500 dark:border-cyan-500 dark:bg-gray-700 dark:text-cyan-400 dark:placeholder-cyan-500"
          type="text"
          value={walletAddr}
          onChange={(e) => setWalletAddr(e.target.value)}
        />

        <div className="w-4 flex-auto p-1">
          <button
            className=" rounded border-b-4 border-cyan-700 bg-cyan-500 px-4 py-2 text-left text-lg font-bold duration-150 hover:border-cyan-500 hover:bg-cyan-400"
            onClick={checkIfWalletTxsLegal}
          >
            Check wallet transactions
          </button>
        </div>
      </div>

      {transactions && (
        <div className=" grid justify-items-center pt-4">
          <div className="relative overflow-x-auto shadow-md sm:rounded-xl">
            <table className=" text-left text-lg rtl:text-right">
              <thead className="bg-gray-50 text-lg dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3">Transaction Hash</th>
                  <th className="px-6 py-3">Legality</th>
                </tr>
              </thead>
              {transactions.map((tx) => (
                <tr
                  className="border-b bg-white hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-600"
                  key={tx.txHash}
                  //   ref="https://www.blockchain.com/explorer/transactions/btc/0b0b6b1319403cc759f9e63d8dcbf095bb1e31303d2c5ecc38d180754414b6c9"
                >
                  <td className="px-6 py-4">{tx.txHash}</td>
                  <td className="px-6 py-4">
                    {tx.isLegal ? "Legal" : "Illegal"}
                  </td>
                </tr>
              ))}
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
