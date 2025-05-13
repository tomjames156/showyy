'use client'
import '@/app/ui/global.css'
import '@/app/ui/googleicons.css'
import Navbar from './ui/Navbar'
import Hero from './ui/Hero'
import About from './ui/About'
import Experience from './ui/Experience'
import Projects from './ui/Projects'
import Footer from './ui/components/Footer'
import { useState, useEffect } from 'react'

export default function Home() {

  const [userData, setUserData] = useState({})

  return (
    <>
      <Navbar/>
      <Hero/>
      <About/>
      <Experience/>
      <Projects/>
      <Footer/>
    </>
  )
}
