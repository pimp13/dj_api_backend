from rest_framework import serializers

from auth_app.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'user')
