from decimal import Context
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth

from validate_email import validate_email
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from expensetracker.settings import EMAIL_HOST_USER

from .utils import token_generator


class RegistrationView(View):
    def get(self, request):
        template_name = 'authentication/register.html'
        context = {}

        return render(request, template_name, context)

    def post(self, request):
        template_name = 'authentication/register.html'
        # Get user data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }
        # Validate
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password is too short')
                    return render(request, template_name, context)
                # Create user account
                user = User.objects.create_user(username=username,
                                                email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = 'http://'+domain+link

                email_subject = 'Activate your account'
                email_body = 'Hi '+user.username + \
                    '. Please use this link to verify your account\n'+activate_url
                email_from = EMAIL_HOST_USER
                email_to = [email]

                email = EmailMessage(
                    email_subject,
                    email_body,
                    email_from,
                    email_to,
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')
        return render(request, template_name, context)


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            msg = 'Username should only contain alphanumeric characters!'
            return JsonResponse({'username_error': msg}, status=400)

        if User.objects.filter(username=username).exists():
            msg = 'Username already exists, choose another one!'
            return JsonResponse({'username_error': msg}, status=409)

        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email, check_mx=True):
            msg = 'Invalid Email!'
            return JsonResponse({'email_error': msg}, status=400)

        if User.objects.filter(email=email).exists():
            msg = 'An account with this Email already exists, choose another one!'
            return JsonResponse({'email_error': msg}, status=409)

        return JsonResponse({'email_valid': True})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                messages.success(request, 'Account is already activated')
                return redirect('login')

            if user.is_active:
                messages.success(request, 'Account is already activated')
                return redirect('login')

            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')
        except Exception as e:
            pass

        return redirect('login')


class LoginView(View):
    template_name = 'authentication/login.html'

    def get(self, request):
        context = {}

        return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        context = {}

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome ' +
                                     user.username+' You are now logged in.')
                    return redirect('index')

                messages.error(
                    request, 'Account is not active, please check your email!')
                return render(request, self.template_name, context)

            messages.error(
                request, 'Invalid credentials, try again!')
            return render(request, self.template_name, context)

        messages.error(
            request, 'Please fill all the fields!')
        return render(request, self.template_name, context)
