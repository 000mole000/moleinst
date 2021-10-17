from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from authorization.models import Subscribe
from authorization.permissions import IsCurrentUser
from blog.blog_serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer, CommentSerializer, \
    CommentCreateSerializer, ReportSerializer
from blog.models import Post, Like, PostFile, Comment, Report, AlertConnect
from blog.permissions import IsOwnerOfPost


class PostRetrieve(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        subscriptions = Subscribe.objects.filter(Q(subscriber=user))
        subscriptions_users = User.objects.filter(Q(subscribers__in=subscriptions))
        queryset = Post.objects.filter(Q(author__in=subscriptions_users)).order_by('-publish_date')
        return queryset


class PostUserList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(author__username=self.kwargs['username']).order_by('-publish_date')
        return queryset


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        if 'files' in self.request.data:
            files = self.request.data.pop("files")
            for file in files:
                print('file', file)
                PostFile.objects.create(file=file, post=post)


class PostUpdate(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfPost]


class LikePost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        sub = Like.objects.get_or_create(post=Post.objects.get(id=request.data['post']),
                                         user=request.user)
        if not sub[1]:
            sub[0].delete()
            return Response(False, status=status.HTTP_201_CREATED)
        else:
            return Response(True, status=status.HTTP_201_CREATED)


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(post=self.kwargs['post']).order_by('-publish_date')
        return queryset


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReportCreate(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AlertPagination(PageNumberPagination):
    page_size = 5


class AlertList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = AlertPagination

    def get_queryset(self):
        user = self.request.user
        alerts = AlertConnect.objects.filter(Q(alert_user=user))
        alerts_users = User.objects.filter(Q(alert_users__in=alerts))
        queryset = Post.objects.filter(Q(author__in=alerts_users)).order_by('-publish_date')
        return queryset


class AlertToggle(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        alert = AlertConnect.objects.get_or_create(user=User.objects.get(username=request.data['user']),
                                                   alert_user=request.user)
        if not alert[1]:
            alert[0].delete()
            return Response(False, status=status.HTTP_201_CREATED)
        else:
            return Response(True, status=status.HTTP_201_CREATED)
