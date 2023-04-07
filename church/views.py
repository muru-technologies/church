import hashlib
import logging
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail

from .models import Sermon, Event, ChildDedication, PrayerRequest, NewBeleiver, Testimony
from .forms import EmailForm

from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

logger = logging.getLogger(__name__)

mailchimp = Client()
mailchimp.set_config({
    'api_key': settings.MAILCHIMP_API_KEY,
    'server': settings.MAILCHIMP_REGION,
})

# view used to check if there is successful connection between mailchimp and the app
def mailchimp_ping_view(request):
    response = mailchimp.ping.get()
    return JsonResponse(response)


def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('subscriber_email')
        try:
            form_email = email

            # member info contains the user information that will be stored in mailchimp
            member_info = {
                'email_address': form_email,
                'status': 'subscribed',
            }
            response = mailchimp.lists.add_list_member(
                settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                member_info)
            logger.info(f'API call successful: {response}')
            return redirect('church:subscribe_success')

        except ApiClientError as error:
            logger.error(f'An exception occurred: {error.text}')
            return redirect('church:subscribe_fail')


# Create your views here.
def index(request):
    return render(request, 'index.html')


def subscribe_success_view(request):
    return render(request, 'message.html', {
        'title': 'Successfully subscribed',
        'message': 'Yay, you have been successfully subscribed to our mailing list.',
        'unsubscribe-link': ''
    })


def subscribe_fail_view(request):
    return render(request, 'message.html', {
        'title': 'Failed to subscribe',
        'message': 'Oops, something went wrong.',
    })


def unsubscribe_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                form_email = form.cleaned_data['email']
                # hashing the user's email using md5 to generate a subscriber hash will allow to manipulate the
                # user's data
                form_email_hash = hashlib.md5(form_email.encode('utf-8').lower()).hexdigest()

                # member_update used to change the user data
                member_update = {
                    'status': 'unsubscribed',
                }
                response = mailchimp.lists.update_list_member(
                    settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                    form_email_hash,
                    member_update,
                )
                logger.info(f'API call successful: {response}')
                return redirect('church:unsubscribe_success')

            except ApiClientError as error:
                logger.error(f'An exception occurred: {error.text}')
                return redirect('church:unsubscribe_fail')

    return render(request, 'unsubscribe.html', {
        'form': EmailForm(),
    })


def unsubscribe_success_view(request):
    return render(request, 'message.html', {
        'title': 'Successfully unsubscribed',
        'message': 'You have been successfully unsubscribed from our mailing list.',
    })


def unsubscribe_fail_view(request):
    return render(request, 'message.html', {
        'title': 'Failed to unsubscribe',
        'message': 'Oops, something went wrong.',
    })


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
    

class EventList(ListView):
    queryset = Event.objects.filter(status='publish').order_by('-publish')
    template_name = 'events.html'
    paginate_by = 6
    

class EventDetail(DetailView):
    model = Event
    template_name = 'event_detail.html'
    
    
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        form_data = {
            'name': name,
            'email': email,
            'message': message,
        }
        message = '''
            From:\n\t\t{}\n
            Message:\n\t\t{}\n
            Email:\n\t\t{}\n
            '''.format(form_data['name'], form_data['message'], form_data['email'],)
        send_mail('You got a mail!', message, '', ['secretary@ackstpeterscathedralvoi.org'])
        messages.success(request, 'Your message has been sent successfully. We will reach out to you as soon as possible')
        return render(request, 'contact.html')

    else:
        return render(request, 'contact.html', {})


def baptism(request):
    return render(request, 'baptism.html')


def getting_married(request):
    return render(request, 'getting_married.html')


def child_dedication(request):
    if request.method == 'POST':
        child_name = request.POST.get('child_name')
        child_gender = request.POST.get('child_gender')
        child_date_of_birth = request.POST.get('child_date_of_birth')
        date_of_dedication = request.POST.get('date_of_dedication')
        mothers_name = request.POST.get('mothers_name')
        mothers_contact = request.POST.get('mothers_contact')
        fathers_name = request.POST.get('fathers_name')
        fathers_contact = request.POST.get('fathers_contact')
        created = timezone.now()
        
        dedication_request = ChildDedication(
            child_name = child_name,
            child_gender = child_gender,
            child_date_of_birth = child_date_of_birth,
            date_of_dedication = date_of_dedication,
            mothers_name = mothers_name,
            mothers_contact = mothers_contact,
            fathers_name = fathers_name,
            fathers_contact = fathers_contact,
            created = created)

        
        
        dedication_request.save()
        messages.success(request, 'You have successfully submitted your request.')
        return render(request, 'child_dedication.html', 
                    {'dedication_request': dedication_request})
        
    return render(request, 'child_dedication.html')
        

def new_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        current_church = request.POST.get('current_church')
        residential_area = request.POST.get('residential_area')
        created = timezone.now()
        
        beleiver = NewBeleiver(
            name = name,
            phone_number = phone_number,
            current_church = current_church,
            residential_area = residential_area,
            created = created
        )
        
        beleiver.save()
        messages.success(request, 'You have successfully registered in our church.')
        return render(request, 'new_member.html',
                      {'beleiver': beleiver})
    else:
        return render(request, 'new_member.html')


def prayer_request(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        title = request.POST.get('title')
        content = request.POST.get('content')
        created = timezone.now()
        
        prayer = PrayerRequest(
            name = name,
            phone_number = phone_number,
            title = title,
            content = content,
            created = created
        )
        
        prayer.save()
        messages.success(request, 'You have successfully submitted your request.')
        return render(request, 'prayer_request.html', 
                      {'prayer': prayer})
    else:
        return render(request, 'prayer_request.html')
    

def testimony(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        title = request.POST.get('title')
        content = request.POST.get('content')
        created = timezone.now()
        
        testimony = Testimony(
            name = name,
            phone_number = phone_number,
            title = title,
            content = content,
            created = created
        )
        
        testimony.save()
        messages.success(request, 'You have successfully submitted your request.')
        return render(request, 'testimony.html',
                      {'testimony':testimony})
    else:
        return render(request, 'testimony.html')

def careers(request):
    return render(request, 'careers.html')

def career_detail(request):
    return render(request, 'career_detail.html')

def kama(request):
    return render(request, 'kama.html')

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
