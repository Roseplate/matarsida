from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from .services.supabase_service import fetch_users, fetch_matarlisti, fetch_stadir, upload_matarsidur_image, create_user, get_user_by_username, auth_user, get_user_by_id, get_user_by_telnum, update_user, check_user_password, update_password, get_user_by_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
import re
from django.core.validators import validate_email


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
'''
# Login / Register
'''
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
    bio = request.POST.get("bio", "").strip()
    phone = request.POST.get("phone", "").strip() or None
    email = request.POST.get("email", "").strip() or None

    errors = []
    if not all ([firstname, lastname, username, password]):
        errors.append("Please fill in all fields.")
    if password != password2:
        errors.append("Passwords do not match.")
    if username and get_user_by_username(username):
        errors.append("Username is taken.")
    if phone:
        if not re.fullmatch(r"\d{3}-\d{4}", phone):
            errors.append("Phone number must look like 123-4567.")
        elif get_user_by_telnum(phone):
            errors.append("Phone number is taken.")
    if email:
        try:
            validate_email(email)
        except ValidationError:
            errors.append("Enter a valid email address.")
    if password:
        try:
            validate_password(password)
        except ValidationError as e:
            errors.extend(e.messages)

    if errors:
        return render(request, "partials/form_message.html", {"errors": errors})

    create_user(firstname, lastname, username, password, bio, phone, email)
    return render(request, "partials/form_message.html",
            {"success": f"User '{username}' created. You can now log in."})

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

def check_telnum(request):
    telnum = request.GET.get('phone', '').strip()
    if not telnum:
        return HttpResponse("")
    owner = get_user_by_telnum(telnum)
    if owner and owner['id'] != request.session.get('user_id'):
        return HttpResponse('<span class="text-red-700">Phone Number Taken</span>')
    return HttpResponse('<span class="text-green-700">Phone Number Available</span>')

def check_email(request):
    email = request.GET.get('email', '').strip()
    if not email:
        return HttpResponse("")
    owner = get_user_by_email(email)
    if owner and owner['id'] != request.session.get('user_id'):
        return HttpResponse('<span class="text-red-700">Email Taken</span>')
    return HttpResponse('<span class="text-green-700">Email Available</span>')


def login_view(request):
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
'''
# profile stuff
'''
def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_user_by_id(user_id)
    if user is None:
        # failsafe is user was deleted for some reason and the session still exists
        request.session.flush()
        return redirect('login')

    return render(request, 'profile.html', {'user': user})

def edit_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        response = HttpResponse()
        response["HX-Redirect"] = reverse('login')
        return response
    if request.method != "POST":
        user = get_user_by_id(user_id)
        return render(request, 'partials/edit_profile_modal.html', {'user': user})

    firstname = request.POST.get('firstname', '').strip()
    lastname = request.POST.get('lastname', '').strip()
    bio = request.POST.get('bio', '').strip()
    phone = request.POST.get('phone', '').strip() or None
    email = request.POST.get('email', '').strip() or None

    errors = []
    if not all ([firstname, lastname]):
        errors.append("First and last anme are required.")
    if phone:
        if not re.fullmatch(r"\d{3}-\d{4}", phone):
            errors.append("Phone number must look like 123-4567")
        else:
            owner = get_user_by_telnum(phone)
            # only happens if someone else has it already taken
            if owner and owner['id'] != user_id:
                errors.append("Phone number is takne")

    if email:
        try:
            validate_email(email)
        except ValidationError:
            errors.append("enter a valid email address")
    
    if errors:
        return render(request, "partials/form_message.html", {"errors": errors})

    update_user(user_id, firstname, lastname, bio, phone, email)
    response = HttpResponse()
    response["HX-Refresh"] = "true"
    return response

def change_password_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        response = HttpResponse()
        response["HX-Redirect"] = reverse("login")
        return response

    if request.method != "POST":
        return render(request, 'partials/edit_password_modal.html')

    old_password = request.POST.get("old_password", "")
    new_password = request.POST.get("new_password", "")
    new_password2 = request.POST.get("new_password2", "")

    errors = []
    if not all ([old_password, new_password, new_password2]):
        errors.append("Please fill in all fields.")
    elif not check_user_password(user_id, old_password):
        errors.append("Current password is wrong.")
    elif new_password != new_password2:
        errors.append("New passwords do not match.")
    else:
        try:
            validate_password(new_password)
        except ValidationError as e:
            errors.extend(e.messages)

    if errors:
        return render(request, "partials/form_message.html", {"errors": errors})

    update_password(user_id, new_password)
    return render(request, "partials/form_message.html",
                  {"success": "Password changed."})
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

'''
# modal's
'''
def menubutton(request):
    return render(request, 'partials/modal.html')

def edit_password_button(request):
    return render(request, 'partials/edit_password_modal.html')

def edit_profile_button(request):
    return render(request, 'partials/edit_profile_modal.html')

def delete(request):
    return HttpResponse()

@require_POST
def logout_view(request):
    request.session.flush()
    return redirect('login')
