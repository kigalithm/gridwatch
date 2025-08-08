import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings
from app.reg.routes import outage_routes, twitter_routes
from app.reg.routes.power_issue_routes import power_issue_route
from app.wasac.routes.water_issue_routes import water_issue_route

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


app.include_router(
    outage_routes.outage_route,
    prefix=settings.API_VERSION_STR + "/outage",
)


app.include_router(
    twitter_routes.twitter_route,
    prefix=settings.API_VERSION_STR + "/twitter",
)

# Water Issue
app.include_router(
    water_issue_route,
    prefix=settings.API_VERSION_STR + "/water-issue",
)

# Power Issue
app.include_router(
    power_issue_route,
    prefix=settings.API_VERSION_STR + "/power-issue",
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
