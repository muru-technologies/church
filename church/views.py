from django.shortcuts import render

from .models import Sermon

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def sermon_list(request):
    sermons = Sermon.objects.filter(status='publish').order_by('-publish')
    return render(request, 
                  'sermons.html', 
                  {'sermons': sermons})

def sermon_detail(request):
    return render(request, 'sermon_detail.html')

def event_list(request):
    return render(request, 'events.html')

def event_detail(request):
    return render(request, 'event_detail.html')

def contact(request):
    return render(request, 'contact.html')

def baptism(request):
    return render(request, 'baptism.html')

def child_dedication(request):
    return render(request, 'child_dedication.html')

def getting_married(request):
    return render(request, 'getting_married.html')

def new_member(request):
    return render(request, 'new_member.html')

def prayer_request(request):
    return render(request, 'prayer_request.html')

def testimony(request):
    return render(request, 'testimony.html')

def careers(request):
    return render(request, 'careers.html')

def career_detail(request):
    return render(request, 'career_detail.html')

def men(request):
    return render(request, 'men.html')

def sunday_school(request):
    return render(request, 'sunday_school.html')

def women(request):
    return render(request, 'women.html')

def youth(request):
    return render(request, 'youth.html')

def give(request):
    return render(request, 'give.html')

def card(request):
    return render(request, 'card.html')

def mpesa(request):
    return render(request, 'mpesa.html')