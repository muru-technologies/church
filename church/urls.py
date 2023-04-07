from django.urls import path, include
from . import views

app_name = 'church'

urlpatterns = [
    # ping mailchimp
    path('ping/', views.mailchimp_ping_view, name='ping'),
    
    path('', views.index, name='index'),
    
    path('subscribe', views.subscribe_view, name='subscribe'),

    path('success/', views.subscribe_success_view, name='subscribe_success'),

    path('fail/', views.subscribe_fail_view, name='subscribe_fail'),

    path('unsubscribe/', views.unsubscribe_view, name='unsubscribe'),

    path('unsubscribe/success/', views.unsubscribe_success_view, name='unsubscribe_success'),

    path('unsubscribe/fail/', views.unsubscribe_fail_view, name='unsubscribe_fail'),
    
    path('about/', views.about, name='about'),
    
    path('child_dedication/', views.child_dedication, name='child_dedication'),
    
    path('prayer_request/', views.prayer_request, name='prayer_request'),
    
    path('contact/', views.contact, name='contact'),
    
    path('baptism/', views.baptism, name='baptism'),
       
    path('getting_married/', views.getting_married, name='getting_married'),
    
    path('new_member/', views.new_member, name='new_member'),
    
    path('testimony/', views.testimony, name='testimony'),
    
    path('kama/', views.kama, name='kama'),
    
    path('mothers-union/', views.women, name='women'),
    
    path('kayo/', views.youth, name='youth'),
    
    path('boys-brigade/', views.boys, name='boys'),
    
    path('children/', views.children, name='children'),
    
    path('girls-friendly-society/', views.girls, name='girls'),
    
    path('praise-and-adoration/', views.praise, name='praise'),
    
    path('choir/', views.choir, name='choir'),
    
    path('sermons/', views.sermon_list, name='sermon_list'),
    
    path('<int:year>/<int:month>/<int:day>/<slug:sermon>/', views.sermon_detail, name='sermon_detail'),
    
    path('events/', views.EventList.as_view(), name='event_list'),
    
    path('<slug:slug>/', views.EventDetail.as_view(), name='event_detail'),
        
    path('careers/', views.careers, name='careers'),
    
    path('career_detail/', views.career_detail, name='career_detail'),   
    
    path('give/', views.give, name='give'),
    
    path('card/', views.card, name='card'),
    
    path('mpesa/', views.mpesa, name='mpesa'),
    
]