from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .services.supabase_service import fetch_users, fetch_matarlisti, fetch_stad

'''
fetch_users: Fetches all users in the users table in the database

fetch_matarlisti: "WIP" fetches all restaurants in the matarsidur table

fetch_stad: "WIP" fetches a single restaurant based on id. Takes one argument which is the id
Example: posts/<int:post_id>/
'''

# Create your views here.
def matarlisti(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def userlist(request):
    Users = fetch_users()
    return render(request, 'userlist.html', {'Users': Users})

def restaurantlist(request):
    matarlisti = fetch_matarlisti()
    return render(request, 'restaurantlist.html', {'matarlisti' : matarlisti})