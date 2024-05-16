from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, identificacion=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(identificacion=identificacion)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, _id):
        try:            
            return CustomUser.objects.get(_id=_id)
        except CustomUser.DoesNotExist:
            return None