from django.urls import path
from . import views

urlpatterns = [
    path('wallet_authorization', views.wallet_authorization, name='wallet_authorization'),
    path('token', views.token, name='token'),
]