from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Sermon

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def sermon_list(request):
    sermons = Sermon.objects.filter(status='publish').order_by('-publish')
    
    p = Paginator(sermons, 4)
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return the last page
        page_obj = p.page(p.num_pages)

    return render(request, 
                  'sermons.html', 
                  {'sermons': page_obj})
    

def sermon_detail(request, year, month, day, sermon):
    sermon = get_object_or_404(Sermon, slug=sermon,
                               status='publish',
                               publish__year=year,
                               publish__month=month,
                               publish__day=day)
    return render(request, 
                  'sermon_detail.html',
                  {'sermon': sermon})
    

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
