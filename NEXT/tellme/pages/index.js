import Head from 'next/head'
import axios from 'axios'
import { useState, useEffect } from 'react'


export default function Home() {

  const [Title, setTitle] = useState()
  const [Description, setDescription] = useState()
  const [Owner, setOwner] = useState()
  const [Files, setFiles] = useState()
  useEffect(()=> {
    setOwner('bashar')
  },[])
  
  async function newarticles(evt) {
    evt.preventDefault()
    
    console.log(Files);
    
    const upload = new FormData();
    upload.append('title', Title);
    upload.append('description', Description);
    upload.append('owner', Owner);
    
    if (Files) { 
      upload.append('files', Files, Files.name);
    }
    else{
      upload.append('files', Files )
    }
    
    await axios.post("http://127.0.0.1:8000/AddArticlse/", upload)
    .then(response => {console.log(response);})
    .catch(error => {console.log(error);})
    
  }


  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <Head>
        <title>Create Next App</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="flex flex-col items-center justify-center flex-1 w-full px-20 text-center">


        {/* <iframe className="flex h-96 w-12/12"
          src="/BASHAR.pdf"
          frameBorder="0"
          scrolling="auto"
          height="100%"
          width="100%"
        ></iframe> */}

        
        <form className="" onSubmit={(evt) => newarticles(evt)}>
        <input required type="text" name="title" placeholder="title" value={Title} onChange={(evt) => setTitle(evt.target.value)} />
          <textarea required type="text" name="description" placeholder="description" value={Description} onChange={(evt) => setDescription(evt.target.value)}  />
          <input type="file" name="files" multiple accept="image/*" onChange={(evt) => setFiles(evt.target.files)} />
        <button type="submit" >chex</button>
        </form>


      </main>

      <footer className="flex items-center justify-center w-full h-24 border-t">
        <a
          className="flex items-center justify-center"
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          <img src="/vercel.svg" alt="Vercel Logo" className="h-4 ml-2" />
        </a>
      </footer>
    </div>
  )
}
