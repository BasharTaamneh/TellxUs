import { createContext, useContext, useState } from 'react'
import jwt from 'jsonwebtoken'
import axios from 'axios'
const baseUrl = ''
const tokenUrl = baseUrl + '/api/token/'
import { useEffect } from 'react'

const AuthContext = createContext()

export function useAuth() {
  const auth = useContext(AuthContext)
  if (!auth) throw new Error('You forgot AuthProvider!')
  return auth
}

export function AuthProvider(props) {
  const [state, setState] = useState({
    tokens: null,
    user: null,
    login: login,
  })

  async function login(username, password) {
    const response = await axios.post(tokenUrl, { username, password })

    const decodedAccess = jwt.decode(response.data.access)

    const newState = {
      tokens: response.data,
      user: {
        id: decodedAccess.user_id,
      },
    }

    localStorage.setItem('token', JSON.stringify(newState))
    setState((prevState) => ({ ...prevState, ...newState }))
  }

  useEffect(() => {
    const data = localStorage.getItem('token')
    if (data) {
      setState(JSON.parse(data))
    }
  }, [])

  return (
    <AuthContext.Provider value={state}>{props.children}</AuthContext.Provider>
  )
}
