'use client'
import '@/app/ui/global.css'
import '@/app/ui/googleicons.css'
import Navbar from './ui/Navbar'
import Hero from './ui/Hero'
import About from './ui/About'
import Experience from './ui/Experience'
import Projects from './ui/Projects'
import Login from './ui/Login'
import Footer from './ui/components/Footer'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

export default function Home() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <>
          <Navbar/>
          <Hero/>
          <About/>
          <Experience/>
          <Projects/>
          <Footer/>
        </>
        }>
        </Route>
        <Route path='/login' element={<Login/>}/>
      </Routes>
    </Router> 
  )
}
