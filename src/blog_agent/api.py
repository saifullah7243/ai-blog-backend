from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from agents import Runner
from sqlalchemy import select
from slugify import slugify
import os

from .agents import seo_blog_agent
from .schemas import BlogInput
from .db import engine, Base, AsyncSessionLocal
from .models import Blog

load_dotenv()

app = FastAPI(title="AI SEO Blog Generator API")

# -------------------------
# CORS Configuration
# -------------------------

FRONTEND_URL = os.getenv("FRONTEND_URL")

origins = ["http://localhost:3000"]

if FRONTEND_URL:
    origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Auto Create Tables
# -------------------------

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# -------------------------
# Generate & Save Blog
# -------------------------

@app.post("/generate-blog")
async def generate_blog(blog_input: BlogInput):
    try:
        formatted_input = f"""
        Topic: {blog_input.topic}
        Primary Keyword: {blog_input.primary_keyword}
        Secondary Keywords: {", ".join(blog_input.secondary_keywords)}
        Target Audience: {blog_input.target_audience}
        Target Word Count: {blog_input.word_count}
        """

        result = await Runner.run(
            seo_blog_agent,
            input=formatted_input,
            max_turns=15,
        )

        output = result.final_output
        slug = slugify(output.title)

        async with AsyncSessionLocal() as session:
            blog = Blog(
                slug=slug,
                title=output.title,
                meta_description=output.meta_description,
                content_html=output.content_html,
            )
            session.add(blog)
            await session.commit()

        return output.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# Get All Blogs
# -------------------------

@app.get("/blogs")
async def get_blogs():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Blog))
        blogs = result.scalars().all()
        return blogs

# -------------------------
# Get Blog By Slug
# -------------------------

@app.get("/blogs/{slug}")
async def get_blog(slug: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Blog).where(Blog.slug == slug)
        )
        blog = result.scalar_one_or_none()

        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        return blog