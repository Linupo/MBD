import Head from "next/head";
import Link from "next/link";
import { useEffect, useState } from "react";
import axios from "axios";
import { getRequest } from "~/api/network";
import TransactionTable from "~/components/transactionTable";

interface transactionResponse {
  txHash: string;
  isLegal: boolean;
}

const transactionRequest = (hash: string) =>
  getRequest({
    path: `transaction/?txHash=${hash}`,
  });

export default function Home() {
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
    <>
      <div>
        <label>
          Enter transaction hash:
          <input
            style={
              isLegal == false
                ? { color: "red" }
                : isLegal == true
                ? { color: "green" }
                : { color: "black" }
            }
            type="text"
            value={txHash}
            onChange={(e) => setTxHash(e.target.value)}
          />
        </label>
        <button onClick={checkIfLegal}>Check if legal</button>
        <TransactionTable />
      </div>
    </>
  );
}
