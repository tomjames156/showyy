"use client"

import TechnologyUsed from "./components/TechnologyUsed"
import { libre_franklin } from './fonts'
import { motion } from "framer-motion"
import Link from "next/link"
import Image from "next/image"
import gmail from "../../public/gmail logo.png"
import github from "../../public/github-logo.png"
import linkedin from "../../public/linkedin.png"

const container = {
    initial: { opacity: 1, scale: 0},
    whileInView: {
        opacity: 1,
        scale: 1,
        transition: {
            delayChildren: 0.1,
            staggerChildren: 0.05,
        }
    }
}

export default function About(){

    return (
        <section id="about" className="mx-5 sm:mx-10 lg:mx-20 xl:mx-40 dark:text-white">
            <h1 className="font-semibold text-[1.4rem] xs:text-2xl">About Me</h1>
            <div className="flex gap-20 flex-col items-center lg:flex-row lg:items-start">
                <div className="basis-[80%]">
                    <p className={`mt-2 leading-[1.4rem] text-[1rem] ${libre_franklin.className} antialiased xs:text-[1.1rem] sm:mt-4`}>I am currently studying for a Bachelor&apos;s of Science in Software engineering student at Nile University of Nigeria, Abuja. At the same time, I&apos;m working towards a career in Data Science through learning from resources online.</p>
                    <p className={`mt-4 leading-[1.4rem] text-[1rem] ${libre_franklin.className} antialiased xs:text-[1.1rem]`}>Here are some technologies I’ve worked with:</p>
                    <motion.ul 
                        className="w-[50%] mt-5 grid grid-cols-1 xxs:grid-cols-2"
                        variants={container}
                        initial='initial'
                        whileInView="whileInView"
                        viewport={{once: true}}>
                        <TechnologyUsed technology="Pandas"/>
                        <TechnologyUsed technology="Python"/>
                        <TechnologyUsed technology="FastAPI"/>
                        <TechnologyUsed technology="Django"/>
                        <TechnologyUsed technology="React"/>
                        <TechnologyUsed technology="JavaScript"/>
                    </motion.ul>
                    <p className={`mt-4 leading-[1.4rem] text-[1rem] ${libre_franklin.className} antialiased xs:text-[1.1rem]`}>Outside of studying, I enjoy lifting weights, swimming, listening to music, watching movies and reading fantasy books. </p>
                </div>
                <div className="basis-[20%]">
                    <motion.div
                        layout
                        initial={{opacity: 0, y: 20}}
                        whileInView={{opacity: 1, y: 0}}
                        transition={{
                            delay: 0.2, 
                            type: "spring",
                            stiffness: 100,
                            damping: 15
                        }}
                        viewport={{once: true}}
                    >
                        <Image
                            src="/me.jpeg"
                            alt='myself'
                            width={300}
                            height={150}
                            className="rounded-3xl"
                        />
                    </motion.div>
                    <div className="flex items-center justify-center gap-4 mt-2 h-fit sm:hidden">
                        <motion.div
                            initial={{opacity: 0, x: -20}}
                            whileInView={{opacity: 1, x: 0}}
                            transition={{
                                delay: 0.2, 
                                type: "spring",
                                stiffness: 100,
                                damping: 15
                            }}
                            viewport={{once: true}}
                        >
                            <Link
                                href="mailto:tomjames156@gmail.com"
                            >
                                <Image 
                                    className="rounded-md hover:-mt-2 transition transition-all duration-200"
                                    src={gmail}
                                    alt='Gmail Logo'
                                    width={25}
                                    height={25}
                                />
                            </Link>
                        </motion.div>
                        <motion.div
                            initial={{opacity: 0, y: 20}}
                            whileInView={{opacity: 1, y: 0}}
                            transition={{
                                delay: 0.2, 
                                type: "spring",
                                stiffness: 100,
                                damping: 15
                            }}
                            viewport={{once: true}}
                        >
                            <Link 
                                href="https://github.com/tomjames156/"
                                target="_blank"
                            >
                                <Image
                                    className="hover:-mt-2 transition transition-all duration-200 dark:bg-white dark:rounded-xl"
                                    src={github}
                                    alt='Github Logo'
                                    width={20}
                                    height={20}
                                />
                            </Link>
                        </motion.div>
                        <motion.div 
                            initial={{opacity: 0, x: 20}}
                            whileInView={{opacity: 1, x: 0}}
                            transition={{
                                delay: 0.2, 
                                type: "spring",
                                stiffness: 100,
                                damping: 15
                            }}
                            viewport={{once: true}}
                        >
                            <Link 
                                href="https://www.linkedin.com/in/tomisin-akinwande-981842247/"
                                target="_blank"
                            >
                                <Image
                                    className="hover:-mt-2 transition transition-all duration-200"
                                    src={linkedin}
                                    alt='Linkedin logo'
                                    width={18}
                                    height={18}
                                />
                            </Link>
                        </motion.div>
                    </div>
                </div>
            </div>
        </section>
    )
}