// import React from 'react'
import Head from 'next/head'
import Footer from '../components/Footer'
import Header from '../components/Header'
import Paswordreset from '../components/Paswordreset'
export default function Resetpassword() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100">
      <Head>
        <title>TellxUs Reset Password</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      {/* <Header /> */}
      <main className="flex w-full flex-1 flex-col items-center justify-center  px-2 text-center ">
        <Paswordreset />
      </main>

      <Footer />
    </div>
  )
}
