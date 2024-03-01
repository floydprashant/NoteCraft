from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    pass


class Chapter(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="UserChapters"
    )
    OCRText = models.TextField()
    title = models.CharField(max_length=200)
    summary = models.TextField()
    notes = models.JSONField(default=list)
    flashcards = models.JSONField(default=dict)
    mcqs = models.JSONField(default=dict)
    tofs = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
