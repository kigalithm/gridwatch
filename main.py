import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.core.settings import Settings


settings = Settings()


app = FastAPI(
    title="Rwanda GridWatch API",
    description="Monitor power outages in Rwanda using REG Twitter data",
    version="1.0.0",
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
