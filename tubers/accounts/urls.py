from django.urls import path
from . import views

urlpatterns = [
   
   path('login',views.login,name="login"),
   path('register',views.register,name="register"),
   path('logouts',views.logouts,name="logouts"),
   path('dashboard',views.dashboard,name="dashboard"),
]