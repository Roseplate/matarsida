from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .services.supabase_service import fetch_users, fetch_matarlisti, fetch_stadir, upload_matarsidur_image

'''
fetch_users: Fetches all users in the users table in the database

fetch_matarlisti: "WIP" fetches all restaurants in the matarsidur table

fetch_stad: "WIP" fetches a single restaurant based on id. Takes one argument which is the id
Example: posts/<int:post_id>/
'''

def upload_image(request, stad_id):
    if request.method == "POST" and 'image' in request.FILES:
        upload_matarsidur_image(stad_id, request.FILES['image'])
        return redirect('restaurantlist')
    return render(request, 'upload_image.html', {'stad_id': stad_id})

def profile(request):
    return render(request, "profile.html")

# Create your views here.
def default(request):
    return redirect("matarlisti")

def matarlisti(request, start=0, amount=20):
    stadir = fetch_stadir(start, amount)
    return render(request, 'index.html', {'stadir': stadir})

def userlist(request):
    users = fetch_users()
    return render(request, 'userlist.html', {'users': users})

def restaurantlist(request):
    matarlisti = fetch_matarlisti()
    return render(request, 'restaurantlist.html', {'matarlisti' : matarlisti})

def friends(request):
    friends = fetch_users()
    return render(request, "friends.html", {'friends': friends})