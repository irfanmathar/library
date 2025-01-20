from django.urls import path
from .views import *
urlpatterns=[
    path('',loginpage),
    path('signup/',signup),
    path('logout/',logoutpage)
]