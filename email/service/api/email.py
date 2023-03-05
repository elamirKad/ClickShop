from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


router = APIRouter()


class Email(BaseModel):
    email: str
    subject: str
    message: str


@router.post("/email")
async def send_email(email: Email):
    return {"message": "Email sent successfully"}
