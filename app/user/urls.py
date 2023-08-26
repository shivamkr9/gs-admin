"""
URL mappings for the user API.
"""
from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("", views.GetUserView.as_view(), name="get-user"),
    path("create/", views.CreateUserView.as_view(), name="create-user"),
    path("update", views.UpdateUserView.as_view(), name="update-user"),
    path("login/", views.CustomTokenObtainPairView.as_view(), name="login-user"),
    path("token/refresh/", views.CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", views.CustomTokenVerifyView.as_view(), name="token_verify"),
    path("logout/", views.LogoutView.as_view(), name="logout"),


]

