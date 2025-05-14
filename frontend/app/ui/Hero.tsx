import { kode_mono } from './fonts'
import Image from 'next/image'
import Link from 'next/link'
import { useContext } from 'react'
import { ProfileContext } from '@/context/ProfileContext'

export default function Hero(){
    const { profile } = useContext(ProfileContext)
    
    const getLinkIcon = (link_type: string) => {
        switch (link_type){
            case "GitHub":
                return '/github.png'
            case "Facebook":
                return '/facebook.png'
            case "Linkedin":
                return '/linkedin-logo.png'
            case "Instagram":
                return '/instagram.png'
        }

    }

    return (
        <section className='flex justify-center pt-60 pb-20 lg:pb-60 dark:text-white' id='hero'>
            <div className='flex-col text-center max-w-[85%] sm:max-w-[80%] md:max-w-[70%] lg:max-w-[45%] '>
                <h1 className='text-[1.75rem] mt-10 text-2xl xs:text-3xl'>I'm a</h1>
                <h3 className={`text-[1.3rem] mt-1 font-medium sm:text-[1.5rem] sm:mt-4 ${kode_mono.className} uppercase`}>{profile.portfolio.role}</h3>
                <div className='flex justify-center gap-6 mt-4'>
                    {profile.portfolio.social_links ? 
                        profile.portfolio.social_links.map((link, index) => (<Link
                            href={link.link_value}
                            target="_blank"
                            className='hover:-mt-1'
                        >
                            <Image
                                src={getLinkIcon(link.link_type)}
                                alt={`${link.link_type} Logo`}
                                width={28}
                                height={28}
                            />
                        </Link>))
                    : <p>No Social Media</p>}
                </div>
                {/* 
                    <Link
                        href="https://web.facebook.com/?_rdc=1&_rdr#"
                        target="_blank"
                        className='hover:-mt-1'
                    >
                        <Image
                            src="/facebook.png"
                            alt='Facebook Logo'
                            width={28}
                            height={28}
                        />
                    </Link>
                    <Link
                        href="https://web.facebook.com/?_rdc=1&_rdr#"
                        target="_blank"
                        className='hover:-mt-1'
                    >
                        <Image
                            src="/linkedin-logo.png"
                            alt='LinkedIn Logo'
                            width={28}
                            height={28}
                        />
                    </Link>
                    <Link
                        href="https://web.facebook.com/?_rdc=1&_rdr#"
                        target="_blank"
                        className='hover:-mt-1'
                    >
                        <Image
                            src="/instagram.png"
                            alt='Instagram Logo'
                            width={28}
                            height={28}
                        />
                    </Link>
                    <Link
                        href="https://www.github.com"
                        target="_blank"
                        className='hover:-mt-1'
                    >
                        <Image
                            src="/github.png"
                            alt='GitHub logo'
                            width={28}
                            height={28}
                        />
                    </Link>
                </div> */}
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