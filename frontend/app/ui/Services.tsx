import { libre_franklin } from "./fonts"
import { services } from "../lib/placeholder-data"
import { motion } from "framer-motion"
import { useContext } from "react"
import { ProfileContext } from "@/context/ProfileContext"
import Image from "next/image"

export default function Services() {
  const {profile} = useContext(ProfileContext)

  const container = {
    initial: { opacity: 1, scale: 0},
    whileInView: {
        opacity: 1,
        scale: 1,
        transition: {
            delayChildren: 0.1,
            staggerChildren: 0.2,
        }
    }
  }

  const item  = {
      initial: { y: 20, opacity: 0 },
      whileInView: {
          y: 0,
          opacity: 1
      }
  }

  return (
    <section id="about" className="mx-5 sm:mx-10 lg:mx-20 xl:mx-40 mt-10 xl:mt-40 dark:text-white">
      <h1 className="font-semibold text-[1.4rem] xs:text-2xl">Services</h1>
      {profile.intro_text && <p className={`mt-2 leading-[1.4rem] text-[1rem] ${libre_franklin.className} antialiased xs:text-[1.1rem] sm:mt-4`}>{profile.intro_text}</p>}
      <motion.ul 
        className='grid grid-cols-1 gap-x-20 gap-y-6 mt-8 xs:grid-cols-2 sm:grid-cols-2 sm:justify-between lg:grid-cols-3  dark:text-white'
        variants={container}
        initial='initial'
        whileInView="whileInView"
        viewport={{amount: 0.1, once: true}}>
      {profile.services_section.services ? profile.services_section.services.map((service, index) => {
          return (
          <motion.li 
              key={index} 
              className='border-[1px] border-solid border-black rounded-xl py-5 px-4 flex flex-col cursor-default hover:-mt-2 hover:border-blue-900 hover:border-[3px] transition transition-all duration-200 dark:border-white items-center' 
              variants={item}
              transition={{
                  type: "spring",
                  stiffness: 100,
                  damping: 15
              }}
              >
              <div>
                <Image
                  src={service.image ? service.image : '/cloud.png'}
                  alt="Cloud Icon"
                  width={50}
                  height={50}
                />
              </div>
              <p className='font-bold text-lg mt-6'>{service.name}</p>
              <p className={`${libre_franklin.className} text-center antialiased text-[1rem] leading-[1.3rem] mt-6 mb-12 xs:text-[1rem]`}>{service.description}</p>
          </motion.li>)
      }) : <h2>No Services</h2>}
      </motion.ul>
    </section>
  )
}
