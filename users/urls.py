from django.urls import path

from users.views import HostView, SignupView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/host', HostView.as_view())
]