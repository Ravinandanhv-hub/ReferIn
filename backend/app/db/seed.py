"""
Seed script: Populates the database with mock jobs and test users.

Usage:
    python -m app.db.seed
"""

import asyncio
import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import text
from app.db.database import engine, async_session_factory, Base
from app.models.user import User
from app.models.job import Job
from app.models.referral import Referral  # noqa: F401
from app.models.notification import Notification  # noqa: F401
from app.core.security import hash_password


MOCK_USERS = [
    {
        "name": "Alex Seeker",
        "email": "seeker@test.com",
        "password": "password123",
        "role": "job_seeker",
        "skills": ["React", "TypeScript", "Python", "Node.js"],
        "experience": 3,
        "location": "Bangalore, India",
        "preferences": {"job_type": ["full_time", "remote"], "locations": ["India", "US"]},
    },
    {
        "name": "Sam Seeker",
        "email": "seeker2@test.com",
        "password": "password123",
        "role": "job_seeker",
        "skills": ["Java", "Spring Boot", "AWS", "Docker"],
        "experience": 5,
        "location": "Hyderabad, India",
        "preferences": {"job_type": ["full_time"], "locations": ["India"]},
    },
    {
        "name": "Jordan Referrer",
        "email": "referrer@test.com",
        "password": "password123",
        "role": "referrer",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "experience": 6,
        "location": "San Francisco, US",
        "preferences": {},
    },
    {
        "name": "Taylor Referrer",
        "email": "referrer2@test.com",
        "password": "password123",
        "role": "referrer",
        "skills": ["React", "Next.js", "GraphQL"],
        "experience": 4,
        "location": "New York, US",
        "preferences": {},
    },
    {
        "name": "Admin User",
        "email": "admin@test.com",
        "password": "password123",
        "role": "admin",
        "skills": [],
        "experience": 10,
        "location": "Remote",
        "preferences": {},
    },
]

MOCK_JOBS = [
    # Google
    {"title": "Senior Frontend Developer", "company": "Google", "location": "Bangalore, India", "type": "full_time", "skills_required": ["React", "TypeScript", "CSS", "GraphQL"], "description": "Join Google's frontend team building next-generation web applications. You'll work on user-facing products used by billions of people worldwide.", "source": "Company Career Page", "apply_url": "https://careers.google.com/jobs/1", "is_remote": False, "experience_min": 3, "experience_max": 7},
    {"title": "Backend Engineer - Cloud", "company": "Google", "location": "Mountain View, US", "type": "full_time", "skills_required": ["Python", "Go", "Kubernetes", "GCP"], "description": "Build and scale Google Cloud Platform services. Work on distributed systems serving millions of requests per second.", "source": "Company Career Page", "apply_url": "https://careers.google.com/jobs/2", "is_remote": False, "experience_min": 4, "experience_max": 10},
    {"title": "ML Engineer", "company": "Google", "location": "Remote", "type": "full_time", "skills_required": ["Python", "TensorFlow", "PyTorch", "ML"], "description": "Develop and deploy machine learning models at scale. Work on cutting-edge AI research and production systems.", "source": "LinkedIn", "apply_url": "https://careers.google.com/jobs/3", "is_remote": True, "experience_min": 3, "experience_max": 8},

    # Microsoft
    {"title": "Full Stack Developer", "company": "Microsoft", "location": "Hyderabad, India", "type": "full_time", "skills_required": ["React", "C#", ".NET", "Azure"], "description": "Build full-stack applications for Microsoft 365. Work with modern web technologies and cloud services.", "source": "Company Career Page", "apply_url": "https://careers.microsoft.com/jobs/1", "is_remote": False, "experience_min": 2, "experience_max": 6},
    {"title": "DevOps Engineer", "company": "Microsoft", "location": "Redmond, US", "type": "full_time", "skills_required": ["Azure", "Docker", "Kubernetes", "Terraform"], "description": "Automate and optimize CI/CD pipelines for Azure services. Ensure reliability and scalability of cloud infrastructure.", "source": "LinkedIn", "apply_url": "https://careers.microsoft.com/jobs/2", "is_remote": False, "experience_min": 3, "experience_max": 8},
    {"title": "Data Scientist", "company": "Microsoft", "location": "Remote", "type": "full_time", "skills_required": ["Python", "SQL", "Azure ML", "Statistics"], "description": "Analyze large datasets and build predictive models. Drive data-driven decision making across product teams.", "source": "Indeed", "apply_url": "https://careers.microsoft.com/jobs/3", "is_remote": True, "experience_min": 2, "experience_max": 5},

    # Amazon
    {"title": "Software Development Engineer", "company": "Amazon", "location": "Bangalore, India", "type": "full_time", "skills_required": ["Java", "AWS", "DynamoDB", "Microservices"], "description": "Design and build scalable systems for Amazon's e-commerce platform. Work on high-traffic services handling millions of transactions.", "source": "Company Career Page", "apply_url": "https://amazon.jobs/1", "is_remote": False, "experience_min": 2, "experience_max": 7},
    {"title": "Frontend Engineer - AWS Console", "company": "Amazon", "location": "Seattle, US", "type": "full_time", "skills_required": ["React", "TypeScript", "AWS", "Node.js"], "description": "Build the AWS Management Console used by millions of developers. Create intuitive interfaces for complex cloud services.", "source": "Company Career Page", "apply_url": "https://amazon.jobs/2", "is_remote": False, "experience_min": 3, "experience_max": 8},
    {"title": "Cloud Solutions Architect", "company": "Amazon", "location": "Remote", "type": "full_time", "skills_required": ["AWS", "Python", "Terraform", "Architecture"], "description": "Help enterprise customers architect and migrate to AWS. Design scalable, secure, and cost-effective cloud solutions.", "source": "LinkedIn", "apply_url": "https://amazon.jobs/3", "is_remote": True, "experience_min": 5, "experience_max": 12},

    # Meta
    {"title": "React Native Developer", "company": "Meta", "location": "Menlo Park, US", "type": "full_time", "skills_required": ["React Native", "JavaScript", "TypeScript", "iOS"], "description": "Build cross-platform mobile experiences for Facebook and Instagram. Push the boundaries of mobile app development.", "source": "Company Career Page", "apply_url": "https://metacareers.com/jobs/1", "is_remote": False, "experience_min": 3, "experience_max": 7},
    {"title": "Production Engineer", "company": "Meta", "location": "London, UK", "type": "full_time", "skills_required": ["Python", "Linux", "Networking", "Automation"], "description": "Ensure the reliability and performance of Meta's infrastructure. Build tools and automation for fleet management.", "source": "LinkedIn", "apply_url": "https://metacareers.com/jobs/2", "is_remote": False, "experience_min": 4, "experience_max": 9},
    {"title": "AI Research Scientist", "company": "Meta", "location": "Remote", "type": "full_time", "skills_required": ["Python", "PyTorch", "NLP", "Computer Vision"], "description": "Conduct cutting-edge research in AI/ML. Publish papers and translate research into production systems.", "source": "Company Career Page", "apply_url": "https://metacareers.com/jobs/3", "is_remote": True, "experience_min": 4, "experience_max": 10},

    # Startups
    {"title": "Founding Engineer", "company": "TechStartup AI", "location": "Bangalore, India", "type": "full_time", "skills_required": ["Python", "FastAPI", "React", "PostgreSQL"], "description": "Join as a founding engineer to build an AI-powered SaaS platform from scratch. Wear multiple hats and shape the product.", "source": "AngelList", "apply_url": "https://techstartupai.com/careers/1", "is_remote": False, "experience_min": 2, "experience_max": 6},
    {"title": "Backend Developer", "company": "FinTech Solutions", "location": "Mumbai, India", "type": "full_time", "skills_required": ["Node.js", "TypeScript", "MongoDB", "Redis"], "description": "Build scalable payment processing systems. Work with financial APIs and ensure PCI compliance.", "source": "Naukri", "apply_url": "https://fintechsolutions.com/careers/1", "is_remote": False, "experience_min": 1, "experience_max": 4},
    {"title": "Mobile App Developer", "company": "HealthTech Pro", "location": "Remote", "type": "full_time", "skills_required": ["Flutter", "Dart", "Firebase", "REST APIs"], "description": "Build a health and wellness mobile app used by thousands. Integrate with wearable devices and health APIs.", "source": "LinkedIn", "apply_url": "https://healthtechpro.com/careers/1", "is_remote": True, "experience_min": 1, "experience_max": 4},

    # Contract/Part-time
    {"title": "UI/UX Designer (Contract)", "company": "DesignCo", "location": "Remote", "type": "contract", "skills_required": ["Figma", "UI Design", "UX Research", "Prototyping"], "description": "Design intuitive user interfaces for a B2B SaaS product. Conduct user research and create interactive prototypes.", "source": "Upwork", "apply_url": "https://designco.com/careers/1", "is_remote": True, "experience_min": 2, "experience_max": 6},
    {"title": "Technical Writer (Part-time)", "company": "DocuTech", "location": "Remote", "type": "part_time", "skills_required": ["Technical Writing", "API Documentation", "Markdown"], "description": "Write and maintain API documentation, tutorials, and developer guides. Work with engineering teams to document features.", "source": "LinkedIn", "apply_url": "https://docutech.com/careers/1", "is_remote": True, "experience_min": 1, "experience_max": 5},
    {"title": "QA Engineer (Contract)", "company": "TestWise", "location": "Pune, India", "type": "contract", "skills_required": ["Selenium", "Python", "API Testing", "CI/CD"], "description": "Develop and maintain automated test suites. Perform manual and automated testing for web applications.", "source": "Naukri", "apply_url": "https://testwise.com/careers/1", "is_remote": False, "experience_min": 2, "experience_max": 5},

    # Internships
    {"title": "Software Engineering Intern", "company": "Google", "location": "Bangalore, India", "type": "internship", "skills_required": ["Python", "Data Structures", "Algorithms"], "description": "Summer internship program for engineering students. Work on real projects alongside experienced engineers.", "source": "Company Career Page", "apply_url": "https://careers.google.com/internship/1", "is_remote": False, "experience_min": 0, "experience_max": 1},
    {"title": "Frontend Intern", "company": "Flipkart", "location": "Bangalore, India", "type": "internship", "skills_required": ["React", "JavaScript", "HTML", "CSS"], "description": "Learn and contribute to India's largest e-commerce platform. Mentored internship with potential full-time offer.", "source": "Company Career Page", "apply_url": "https://flipkart.com/careers/intern/1", "is_remote": False, "experience_min": 0, "experience_max": 1},

    # More diverse jobs
    {"title": "Senior Python Developer", "company": "DataFlow Inc", "location": "Hyderabad, India", "type": "full_time", "skills_required": ["Python", "Django", "PostgreSQL", "Redis"], "description": "Build data pipelines and APIs for a real-time analytics platform. Scale systems to handle millions of events per day.", "source": "LinkedIn", "apply_url": "https://dataflow.com/careers/1", "is_remote": False, "experience_min": 4, "experience_max": 8},
    {"title": "iOS Developer", "company": "AppVenture", "location": "San Francisco, US", "type": "full_time", "skills_required": ["Swift", "SwiftUI", "iOS", "Core Data"], "description": "Build beautiful iOS apps for a consumer fintech product. Push SwiftUI to its limits with complex animations.", "source": "AngelList", "apply_url": "https://appventure.com/careers/1", "is_remote": False, "experience_min": 2, "experience_max": 6},
    {"title": "Platform Engineer", "company": "CloudNine", "location": "Remote", "type": "full_time", "skills_required": ["Kubernetes", "Docker", "AWS", "Terraform", "Go"], "description": "Build and maintain the internal developer platform. Create self-service infrastructure for engineering teams.", "source": "Indeed", "apply_url": "https://cloudnine.com/careers/1", "is_remote": True, "experience_min": 4, "experience_max": 9},
    {"title": "Security Engineer", "company": "CyberShield", "location": "London, UK", "type": "full_time", "skills_required": ["Security", "Python", "Penetration Testing", "OWASP"], "description": "Conduct security assessments and penetration testing. Implement security best practices across the organization.", "source": "LinkedIn", "apply_url": "https://cybershield.com/careers/1", "is_remote": False, "experience_min": 3, "experience_max": 7},
    {"title": "Data Engineer", "company": "BigData Corp", "location": "Bangalore, India", "type": "full_time", "skills_required": ["Python", "Spark", "Airflow", "SQL", "AWS"], "description": "Build and maintain data pipelines processing terabytes of data daily. Design data warehouse schemas and ETL processes.", "source": "Naukri", "apply_url": "https://bigdatacorp.com/careers/1", "is_remote": False, "experience_min": 2, "experience_max": 6},
    {"title": "Blockchain Developer", "company": "Web3 Labs", "location": "Remote", "type": "full_time", "skills_required": ["Solidity", "Ethereum", "Web3.js", "React"], "description": "Build decentralized applications and smart contracts. Work on DeFi protocols and NFT marketplaces.", "source": "AngelList", "apply_url": "https://web3labs.com/careers/1", "is_remote": True, "experience_min": 1, "experience_max": 5},
    {"title": "Tech Lead - Payments", "company": "PayEase", "location": "Mumbai, India", "type": "full_time", "skills_required": ["Java", "Microservices", "Kafka", "PostgreSQL"], "description": "Lead a team building payment gateway infrastructure. Handle millions of transactions with 99.99% uptime.", "source": "Naukri", "apply_url": "https://payease.com/careers/1", "is_remote": False, "experience_min": 7, "experience_max": 12},
    {"title": "SRE Engineer", "company": "Netflix", "location": "Remote", "type": "full_time", "skills_required": ["Linux", "Python", "AWS", "Monitoring", "Incident Response"], "description": "Ensure the reliability of Netflix's streaming platform. Build monitoring and alerting systems at massive scale.", "source": "Company Career Page", "apply_url": "https://jobs.netflix.com/1", "is_remote": True, "experience_min": 4, "experience_max": 9},
    {"title": "Android Developer", "company": "Swiggy", "location": "Bangalore, India", "type": "full_time", "skills_required": ["Kotlin", "Android", "MVVM", "Jetpack Compose"], "description": "Build features for India's leading food delivery app. Work on a Kotlin-first Android codebase with modern architecture.", "source": "Company Career Page", "apply_url": "https://swiggy.com/careers/1", "is_remote": False, "experience_min": 2, "experience_max": 5},
    {"title": "DevRel Engineer", "company": "Postman", "location": "Bangalore, India", "type": "full_time", "skills_required": ["APIs", "Technical Writing", "Public Speaking", "JavaScript"], "description": "Be the bridge between Postman and the developer community. Create content, speak at conferences, and build tools.", "source": "LinkedIn", "apply_url": "https://postman.com/careers/1", "is_remote": False, "experience_min": 2, "experience_max": 6},
    {"title": "Rust Systems Programmer", "company": "CloudFlare", "location": "Remote", "type": "full_time", "skills_required": ["Rust", "Systems Programming", "Networking", "Linux"], "description": "Build high-performance edge computing services in Rust. Write code that runs on servers across 300+ cities worldwide.", "source": "Company Career Page", "apply_url": "https://cloudflare.com/careers/1", "is_remote": True, "experience_min": 3, "experience_max": 8},
    {"title": "Product Manager - Developer Tools", "company": "GitHub", "location": "Remote", "type": "full_time", "skills_required": ["Product Management", "Agile", "Developer Tools", "Analytics"], "description": "Define the roadmap for GitHub's developer collaboration tools. Work with engineering to ship features used by millions of developers.", "source": "Company Career Page", "apply_url": "https://github.com/about/careers/1", "is_remote": True, "experience_min": 4, "experience_max": 9},
    {"title": "Computer Vision Engineer", "company": "Tesla", "location": "Palo Alto, US", "type": "full_time", "skills_required": ["Python", "Computer Vision", "PyTorch", "C++"], "description": "Develop perception systems for autonomous driving. Work on object detection, tracking, and scene understanding.", "source": "Company Career Page", "apply_url": "https://tesla.com/careers/1", "is_remote": False, "experience_min": 3, "experience_max": 8},
    {"title": "NLP Engineer", "company": "OpenAI Partner", "location": "Remote", "type": "full_time", "skills_required": ["Python", "NLP", "Transformers", "LLMs", "HuggingFace"], "description": "Build NLP products powered by large language models. Fine-tune and deploy LLMs for enterprise use cases.", "source": "LinkedIn", "apply_url": "https://openaipartner.com/careers/1", "is_remote": True, "experience_min": 2, "experience_max": 6},
    {"title": "Go Backend Developer", "company": "CoinSwitch", "location": "Bangalore, India", "type": "full_time", "skills_required": ["Go", "gRPC", "PostgreSQL", "Redis"], "description": "Build high-throughput trading systems in Go. Handle real-time market data and order execution.", "source": "Naukri", "apply_url": "https://coinswitch.com/careers/1", "is_remote": False, "experience_min": 2, "experience_max": 5},
    {"title": "Vue.js Frontend Developer", "company": "DigitalOcean", "location": "Remote", "type": "full_time", "skills_required": ["Vue.js", "TypeScript", "Tailwind CSS", "GraphQL"], "description": "Build the DigitalOcean Cloud Console. Create intuitive interfaces for cloud infrastructure management.", "source": "Company Career Page", "apply_url": "https://digitalocean.com/careers/1", "is_remote": True, "experience_min": 2, "experience_max": 6},
    {"title": "Embedded Systems Engineer", "company": "Qualcomm", "location": "Hyderabad, India", "type": "full_time", "skills_required": ["C", "C++", "RTOS", "ARM"], "description": "Develop firmware for mobile chipsets. Optimize for performance, power consumption, and memory footprint.", "source": "Company Career Page", "apply_url": "https://qualcomm.com/careers/1", "is_remote": False, "experience_min": 3, "experience_max": 8},
    {"title": "Database Administrator", "company": "Oracle", "location": "Bangalore, India", "type": "full_time", "skills_required": ["Oracle DB", "SQL", "Performance Tuning", "RAC"], "description": "Manage and optimize enterprise Oracle database installations. Ensure high availability and disaster recovery.", "source": "Company Career Page", "apply_url": "https://oracle.com/careers/1", "is_remote": False, "experience_min": 5, "experience_max": 10},
    {"title": "Salesforce Developer", "company": "Infosys", "location": "Pune, India", "type": "full_time", "skills_required": ["Salesforce", "Apex", "Lightning", "Integration"], "description": "Develop and customize Salesforce solutions for enterprise clients. Build Lightning components and Apex triggers.", "source": "Naukri", "apply_url": "https://infosys.com/careers/1", "is_remote": False, "experience_min": 2, "experience_max": 6},
    {"title": "Staff Engineer - Infrastructure", "company": "Uber", "location": "Bangalore, India", "type": "full_time", "skills_required": ["Go", "Java", "Kafka", "Cassandra", "Microservices"], "description": "Design and build Uber's core infrastructure. Work on systems that handle millions of trips per day.", "source": "Company Career Page", "apply_url": "https://uber.com/careers/1", "is_remote": False, "experience_min": 8, "experience_max": 15},
    {"title": "Junior Web Developer", "company": "Freshworks", "location": "Chennai, India", "type": "full_time", "skills_required": ["HTML", "CSS", "JavaScript", "React"], "description": "Start your career building SaaS products. Mentored role with structured learning and growth opportunities.", "source": "Company Career Page", "apply_url": "https://freshworks.com/careers/1", "is_remote": False, "experience_min": 0, "experience_max": 2},
    {"title": "MLOps Engineer", "company": "Spotify", "location": "Remote", "type": "full_time", "skills_required": ["Python", "MLflow", "Kubernetes", "Docker", "AWS"], "description": "Build and maintain ML infrastructure for Spotify's recommendation systems. Deploy and monitor ML models at scale.", "source": "LinkedIn", "apply_url": "https://spotify.com/careers/1", "is_remote": True, "experience_min": 3, "experience_max": 7},
    {"title": "Technical Program Manager", "company": "Stripe", "location": "Remote", "type": "full_time", "skills_required": ["Program Management", "Technical Background", "Agile", "Cross-functional"], "description": "Drive complex engineering programs across multiple teams. Ensure timely delivery of Stripe's payment products.", "source": "Company Career Page", "apply_url": "https://stripe.com/careers/1", "is_remote": True, "experience_min": 5, "experience_max": 10},
    {"title": "React Developer", "company": "Zerodha", "location": "Bangalore, India", "type": "full_time", "skills_required": ["React", "TypeScript", "D3.js", "WebSocket"], "description": "Build India's most popular stock trading platform. Work on real-time charting and trading interfaces.", "source": "Company Career Page", "apply_url": "https://zerodha.com/careers/1", "is_remote": False, "experience_min": 2, "experience_max": 5},
]


async def seed_database():
    """Create tables and seed with mock data."""
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed data
    async with async_session_factory() as session:
        # Check if already seeded
        result = await session.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        if count > 0:
            print("Database already seeded. Skipping...")
            return

        # Create users
        for user_data in MOCK_USERS:
            user = User(
                name=user_data["name"],
                email=user_data["email"],
                hashed_password=hash_password(user_data["password"]),
                role=user_data["role"],
                skills=user_data["skills"],
                experience=user_data["experience"],
                location=user_data["location"],
                preferences=user_data["preferences"],
            )
            session.add(user)

        # Create jobs with staggered posted_at dates
        now = datetime.now(timezone.utc)
        for i, job_data in enumerate(MOCK_JOBS):
            job = Job(
                title=job_data["title"],
                company=job_data["company"],
                location=job_data["location"],
                type=job_data["type"],
                skills_required=job_data["skills_required"],
                description=job_data["description"],
                source=job_data["source"],
                apply_url=job_data["apply_url"],
                is_remote=job_data["is_remote"],
                experience_min=job_data["experience_min"],
                experience_max=job_data["experience_max"],
                posted_at=(now - timedelta(days=i)).isoformat(),
            )
            session.add(job)

        await session.commit()
        print(f"Seeded {len(MOCK_USERS)} users and {len(MOCK_JOBS)} jobs successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())
