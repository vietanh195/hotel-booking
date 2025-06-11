from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.user_profile, name='user_profile'),
    path('admin/', views.admin_dashboard, name='admin_dashboard')
]