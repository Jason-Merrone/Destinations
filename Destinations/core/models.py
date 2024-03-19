from django.db import models
import uuid

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

class Session(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, default=uuid.uuid4)

class Destination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destinations')
    name = models.CharField(max_length=255)
    review = models.TextField()
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    share_publicly = models.BooleanField(default=False)

    def __str__(self):
        return self.name