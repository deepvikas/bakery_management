from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import SignupView, LoginView, LogoutView, ShowUsersView, DeleteUserView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup-view'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),
    path('show/users/', ShowUsersView.as_view(), name='show-users-view'),
    path('delete/user/', DeleteUserView.as_view(), name='delete-users-view'),
]
