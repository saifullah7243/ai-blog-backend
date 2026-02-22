from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from agents import Runner
from .agents import seo_blog_agent
from .schemas import BlogInput
import os

load_dotenv()

app = FastAPI(title="AI SEO Blog Generator API")

# Get frontend URL from Railway environment variable
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Allowed origins
origins = [
    "http://localhost:3000",  # Local dev
]

if FRONTEND_URL:
    origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "API is running"}


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

        return result.final_output.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
