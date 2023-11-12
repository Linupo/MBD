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
  const [transactions, setTransactions] = useState<any[]>();
  const [walletAddr, setWalletAddr] = useState<string>("");

  const fetchData = async () => {
    await walletTransactionsRequest(walletAddr).then((data: any) => {
      setTransactions(data);
      console.log(data);
    });
  };

  const checkIfWalletTxsLegal = () => {
    fetchData().catch(console.error);
  };

  return (
    <div>
      <label>
        Enter wallet address:
        <input
          type="text"
          value={walletAddr}
          onChange={(e) => setWalletAddr(e.target.value)}
        />
      </label>
      <button onClick={checkIfWalletTxsLegal}>Check if legal</button>

      <table>
        <tr>
          <th>Transaction Hash</th>
          <th>Legality</th>
        </tr>
        {transactions &&
          transactions.map((tx) => (
            <tr key={tx.txHash}>
              <td>{tx.txHash}</td>
              <td>{tx.isLegal ? "Legal" : "Illegal"}</td>
            </tr>
          ))}
      </table>
    </div>
  );
}
