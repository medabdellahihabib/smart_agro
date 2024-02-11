# apps/app_amart/urls.py
from django.urls import path
from . import views
from .views import contact_view,contact_submit_view,messages_view,CustomLogoutView,predict_crop,weather_view
from django.contrib.auth import views as auth_views







urlpatterns = [
    path('accueil', views.accueil, name='accueil'),
    path('services/',views.services,name='services'),
    path('about-us/', views.about_us, name='about_us'),
    
    path('contact/', contact_view, name='contact'),
    path('contact_submit/', contact_submit_view, name='contact_submit'),
    path('messages/', messages_view, name='messages'),
    
    path('predict/', predict_crop, name='predict_crop'),
    
    path('accueil/', views.dashboard, name='dashboard'),
    path('', auth_views.LoginView.as_view(template_name='app_amart/login.html'), name='login'),

    
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path('register/', views.register, name='register'),
    
    path('weather/', weather_view, name='weather'),
    
    path('weather1/', views.index, name="home"),
    path("result", views.result, name="result"),
    
    
    
]
