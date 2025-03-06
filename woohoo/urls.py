from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from users import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("profile/", user_views.profile, name="profile"),
    path("register/", user_views.register, name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"),
]
