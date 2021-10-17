from django.urls import path
from ccg import views

urlpatterns = [
    path('room/create/', views.RoomCreate.as_view()),
    path('room/connect/', views.ConnectRoom.as_view()),
    path('room/delete/<str:name>/', views.RoomDestroy.as_view()),
    path('room/<str:name>/', views.RoomRetrieve.as_view()),
    path('player/<int:User_id>/', views.PlayerRetrieve.as_view()),
]