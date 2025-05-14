'use client'

import { useState} from "react"

function Login() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const updateUsername = (e: any) => {
    setUsername(e.target.value)
  }

  const updatePassword = (e: any) => {
    setPassword(e.target.value)
  }

  const handleSubmit = async (e: any) => {
    e.preventDefault()

    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await fetch('http://127.0.0.1:5000/auth/login/', {
        method: 'POST',
        body: formData,
    });

    const responseData = await response.json();
    console.log(responseData)
  }

  return (
    <form onSubmit={handleSubmit}>
        <input type="text" id="username" name="username" placeholder="username" onChange={updateUsername} value={username}/><br/>
        <input type="password" id="password" name="password" placeholder="Enter Password" onChange={updatePassword} value={password}/><br/>
        <input type="submit" value="Login"/>
    </form>
)}

export default Login