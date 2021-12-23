from django.shortcuts import render
from django.views import View


class RegistrationView(View):
    def get(self, request):
        template_name = 'authentication/register.html'
        context = {}
        return render(request, template_name, context)
