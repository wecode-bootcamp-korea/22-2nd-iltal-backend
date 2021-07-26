from django.urls import path

from users.views import HostView, SignupView, SigninView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/signin', SigninView.as_view()),
    path('/host',   HostView.as_view())
]