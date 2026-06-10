from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Admin username bilan, API email bilan kiradi
        try:
            # Avval username bilan qidir (admin uchun)
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                # Topilmasa email bilan qidir (API uchun)
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None