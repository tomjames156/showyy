import '@/app/ui/global.css'
import '@/app/ui/googleicons.css'
import Navbar from './ui/Navbar'
import Hero from './ui/Hero'
import About from './ui/About'
import Experience from './ui/Experience'
import Projects from './ui/Projects'
import Footer from './ui/components/Footer'

export default function Home() {
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
