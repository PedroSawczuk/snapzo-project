import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUIDField
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(verbose_name='Conteúdo')

    class Status(models.TextChoices):
        PUBLIC = 'Público', 'Público'
        ARCHIVED = 'Arquivado', 'Arquivado'

    is_published = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PUBLIC,
        verbose_name='Status'
    )
    
    view_count = models.PositiveIntegerField(default=0, verbose_name='Visualizações')  
    like_count = models.PositiveIntegerField(default=0, verbose_name='Curtidas')      

    def post_image_path(instance, filename):
        return f'posts_images/{instance.user.username}/{slugify(filename)}'
    
    image = models.ImageField(upload_to=post_image_path, blank=True, null=True, verbose_name='Imagem')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'Post de {self.user.username}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'post')  

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"