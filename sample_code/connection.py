import pika

RABBITMQ_URL = "amqp://username:password@localhost:5672/%2F"

def get_connection():
    params = pika.URLParameters(RABBITMQ_URL)
    return pika.BlockingConnection(params)