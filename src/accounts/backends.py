from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomBackend(ModelBackend):
    def authenticate(self, request, login=None, password=None, **kwargs):
        if login is None or password is None:
            return
        try:
            user = User.objects.get(email=login)
        except User.DoesNotExist:
            try:
                user = User.objects.get(phone=login)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None


