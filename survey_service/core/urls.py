from django.conf.urls import url

from . import views

urlpatterns = [
    url('admin/login/', views.LoginView.as_view()),
    url('admin/logout/', views.LogoutView.as_view()),
]
