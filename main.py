import os
from dotenv import load_dotenv 
import logging
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Agent import Agent
from Database.database_connection import Database
import time


#logging
LOG_FILE = "app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE), 
        logging.StreamHandler() 
    ]
)
logger = logging.getLogger(__name__)

#load env 
load_dotenv() 
DATABASE_URL = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_instance = Database(DATABASE_URL)
agent = Agent(database_url=DATABASE_URL, gemini_api_key=GEMINI_API_KEY)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    process_time = time.time() - start_time
    return response

class QueryRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        logger.info(f"Question: {request.question}")
        answer = agent.response(request.question)
        logger.info(f"Answer: {answer[:100]}...")  
        return {"response": answer}
    except Exception as e:
        logger.error(f"Error", exc_info=True)
        return {"error": "Connection loss"}
