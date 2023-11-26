import Link from "next/link";
import { useState } from "react";
import { getRequest } from "~/api/network";
import * as luxon from "luxon";
import toast from "react-hot-toast";

function timestampToDateWithTime(timestamp: number): string {
  const date = luxon.DateTime.fromMillis(timestamp, { zone: "Europe/Vilnius" });
  const options = {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  };
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

  const fetchData = async () => {
    await walletTransactionsRequest(walletAddr).then(
      (data: transactionResponse[]) => {
        setTransactions(data);
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
