from rest_framework import serializers

from authorization.auth_seriallizers import UserSerializer
from blog.models import Post, PostFile, Like, Comment, Report


class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFile
        fields = ['id', 'file', 'type']


class PostSerializer(serializers.ModelSerializer):
    files = PostFileSerializer(many=True)
    author = UserSerializer()
    likes_count = serializers.IntegerField(source='likes.all.count')
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'files', 'publish_date', 'liked', 'likes_count']

    def get_liked(self, obj):
        return Like.objects.filter(post=obj, user=self.context['request'].user).exists()


class PostAlertSerializer(serializers.ModelSerializer):
    files = PostFileSerializer(many=True)
    author = UserSerializer()
    likes_count = serializers.IntegerField(source='likes.all.count')

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'files', 'publish_date', 'likes_count']


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['author', 'text']


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text', 'publish_date']


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'post', 'text']


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['id', 'type', 'text', 'post']
