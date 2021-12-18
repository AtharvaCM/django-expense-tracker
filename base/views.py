from django.shortcuts import render

# Create your views here.


def index(request):
    template_name = 'base/base.html'
    context = {}
    return render(request, template_name, context)


def add_expense(request):
    template_name = 'base/add_expense.html'
    context = {}
    return render(request, template_name, context)
