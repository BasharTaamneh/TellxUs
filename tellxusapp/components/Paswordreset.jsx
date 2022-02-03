export default function Paswordreset() {
  return (
    <div class="w-full flex h-screen items-center justify-center bg-gray-100">
      <form class="flex flex-col shadow-xl w-4/12">
        <div class="space-y-8 rounded-tl-2xl rounded-tr-2xl bg-gradient-to-tr from-pink-500 to-pink-300 py-6 px-14 text-center">
          <h2 class="text-xs uppercase text-white">
            don't miss out the latest
          </h2>
          <h4 class="text-center text-xl font-bold text-white">
            Weekly FREE UI resources
            <br />
            straight to your inbox
          </h4>
        </div>
        <div class="flex flex-col space-y-5 bg-white py-6 px-8">
          <input
            type="text"
            placeholder="Enter your email address"
            class="rounded-md border-2 border-gray-200 px-2 py-2 focus:border-transparent focus:outline-none focus:ring-1 focus:ring-pink-300"
          />
          <button class="w-full rounded-md bg-pink-400 py-3 text-sm text-white shadow-lg focus:border-transparent focus:outline-none focus:ring-2 focus:ring-pink-500">
            Stay Inspired
          </button>
          <span class="text-center text-sm text-gray-400">
            or subscribe using
          </span>
          
        </div>
      </form>
    </div>
  )
}
