# apps/app_amart/urls.py
from django.urls import path
from . import views
from .views import contact_view,contact_submit_view,messages_view

urlpatterns = [
    path('accueil/', views.accueil, name='accueil'),
    path('services/',views.services,name='services'),
    path('about-us/', views.about_us, name='about_us'),
    
    path('contact/', contact_view, name='contact'),
    path('contact_submit/', contact_submit_view, name='contact_submit'),
    path('messages/', messages_view, name='messages'),
    
]
