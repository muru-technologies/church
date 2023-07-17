import os
import datetime
import hashlib
import logging
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf

from .models import Sermon, Event, ChildDedication, PrayerRequest, NewBeleiver, Testimony, Career, MpesaPayment, CardPayment
from .forms import EmailForm
# from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword

from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import requests
from requests.auth import HTTPBasicAuth
import braintree


# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

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
    

def career_list(request):
    careers = Career.objects.filter(status='publish').order_by('-publish')

    return render(request, 
                  'careers.html', 
                  {'careers ': careers })
    

def career_detail(request, year, month, day, career):
    career = get_object_or_404(Career, slug=career,
                               status='publish',
                               publish__year=year,
                               publish__month=month,
                               publish__day=day)
    return render(request, 
                  'career_detail.html',
                  {'career': career})


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

def kama(request):
    return render(request, 'kama.html')

def women(request):
    return render(request, 'women.html')

def youth(request):
    return render(request, 'youth.html')

def boys(request):
    return render(request, 'boys.html')

def girls(request):
    return render(request, 'girls.html')

def children(request):
    return render(request, 'children.html')

def praise(request):
    return render(request, 'praise.html')

def choir(request):
    return render(request, 'choir.html')


def committees(request):
    return render(request, 'committee.html')


def give(request):
    return render(request, 'coming_soon.html')
    # return render(request, 'give.html')

# def get_access_token(request):
    consumer_key = 'AteCdAQlFkkUpu4xLtNdBeHhA76yaWJJ'
    consumer_secret = 'hvKGbT7Uk713czvP'

    # url for generating mpesa token
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    # initiate http call to mpesa sandbox
    r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    # parsing the json string from safaricom
    mpesa_access_token = json.loads(r.text)

    # accessing the mpesa token
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)

def card(request):
    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        amount = request.POST.get('amount')
        
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': amount,
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        
        if result.is_success:
            braintree_id = result.transaction.id
            name = request.POST.get('name')
            phone_number = request.POST.get('phone_number')
            purpose = request.POST.get('purpose')
            amount = amount
            status = True
            
            print(nonce)
            
            payment = CardPayment(
                braintree_id = braintree_id,
                holder_name = name,
                phone_number = phone_number,
                purpose = purpose,
                amount = amount,
                status = status
            )
            
            payment.save()
            
            messages.success(request, 'You have successfully submitted your request.')
            return render(request, 'card.html')
       
        else:
            messages.error(request, 'Error Making Payment Please Try Again Later.')
            return render(request, 'card.html')
    else:   
        # generate token
        client_token = gateway.client_token.generate()
        return render(request, 'coming_soon.html') # 'card.html',
                      # {'client_token': client_token,})
    
    
# # mpesa STK PUSH
# @csrf_exempt
# def mpesa(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#         amount = request.POST.get('amount')
        
#         phone_number_1 = phone_number[1:]
        
#         str_phone_number = str(phone_number_1)
        
#         phone_number_2 = '254' + str_phone_number
        
#         print(phone_number_2)
        
        
#         if request.POST.get('purpose') == 'other':
#             purpose = request.POST.get('other-donation')
#         else:
#             purpose = request.POST.get('purpose')
        
#         access_token = MpesaAccessToken.validated_mpesa_access_token
#         api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

#         headers = {"Authorization": "Bearer %s" % access_token}

#         # request info to daraja
#         payload = {
#             "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,  # paybill or buy goods till number
#             "Password": LipanaMpesaPpassword.decode_password,  # password used to encrypt the requests sent
#             "Timestamp": LipanaMpesaPpassword.lipa_time,  # transaction timestamp
#             "TransactionType": "CustomerPayBillOnline",  # used to identify the type of transaction
#             "Amount": amount,  # the amount you intend to pay
#             "PartyA": phone_number_2,  # phone number sending the money
#             "PartyB": LipanaMpesaPpassword.Business_short_code,  # organization receiving the funds can also be
#             "PhoneNumber": phone_number_2,  # number to receive the STK pin Prompt. can be same as PartA
#             "CallBackURL": "https://2d3d154b2ad0ff.lhr.life/mpesa-callback/",  # valid secure url used to receive notifications
#             # from mpesa api. it is the endpoint to which the results will be sent by the mpesa api
#             "AccountReference": purpose,  # the name of the business
#             "TransactionDesc": "Payment for ACK St. Peter's Cathedral Voi",  # a description of the transaction
#         }

#         response = requests.post(api_url, json=payload, headers=headers)
        
#         print("this is the response")
#         print(response.text)
        
        
#         # Parse response and save payment details to database
#         print(response.status_code)
        
#         if response.status_code == 200:
#             response_data = response.json()
#             print(response_data)
            
#             if response_data['ResponseCode'] == '0':
                            
                        
#                 messages.info(request, "Check your phone and enter the pin to complete the payment")
#                 return render(request, 'mpesa.html')
                   
#             else:
#                 messages.error(request, "Transaction failed. Please try again!")
#                 return render(request, 'mpesa.html')
#         else:
#             messages.error(request, "Transaction failed. Please try again!")
#             return render(request, 'mpesa.html')
#     else:
        
#         return render(request, 'mpesa.html')
    

# # call back url
# @csrf_exempt
# def mpesa_callback(request):
    
#     print("this is the mpesa ressponse")
#     # Extract the response from the Daraja API
#     response = json.loads(request.body)
    
    
#     print(response)
    
#     result_code = response['Body']['stkCallback']['ResultCode']
#     amount = response['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
#     receipt_number = response['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
#     transaction_date = str(response['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value'])
#     transaction_date = datetime.datetime.strptime(transaction_date, '%Y%m%d%H%M%S')
#     formatted_date = transaction_date.strftime('%B %d, %Y %I:%M %p')
#     datetime_obj = datetime.datetime.strptime(formatted_date, '%B %d, %Y %I:%M %p')
#     formatted_datetime_str = datetime_obj.isoformat()
#     phone_number = response['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
        
#     # Process the response
#     if result_code == 0:
#         # Payment was successful, update the UI
#         mpesa_payment = MpesaPayment.objects.create(
#             receipt_number = receipt_number,
#             phone_number = phone_number, 
#             amount = amount,
#             date = formatted_datetime_str,
#             status = True)
        
#         mpesa_payment.save()
        
#         return render(request, 'success.html')
        
#     else:
#        return render(request, 'failed.html')
