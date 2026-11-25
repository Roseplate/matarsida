from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from .services.supabase_service import get_users, get_matarlisti, get_stadir, upload_matarsidur_image, create_user, get_user_by_username, auth_user
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST

# Views
def default(request):
    return redirect("matarlisti")

def matarlisti(request, start=0, amount=20):
    stadir = get_stadir(start, amount)
    return render(request, 'index.html', {'stadir': stadir})

def history(request):
    return render(request, "history.html")

def profile(request):
    return render(request, "profile.html")

def upload_image(request, stad_id):
    if request.method == "POST" and 'image' in request.FILES:
        upload_matarsidur_image(stad_id, request.FILES['image'])
        return redirect('restaurantlist')
    return render(request, 'dev/upload_image.html', {'stad_id': stad_id})

def userlist(request):
    users = get_users()
    return render(request, 'dev/userlist.html', {'users': users})

def restaurantlist(request):
    matarlisti = get_matarlisti()
    return render(request, 'dev/restaurantlist.html', {'matarlisti' : matarlisti})

# Login Stuff
def register(request):
    '''
    just creates the user with a hashed password
    '''
    if request.method !="POST":
        return render(request, 'register.html')
    
    firstname = request.POST.get("firstname", "").strip()
    lastname = request.POST.get("lastname", "").strip()
    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")
    password2 = request.POST.get("password2", "")

    errors = []
    if not all ([firstname, lastname, username, password]):
        errors.append("Please fill in all fields.")
    if password != password2:
        errors.append("Passwords do not match.")
    if username and get_user_by_username(username):
        errors.append("Username is taken.")
    if password:
        try:
            validate_password(password)
        except ValidationError as e:
            errors.extend(e.messages)
    
    if errors:
        return render(request, "partials/form_message.html", {"errors": errors})

    create_user(firstname, lastname, username, password)
    return render(request, "partials/form_message.html",
            {"success": f"User '{username}' created. You can now log in."})

def login(request):
    if request.method != "POST":
        return render(request, "login.html")
    
    user = auth_user(request.POST.get('username', '').strip(),
                     request.POST.get('password', ''))

    if user is None:
        return render(request, "partials/form_message.html",
                      {"errors": ["Wrong Username or Password."]})

    request.session.cycle_key() # creates a new session id on login to prevent session fixation
    request.session['user_id'] = user['id']
    request.session['username'] = user['username']
    response = HttpResponse()
    response["HX-Redirect"] = reverse("login")
    return response

@require_POST
def logout(request):
    request.session.flush()
    return redirect('matarlisti')

# HTMX
def check_username(request):
    '''
    htmx live check is on while typing in the username field :D
    '''
    username = request.GET.get('username', "").strip()
    if not username:
        return HttpResponse("")
    if get_user_by_username(username):
        return HttpResponse('<span class="text-red-700">Username Taken</span>')
    return HttpResponse('<span class="text-green-700">Username Available</span>')

def menubutton(request):
    return render(request, 'partials/menu_button_modal.html')

def delete(request):
    return HttpResponse()

