# LLM Text Classification Microservice

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-green)
![OpenAI](https://img.shields.io/badge/OpenAI-1.12.0-orange)
![License](https://img.shields.io/badge/license-MIT-purple)

## Features <a name="features"></a>
✔ **Multi-classification** through single API endpoint  
✔ **Production-ready** with rate limiting and health checks  
✔ **Config-driven** behavior (no code changes needed)  
✔ **Scalable** async architecture  

## Quick Start <a name="quick-start"></a>
## Setup Instructions 🚀

### Clone Repo 
https://github.com/sebabomashudu/llm-classifier.git
### Install dependencies
1. Navigate to the backend folder:
   ```bash
   cd llm-classifier
2. Install  dependencies:
   ```bash
   pip install -r requirements.txt  
3. Configure environment:
   ```bash
   cp .env.example .env  # Add your OpenAI key
4. Run service
   Access docs: http://localhost:8000/docs
   ```bash
   python -m uvicorn app.main:app --reload

### API Reference <a name="api-reference"></a>
1. **POST /classify:**
![image](https://github.com/user-attachments/assets/62760d6a-3d50-4335-be3a-a3f5394130c4)

2. **GET /health:**
   ![image](https://github.com/user-attachments/assets/c68cb337-ca06-469f-a644-ffc47cfee2e3)
   
### Loogging
Logs are written to logs/service.log with rotation:
Max size: 10MB
Keep 5 backup files

1. Sample log entry:
   ```bash
   2025-05-23 00:42:57,863 - root - INFO - Health check - Service is healthy (no requests handled yet)

### Running Tests
1. Unit and Integration Test:
   ```bash
   py -m pytest -v tests/  # Verbose mode

### CI/CD Pipeline 🚀

The repository includes a **.github/workflows/python-publish.yml**
1. Install dependancies
2. Run tests




