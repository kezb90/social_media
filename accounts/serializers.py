from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'birthday', )

    def get_age(self, obj):
        return obj.calculate_age()
