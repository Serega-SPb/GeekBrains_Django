from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


def validate_image(image):
    file_size = image.file.size
    limit_kb = 500
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', default='users_avatars/default-avatar.jpg')
    age = models.PositiveIntegerField(null=True)


class UserActivation(models.Model):
    user = models.OneToOneField(ShopUser, on_delete=models.CASCADE, primary_key=True, related_name='code')
    code = models.CharField(max_length=128)
    expired_to = models.DateTimeField(default=now() + timedelta(days=2))

    def code_is_valid(self):
        return self.expired_to > now()
