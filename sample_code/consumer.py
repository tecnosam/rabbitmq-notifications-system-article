
from models import EmailPayload, NotificationMessage
from connection import get_connection


def email_callback(ch, method, properties, body):
    try:
        message = NotificationMessage.model_validate_json(body)
        payload = EmailPayload(**message.payload)

        print(f"[EmailService] Sending email to {payload.recipient.address}")
        success = True  # Replace with actual email API logic

        if success:
            # after processing, we acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"[Consumer] Processed message {message.id}")
        else:
            # If something went wrong, we send a "not-acknowledged" signal to RabbitMQ
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            print(f"[Consumer] Failed message {message.id}, requeued: False")

    except Exception as e:
        print(f"[Consumer] Error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


if __name__ == "__main__":

    QUEUE_NAME = "email-queue"
    PREFETCH_COUNT = 50  # prefetch limit of 50 messages

    connection = get_connection()
    channel = connection.channel()
    channel.basic_qos(prefetch_count=PREFETCH_COUNT)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=email_callback,
        auto_ack=False
    )

    print("[Consumer] Listening on email-queue")
    channel.start_consuming()
