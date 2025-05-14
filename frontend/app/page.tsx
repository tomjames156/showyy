'use client'
import '@/app/ui/global.css'
import '@/app/ui/googleicons.css'
import Navbar from './ui/Navbar'
import Hero from './ui/Hero'
import About from './ui/About'
import Experience from './ui/Experience'
import Services from './ui/Services'
import Projects from './ui/Projects'
import Testimonials from './ui/Testimonials'
import Contact from './ui/Contact'
import Footer from './ui/components/Footer'
import { useState, useEffect } from 'react'

export default function Home() {

  const [userData, setUserData] = useState({})

  const getProfile = async () => {
    const response = await fetch("http://127.0.0.1:5000/user/1/", {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    const profile = await response.json()
    console.log(profile)
    return profile
  }

  return (
    <>
      <Navbar/>
      <Hero/>
      <About/>
      <Experience/>
      <Services/>
      <Projects/>
      <Testimonials/>
      <Contact/>
      <Footer/>
    </>
  )
}
