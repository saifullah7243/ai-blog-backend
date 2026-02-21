import re
import json
from typing import Dict
from agents import function_tool


# ✅ Keyword Density Tool
@function_tool
def calculate_keyword_density(content: str, keyword: str) -> Dict:
    words = re.findall(r"\w+", content.lower())
    total_words = len(words)
    keyword_count = content.lower().count(keyword.lower())
    density = (keyword_count / total_words) * 100 if total_words > 0 else 0

    return {
        "total_words": total_words,
        "keyword_count": keyword_count,
        "keyword_density": round(density, 2)
    }


# ✅ Word Count Validator
@function_tool
def validate_word_count(content: str, target_word_count: int) -> Dict:
    words = re.findall(r"\w+", content)
    total_words = len(words)

    return {
        "total_words": total_words,
        "target_word_count": target_word_count,
        "meets_requirement": total_words >= target_word_count
    }


# ✅ Slug Generator
@function_tool
def generate_slug(title: str) -> Dict:
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"\s+", "-", slug)
    return {"slug": slug}


# ✅ JSON-LD Generator
@function_tool
def generate_json_ld(title: str, description: str, url: str) -> Dict:
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "mainEntityOfPage": url,
        "author": {
            "@type": "Organization",
            "name": "AI Blog Generator"
        }
    }
    return schema