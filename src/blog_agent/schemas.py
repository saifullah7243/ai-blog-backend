from pydantic import BaseModel, Field
from typing import List


# INPUT
class BlogInput(BaseModel):
    topic: str
    primary_keyword: str
    secondary_keywords: List[str] = []
    target_audience: str
    word_count: int = 1000


# FAQ
class FAQItem(BaseModel):
    question: str
    answer: str


# STRUCTURED SECTIONS (NO DICT)
class StructuredSections(BaseModel):
    introduction: str
    main_content: str
    technical_details: str
    conclusion: str


# JSON-LD (STRICT FIELDS)
class JsonLD(BaseModel):
    context: str = Field(default="https://schema.org")
    type: str = Field(default="Article")
    headline: str
    description: str
    author_name: str


# OUTPUT
class BlogOutput(BaseModel):
    title: str
    slug: str
    meta_description: str

    headings: List[str]
    content_html: str
    featured_image_alt: str
    clean_url: str

    summary: str
    faqs: List[FAQItem]
    bullet_points: List[str]

    structured_sections: StructuredSections
    json_ld: JsonLD

    keyword_density: float
    call_to_action: str