import Head from 'next/head'
import styles from '../styles/Home.module.css'

const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {CHTML} = require('mathjax-full/js/output/chtml.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const {AssistiveMmlHandler} = require('mathjax-full/js/a11y/assistive-mml.js');

const {AllPackages} = require('mathjax-full/js/input/tex/AllPackages.js');

export default function Home() {

  const adaptor = liteAdaptor();
  const handler = RegisterHTMLHandler(adaptor);

  const tex = new TeX();
  const chtml = new CHTML();
  const html = mathjax.document('\[ \int_{a}^{b} x^2 \,dx \]', {InputJax: tex, OutputJax: chtml});

  //console.log(adaptor.textContent(chtml.styleSheet(html)))
  console.log(chtml)
  //console.log(html.document.body)

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
