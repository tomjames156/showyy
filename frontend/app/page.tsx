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
import { useContext } from 'react'
import { ProfileContext } from '@/context/ProfileContext'

export default function Home() {
  const { profile } = useContext(ProfileContext)

  return (profile ?
    <>
      <Navbar/>
      <Hero />
      <About/>
      <Experience/>
      <Services/>
      <Projects/>
      <Testimonials/>
      <Contact/>
      <Footer/>
    </> : <p>No Profile</p>
  )
}
