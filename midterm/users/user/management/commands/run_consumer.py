from django.core.management.base import BaseCommand
from user.consumer import start_consuming  # Ensure correct import path


class Command(BaseCommand):
    help = "Runs the RabbitMQ consumer for notifications"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting RabbitMQ consumer...")
        start_consuming()
