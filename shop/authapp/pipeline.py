from urllib import request

from django.core.files import File
from django.utils.six import BytesIO
from social_core.exceptions import AuthForbidden

from authapp.models import *


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        keys = response.keys()
        if 'gender' in keys:
            if response['gender'] == 'male':
                user.profile.gender = ShopUserProfile.MALE
            else:
                user.profile.gender = ShopUserProfile.FEMALE
        if 'tagline' in keys:
            user.profile.tags_line = response['tagline']
        if 'aboutMe' in keys:
            user.profile.tags_line = response['aboutMe']
        if 'ageRange' in keys:
            min_age = response['ageRange']['min']
            if int(min_age) < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
        # else:
        #     raise AuthForbidden('social_core.backends.google.GoogleOAuth2')

        if 'picture' in keys:
            img = request.urlopen(response['picture'])
            io = BytesIO(img.read())
            user.avatar.save(f'{user.username}_avatar.jpg', File(io))
        user.save()



