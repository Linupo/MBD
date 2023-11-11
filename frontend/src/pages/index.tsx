import Head from "next/head";
import Link from "next/link";
import { useEffect, useState } from "react";
import axios from "axios";
import { getRequest } from "~/api/network";

export const transactionRequest = () =>
  getRequest({
    path: "transaction/?txHash=48cc5af8141a7be7b396029e5093a9f0fe78ea03076ebd4bc805bd977e93fbcc",
  });

export default function Home() {
  const [isLegal, setIsLegal] = useState<boolean>(false);

  const fetchData = async () => {
    await transactionRequest().then((data: any) => console.log(data));
  };

  useEffect(() => {
    fetchData()
      // make sure to catch any error
      .catch(console.error);
  }, []);

  return <></>;
}
