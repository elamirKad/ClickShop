from fastapi import FastAPI
from api.email import router as email_router

app = FastAPI()

app.include_router(email_router, prefix="/email", tags=["email"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
