from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from datetime import date
import os
from django.dispatch import receiver
from django.db.models.signals import post_save


"""
User
"""
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('メールアドレスを入力してください')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=255,
        unique=True,
    )
    registered_at = models.DateTimeField(
        verbose_name='登録日時',
        auto_now_add=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email


"""
Profile
"""
def upload_image_to(instance, filename):
    image_id = str(instance.user.id)
    return os.path.join('account', 'user_image', image_id, filename)


class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)

    username = models.CharField(
        verbose_name='ユーザー名',
        max_length=50,
        default='Anonymous user',
        blank=True,
    )

    introduction = models.CharField(
        verbose_name='自己PR',
        max_length=255,
        default='',
        null=True,
        blank=True
    )

    birth = models.DateField(
        verbose_name='生年月日',
        null=True,
        blank=True
    )

    @property
    def age(self):
        if self.birth:
            today = date.today()
            return today.year - self.birth.year - ((today.month, today.day) < (self.birth.month, self.birth.day))
        else:
            return

    image = models.ImageField(
        verbose_name='アイコン画像',
        upload_to=upload_image_to,
        default='',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
