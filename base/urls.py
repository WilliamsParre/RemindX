from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('add_task/', views.add_task, name='add_task'),
    path('update_task/<str:pk>/', views.update_task, name='update_task'),
    path('set_done/<str:pk>/', views.set_done, name='set_done'),
    path('set_pending/<str:pk>/', views.set_pending, name='set_pending'),
    path('delete_task/<str:pk>/', views.delete_task, name='delete_task')
]
