import Image from 'next/image'
export default function Header() {
  return (
    <header className="sticky top-0 h-20 w-full items-center justify-center rounded bg-white bg-opacity-20 shadow-xl">
      <div className="absolute left-6 top-2.5">
        <Image
          className=" animate-pulse "
          src="/TellxUslogo.png"
          alt="app logo"
          width={60}
          height={60}
        />
      </div>
    </header>
  )
}
