from dj_rest_auth.social_serializers import TwitterLoginSerializer
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from authorization.auth_seriallizers import UserSerializer

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.discord.views import DiscordOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView

from authorization.models import Subscribe
from authorization.permissions import IsCurrentUser


class DiscordLogin(SocialLoginView):
    adapter_class = DiscordOAuth2Adapter
    callback_url = 'http://localhost:8080/social/discord'
    client_class = OAuth2Client


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = 'http://localhost:8080/social/github/'
    client_class = OAuth2Client


class GithubConnect(SocialConnectView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = 'http://localhost:8080/social/github/'
    client_class = OAuth2Client


class DiscordConnect(SocialConnectView):
    adapter_class = DiscordOAuth2Adapter
    callback_url = 'http://localhost:8080/social/discord'
    client_class = OAuth2Client


class CurrentUserRetrieve(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class SubscriptionsPagination(PageNumberPagination):
    page_size = 1


class SubscriptionsList(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = SubscriptionsPagination

    def get_queryset(self):
        subscriptions = Subscribe.objects.filter(Q(subscriber=self.request.user))
        queryset = User.objects.filter(Q(subscribers__in=subscriptions))
        return queryset


# class UpdateUserRetrieve(generics.UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated, IsCurrentUser]
#     lookup_field = 'username'


class SubscribeToggle(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        sub = Subscribe.objects.get_or_create(user=User.objects.get(username=request.data['user']),
                                              subscriber=request.user)
        if not sub[1]:
            sub[0].delete()
            return Response(False, status=status.HTTP_201_CREATED)
        else:
            return Response(True, status=status.HTTP_201_CREATED)

#
# class SubscribeCreate(generics.CreateAPIView):
#     queryset = Subscribe.objects.all()
#     serializer_class = SubscribeCreateSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def create(self, request, *args, **kwargs):
#         request.data._mutable = True
#         request.data['subscriber'] = request.user.id
#         request.data._mutable = False
#
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
