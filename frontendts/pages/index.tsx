import Head from "next/head";
import styles from "../styles/Home.module.css";
import "../node_modules/katex/dist/katex.css";
import { NextPage } from "next";
import Cells from "../components/Cells";

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>M L I M</title>
        <meta name="description" content="M L I M" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <Cells />
      </main>
    </div>
  );
};

export default Home;
