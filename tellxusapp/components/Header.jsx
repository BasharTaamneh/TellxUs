import Image from 'next/image'
export default function Header() {
  return (
    <header className="relative h-20 w-full items-center justify-center border-b bg-gray-700">
      <Image className="absolute "
        src="/Logo.png"
        alt="app logo"
        width={65}
        height={75}
      />
    </header>
  )
}
