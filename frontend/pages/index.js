import Head from 'next/head'
import styles from '../styles/Home.module.css'

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>M L I M</title>
        <meta name="description" content="M L I M M L I M M L I M" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <div className="text-orange-500">
          Put a REPL here ⬇
        </div>
        <REPL/>
      </main>
    </div>
  )
}
