'use client'

import { workExperiences } from '@/app/lib/placeholder-data'
import { libre_franklin } from './fonts'
import { motion } from 'framer-motion'
import { useState, useContext } from 'react'
import { ProfileContext } from '@/context/ProfileContext'

const container = {
    initial: { 
        opacity: 1, 
        scale: 0,
    },
    whileInView: {
        opacity: 1,
        scale: 1,
        transition: {
            delayChildren: 0.1,
            staggerChildren: 0.1,
        }
    }
}

const item  = {
    initial: { opacity: 0, x: 20},
    whileInView: {
        opacity: 1,
        x: 0 
    }
}

export default function Experience(){
    const [ activeIndex, setActiveIndex ] = useState(0)
    const context = useContext(ProfileContext)

    if (!context) {
        return <div>Profile data is not available.  Make sure you are within a ProfileProvider.</div>;
    }

    const { profile } = context

    return(
        <section className="mt-20 mx-5 sm:mx-10 mx-40 sm:mx-10 lg:mx-20 xl:mx-40 dark:text-white" id='experience'>
            <h1 className="font-semibold text-[1.4rem] xs:text-2xl">Experience</h1>
            {profile?.experiences ? <div className='mt-4 flex justify-between flex-col lg:flex-row'>
                <ul className='w-full flex flex-wrap gap-4 justify-between mb-4 lg:w-[20%] lg:flex-col'>
                    {profile.experiences && profile?.experiences.map((exp, index) => (
                        index !==  activeIndex?
                        <li key={index} className='flex justify-between pr-10'>    
                            <p className='uppercase text-[0.9rem] font-bold text-gray-400 cursor-pointer hover:text-gray-500 
                            tansition transition-all duration-200 xs:text-[1rem] dark:hover:text-gray-200' onClick={() => {setActiveIndex(index)}}>{exp.organization}</p>
                        </li> :
                        <li key={index} className='flex justify-between pr-10'>
                            <p className='uppercase text-[0.9rem] font-bold text-blue-900 border-b-[4px] border-[#0038BC] lg:border-none xs:text-[1rem] dark:text-blue-400 dark:border-blue-400'>{exp.organization}</p>
                            <div className='w-[4px] h-full bg-[#0038BC] hidden lg:block'></div>
                        </li>
                    ))}
                </ul>
                <div className='w-full h-[100%] lg:w-[80%]'>
                    <h1 className='font-bold text-[1rem] xs:text-[1.2rem]'>{profile.experiences[activeIndex]?.role} @ <span className='text-blue-900 dark:text-blue-400'>{profile.experiences[activeIndex].organization}</span></h1>
                    <h2 className='uppercase mt-2 mb-8 text-[0.85rem] text-gray-400 xs:text-[0.9rem]'>{workExperiences[activeIndex].duration}</h2>
                        {profile.experiences[activeIndex].bullet_points.map((bullet, index) => (
                            <motion.ul
                                key='none' 
                                className='flex flex-col pb-4' 
                                initial="initial"
                                whileInView="whileInView"
                                variants={container}
                                viewport={{once: true}}
                            >
                                <motion.li key={`bullet-${index}`} className='flex items-start gap-4' variants={item} layout
                                >
                                    <div>
                                        <div className='w-[0.5rem] bg-blue-900 h-[0.5rem] rounded-xl dark:bg-blue-400'>
                                        </div>
                                    </div>
                                    <div className={`text-[1rem] ${libre_franklin.className} antialiased -mt-2 text-justify xs:text-[1.1rem]`}>{bullet.bullet_point}</div>
                                </motion.li>
                            </motion.ul>
                        ))}
                </div>
            </div> : <h2>No Work Experience</h2>}
        </section>
        
    )
}