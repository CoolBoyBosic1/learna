from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('find_friends/', views.find_friends, name='find_friends'),
    path('find_tutor_indiv/', views.find_tutor_indiv, name='find_tutor_indiv'),
    path('find_tutor_group/', views.find_tutor_group, name='find_tutor_group'),
    path('become_tutor/', views.become_tutor, name='become_tutor'),
]
