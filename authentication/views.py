from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User


class RegistrationView(View):
    def get(self, request):
        template_name = 'authentication/register.html'
        context = {}
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
