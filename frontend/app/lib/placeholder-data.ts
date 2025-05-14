import { WorkExperience, ProjectSlide, ProjectTile, ClientTestimonial, UserData, Experience, AboutSection, Tool, ContactSection, Location, Service, ServicesSection, Portfolio, SocialLink, BulletPoint, Project } from './definitions'

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

export const services: Service[] = [
    {
        name: "Cloud Engineering",
        description: "Encompassing tasks like cloud migration, architecture, security and optimization while also ensuring data accessibility, security, and efficient processing.",
        image: "cloud.png"
    },
    {
        name: "Cloud Engineering",
        description: "Encompassing tasks like cloud migration, architecture, security and optimization while also ensuring data accessibility, security, and efficient processing.",
        image: "cloud.png"
    },
    {
        name: "Cloud Engineering",
        description: "Encompassing tasks like cloud migration, architecture, security and optimization while also ensuring data accessibility, security, and efficient processing.",
        image: "cloud.png"
    }
]

export const userTestimonials: ClientTestimonial[] = [
    {
        name: "Eze Josh",
        organization: "Tourify",
        testimonial: "Lorem ipsum dolor sit amet consectetur. Viverra odio orci tellus ornare blandit. Eros nisl vulputate suscipit. Proin commodo dui ultricies senectus aliquam.",
        image: "profile_user.png"
    }
]

const my_tools : Tool[] = [
    {"name": "React"},
    {"name": "Python"},
    {"name": "Django"}
]

const about_me : AboutSection = {
    "paragraph1": "I'm Tomi",
    "paragraph2": null,
    "picture": null,
    "skills_intro": "These are some things I'm good at",
    "tools": my_tools
}

const my_location: Location = {
    "city": "Times Square",
    "country": "U.S.A",
    "state": "New York"
}

const contact_me: ContactSection = {
    "contact_email": "tomjames156@gmail.com",
    "intro_text": "You can contact me about it",
    "location": my_location,
    "phone_number": "08125887094"
}

const my_projects: Project[] = [
    {
        "description": "Tourism web app",
        "highlight": true,
        "image": "770520bab6f8d8b4ae1df0e36d35f68e.jpeg",
        "name": "Tourify",
        "tools": []
    },
    {
        "description": "Freelance portfolio showcase",
        "highlight": false,
        "image": null,
        "name": "Freelancr",
        "tools": [
            {
                "name": "ReactJS"
            },
            {
                "name": "Flask"
            },
            {
                "name": "NextJS"
            }
        ]
    }
]

const my_services: Service[] = [
    {
        "description": "Implementing user interfaces from designs",
        "image": null,
        "name": "Frontend Development"
    }
]

const my_services_sect: ServicesSection = {
    "intro_text": null,
    "services": my_services
}

const my_points : BulletPoint[] = [
    {
        bullet_point: "Made several projects"
    },{
        bullet_point: "Met new people"
    }
]

const my_experience : Experience = {
    end_date: "Wed, 10 Jun 2026 00:00:00 GMT",
    organization: "Nile University of Nigeria",
    role: "Software Engineering Student",
    start_date: "Tue, 20 Sep 2022 00:00:00 GMT",
    bullet_points: my_points
}

const my_links : SocialLink[] = [
    {
        "link_type": "GitHub",
        "link_value": "www.github.com/tomjames156"
    }
]

const my_portfolio : Portfolio = {
    "profile_pic": null,
    "resume": null,
    "role": "Freelancer",
    "social_links": my_links
}

// const about_me : AboutSection = {}

export const defaultData: UserData ={
    username: "tom1sin",
    experiences: my_experience,
    about_section: about_me,
    client_testimonials: userTestimonials,
    contact_section: contact_me,
    portfolio: my_portfolio,
    projects: my_projects,
    services_section: my_services_sect
}
