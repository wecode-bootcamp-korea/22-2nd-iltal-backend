from django.urls import path

from users.views import HostView

urlpatterns = [
    path('/host/<int:user_id>', HostView.as_view())
]
