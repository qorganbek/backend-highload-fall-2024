from django.db import models

class FileUpload(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=20, default='Pending')  # Pending, Processing, Completed, Failed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)