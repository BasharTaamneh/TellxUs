import Head from 'next/head'
import Footer from "../components/Footer"
import Header from "../components/Header"
import Signin from "../components/Signin"

import { useRouter } from 'next/router'
export default function Home() {
  const router = useRouter()

  
  return (
    <>
      <div className="flex  min-h-screen flex-col items-center justify-center bg-red-500">
        <Head>
          <title>TellxUs</title>
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <Header />
        <main className="flex w-full flex-1 flex-col items-center justify-center px-2 text-center ">

          <button type="button" onClick={() => router.push('Signinpage')}>gggg</button>
          {/* <Signin/> */}
        </main>
      </div>
      <Footer />
    </>
  )
}
