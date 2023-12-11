import Link from "next/link";
import { useState } from "react";
import { getRequest } from "~/api/network";
import * as luxon from "luxon";
import toast from "react-hot-toast";

function timestampToDateWithTime(timestamp: number): string {
  const date = luxon.DateTime.fromMillis(timestamp, { zone: "Europe/Vilnius" });
  return date.toLocaleString(luxon.DateTime.DATETIME_FULL_WITH_SECONDS);
}

function calculateValue(inputs: any): number {
  let value = 0;
  inputs.map((input: any) => {
    console.log(input);
    if (input.prev_out.value) {
      value = value + input.prev_out.value;
    }
  });
  // satoshis to bitcoin conversion
  return value / 100000000;
}
interface transactionResponse {
  isLegal: boolean;
  rawTx: any;
}

const walletTransactionsRequest = (hash: string) =>
  getRequest({
    path: `wallet/?walletAddr=${hash}`,
  });

export default function TransactionTable() {
  const [transactions, setTransactions] = useState<transactionResponse[]>();
  const [walletAddr, setWalletAddr] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const fetchData = async () => {
    setIsLoading(true);
    await walletTransactionsRequest(walletAddr).then(
      (data: transactionResponse[]) => {
        setTransactions(data);
        setIsLoading(false);
        toast.success("Success");
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
            disabled={isLoading}
          >
            <svg
              aria-hidden="true"
              role="status"
              className={
                isLoading
                  ? "me-3 inline h-4 w-4 animate-spin text-gray-200 dark:text-gray-600"
                  : "hidden"
              }
              viewBox="0 0 100 101"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                fill="currentColor"
              />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                fill="#1C64F2"
              />
            </svg>
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
                  <th className="px-6 py-3">Index</th>
                  <th className="px-6 py-3">Hash</th>
                  <th className="px-6 py-3">Time</th>
                  <th className="px-6 py-3">Value</th>
                  <th className="px-6 py-3">Legality</th>
                </tr>
              </thead>
              {transactions.map((tx, index) => (
                <tr
                  className="border-b bg-white hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-600"
                  key={tx.rawTx.hash}
                >
                  <td className="px-6 py-4">{index + 1}</td>
                  <Link
                    href={`https://www.blockchain.com/explorer/transactions/btc/${tx.rawTx.hash}`}
                  >
                    <td className="px-6 py-4">{tx.rawTx.hash}</td>
                  </Link>
                  <td className="px-6 py-4">
                    {timestampToDateWithTime(tx.rawTx.time * 1000)}
                  </td>
                  <td className="px-6 py-4 text-right">
                    {calculateValue(tx.rawTx.inputs)} BTC
                  </td>

                  <td
                    className={
                      tx.isLegal
                        ? "px-6 py-4 text-green-300"
                        : "px-6 py-4 text-red-300"
                    }
                  >
                    <div>{tx.isLegal ? "Legal" : "Illegal"}</div>
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
