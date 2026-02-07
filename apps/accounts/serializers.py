from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Customer, CustomUser
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # AuthUser = TypeVar('AuthUser', get_user_model(), TokenUser)
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        # token["user_membership"] = user.customer.membership.model.level
        return token

class ShortCustomerSerializer(serializers.ModelSerializer):
    def get_full_name(self, obj):
        return obj.full_name
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = [
            "id",
            "profile_pic",
            "full_name",
            "reputation",
            "is_seller",
        ]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = [
            'id',
            'username',
            'email',
            'password'
        ]

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = authenticate(
                request=self.context['request'],
                username=email, 
                password=password
                  )
            if not user:
                msg = ('No se pudo iniciar con estas credenciales')
                raise serializers.ValidationError(msg, code="authorization")
            data['user'] = user
            return data
        else:
            msg = ('Debes incluir tus credenciales')
            raise serializers.ValidationError(msg, code='authorization')
    
