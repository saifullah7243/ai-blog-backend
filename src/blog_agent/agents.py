from agents import Agent
from .schemas import BlogOutput
from .tools import (
    calculate_keyword_density,
    validate_word_count,
    generate_slug,
    generate_json_ld
)

seo_blog_agent = Agent(
    name="SEO AEO GEO Content Engine",
    model="gpt-4o-mini",
    instructions="""
You are an advanced SEO, AEO, and GEO optimization engine.

SEO REQUIREMENTS:
- Use semantic HTML (<article>, <section>, <h1>, <h2>, <h3>, <ul>, <li>)
- Proper heading hierarchy
- Optimized meta description
- Clean URL
- Include JSON-LD structured data
- Include optimized image with alt text

AEO REQUIREMENTS:
- Answer direct user questions clearly
- Include FAQ section
- Use bullet point explanations
- Provide summary
- Optimize for AI Overview and voice search

GEO REQUIREMENTS:
- Structured content sections
- Clear summaries
- Avoid fluff
- LLM-friendly formatting
- Include schema markup

Generate content first.
Then call tools only if necessary.
Do not repeatedly revalidate.
Return final structured output.

Return strictly structured JSON matching BlogOutput schema.
""",
    tools=[
        calculate_keyword_density,
        validate_word_count,
        generate_slug,
        generate_json_ld
    ],
    output_type=BlogOutput
)