import TransactionLegalityCheck from "~/components/transactionLegalityCheck";
import TransactionTable from "~/components/transactionTable";

export default function Home() {
  return (
    <>
      <main className="flex min-h-screen flex-col bg-gradient-to-b from-[#020024] to-[#096a79]">
        <TransactionLegalityCheck />
        <TransactionTable />
      </main>
    </>
  );
}
