# mainapp/urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import (
    select_subject, select_time, profile, tutor_indiv_final,
    find_friends_final, tutor_group_final, user_login, profile_api, final_step, user_logout,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', user_login, name='login'),
    path('select_subject/', select_subject, name='select_subject'),
    path('select_time/', select_time, name='select_time'),
    path('profile/', profile, name='profile'),
    path('find_friends_final/', find_friends_final, name='find_friends_final'),
    path('tutor_indiv_final/', tutor_indiv_final, name='tutor_indiv_final'),
    path('tutor_group_final/', tutor_group_final, name='tutor_group_final'),
    path('logout/', user_logout, name='logout'),

    path('final_step/', final_step, name='final_step'),
    path('api/profile/', profile_api, name='profile_api')
]
