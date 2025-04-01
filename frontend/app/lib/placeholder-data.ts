import { WorkExperience, ProjectSlide, ProjectTile } from './definitions'

export const workExperiences: WorkExperience[] = [
    {
        exp_id: 0,
        organisation: "Nile University",
        role: "Software Engineering Student",
        duration: "September 2022 - Present",
        experiences: [
            "Headed the design and development of Tourify, a conceptual technology startup aimed at improving tourism within Abuja.",
            "Collaborated with other members of the design team in creating prototypes of website’s intuitive user interface using Figma.",
            "Led the implementation of the design into a functional website using ReactJS and SCSS. Collaborated with and guided other members of the development team in completing the implementation within established deadlines.",
            "Implemented user authentication and a simple backend using Firebase."
        ]

    },
    {
        exp_id: 1,
        organisation: "ChitHub",
        role: "Data Science Intern",
        duration: "July 2024 - Present",
        experiences: [
            "Developed and containerised a data-intensive API using FastAPI for generating result summaries, aggregates and visualisations in the ERMS application.",
            "Automated the population of databases with result data using Python scripts.",
            "Implemented an AI model locally using Python to generate description metadata for different electoral divisions.",
            "Implemented web scrapers using BeautifulSoup to get states’ descriptions from Wikipedia."
        ]

    },
    {
        exp_id: 2,
        organisation: "Medbolt",
        role: "Frontend Engineer",
        duration: "December 2022 - December 2023",
        experiences: [
            "Developed the landing page for the Medbolt AI solutions flagship product Medbolt, an AI powered healthcare solution.",
            "Collaborated with the lead product designer in implementing the user interface of Medbolt's web application using ReactJS and SCSS."
        ]

    }
]

export const projectsSlides: ProjectSlide[] = [
    {
        proj_id: 0,
        proj_img: "/heart-disease.png",
        proj_name: 'Heart Disease Analysis',
        proj_descr: "Exploratory Data Analysis on patients' data to determine patterns and likelihood of heart disease",
        tech_used: ["Python", "Pandas", "Matplotlib", "Seaborn"],
        live_site: "https://www.kaggle.com/code/akinwandetomisin/heart-disease-exploratory-data-analysis"
    },
    {
        proj_id: 1,
        proj_img: "/student-depression.png",
        proj_name: 'Student Depression Analysis',
        proj_descr: "Exploratory Data Analysis on data about students mental health and sleep habits at different education levels",
        tech_used: ["Python", "Pandas", "Matplotlib", "Seaborn"],
        live_site: "https://www.kaggle.com/code/akinwandetomisin/student-depression-exploratory-data-analysis"
    },
    {
        proj_id: 2,
        proj_img: "/tourify.png",
        proj_name: 'Tourify',
        proj_descr: "A website that helps tourists discover exciting locations within Abuja",
        tech_used: ["ReactJS", "Firebase", "SCSS"],
        github_link: "https://github.com/tomjames156/Tourify",
        live_site: "https://tourify-iota.vercel.app/"
    },
    {
        proj_id: 3,
        proj_img: "/medbolt-website.png",
        proj_name: 'Medbolt',
        proj_descr: "A landing page website for a Nigerian healthcare tech startup",
        tech_used: ["ReactJS", "SCSS"],
        live_site: "https://medbolt-website.vercel.app/"
    }
]

export const projectTiles: ProjectTile[] = [
    {
        proj_id: 0,
        proj_name: "Taskify Frontend",
        proj_descr: "A web application with an intuitive user interface that allows users to efficently manage tasks.",
        tech_used: ["React.js", "SASS"],
        github_link: "https://github.com/tomjames156/task_manager",
    }, 
    {
        proj_id: 1,
        proj_name: "Taskify Backend",
        proj_descr: "A Python backend service to manage user's tasks and profiles as well as authentication in the Taskify app.",
        tech_used: ["Python (Django, DRF)", "JWT"],
        github_link: "https://github.com/tomjames156/taskify_api",
    },
    {
        proj_id: 2,
        proj_name: "Getlinked Hackathon",
        proj_descr: "A landing page which was my submisson for the Getlinked web development pre-hackathon",
        tech_used: ["React.js", "SASS"],
        github_link: "https://github.com/tomjames156/Getlinked-hackathon",
        live_site: "https://getlinked-hackathon-three.vercel.app/"
    },
    {
        proj_id: 3,
        proj_name: "Sticky Notes Clone",
        proj_descr: "A fullstack web application clone of the Windows Sticky Notes app.",
        tech_used: ["Python (Django)", "SASS", "TinyMCE"],
        github_link: "https://github.com/tomjames156/Sticky-Notes",
    },
    {
        proj_id: 4,
        proj_name: "Tomi's Food Reviews",
        proj_descr: "A static website/blog with an appealing user interface  where I review foods sold at Nile University.",
        tech_used: ["HTML", "CSS", "JavaScript"],
        github_link: "https://github.com/tomjames156/food_reviews",
        live_site: "https://tomis-food-reviews.netlify.app/"
    },
]