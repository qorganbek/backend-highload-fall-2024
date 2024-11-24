import pika
import json


class RabbitMQProducer:
    def __init__(self, queue_name="order_notifications"):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def send_message(self, message):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            ),
        )
        print(f"Sent message: {message}")

    def close(self):
        self.connection.close()
