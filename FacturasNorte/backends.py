__author__ = 'Julian'
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, check_password

class Emailbackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        try:
            usuario = User.objects.get(email=username)
            if usuario.check_password(password):
                return usuario
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
