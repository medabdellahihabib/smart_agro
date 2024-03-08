# apps/app_amart/urls.py
from django.urls import path
from . import views
from .views import contact_view,contact_submit_view,dashboard1,messages_view,predict_prod,CustomLogoutView,predict_crop,weather_view
from django.contrib.auth import views as auth_views
from . import views1






urlpatterns = [
    path('accueil', views.accueil, name='accueil'),
    path('services/',views.services,name='services'),
    path('about-us/', views.about_us, name='about_us'),
    
    path('accuei/', dashboard1, name='dashboard1'),
    
    path('contact/', contact_view, name='contact'),
    path('contact_submit/', contact_submit_view, name='contact_submit'),
    path('messages/', messages_view, name='messages'),
    
    path('predict1/', predict_crop, name='predict_crop'),
    
    path('accueil/', views.dashboard, name='dashboard'),
    path('', auth_views.LoginView.as_view(template_name='app_amart/login.html'), name='login'),

    
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
 
    
    
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path('register/', views.register, name='register'),
    
    path('weather/', weather_view, name='weather'),
    
    path('weather1/', views.index, name="home"),
    path("result", views.result, name="result"),
    
    
    
    
    path("prediction", views.index, name="index"),
    path("predictt/", views.predict_prod, name="predict_prod"),
    
    
    
    path('retrainer/', views1.retrainer, name='retrainer'),
    path('stoptrainer/', views1.stoptrainer, name='stoptrainer'),
    path('hom/', views1.hom, name='hom'),
    path('success/', views1.success, name='success'),
    path('camera/', views1.cam, name='cam'),
    path('video_feed/', views1.video_feed, name='video_feed'),
    path('capture/', views1.capture, name='capture'),
    path('save/', views1.save, name='save'),
    
    
    
    
]
