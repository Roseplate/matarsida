from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .services.supabase_service import fetch_users

# Create your views here.
def default(request):
    template = loader.get_template("index.html")
    return redirect("matarlisti")

def matarlisti(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def UserList(request):
    Users = fetch_users()
    return render(request, 'userlist.html', {'Users': Users})