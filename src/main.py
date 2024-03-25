from fastapi import FastAPI
# from .cron import run_cron
from .bot import run_bot

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await run_bot()
    #await run_cron()


@app.get("/")
async def main_page():
    return {"result": "true"}
