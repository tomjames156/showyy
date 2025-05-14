export type WorkExperience = {
    organisation: string,
    exp_id: number,
    role: string,
    duration: string,
    experiences: string[]
}

export type ProjectSlide = {
    proj_id: number,
    proj_img: string | null,
    proj_name: string
    proj_descr: string,
    tech_used: string[],
    github_link?: string,
    live_site?: string
}

export type ProjectTile = {
    proj_id: number,
    proj_name: string,
    proj_descr: string,
    tech_used: string[],
    github_link?: string,
    live_site?: string
}

export type ClientTestimonial = {
    image: string | null,
    name: string,
    testimonial: string,
    organization: string
}

export type Tool = {
    name: string
}

export type AboutSection = {
    paragraph1: string | null,
    paragraph2: string | null,
    picture: string | null,
    skills_intro: string | null,
    tools: Tool[]
}
export type Location = {
    city: string,
    country: string,
    state: string
}
export type ContactSection = {
    contact_email: string | null,
    intro_text: string | null,
    location: Location | null,
    phone_number: string | null
}
export type BulletPoint = {
    bullet_point: string,
}
export type Experience = {
    bullet_points: BulletPoint[],
    organization: string,
    role: string,
    end_date: string,
    start_date: string
}
export type SocialLink = {
    link_type: string,
    link_value: string
}
export type Portfolio = {
    profile_pic: string | null,
    resume: string | null,
    role: string,
    social_links: SocialLink[]
}
export type Project = {
    description: string,
    highlight: boolean,
    image: string | null,
    name: string,
    tools: Tool[]
}

export type Service = {
    description: string,
    image: string | null,
    name: string
}

export type ServicesSection = {
    intro_text: string | null,
    services: Service[],
}

export type UserData = {
    username: string,
    about_section: AboutSection
    client_testimonials: ClientTestimonial[]
    contact_section: ContactSection
    experiences: Experience[]
    portfolio: Portfolio
    projects: Project[]
    services_section: ServicesSection
}

// {
//     "about_section": {
//         "paragraph1": "I'm Tomi",
//         "paragraph2": null,
//         "picture": null,
//         "skills_intro": "These are some things I'm good at",
//         "tools": []
//     },
//     "client_testimonials": [
//         {
//             "image": "a41f2afa9c77c29b7c2285a55e6dd6ab.png",
//             "name": "Alice In Wonderland",
//             "organization": "Wonderland",
//             "testimonial": "He got the job done"
//         },
//         {
//             "image": null,
//             "name": "Tomisin Akinwande",
//             "organization": "MoonLit Co",
//             "testimonial": "He completed the tasks on time and correctlu, 10/10"
//         }
//     ],
//     "contact_section": {
//         "contact_email": "tomjames156@gmail.com",
//         "intro_text": "You can contact me about it",
//         "location": {
//             "city": "Times Square",
//             "country": "U.S.A",
//             "state": "New York"
//         },
//         "phone_number": "08125887094"
//     },
//     "experiences": [
//         {
//             "bullet_points": [
//                 {
//                     "bullet_point": "Made several projects"
//                 },
//                 {
//                     "bullet_point": "Led several group projects"
//                 },
//                 {
//                     "bullet_point": "Team work"
//                 },
//                 {
//                     "bullet_point": "Software Director for NACOS Nile Chapter"
//                 }
//             ],
//             "end_date": "Wed, 10 Jun 2026 00:00:00 GMT",
//             "organization": "Nile University of Nigeria",
//             "role": "Software Engineering Student",
//             "start_date": "Tue, 20 Sep 2022 00:00:00 GMT"
//         }
//     ],
//     "portfolio": {
//         "profile_pic": null,
//         "resume": null,
//         "role": "Freelancer",
//         "social_links": [
//             {
//                 "link_type": "GitHub",
//                 "link_value": "www.github.com/tomjames156"
//             }
//         ],
//         "user_id": 1
//     },
//     "projects": [
//         {
//             "description": "Tourism web app",
//             "highlight": true,
//             "image": "770520bab6f8d8b4ae1df0e36d35f68e.jpeg",
//             "name": "Tourify",
//             "tools": []
//         },
//         {
//             "description": "Freelance portfolio showcase",
//             "highlight": false,
//             "image": null,
//             "name": "Freelancr",
//             "tools": [
//                 {
//                     "name": "ReactJS"
//                 },
//                 {
//                     "name": "Flask"
//                 },
//                 {
//                     "name": "NextJS"
//                 }
//             ]
//         }
//     ],
//     "services_section": {
//         "intro_text": null,
//         "services": [
//             {
//                 "description": "Implementing user interfaces from designs",
//                 "image": null,
//                 "name": "Frontend Development"
//             }
//         ]
//     },
//     "username": "tom1"
// }