
from django.urls import path
from django.urls import include, path
from authentication.views import *


urlpatterns = [
path('token/', LoginTokenView.as_view(), name="login-token"),
path('login/', LoginView.as_view(), name="login"),
]