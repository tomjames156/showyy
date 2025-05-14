import Link from "next/link"
import { useContext } from "react"
import { ProfileContext } from "@/context/ProfileContext"

export default function Navbar(){
    const context = useContext(ProfileContext)

    if (!context) {
        return <div>Profile data is not available.  Make sure you are within a ProfileProvider.</div>;
    }

    const { profile } = context

    return (
        <nav className="flex justify-between items-end px-2 bg-white xs:px-5 sm:px-10 lg:px-12 py-4 fixed left-0 top-0 w-full z-20 dark:bg-black dark:text-white">
            <div className="flex-2 flex items-center gap-3">
                <Link href='/' className="font-bold text-[0.95rem] hover:text-gray-500 transition transition-all duration-200 2xs:text-[1rem] xs:text-[1.2rem">{profile?.username}</Link>
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
