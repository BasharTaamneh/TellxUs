import Head from 'next/head'
import Footer from "../components/Footer"
import Header from "../components/Header"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center ">
      <Head>
        <title>TellxUs</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Header/>
      <main className="flex w-full flex-1 flex-col items-center justify-center px-2 text-center bg-yellow-200 ">
        <h1 className=" text-2xl font-black opacity-50">hii</h1>

      </main>

      <Footer/>
    </div>
  )
}
