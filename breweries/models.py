from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brewery_id = models.UUIDField()
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Review by {self.user.username} - {self.rating} stars'
