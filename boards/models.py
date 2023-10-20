from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.
class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(User, related_name='like_boards')
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField()

    def update_counter(self):
        self.view_count += 1
        self.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)