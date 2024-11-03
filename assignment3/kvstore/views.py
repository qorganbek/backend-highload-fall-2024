from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import KeyValue
from .serializers import KeyValueSerializer
from django.db import transaction


class KeyValueStoreView(APIView):
    def get(self, request, key):
        try:
            kv = KeyValue.objects.get(key=key)
            serializer = KeyValueSerializer(kv)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KeyValue.DoesNotExist:
            return Response({'error': 'Key not found'}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def post(self, request):
        serializer = KeyValueSerializer(data=request.data)
        if serializer.is_valid():
            key = serializer.validated_data['key']
            # Ensure atomicity for updates
            KeyValue.objects.update_or_create(key=key, defaults={'value': serializer.validated_data['value']})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
