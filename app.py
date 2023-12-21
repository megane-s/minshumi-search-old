
from fastapi import FastAPI
import uvicorn
import search_art.router

app = FastAPI()

app.include_router(search_art.router.router)

if __name__ == "__main__":
  uvicorn.run(app, host="localhost", port=8000, log_level="debug")
