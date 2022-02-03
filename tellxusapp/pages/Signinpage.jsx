import React from 'react'
import Head from 'next/head'
import Footer from '../components/Footer'
import Signin from '../components/Signin'
import BGImage from '../components/BGImage'
export default function Signinpage() {
  return (
    <>
      <div
        className=" flex min-h-screen flex-col items-center justify-center bg-opacity-50 bg-cover bg-no-repeat"
        style={{
          'background-image': " url('/undraw_Login_re_4vu2.png')",
          'background-size': `${BGImage()?.width}px  ${BGImage()?.height}px` ,

        }}
      >
        <Head>
          <title>TellxUs Sign In</title>
          <link rel="icon" href="/favicon.ico" />
        </Head>

        <main className="flex w-full flex-1 flex-col items-center justify-center  px-2 text-center ">
          <Signin />
        </main>
      </div>
      <Footer />
    </>
  )
}
