from rest_framework import serializers
from auth_.models import MainUser, Profile


class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff', 'photo')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'bio', 'location', 'user')
