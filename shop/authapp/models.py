from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .storage import OverwriteStorage

def get_default_expired_date():
    return now() + timedelta(days=2)


def validate_image(image):
    file_size = image.file.size
    limit_kb = 500
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars',
                               default='users_avatars/default-avatar.jpg',
                               storage=OverwriteStorage(),
                               validators=[validate_image])
    age = models.PositiveIntegerField(null=True)


class UserActivation(models.Model):
    user = models.OneToOneField(ShopUser, on_delete=models.CASCADE, primary_key=True, related_name='code')
    code = models.CharField(max_length=128)
    expired_to = models.DateTimeField(default=get_default_expired_date)

    def code_is_valid(self):
        return self.expired_to > now()


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(ShopUser, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    tags_line = models.CharField(max_length=128, blank=True)
    aboutMe = models.TextField(max_length=512, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

