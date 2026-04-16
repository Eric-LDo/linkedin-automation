from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="LinkedIn Automation API",
    version="1.0.0",
    description="API for automating LinkedIn tasks such as sending connection requests and messages.",
)
app.include_router(router)