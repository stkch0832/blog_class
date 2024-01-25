from django.db import models
from django.contrib.auth import get_user_model
import os

User = get_user_model()

def upload_pict_to(instance, filename):
    post_id = str(instance.author.id)
    return os.path.join('blog', 'upload_pict', post_id, filename)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name='タイトル',
        max_length=30
    )
    content = models.TextField(
        verbose_name='本文',
        max_length=500
    )
    image = models.ImageField(
        verbose_name='画像',
        upload_to=upload_pict_to,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        verbose_name='作成日時',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='更新日時',
        auto_now=True,
    )

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.title
