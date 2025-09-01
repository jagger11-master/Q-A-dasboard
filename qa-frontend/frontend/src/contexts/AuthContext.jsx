import { createContext, useContext, useEffect, useState } from 'react'
import { api } from '../services/api'


const AuthContext = createContext(null) 

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null) // { id, name, email, role }

  useEffect(() => {
    const token = localStorage.getItem('token')
    const u = localStorage.getItem('user')
    if (token && u) setUser(JSON.parse(u))
  }, [])

  async function login(email, password) {
    try{
    const { data } = await api.post('/auth/login', { email, password })
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
    setUser(data.user)
    return {success:true,user:data.user}
  } catch(err) {
    return { success:false,error:err.response?.data?.message||'login failed'}
  }
}
  async function register(payload) {
    try{
    const { data } = await api.post('/auth/register', payload)
    return {success: true, user: data.user}
    }catch(err){
    return { success: false, error: err.response?.data?.message||'Registration failed'}
  } 
}
  function logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth= () => useContext(AuthContext)
