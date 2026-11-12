from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .services.supabase_service import fetch_users

# Create your views here.
def matarlisti(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def UserList(request):
    Users = fetch_users()
    return render(request, 'test.html', {'Users': Users})