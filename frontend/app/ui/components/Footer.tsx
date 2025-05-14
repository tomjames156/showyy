import { libre_franklin } from "../fonts"
import Image from "next/image"
import Link from "next/link"

export default function Footer (){
    return (
    <footer className="mt-32 mb-8">
        <div className="flex justify-center gap-10">
            <Link
                href="https://web.facebook.com/?_rdc=1&_rdr#"
                target="_blank"
                className='hover:-mt-1'
            >
                <Image
                    src='/facebook.png'
                    alt='facebook'
                    width={25}
                    height={25}
                />
            </Link>
            <Link
                href="https://web.facebook.com/?_rdc=1&_rdr#"
                target="_blank"
                className='hover:-mt-1'
            >
                <Image
                    src='/linkedin-logo.png'
                    alt='LinkedIn'
                    width={25}
                    height={25}
                />
            </Link>
            <Link
                href="https://web.facebook.com/?_rdc=1&_rdr#"
                target="_blank"
                className='hover:-mt-1'
            >
                <Image
                    src='/instagram.png'
                    alt='Instagram'
                    width={25}
                    height={25}
                />
            </Link>
            <Link
                href="https://web.facebook.com/?_rdc=1&_rdr#"
                target="_blank"
                className='hover:-mt-1'
            >
                <Image
                    src='/github.png'
                    alt='GitHub'
                    width={25}
                    height={25}
                />
            </Link>
        </div>
        <p className={`${libre_franklin.className} antialiased text-center text-xs mt-4 dark:text-white`}>Powered by Freelancr <br/>&copy; 2025</p>
    </footer>)
}