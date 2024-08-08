from django.urls import path

from .views import SignUpView, LoginView

app_name = 'myauth'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
]
