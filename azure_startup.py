#!/usr/bin/env python3
"""
Azure App Service startup script for FastAPI application.
This script prepares the environment and starts the ASGI server.
"""

import os
import sys
import logging
import subprocess
from pathlib import Path
import importlib.util
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Main startup routine for Azure App Service."""
    logger.info("=" * 70)
    logger.info("🚀 FastAPI Application Startup (Azure App Service)")
    logger.info("=" * 70)
    
    # Step 1: Verify environment
    logger.info("Step 1: Verifying environment...")
    
    # Check required environment variables
    required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.warning(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        logger.warning("   Please add these to Azure Portal → Configuration → Application settings")
    else:
        logger.info("✓ All required environment variables set")
    
    # Step 2: Verify MySQL dependency
    logger.info("\nStep 2: Verifying Python dependencies...")
    try:
        import pymysql
        logger.info(f"✓ pymysql {pymysql.__version__} installed")
    except ImportError:
        logger.error("✗ pymysql not installed - installing now...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyMySQL==1.1.0"], check=True)
        logger.info("✓ pymysql installed")

    # Ensure the rest of the application dependencies are available before
    # importing config.py, which depends on pydantic_settings.
    try:
        if importlib.util.find_spec("pydantic_settings") is None or importlib.util.find_spec("fastapi") is None:
            req_path = Path(__file__).with_name("requirements.txt")
            if req_path.exists():
                logger.info("Core dependencies missing — installing requirements.txt before loading config...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_path)], check=True)
                logger.info("✓ requirements installed")
            else:
                logger.warning("requirements.txt not found; cannot auto-install dependencies")
    except Exception as e:
        logger.error(f"Failed to ensure core dependencies: {e}")

    # Step 3: Platform check
    logger.info("\nStep 3: Checking runtime platform...")
    if os.path.exists("/etc/os-release"):
        logger.info("Linux system detected")
    else:
        logger.info("Windows system detected")
    
    # Step 4: Test configuration loading
    logger.info("\nStep 4: Loading configuration...")
    # Some Azure runtimes may not have installed all packages yet; ensure
    # `pydantic-settings` and `pydantic` are available before importing
    # `config.py` which depends on them.
    try:
        import pydantic_settings  # type: ignore
        import pydantic  # type: ignore
        logger.info("✓ pydantic and pydantic_settings available")
    except Exception:
        logger.warning("pydantic or pydantic_settings missing — installing minimal packages...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pydantic>=2.5.0", "pydantic-settings>=2.0.0"], check=True)
            logger.info("✓ pydantic and pydantic_settings installed")
            # Validate installation: invalidate import caches then check spec/import
            try:
                import importlib
                importlib.invalidate_caches()
                spec = importlib.util.find_spec("pydantic_settings")
                if spec is None:
                    logger.error("pydantic_settings still not found after install")
                    logger.error(f"sys.executable={sys.executable}")
                    logger.error(f"sys.path={sys.path}")
                    try:
                        out = subprocess.check_output([sys.executable, "-m", "pip", "show", "pydantic-settings"], stderr=subprocess.STDOUT, text=True)
                        logger.error("pip show pydantic-settings output:\n" + out)
                    except Exception as e:
                        logger.error(f"Failed to run 'pip show': {e}")
                else:
                    logger.info("pydantic_settings importable after install")
            except Exception as e:
                logger.error(f"Diagnostic import check failed: {e}")
        except Exception as e:
            logger.error(f"Failed to install pydantic packages: {e}")
            # Continue — the subsequent import will fail and exit with a clear message
    try:
        from config import get_settings
        settings = get_settings()
        config_summary = settings.get_db_config_summary()
        logger.info("✓ Settings loaded successfully")
        for key, value in config_summary.items():
            if key != "database":
                logger.info(f"  {key}: {value}")
    except Exception as e:
        logger.error(f"✗ Failed to load settings: {e}")
        sys.exit(1)
    
    # Step 5: Start the FastAPI application
    logger.info("\nStep 5: Starting FastAPI application...")
    logger.info("=" * 70)
    
    port = int(os.getenv("PORT", 8000))
    
    # Import and run the app
    try:
        # Ensure FastAPI is present before starting uvicorn
        try:
            import fastapi  # noqa: F401
            logger.info("✓ fastapi available")
        except Exception:
            logger.warning("fastapi not found — installing requirements.txt...")
            req_path = Path(__file__).with_name("requirements.txt")
            if req_path.exists():
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_path)], check=True)
                    import importlib
                    importlib.invalidate_caches()
                    logger.info("✓ requirements installed; validating fastapi import")
                except Exception as e:
                    logger.error(f"Failed to install requirements: {e}")
            else:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "fastapi[all]"], check=True)
                    import importlib
                    importlib.invalidate_caches()
                except Exception as e:
                    logger.error(f"Failed to install fastapi directly: {e}")

        import uvicorn
        
        logger.info(f"Starting uvicorn on port {port}")
        
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            reload=False  # Never use reload in production
        )
    except ImportError:
        logger.error("uvicorn not installed - installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn"], check=True)
        import uvicorn
        
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            reload=False
        )
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
