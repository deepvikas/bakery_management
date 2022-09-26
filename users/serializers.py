from rest_framework import serializers
from .models import BakeryUser


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BakeryUser
        fields = ('username', 'password', 'user_type')

        # def create(self, validated_data):
            # password = validated_data.pop('password')
            # user = super().create(validated_data)
            # user.set_password(password)
            # user.save()
            # return user