from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):

    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'timestamp', 'user_username']


class PostSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    comment_count = serializers.SerializerMethodField()

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'text',
            'timestamp',
            'user_username',
            'comment_count',
            'comments',
        ]

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_comments(self, obj):

        latest_comments = obj.comments.order_by('-timestamp')[:3]
        return CommentSerializer(latest_comments, many=True).data

