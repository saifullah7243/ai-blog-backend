"""
Production entry point for Railway deployment.
This exposes the FastAPI app instance for Uvicorn.
"""

from src.blog_agent.api import app

# Optional: allow running locally via `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
