from django.urls import path
from blog import views

urlpatterns = [
    path('post/create/', views.PostCreate.as_view()),
    path('post/update/<str:pk>/', views.PostUpdate.as_view()),
    path('post/like/', views.LikePost.as_view()),
    path('post/comment/create/', views.CommentCreate.as_view()),
    path('post/comments/<str:post>/', views.CommentList.as_view()),
    path('post/report/', views.ReportCreate.as_view()),
    path('post/<str:pk>/', views.PostRetrieve.as_view()),
    path('alerts/', views.AlertList.as_view()),
    path('alert/', views.AlertToggle.as_view()),
    path('alerts/', views.AlertList.as_view()),
    path('subscriptions/', views.PostList.as_view()),
    path('posts/<str:username>/', views.PostUserList.as_view()),
]
