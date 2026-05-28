"""
Azure App Service wrapper for FastAPI application.
This file helps Azure properly recognize and run the FastAPI app.
"""

import os
import sys
import logging
import subprocess
from pathlib import Path

import importlib.util

# Configure logging for Azure
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def ensure_dependencies() -> None:
    """Install project dependencies when the runtime is missing them."""
    if importlib.util.find_spec("fastapi") is not None:
        return

    requirements_path = Path(__file__).with_name("requirements.txt")
    if not requirements_path.exists():
        raise ImportError("fastapi is missing and requirements.txt was not found")

    logger.warning("FastAPI is missing from the runtime; installing requirements.txt...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
        check=True,
    )


ensure_dependencies()

# Import the FastAPI app
try:
    from main import app
    logger.info("✓ FastAPI app imported successfully")
except ImportError as e:
    logger.error(f"✗ Failed to import FastAPI app: {e}")
    sys.exit(1)

# For Azure App Service, expose the app for ASGI server
# This is used by Azure when running: python -m uvicorn app:app

if __name__ == "__main__":
    # Run with uvicorn (this is for local testing)
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting FastAPI server on port {port}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
