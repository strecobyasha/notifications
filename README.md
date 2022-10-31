# Notifications

This is a small ready to deploy notifications service, based on RabbitMQ. Now it uses scheduler to create messages, but could be extended for other sources, such as admin panel or api.

### Tools

RabbitMQ for messages queues. \
Celery for scheduling messages. \
Docker for fast deployment.

### How to run the service

```bash 
make build
```
