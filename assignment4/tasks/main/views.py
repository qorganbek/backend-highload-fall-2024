from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django_otp.decorators import otp_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .forms import EmailForm
from .tasks import send_email_task
from .serializers import SecureUserInfoModelSerializer
from .permissions import IsAdminOrReadOnly
from .models import SecureUserInfoModel



def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save()
            send_email_task.delay(email.recipient, email.subject, email.body)
            messages.success(request, 'Your email is being sent in the background!')
            return redirect('send_email')
    else:
        form = EmailForm()
    return render(request, 'send_email.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


@otp_required
def protected_view(request):
    return render(request, "protected.html")



class SecureAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request, pk=None):
        if pk:
            try:
                secure_instance = SecureUserInfoModel.objects.get(pk=pk)
                serializer = SecureUserInfoModelSerializer(secure_instance)
                return Response(serializer.data)
            except SecureUserInfoModel.DoesNotExist:
                return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            secure_instances = SecureUserInfoModel.objects.all()
            serializer = SecureUserInfoModelSerializer(secure_instances, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = SecureUserInfoModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            secure_instance = SecureUserInfoModel.objects.get(pk=pk)
        except SecureUserInfoModel.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SecureUserInfoModelSerializer(secure_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            secure_instance = SecureUserInfoModel.objects.get(pk=pk)
            secure_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SecureUserInfoModel.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
