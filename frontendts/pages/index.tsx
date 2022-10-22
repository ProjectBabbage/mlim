import Head from "next/head";
import styles from "../styles/Home.module.css";
import REPL from "../components/repl";
import { useState } from "react";
import "../node_modules/katex/dist/katex.css";
import Workspace from "../components/Workspace";
import { NextPage } from "next";

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>M L I M</title>
        <meta name="description" content="M L I M M L I M M L I M" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <Workspace />
        <div className="text-orange-500">Put a REPL here ⬇</div>
        <REPL />
      </main>
    </div>
  );
};

export default Home;
