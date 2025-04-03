import { motion } from 'framer-motion';

type TechnologyUsedProps = {
    technology: string;
}

const item  = {
    initial: { x: 20, opacity: 0},
    whileInView: {
        x: 0,
        opacity: 1
    }
}

export default function TechnologyUsed({technology}: TechnologyUsedProps){
    return (
        <motion.div className='flex items-center gap-3 xxs:pl-3' variants={item}>
            <div className='w-[0.5rem] bg-blue-900 h-[0.5rem] rounded-xl dark:bg-blue-400'>
            </div>
            <div className='font-medium text-[1rem] xs:text-[1.1rem]'>{technology}</div>
        </motion.div>
    )
}