import { useState } from "react";
import { getRequest } from "~/api/network";
import TransactionGraph from "./transactionGraph";
import toast from "react-hot-toast";
interface transactionResponse {
  txHash: string;
  isLegal: boolean;
  rawTx: any;
}

const transactionRequest = (hash: string) =>
  getRequest({
    path: `transaction/?txHash=${hash}`,
  });

interface rawTransaction {
  fee: number;
  block_index: number;
  time: number;
  vin_sz: number;
  vout_sz: number;
}

export default function TransactionLegalityCheck() {
  const [isLegal, setIsLegal] = useState<boolean>();
  const [txHash, setTxHash] = useState<string>("");
  const [txHashInput, setTxHashInput] = useState<string>("");
  const [rawTxData, setRawTxData] = useState<rawTransaction>();

  const fetchData = async () => {
    await transactionRequest(txHashInput).then((data: transactionResponse) => {
      if (data.rawTx.error === "not-found-or-invalid-arg") {
        toast.error(data.rawTx.message);
        return;
      }
      setIsLegal(data.isLegal);
      setRawTxData(data.rawTx);
    });
  };

  const checkIfLegal = () => {
    setRawTxData(undefined);
    fetchData().catch(console.error);
  };
  return (
    <div className="font-mono text-white">
      <div className="flex-center p flex justify-center pt-6 text-lg">
        <div className="w-4 flex-auto p-4 text-right ">
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
          value={txHashInput}
          onChange={(e) => setTxHashInput(e.target.value)}
        />
        <div className="w-4 flex-auto p-1">
          <button
            className=" rounded border-b-4 border-cyan-700 bg-cyan-500 px-4 py-2 text-left font-mono text-lg font-bold duration-150 hover:border-cyan-500 hover:bg-cyan-400"
            onClick={() => {
              setTxHash(txHashInput);
              checkIfLegal();
            }}
          >
            Check if legal
          </button>
        </div>
      </div>

      {rawTxData && (
        <div className=" grid justify-items-center pt-4">
          <div className="relative overflow-x-auto shadow-md sm:rounded-xl">
            <table className=" border-collapse border border-gray-500 text-left text-lg rtl:text-right">
              <thead className="bg-gray-50 text-lg dark:bg-gray-700">
                <tr className="border-b border-gray-500">
                  <th
                    className="border border-gray-500 px-6 py-3 text-center text-2xl font-extrabold"
                    colSpan={6}
                  >
                    Transaction Info
                  </th>
                </tr>
                <tr className="border-b border-gray-500">
                  <th className="border border-gray-500 px-6 py-3">Time</th>
                  <th className="border border-gray-500 px-6 py-3">Inputs</th>
                  <th className="border border-gray-500 px-6 py-3">Outputs</th>
                  {/* <th className="px-6 py-3 border border-gray-500">Amount</th> */}
                  <th className="border border-gray-500 px-6 py-3">Fee</th>
                  <th className="border border-gray-500 px-6 py-3">Block ID</th>
                  <th className="border border-gray-500 px-6 py-3">Legal</th>
                </tr>
                <tr className="border-b bg-white hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-600">
                  <td className="border border-gray-500 px-6 py-4 text-center">
                    {new Date(rawTxData.time * 1000).toLocaleString()}
                  </td>
                  <td className="border border-gray-500 px-6 py-4 text-center">
                    {rawTxData.vin_sz}
                  </td>
                  <td className="border border-gray-500 px-6 py-4 text-center">
                    {rawTxData.vout_sz}
                  </td>
                  {/* <td className="px-6 py-4 text-center border border-gray-500">{rawTxData.Amount}</td> */}
                  <td className="border border-gray-500 px-6 py-4 text-center">
                    {rawTxData.fee}
                  </td>
                  <td className="border border-gray-500 px-6 py-4 text-center">
                    {rawTxData.block_index}
                  </td>
                  <td
                    className={`border border-gray-500 px-6 py-4 text-center ${
                      isLegal ? "text-green-500" : "text-red-500"
                    }`}
                  >
                    {isLegal ? "True" : "False"}
                  </td>
                </tr>
              </thead>
            </table>
          </div>
        </div>
      )}

      {rawTxData && (
        <div className="flex flex-col items-center justify-center pt-9">
          <div className="mb-4 text-2xl font-bold">
            Model decision explanation
          </div>
          <img className="rounded-lg" src={`/${txHash}.png`} />
        </div>
      )}

      {/* {rawTxData && <TransactionGraph rawTx={rawTxData} />} */}
    </div>
  );
}
