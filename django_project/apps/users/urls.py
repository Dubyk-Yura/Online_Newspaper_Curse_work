from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('follow/<int:author_id>/', views.toggle_follow, name='toggle_follow'),
    path('profile/', views.profile_view, name='profile'),
]
