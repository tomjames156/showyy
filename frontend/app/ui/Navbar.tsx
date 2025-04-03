import Link from "next/link"
import Image from "next/image"
import gmail from "../../public/gmail logo.png"
import github from "../../public/github-logo.png"
import linkedin from "../../public/linkedin.png"

export default function Navbar(){
    return (
        <nav className="flex justify-between items-end px-2 bg-white xs:px-5 sm:px-10 lg:px-12 py-4 fixed left-0 top-0 w-full z-20 dark:bg-black dark:text-white">
            <div className="flex-2 flex items-center gap-3">
                <Link href='/' className="font-bold text-[0.95rem] hover:text-gray-500 transition transition-all duration-200 2xs:text-[1rem] xs:text-[1.2rem">tom1sin</Link>
                <div className="hidden sm:block">                
                    <div className="flex items-center justify-center gap-4">
                        <Link
                            href="mailto:tomjames156@gmail.com"
                        >
                            <Image 
                                className="hover:-mt-2 transition transition-all duration-200
                                rounded-md"
                                src={gmail}
                                alt='Gmail Logo'
                                width={25}
                                height={25}
                            />
                        </Link>
                        <Link 
                            href="https://github.com/tomjames156/"
                            target="_blank"
                            className="dark:bg-white dark:rounded-xl"
                        >
                            <Image
                                className="hover:-mt-2 transition transition-all duration-200"
                                src={github}
                                alt='Github Logo'
                                width={20}
                                height={20}
                            />
                        </Link>
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
                    </div>
                </div>
            </div>
            <div className="flex-2 flex gap-2 fold:gap-4 2xs:gap-6 xs:gap-12">
                <Link href='#about' className="text-[0.9rem]
                dark:text-white font-medium hover:font-bold transition transition-all duration-200 2xs:text-[0.9rem] xs:text-[1rem]">About</Link>
                <Link href='#projects' className="text-[0.9rem] font-medium hover:font-bold transition transition-all duration-200 2xs:text-[0.9rem] xs:text-[1rem]">Projects</Link>
                <Link href='#experience' className="text-[0.9rem] font-medium hover:font-bold transition transition-all duration-200 2xs:text-[0.9rem] xs:text-[1rem]">Experience</Link>
            </div>
        </nav>
    )
}
