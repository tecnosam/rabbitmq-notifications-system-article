# Scalable Notification Service with RabbitMQ
This project demonstrates a production-ready notification pipeline using RabbitMQ. It includes:

Dockerized RabbitMQ with management UI and pre-configured exchanges, queues, and permissions

Sample producer and consumer code in Python

Retry handling and dead-letter queue (DLQ) logic

## Requirements
- Docker & Docker Compose
- Python 3.12
- pip or a virtual environment

## Getting Started

### 1. Start the RabbitMQ Broker

```bash
docker-compose up -d
```
This will:
- Start RabbitMQ with the management UI on http://localhost:15672
- Load all queues, exchanges, and user permissions via broker/definitions.json

Default Credentials:

```
Username: username
Password: password
```

### 2. Install Python Dependencies

From the project root:

```bash
pip install -r sample_code/requirements.txt
```

### 3. Run the Sample Producer
This sends a test email notification to RabbitMQ.

```bash
python sample_code/producer.py
```

After publishing, you can confirm the message landed in the queue from the RabbitMQ dashboard.

### 4. Run the Consumer

This script listens to the email-queue and processes messages with retry and DLQ handling.

```bash
python sample_code/consumer.py
```

You’ll see logs for every message processed, retried, or dead-lettered.

## Notes

- Retry queue uses TTL and dead-letter routing to implement delayed retries.
- DLQ captures permanently failed messages after max retry attempts.
- Messages are acknowledged manually to ensure reliability.