from django.urls import path
from . import views

urlpatterns = [
    # Home URL
    path('', views.home, name='home'),

    # LogIn and SignUp URLs
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),

    # Task URLs
    path('add_task/', views.add_task, name='add_task'),
    path('update_task/<str:pk>/', views.update_task, name='update_task'),
    path('delete_task/<str:pk>/', views.delete_task, name='delete_task'),

    # Profile URLs
    path('profile/', views.user_profile, name='profile'),
    path('add_profile/', views.add_profile, name='add_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),

    # Status Setting URLs
    path('set_done/<str:pk>/', views.set_done, name='set_done'),
    path('set_pending/<str:pk>/', views.set_pending, name='set_pending'),

    # Password URL
    path('change_password/', views.change_password, name='change_password'),


    # Delete History URL
    path('delete_history', views.delete_history, name='delete_history'),

    # Delete Account URL
    path('delete_account/', views.delete_account, name='delete_account')
]
