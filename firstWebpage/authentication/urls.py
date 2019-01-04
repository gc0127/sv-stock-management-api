from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .api import LoginView, LogoutView, ChangePasswordView

urlpatterns = [
    url(r'^login/$', csrf_exempt(LoginView.as_view())),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^changePassword/$', ChangePasswordView.as_view())
]