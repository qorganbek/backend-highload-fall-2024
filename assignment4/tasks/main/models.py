from django.db import models
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from encrypted_model_fields.fields import EncryptedCharField

class Email(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class SecureUserInfoModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
    website = models.URLField(validators=[URLValidator()])
    encrypted_bin = EncryptedCharField(max_length=100)