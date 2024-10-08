from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # O usuário que recebe a notificação
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='notifications')  # O post relacionado
    message = models.CharField(max_length=255)
    post_url = models.URLField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.liker.username} curtiu um post de {self.user.username}"
