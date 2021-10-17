from django.urls import path
from authorization import views

urlpatterns = [
    path('user/me/', views.CurrentUserRetrieve.as_view()),
    path('user/<str:username>/', views.UserRetrieve.as_view()),
    # path('user/update/<str:username>/', views.UpdateUserRetrieve.as_view()),
    path('subscribe/', views.SubscribeToggle.as_view()),
    path('subscriptions/', views.SubscriptionsList.as_view()),
]
