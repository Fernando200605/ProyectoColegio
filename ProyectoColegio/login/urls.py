from django.urls import path
from login.views import *

app_name = 'login'
urlpatterns = [
    path ('login/', LoginFormView.as_view(), name='login'),   
    path('logout/', LogoutFormView.as_view(), name='logout'),
]