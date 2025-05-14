import Image from "next/image"
import { useState } from "react"
import { libre_franklin } from "./fonts"
import { userTestimonials } from "../lib/placeholder-data"

export default function Testimonials() {
    const [activeIndex, setActiveIndex] = useState(0)
    const allTestimonials = [{}, {}, {}, {}]

  return (
    <aside className="mx-5 sm:mx-10 lg:mx-20 xl:mx-80 mt-10 dark:text-white">
        {
            userTestimonials.map((testimonial, index) => {
                return (
                    <div className="flex-col justify-items-center text-center" key={index}>
                        <div className="flex gap-4">
                            <div>
                                <Image
                                    src='/quotation-mark.png'
                                    alt='left-quote'
                                    width={50}
                                    height={50}
                                    className="-mt-2"
                                />
                            </div>
                            <p className={`${libre_franklin.className} text-[1rem]`}>{testimonial.testimonial}</p>
                            <div>
                                <Image
                                    src='/quotation-right-mark.png'
                                    alt='left-quote'
                                    width={50}
                                    height={50}
                                    className="-mt-2"
                                />
                            </div>  
                        </div>
                        <Image
                            src='/profile_user.png'
                            alt='default pic'
                            width={40}
                            height={40}
                            className="mt-4"
                        />
                        <p className="uppercase font-semibold mt-2 text-[0.95rem]">{testimonial.name}</p>
                        <p className="uppercase text-[0.8rem]">{testimonial.organization}</p>
                    </div>
                )
            })
        }
        <div className="flex gap-x-4 justify-center mt-2">
            {
                allTestimonials.map((testimonial, index) => {
                    return (
                        <div className="w-[7px] h-[7px] bg-black rounded-[50%]"></div>
                    )
                })
            }
        </div>
    </aside>
  )
}
