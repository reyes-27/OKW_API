from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            # 1. You must return the result of the query
            return UserModel.objects.get(pk=user_id)
        # 2. REMOVE the parentheses () after DoesNotExist
        except UserModel.DoesNotExist: 
            return None
        