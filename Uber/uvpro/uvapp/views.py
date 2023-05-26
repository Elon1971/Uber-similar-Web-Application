from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . tokens import generate_token
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import AP
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import APISerializer
from django_filters.rest_framework import DjangoFilterBackend


# class MPN(LimitOffsetPagination):
#     default_limit = 10
#     limit_query_param = 20
#     max_limit = 50
#     offset_query_param = 'p'
#
# class List_and_Create_Data(ListCreateAPIView):
#     queryset = AP.objects.all()
#     serializer_class = APISerializer
#     pagination_class = MPN
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['name', 'email', 'password', 'number']
#
#
# class Retrieve_Update_Delete_Data(RetrieveUpdateDestroyAPIView):
#     queryset = AP.objects.all()
#     serializer_class = APISerializer
#     pagination_class = MPN
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['name', 'email', 'password', 'number']


def welcome(request):
    return render(request, 'welcome.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        number = request.POST['number']

        # myuser = User.objects.create_user(name=name, email=email, password=password)
        myuser = AP(name=name, email=email, password=password, number=number)
        myuser.first_name = name
        myuser.is_active = False
        myuser.save()

    #SENDING WELCOME MAIL

        subject = "Welcome To Uber"
        message = "Hello" + myuser.first_name
        from_email = settings.EMAIL_HOST_USER
        to = [myuser.email]
        send_mail(subject, message, from_email, to, fail_silently=True)

    #SENDING CONFIRMATION MAIL

        con = get_current_site(request)
        subjectc = "Confirm yourself to Uber"
        toc = [myuser.email]
        messagec = render_to_string('confirm_mail.html', {
                                        'name': myuser.first_name,
                                        'domain': con.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                                        'token': generate_token.make_token(myuser)
        })
        send_mail(subjectc, messagec, settings.EMAIL_HOST_USER, toc, fail_silently=True)
        myuser.save()
        return redirect('signin')
    return render(request, 'signup.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        # myuser = User.objects.get(pk=uid)
        myuser = AP(pk=uid)
    except:
        (TypeError, ValueError, OverflowError, User.DoesNotExist)
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, 'You have successfully logged in')
        return redirect('signin')
    else:
        return render(request, 'ac.html')
    

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            fn = user.first_name
            return render(request, 'home.html', {'fn': fn})
        else:
            messages.error(request, 'Bad Credentials')
            return redirect('home')
    return render(request, 'signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return render(request, 'signout.html')


def home(request):
    return render(request, 'home.html')


def drive(request):
    return render(request, 'drive.html')


def rent(request):
    return render(request, 'rent.html')