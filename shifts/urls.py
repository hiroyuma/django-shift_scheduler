# shifts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit_shift/', views.submit_shift_requests, name='submit_shift'),
    path('view_shifts/', views.view_shift_requests, name='view_shifts'),
    path('view_myshifts/', views.view_myshift_requests, name='view_myshifts'),
]
