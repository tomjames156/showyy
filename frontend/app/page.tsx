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
import { useSearchParams } from 'next/navigation'

interface UserData {
  id: number;
  name: string;
  username: string;
  email: string;
  profile: {  // Add the profile property here
      role: string;
      resume?: string; //  Optional
      profile_pic?: string; // Optional
      location_id: number;
      social_links?: { name: string; url: string }[]; // Optional
  };
  // Add other properties as needed
}

export default function Home() {
  const searchParams = useSearchParams()
  const [userData, setUserData] = useState<UserData | {}>({})
  const username = searchParams.get('username')

  const getProfile = async () => {
    const response = await fetch(`http://127.0.0.1:5000/profile/${username}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    const profile = await response.json()
    console.log(profile.portfolio.role)
    setUserData(profile)
  }

  useEffect(() => {
    getProfile()
  }, [])

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
