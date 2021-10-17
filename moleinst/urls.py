from allauth.account.views import ConfirmEmailView
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from authorization.views import GithubLogin, DiscordLogin, GithubConnect, DiscordConnect
from moleinst import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('django.contrib.auth.urls')),
    re_path(r'^dj-rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(),
            name='account_confirm_email'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/discord/', DiscordLogin.as_view(), name='github_login'),
    path('dj-rest-auth/discord/connect/', DiscordConnect.as_view(), name='discord_connect'),
    path('dj-rest-auth/github/', GithubLogin.as_view(), name='github_login'),
    path('dj-rest-auth/github/connect/', GithubConnect.as_view(), name='github_connect'),
    path('api/v1/', include('authorization.urls')),
    path('api/v1/blog/', include('blog.urls')),
    path('api/v1/ccg/', include('ccg.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
