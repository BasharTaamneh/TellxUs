import React, { useState } from 'react'
import { useRouter } from 'next/router'
import Image from 'next/image'

export default function Signin() {
  const [passwordvisibility, setpasswordvisibility] = useState('password')
  const [Typing, setTyping] = useState(false)
  const [Typing1, setTyping1] = useState(false)

  function passwordvisibleshow() {
    if (passwordvisibility == 'password') {
      setpasswordvisibility('text')
    } else if (passwordvisibility == 'text') {
      setpasswordvisibility('password')
    }
  }

  const router = useRouter()
  return (
    <div
      id="signin"
      className="flex h-screen w-11/12 items-center justify-center "
    >
      <form
        className="mb-4 mt-2 w-full min-w-fit max-w-5xl space-y-6 rounded-2xl bg-gray-600 bg-opacity-50  p-6 shadow-2xl"
        onSubmit={(e) => e.preventDefault()}
      >
        <div className="flex items-center justify-between">
          <span className="flex h-8 w-8  items-center justify-center rounded border-2 border-green-500 ">
            <span className="flex h-6 w-6 animate-spin items-center justify-center rounded border border-green-500 ">
              <span className="flex h-8 w-8 animate-ping rounded border border-green-500  ">
                <span className="flex h-8 w-8 animate-pulse rounded border border-green-500  "></span>
              </span>
            </span>
          </span>
          <h1
            className="w-auto  text-3xl font-bold text-green-700 hover:animate-pulse hover:underline sm:text-4xl md:text-5xl  lg:text-6xl xl:text-7xl"
            onClick={() => router.push('/')}
          >
            TellxUs
          </h1>
          <span className="flex h-8 w-8  items-center justify-center rounded border-2 border-green-500 ">
            <span className="flex h-6 w-6 animate-spin items-center justify-center rounded border border-green-500 ">
              <span className="flex h-8 w-8 animate-ping rounded border border-green-500  ">
                <span className="flex h-8 w-8 animate-pulse rounded border border-green-500  "></span>
              </span>
            </span>
          </span>
        </div>
        <div className="inline-flex w-full flex-row justify-between rounded border border-gray-200 bg-gray-50">
          {Typing ? (
            <Image
              src="/icons8-dots-loading.gif"
              alt="app logo"
              width={30}
              height={10}
            />
          ) : (
            <></>
          )}
          <input
            onChange={(e) =>
              e.target.value ? setTyping(true) : setTyping(false)
            }
            className="w-11/12 rounded  bg-gray-50 p-4 text-lg text-gray-600 focus:outline-none"
            type="text"
            placeholder="Username"
            name="username"
            required
          />
        </div>
        <div className="inline-flex w-full flex-row justify-between rounded border border-gray-200 bg-gray-50">
          {Typing1 ? (
            <Image
              src="/icons8-dots-loading.gif"
              alt="app logo"
              width={30}
              height={10}
            />
          ) : (
            <></>
          )}
          <input
            onChange={(e) =>
              e.target.value ? setTyping1(true) : setTyping1(false)
            }
            className="w-10/12 rounded  bg-gray-50 p-4 text-lg text-gray-600 focus:outline-none"
            type={passwordvisibility}
            placeholder="Password"
            name="password"
            required
          ></input>

          <button
            className="items-center  justify-center "
            onClick={() => passwordvisibleshow()}
          >
            {passwordvisibility == 'password' ? (
              <svg
                className="mr-2"
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 0 24 24"
                width="24px"
                fill="#000000"
              >
                <path
                  d="M0 0h24v24H0zm0 0h24v24H0zm0 0h24v24H0zm0 0h24v24H0z"
                  fill="none"
                />
                <path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z" />
              </svg>
            ) : (
              <svg
                className="mr-2 "
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 0 24 24"
                width="24px"
                fill="#000000"
              >
                <path d="M0 0h24v24H0z" fill="none" />
                <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z" />
              </svg>
            )}
          </button>
        </div>
        <div>
          <button className="w-full rounded bg-green-600 py-4 text-lg font-bold text-gray-50 transition duration-200 hover:bg-green-700">
            Sign In
          </button>
        </div>
        <div>
          <a
            className="text-lg font-bold text-green-800 hover:animate-pulse hover:underline"
            onClick={() => router.push('/Resetpassword')}
          >
            Forgot password?
          </a>
        </div>
        <hr />
        <div>
          <button className="w-64  rounded bg-green-600 py-4 font-bold text-gray-50 transition duration-200 hover:bg-green-700 sm:w-96 lg:w-6/12 lg:text-lg ">
            Create an account
          </button>
        </div>
        <div className="flex items-center justify-center"></div>
      </form>
    </div>
  )
}
