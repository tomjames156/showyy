import { libre_franklin } from "./fonts"
import Image from "next/image"

export default function Contact() {
  return (
    <section id="about" className="mx-5 sm:mx-10 lg:mx-20 xl:mx-40 mt-10 xl:mt-24 dark:text-white">
      <h1 className="font-semibold text-[1.4rem] xs:text-2xl">Contact Me</h1>
      <p className={`mt-2 leading-[1.4rem] text-[1rem] ${libre_franklin.className} antialiased xs:text-[1.1rem] sm:mt-4`}>Below are some of my contact information. Feel free to reach out to me for any inquiries and I’ll get back to you promptly</p>
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
            <p className={`${libre_franklin.className}`}>+234 607 982 3730</p>
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
            <p className={`${libre_franklin.className}`}>example@gmail.com</p>
        </div>
        <div className="flex-col justify-items-center text-center">
            <Image
                src="/location-pin.png"
                alt="location pin"
                width={30}
                height={30}
                className="mb-4"
            />
            <h3 className="font-bold text-[1.1rem]">Lokogoma</h3>
            <p className={`${libre_franklin.className}`}>Abuja</p>
        </div>
      </div>
    </section>
  )
}
