import { libre_franklin } from "./fonts"
import Image from "next/image"
import { useContext } from "react"
import { ProfileContext } from "@/context/ProfileContext"

export default function Contact() {
    const { profile } = useContext(ProfileContext)

    if(!profile.contact_section){
        return (<section id="about" className="mx-5 sm:mx-10 lg:mx-20 xl:mx-40 mt-10 xl:mt-24 dark:text-white">
            <h1 className="font-semibold text-[1.4rem] xs:text-2xl">Contact Me</h1>
            <p className="mt-4">No Contact Details</p>
        </section>)
    }

  return (
    <section id="about" className="mx-5 sm:mx-10 lg:mx-20 xl:mx-40 mt-10 xl:mt-24 dark:text-white">
      <h1 className="font-semibold text-[1.4rem] xs:text-2xl">Contact Me</h1>
      <p className={`mt-2 leading-[1.4rem] text-[1rem] ${libre_franklin.className} antialiased xs:text-[1.1rem] sm:mt-4`}>{profile.contact_section.intro_text}</p>
      <div className="grid grid-cols-1 justify-between gap-y-12 mt-8 items-center xs:grid-cols-2 md:grid-cols-3">
        <div className="flex-col justify-items-center text-center">
            <Image
                src="/smartphone-call.png"
                alt="smartphone"
                width={40}
                height={40}
                className="mb-4"
            />
            <h3 className="font-bold text-[1.1rem]">Call me</h3>
            <p className={`${libre_franklin.className}`}>{profile.contact_section.phone_number}</p>
        </div>
        <div className="flex-col justify-items-center text-center">
            <Image
                src="/email.png"
                alt="email envelope"
                width={40}
                height={40}
                className="mb-4"
            />
            <h3 className="font-bold text-[1.1rem]">Send an email</h3>
            <p className={`${libre_franklin.className}`}>{profile.contact_section.contact_email}</p>
        </div>
        <div className="flex-col justify-items-center text-center">
            <Image
                src="/location-pin.png"
                alt="location pin"
                width={30}
                height={30}
                className="mb-4"
            />
            <h3 className="font-bold text-[1.1rem]">{profile.contact_section.location.city}</h3>
            <p className={`${libre_franklin.className}`}>{profile.contact_section.location.state}</p>
        </div>
      </div>
    </section>
  )
}
