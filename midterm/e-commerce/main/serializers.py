from rest_framework import serializers

from .producer import RabbitMQProducer
from .constant import ORDER_UPDATE
from .models import Category, Product, Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']  # Make certain fields read-only


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Nested serializer to show product details

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'product', 'quantity', 'order_date', 'status']
        read_only_fields = ['id', 'order_date']  # Make certain fields read-only

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        self.send_order_notification(order.user_id, order.id)
        return order

    def send_order_notification(self, user_id, order_id):
        producer = RabbitMQProducer()
        message = {
            'user_id': user_id,
            'order_id': order_id,
            'notification_type': ORDER_UPDATE,
            'message': f'Your order #{order_id} has been created.',
        }
        producer.send_message(message)
        producer.close()

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
