from django.contrib import admin
from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.main, name='main'),
    path('index/', views.index, name='index'),
    path('candidate/', views.candidate, name='candidate'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit_candidate_registration/', views.submit_candidate_registration, name='submit_candidate_registration'),
    path('view_candidates/', views.view_candidates, name='view_candidates'),
    path('delete_candidate/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
    path('submit_company_registration/', views.submit_company_registration, name='submit_company_registration'),
    path('view_companies/', views.view_companies, name='view_companies'),
    path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),
    path('update-candidate-status/<int:candidate_id>/', views.update_candidate_status, name='update_candidate_status'),
]
