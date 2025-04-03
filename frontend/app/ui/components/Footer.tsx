import { libre_franklin } from "../fonts"

export default function Footer (){
    return (<footer className="mt-32 mb-8">
        <p className={`${libre_franklin.className} antialiased text-center text-xs dark:text-white`}>Developed by Tomisin Akinwande <br/>&copy; 2025</p>
    </footer>)
}