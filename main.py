from fastapi import FastAPI
from dotenv import load_dotenv

_ = load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
  return {"message": "Hello World"}

