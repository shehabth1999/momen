from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from accounts.models import BaseUser
from django.utils.translation import gettext_lazy as _

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = BaseUser
        fields = ['id', 'username', 'email', 'token', 'password', 'is_superuser','amount']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['token'] = self.get_token(instance)
        return ret
