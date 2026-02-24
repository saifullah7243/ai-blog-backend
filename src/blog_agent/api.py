from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from agents import Runner
from sqlalchemy import select
from slugify import slugify
import os

from .agents import seo_blog_agent
from .schemas import BlogInput
import asyncio

load_dotenv()

app = FastAPI(title="AI SEO Blog Generator API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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