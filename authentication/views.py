from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from validate_email import validate_email
from django.core.mail import EmailMessage

from expensetracker.settings import EMAIL_HOST_USER


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

                email_subject = 'Activate your account'
                email_body = 'body'
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
            else:
                messages.error(request, 'Email already exists')
        else:
            messages.error(request, 'Username already exists')
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
