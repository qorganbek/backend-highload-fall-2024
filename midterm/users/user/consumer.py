import pika
import json
from user.models import Notification
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


def callback(ch, method, properties, body):
    message = json.loads(body)
    user_id = message["user_id"]
    order_id = message["order_id"]

    # Get the recipient user
    recipient = CustomUser.objects.get(id=user_id)

    # Create a notification
    notification = Notification(
        sender=None,  # Set to admin or a specific user
        recipient=recipient,
        message=f"Your order #{order_id} has been created.",
        notification_type=Notification.ORDER_UPDATE,
    )
    notification.save()
    print(f"Notification created for user {recipient.id}: {notification.message}")


def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="order_notifications", durable=True)
    channel.basic_consume(
        queue="order_notifications", on_message_callback=callback, auto_ack=True
    )

    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
