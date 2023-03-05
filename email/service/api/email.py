import os
import aio_pika
import asyncio
from fastapi import APIRouter, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()


async def consume(loop):
    # Create a connection to RabbitMQ
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@localhost/", loop=loop
    )

    # Create a channel
    channel = await connection.channel()

    # Declare the queue
    queue = await channel.declare_queue("my_queue")

    # Start consuming messages
    await queue.consume(message_handler)


# Define the message handler function
async def message_handler(message: aio_pika.IncomingMessage):
    async with message.process():
        payload = message.body.decode()
        subject, email_to, template, body = payload.split("|")
        await send_email_async(subject, email_to, template, body)


@router.on_event("startup")
async def startup_event():
    # Start the RabbitMQ consumer
    loop = asyncio.get_event_loop()
    await consume(loop)
    print("Started consuming messages...")


@router.on_event("shutdown")
async def shutdown_event():
    # Stop the RabbitMQ consumer
    loop = asyncio.get_event_loop()
    await loop.shutdown_asyncgens()
    print("Stopped consuming messages...")


class Envs:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME = os.getenv("MAIN_FROM_NAME")


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="./templates",
)


async def send_email_async(subject: str, email_to: str, template: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name=template)


def send_email_background(
    background_tasks: BackgroundTasks,
    subject: str,
    email_to: str,
    template: str,
    body: dict,
):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html",
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message, template_name=template)
