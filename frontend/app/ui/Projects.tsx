"use client"

import { libre_franklin } from './fonts'
import { useState } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import gitLogoBlue from "../../public/git-blue.png"
import earthBlue from "../../public/earth-blue.png"
import { projectsSlides, projectTiles } from '../lib/placeholder-data'
import Image from 'next/image'

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


export default function Projects(){

    const [activeIndex, setActiveIndex] = useState(0)

    const listItems = (arr: string[]) => {
        let list_str = ""
        for(let i = 0; i < arr.length; i++){
            if (i !== arr.length - 1){
                list_str += `${arr[i]}, `
            }else{
                list_str += arr[i]
            }
        }
        return list_str
    }

    const prevProject = () => {
        if (activeIndex > 0){
            setActiveIndex(activeIndex - 1)
        }else{
            setActiveIndex(projectsSlides.length - 1)
        }
    }

    const nextProject = () => {
        if (activeIndex < projectsSlides.length - 1){
            setActiveIndex(activeIndex + 1)
        }else{
            setActiveIndex(0)
        }
        
    }

    return (
        <section className="mx-5 mt-20 sm:mx-10 lg:mx-20 xl:mx-40 xl:mt-40" id="projects">
            <h1 className="font-semibold text-[1.4rem] xs:text-2xl dark:text-white">Projects</h1>
            <motion.div className='mt-12 relative w-full h-fit 
            overflow-hidden'
            initial={{opacity: 1, scale: 0.95}}
                    whileInView={{opacity: 1, scale: 1}}
                    transition={{delay: 0.1}}
                    viewport={{once: true, amount: 1}}
                    layout
            >
                <div
                    className='flex transition transition-all ease duration-200 object-contain relative'
                    style={{
                        transform: `translateX(-${activeIndex * 100}%)`
                    }}
                >
                    {projectsSlides.map((proj, index) => {
                        return(
                            <Image
                                key={index}
                                src={proj.proj_img}
                                alt={`${proj.proj_name} project screenshot`}
                                width={50000}
                                height={100}
                                className='border-[1px] border-solid border-black blur-[2px] rounded-2xl w-[100%] h-[auto]'
                            />
                        )
                    })}
                </div>
                <div className='absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col gap-y-2 text-center bg-blue-900 text-white pt-8 pb-4 px-20 w-[38rem] rounded-xl hidden lg:flex'>
                    <p className='text-[1.9rem] font-medium'>{projectsSlides[activeIndex].proj_name}</p>
                    <p className={`${libre_franklin.className} antialiased`}>{projectsSlides[activeIndex].proj_descr}</p>
                    <p className='font-bold text-[0.9rem]'>{listItems(projectsSlides[activeIndex].tech_used)}</p>
                    <div className='flex gap-x-2 justify-center'>
                        {projectsSlides[activeIndex].github_link && <Link 
                            href={projectsSlides[activeIndex].github_link}
                            target='_blank'
                            title='GitHub Repository'
                        >
                            <Image 
                                src="/git.png"
                                width={20}
                                height={25}
                                alt="github logo"
                                className='hover:scale-[1.1]'/>
                        </Link>}
                        {projectsSlides[activeIndex].live_site && <Link
                            href={projectsSlides[activeIndex].live_site}
                            target='_blank'
                            title='Live Site'
                        >
                            <Image 
                                src="/public.png"
                                width={18}
                                height={15}
                                alt="earth"
                                className='hover:scale-[1.1]'/>
                        </Link>}
                    </div>
                </div>
                <div className='absolute top-1/2 -left-1 -translate-y-1/2 material-symbols-rounded text-[2.5rem] cursor-pointer hover:-left-2 hover:scale-[1.1] transition-transform duration-200 xs:-left-2 xs:text-[6rem] xs:hover:-left-4 xs:hover:scale-[1.15]' onClick={prevProject}>
                    chevron_left
                </div>
                <div className='absolute top-1/2 -right-1
                -translate-y-1/2 material-symbols-rounded text-[2.5rem] cursor-pointer hover:-right-2 hover:scale-[1.1] transition-transform duration-200 xs:-right-2 xs:text-[6rem] xs:hover:-right-4 xs:hover:scale-[1.15]' onClick={nextProject}>
                    chevron_right
                </div>
            </motion.div>
            <div className='w-full flex justify-center lg:hidden'>
                <div className='flex flex-col gap-y-1 text-center bg-blue-900 text-white pt-4 pb-2 px-2 w-full mt-4 rounded-xl xs:pt-8 xs:pb-4 xs:px-5 xs:gap-y-2 2xs:w-[95%] xs:max-w-[38rem] xs:px-20'>
                    <p className='text-[1.1rem] font-medium sm:text-[1.9rem]'>{projectsSlides[activeIndex].proj_name}</p>
                    <p className={`${libre_franklin.className} antialiased text-[0.85rem] xs:text-[0.9rem]`}>{projectsSlides[activeIndex].proj_descr}</p>
                    <p className='font-bold text-[0.75rem] xs:text-[0.75rem] sm:text-[1rem]'>{listItems(projectsSlides[activeIndex].tech_used)}</p>
                    <div className='flex gap-x-2 justify-center'>
                        {projectsSlides[activeIndex].github_link && <Link 
                            href={projectsSlides[activeIndex].github_link}
                            target='_blank'
                            title='GitHub Repository'
                        >
                            <Image 
                                src="/git.png"
                                width={20}
                                height={25}
                                alt="github logo"
                                className='hover:scale-[1.1]'/>
                        </Link>}
                        {projectsSlides[activeIndex].live_site && <Link
                            href={projectsSlides[activeIndex].live_site}
                            target='_blank'
                            title='Live Site'
                        >
                            <Image 
                                src="/public.png"
                                width={18}
                                height={15}
                                alt="earth"
                                className='hover:scale-[1.1]'/>
                        </Link>}
                    </div>
                </div>
            </div>
            <div className='w-full h-16 flex items-center justify-center gap-x-4'>
                {projectsSlides && projectsSlides.map((project, index) => {
                    return (index != activeIndex ? <div key={index} className="w-8 h-[0.275rem] bg-[#D9D9D9] cursor-pointer hover:bg-gray-400 transition transition-all duration-100 2xs:w-12" onClick={() => {setActiveIndex(index)}}></div> :
                        <div key={index} className="w-8 h-[0.275rem] bg-blue-900 cursor-pointer 2xs:w-12" onClick={() => {setActiveIndex(index)}}></div>
                    )
                })}
            </div>
            <motion.ul 
                className='grid grid-cols-1 gap-x-4 gap-y-6 px-2 2xs:px-10 xs:grid-cols-2 xs:px-0 sm:px-10 sm:grid-cols-2 sm:justify-between lg:grid-cols-3 xl:px-24 dark:text-white'
                variants={container}
                initial='initial'
                whileInView="whileInView"
                viewport={{amount: 0.1, once: true}}>
                {projectTiles.map((project, index) => {
                    return (
                    <motion.li 
                        key={index} 
                        className='border-[1px] border-solid border-black rounded-xl py-5 px-4 flex flex-col cursor-default hover:-mt-2 hover:border-blue-900 hover:border-[3px] transition transition-all duration-200 dark:border-white' 
                        variants={item}
                        transition={{
                            type: "spring",
                            stiffness: 100,
                            damping: 15
                        }}
                        >
                        <div className='flex gap-4 justify-end'>
                            {project.github_link && <Link 
                                href={project.github_link}
                                target='_blank'
                                className='hover:-mt-1 transition transition-all duration-10'
                            >
                                <Image
                                    src={gitLogoBlue}
                                    width={20}
                                    height={15}
                                    alt='Github Logo'
                                    className='dark:bg-white dark:rounded-xl'
                                />
                            </Link>}
                            {project.live_site && <Link
                                href={project.live_site}
                                target='_blank'
                                className='hover:-mt-1 transition transition-all duration-10'
                            >
                                <Image
                                    src={earthBlue}
                                    width={18}
                                    height={15}
                                    alt='Earth Globe Blue'
                                    className='dark:bg-white dark:rounded-xl'
                                />
                            </Link>}
                        </div>
                        <p className='font-bold text-lg mt-6'>{project.proj_name}</p>
                        <p className={`${libre_franklin.className} antialiased text-[1rem] leading-[1.3rem] mt-6 mb-12 xs:text-[1rem]`}>{project.proj_descr}</p>
                        <p className='text-[0.9rem] xs:text-sm'>{listItems(project.tech_used)}</p>
                    </motion.li>)
                }) }
            </motion.ul>
        </section>
    )
}
