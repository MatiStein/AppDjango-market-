from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from users.views import  *
from users.api import *



urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path("user",UserAPIView.as_view(), name='user'),
    path('register', RegisterApi.as_view()),

]
