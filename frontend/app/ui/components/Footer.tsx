import { libre_franklin } from "../fonts"
import Image from "next/image"
import Link from "next/link"
import { useContext } from "react"
import { ProfileContext } from "@/context/ProfileContext"

export default function Footer (){
    const {profile} = useContext(ProfileContext)

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
    <footer className="mt-32 mb-8">
        <div className="flex justify-center gap-10">
            {profile.portfolio.social_links ? 
                profile.portfolio.social_links.map((link, index) => (<Link
                    href={link.link_value}
                    target="_blank"
                    className='hover:-mt-1'
                >
                    <Image
                        src={getLinkIcon(link.link_type)}
                        alt={`${link.link_type} Logo`}
                        width={25}
                        height={25}
                    />
                </Link>))
            : <p>No Social Media</p>}
        </div>
        <p className={`${libre_franklin.className} antialiased text-center text-xs mt-4 dark:text-white`}>Powered by Freelancr <br/>&copy; 2025</p>
    </footer>)
}