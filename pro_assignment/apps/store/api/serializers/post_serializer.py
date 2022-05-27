from rest_framework import serializers
from pro_assignment.apps.store.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Post serializer"""
    class Meta:
        model = Post
        fields = '__all__'
