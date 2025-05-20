import Link from "next/link";
import { useState } from "react";
import { getRequest } from "~/api/network";
import * as luxon from "luxon";
import toast from "react-hot-toast";

function timestampToDateWithTime(timestamp: number): string {
  const date = luxon.DateTime.fromMillis(timestamp, { zone: "Europe/Vilnius" });
  return date.toLocaleString(luxon.DateTime.DATETIME_FULL_WITH_SECONDS);
}

function determineIsTxOutgoing(tx: any, walletAddr: string): boolean {
  return tx.inputs.some(function (input: any) {
    return input.prev_out.addr == walletAddr;
  });
}

function calculateValue(inputs: any, outputs: any, walletAddr: string): number {
  let value = 0;
  outputs.map((out: any) => {
    if (out.value && out.addr == walletAddr) {
      value = out.value;
    }
  });
  inputs.map((input: any) => {
    if (input.prev_out.value && input.prev_out.addr == walletAddr) {
      value = input.prev_out.value;
    }
  });
  // satoshis to bitcoin conversion
  return value / 100000000;
}
interface transactionResponse {
  isLegal: boolean;
  rawTx: any;
}

interface walletResponse {
  n_tx: number;
  total_received: number;
  total_sent: number;
  final_balance: number;
  transactions: transactionResponse[];
}

interface walletInfo {
  n_tx: number;
  total_received: number;
  total_sent: number;
  final_balance: number;
}

const walletTransactionsRequest = (hash: string) =>
  getRequest({
    path: `wallet/?walletAddr=${hash}`,
  });

export default function TransactionTable() {
  const [transactions, setTransactions] = useState<transactionResponse[]>();
  const [walletAddrFieldValue, setWalletAddrFieldValue] = useState<string>("");
  const [walletAddr, setWalletAddr] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [walletInfo, setWalletInfo] = useState<walletInfo>();

  const fetchData = async () => {
    setIsLoading(true);
    await walletTransactionsRequest(walletAddrFieldValue).then((data: walletResponse) => {
      console.log(data);
      if (data.transactions === undefined) {
        toast.error("Wallet does not exist");
        setIsLoading(false);
        return;
      }
      if (data.n_tx === 0) {
        toast.success("Wallet exists but has no transactions yet");
        setIsLoading(false);
        return;
      }
      setWalletInfo({
        n_tx: data.n_tx,
        total_received: data.total_received,
        total_sent: data.total_sent,
        final_balance: data.final_balance,
      });
      setTransactions(data.transactions);
      setIsLoading(false);
      toast.success("Success");
    });
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
          value={walletAddrFieldValue}
          onChange={(e) => setWalletAddrFieldValue(e.target.value)}
        />

        <div className="w-4 flex-auto p-1">
          <button
            className=" rounded border-b-4 border-cyan-700 bg-cyan-500 px-4 py-2 text-left text-lg font-bold duration-150 hover:border-cyan-500 hover:bg-cyan-400"
            onClick={() => {
              setWalletAddr(walletAddrFieldValue);
              checkIfWalletTxsLegal();
            }}
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

      {walletInfo && (
        <div className=" grid justify-items-center pt-4">
          <div className="relative overflow-x-auto shadow-md sm:rounded-xl">
            <table className=" text-left text-lg rtl:text-right">
              <thead className="bg-gray-50 text-lg dark:bg-gray-700">
                <tr>
                  <th
                    className="px-6 py-3 text-center text-2xl font-extrabold"
                    colSpan={4}
                  >
                    Wallet Info
                  </th>
                </tr>
                <tr>
                  <th className="px-6 py-3">Number of transactions</th>
                  <th className="px-6 py-3">Total received</th>
                  <th className="px-6 py-3">Total sent</th>
                  <th className="px-6 py-3">Final balance</th>
                </tr>
                <tr className="border-b bg-white hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-600">
                  <td className="px-6 py-4 text-center">{walletInfo.n_tx}</td>
                  <td className="px-6 py-4 text-center">
                    {walletInfo.total_received / 100000000} BTC
                  </td>
                  <td className="px-6 py-4 text-center">
                    {walletInfo.total_sent / 100000000} BTC
                  </td>
                  <td className="px-6 py-4 text-center">
                    {walletInfo.final_balance / 100000000} BTC
                  </td>
                </tr>
              </thead>
            </table>
          </div>
        </div>
      )}

      {transactions && (
        <div className=" grid justify-items-center pt-4">
          <div className="relative overflow-x-auto shadow-md sm:rounded-xl">
            <table className=" text-left text-lg rtl:text-right">
              <thead className="bg-gray-50 text-lg dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3">Index</th>
                  <th className="px-6 py-3">In/Out</th>
                  <th className="px-6 py-3">Value</th>
                  <th className="px-6 py-3">Hash</th>
                  <th className="px-6 py-3">Time</th>
                  <th className="px-6 py-3">Legality</th>
                </tr>
              </thead>
              {transactions.map((tx, index) => (
                <tr
                  className="border-b bg-white hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-600"
                  key={tx.rawTx.hash}
                >
                  <td className="px-6 py-4">{index + 1}</td>
                  <td className="px-6 py-4">
                    {determineIsTxOutgoing(tx.rawTx, walletAddr) ? (
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="1.5"
                        stroke="currentColor"
                        className="h-6 w-6 text-green-500"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M9 8.25H7.5a2.25 2.25 0 00-2.25 2.25v9a2.25 2.25 0 002.25 2.25h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25H15M9 12l3 3m0 0l3-3m-3 3V2.25"
                        />
                      </svg>
                    ) : (
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="1.5"
                        stroke="currentColor"
                        className="h-6 w-6 text-red-500"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M9 8.25H7.5a2.25 2.25 0 00-2.25 2.25v9a2.25 2.25 0 002.25 2.25h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25H15m0-3l-3-3m0 0l-3 3m3-3V15"
                        />
                      </svg>
                    )}
                  </td>
                  <td className="px-6 py-4 text-right">
                    {calculateValue(tx.rawTx.inputs, tx.rawTx.out, walletAddr)}{" "}
                    BTC
                  </td>

                  <Link
                    href={`https://www.blockchain.com/explorer/transactions/btc/${tx.rawTx.hash}`}
                  >
                    <td className="px-6 py-4">{tx.rawTx.hash}</td>
                  </Link>
                  <td className="px-6 py-4">
                    {timestampToDateWithTime(tx.rawTx.time * 1000)}
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
