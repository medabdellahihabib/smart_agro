# apps/app_amart/urls.py
from django.urls import path
from . import views
from .views import contact_view,contact_submit_view,dashboard1,predict_prod,CustomLogoutView,predict_crop,weather_view
from django.contrib.auth import views as auth_views







urlpatterns = [
    path('accueil', views.accueil, name='accueil'),
    path('services/',views.services,name='services'),
    path('about-us/', views.about_us, name='about_us'),
    
    path('accuei/', dashboard1, name='dashboard1'),
    
    
    
    path('contact/', contact_view, name='contact'),
    path('contact_submit/', contact_submit_view, name='contact_submit'),
    
    
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
    
    
    
    
    path("prediction", views.inde, name="index"),
    path("predict/", views.predict_prod, name="predict_prod"),
   
    
    
    path('contact1/', views.contact_vie, name='contact1'),
    
    
    
    path('retrainer/', views.retrainer, name='retrainer'),
    path('stoptrainer/', views.stoptrainer, name='stoptrainer'),
    path('hom/', views.hom, name='hom'),
    path('success/', views.success, name='success'),
    path('camera/', views.cam, name='cam'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('capture/', views.capture, name='capture'),
    path('save/', views.save, name='save'),
]

    
    
    
    
    

