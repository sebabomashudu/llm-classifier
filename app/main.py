from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv
from app.llm import OpenAIService
from app.config import ConfigLoader
import time

load_dotenv()

# Configuration
config = ConfigLoader()

# Logging Setup
os.makedirs("logs", exist_ok=True)
handler = RotatingFileHandler(
    "logs/service.log",
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
logging.basicConfig(
    level=config.get("logging.level", "INFO"),
    handlers=[handler],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    app.state.llm = OpenAIService()
    app.state.metrics = {
        "total_requests": 0,
        "avg_time": 0.0
    }

@app.post("/classify")
@limiter.limit("60/minute")
async def classify(request: Request, text: str, config_name: str = None):
    start = time.time()
    try:
        prompt_config = config.get_prompt_config(config_name)
        result = await app.state.llm.classify(
            system_prompt=prompt_config["system"],
            user_prompt=prompt_config["user_template"].format(text=text)
        )
        
        # Fixed metrics calculation with properly balanced parentheses
        proc_time = time.time() - start
        app.state.metrics["total_requests"] += 1
        app.state.metrics["avg_time"] = (
            (app.state.metrics["avg_time"] * (app.state.metrics["total_requests"] - 1) + proc_time
        ) / app.state.metrics["total_requests"]
        )
        return {
            "classification": result,
            "processing_time": f"{proc_time:.2f}s"
        }
    except ValueError as e:
        raise HTTPException(
        status_code=400,
        detail={
                "error": "Invalid configuration",
                "message": str(e),
                "available_configs": config.get_available_configs()
            }
        )    
    except RateLimitExceeded:
        logging.warning("Rate limit exceeded")
        raise HTTPException(429, "Too many requests")
    except Exception as e:
        logging.error(f"Classification failed: {str(e)}")
        raise HTTPException(500, f"Service error: {str(e)}")

@app.get("/health")
async def health_check(request: Request):
    # Get health metrics
    health_status = {
        "status": "healthy",
        "requests_handled": app.state.metrics["total_requests"],
        "avg_response_time": f"{app.state.metrics['avg_time']:.2f}s"
    }
    
    # Log different levels based on conditions
    if app.state.metrics["total_requests"] == 0:
        logging.info("Health check - Service is healthy (no requests handled yet)")
    elif app.state.metrics["avg_time"] > 1.0:
        logging.warning(
            f"Health check - High avg response time: {health_status['avg_response_time']} "
            f"(Total requests: {health_status['requests_handled']})"
        )
    else:
        logging.debug(
            f"Health check - Normal operation: {health_status['avg_response_time']} "
            f"response time ({health_status['requests_handled']} requests)"
        )
    
    return health_status