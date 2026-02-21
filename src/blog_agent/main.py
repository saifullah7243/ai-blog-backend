import asyncio
from dotenv import load_dotenv
from agents import Runner
from .agents import seo_blog_agent
from .schemas import BlogInput

load_dotenv()


async def run():
    blog_input = BlogInput(
        topic="AI Agents in 2026",
        primary_keyword="AI Agents",
        secondary_keywords=["OpenAI SDK", "AI automation", "future of AI"],
        target_audience="Developers and tech entrepreneurs",
        word_count=1200,
    )

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
        max_turns=20
    )

    # Print structured JSON output
    print(result.final_output.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(run())