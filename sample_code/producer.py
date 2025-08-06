import json
from models import EmailPayload, Metadata, NotificationMessage, Recipient
from connection import get_connection
from pydantic import BaseModel
import pika

EXCHANGE_NAME = "notifications-exchange"

def publish_notification(route: str, schema: str, payload_model: BaseModel, metadata: Metadata):
    connection = get_connection()
    channel = connection.channel()

    message = NotificationMessage(
        messageRoute=route,
        schema=schema,
        payload=payload_model.dict(),
        metadata=metadata
    )

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=route,
        body=message.json(),
        properties=pika.BasicProperties(
            delivery_mode=2  # Mark as persistent (survives broker restarts)
        )
    )

    print(f"[Producer] Published message to '{route}' queue: {message.id}")
    connection.close()


if __name__ == "__main__":
    payload = EmailPayload(
        recipient=Recipient(address="user@example.com", name="Jane Doe"),
        subject="Welcome to Our Service",
        body="Hi Jane, thanks for signing up!",
        templateId="welcome_email_v1",
        data={"firstName": "Jane", "signupDate": "2025-07-27"}
    )

    metadata = Metadata(sourceService="user-signup-service")
    publish_notification("email", "EmailPayloadV1", payload, metadata)
