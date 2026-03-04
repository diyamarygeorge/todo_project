from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('toggle/<int:note_id>/', views.toggle_note, name='toggle'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
