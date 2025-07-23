"""
Application runner for Text2SQL Assistant
"""
import uvicorn
from app.utils.config import get_settings

def main():
    """Run the FastAPI application"""
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level="info" if not settings.DEBUG_MODE else "debug"
    )

if __name__ == "__main__":
    main() 