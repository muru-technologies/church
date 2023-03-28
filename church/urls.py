from django.urls import path, include
from . import views

app_name = 'church'

urlpatterns = [
    
    path('', views.index, name='index'),
    
    path('about/', views.about, name='about'),
    
    path('sermons/', views.sermon_list, name='sermon_list'),
    
    path('sermon_detail/', views.sermon_detail, name='sermon_detail'),
    
    path('events/', views.event_list, name='event_list'),
    
    path('event_detail/', views.event_detail, name='event_detail'),
    
    path('contact/', views.contact, name='contact'),
    
    path('baptism/', views.baptism, name='baptism'),
    
    path('child_dedication/', views.child_dedication, name='child_dedication'),
    
    path('getting_married/', views.getting_married, name='getting_married'),
    
    path('new_member/', views.new_member, name='new_member'),
    
    path('prayer_request/', views.prayer_request, name='prayer_request'),
    
    path('testimony/', views.testimony, name='testimony'),
    
    path('careers/', views.careers, name='careers'),
    
    path('career_detail/', views.career_detail, name='career_detail'),
    
    path('men/', views.men, name='men'),
    
    path('sunday_school/', views.sunday_school, name='sunday_school'),
    
    path('women/', views.women, name='women'),
    
    path('youth/', views.youth, name='youth'),
    
    path('give/', views.give, name='give'),
    
    path('card/', views.card, name='card'),
    
    path('mpesa/', views.mpesa, name='mpesa'),
    
]