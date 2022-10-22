import Head from 'next/head'
import Image from 'next/image'
import REPL from '../components/repl'
import styles from '../styles/Home.module.css'
import MathJax from 'mathjax-full'

export default function Home() {

  MathJax.tex2svg('\\frac{1}{x^2-1}', {display: true})

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
