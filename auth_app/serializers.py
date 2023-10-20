from rest_framework import serializers

from auth_app.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'surname',
            'phone',
            'nickname',
            'password',
        ]