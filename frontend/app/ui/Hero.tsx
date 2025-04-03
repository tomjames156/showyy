import { libre_franklin } from './fonts'
import Link from 'next/link'

export default function Hero(){
    return (
        <section className='flex justify-center pt-60 pb-20 lg:pb-60 dark:text-white' id='hero'>
            <div className='flex-col text-center max-w-[85%] sm:max-w-[80%] md:max-w-[70%] lg:max-w-[45%] '>
                <p className='text-9xl wavehand'>👋🏾</p>
                <h1 className='text-[1.75rem] mt-10 font-bold xs:text-3xl sm:text-4xl'>Hi there, I’m Tomisin</h1>
                <h3 className='text-[1.3rem] mt-1 font-medium sm:text-2xl sm:mt-4'>I love writing code</h3>
                <p className={`mt-1 leading-[1.3rem] text-[1rem] ${libre_franklin.className} antialiased xs:text-[1.1rem] xs:mt-2 sm:mt-4 sm:text-[1.1rem] sm:leading-[1.4rem]`}>I’m a budding data scientist and and software engineering student from Abuja, Nigeria. I’m passionate about finding actionable insights from data and building innovative solutions to real-world problems.</p>
                <Link href="/resume.pdf" target='_blank' download={true} title="Download Resume" className='w-fit mt-10 mx-auto flex border-[0.1rem] border-blue-900 text-center items-center text-blue-900 pl-2 pr-4 py-0.5 rounded-md gap-[0.25rem] transition-all ease-in-out duration-100 hover:bg-blue-900 hover:text-white hover:border-[0.15rem] text-[1rem] dark:hover:border-blue-400 dark:hover:text-blue-400
                dark:hover:bg-black dark:bg-white
                dark:text-black dark:border-white'>
                    <span className="material-symbols-rounded hover:[--font-FILL:1] hover:[--font-wght:600]">
                        download
                    </span>  
                    Resume       
                </Link>
            </div>
        </section>
    )
}