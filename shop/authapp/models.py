from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser


def validate_image(image):
    file_size = image.file.size
    limit_kb = 500
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', default='users_avatars/default-avatar.jpg')
    age = models.PositiveIntegerField()
