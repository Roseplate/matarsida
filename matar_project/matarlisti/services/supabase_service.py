from supabase import create_client, Client
from django.conf import settings
import os
import time
from django.contrib.auth.hashers import make_password, check_password

def get_supabase_client() -> Client:
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def get_user_by_username(username):
    supabase = get_supabase_client()
    response = (
        supabase.table('users')
        .select('id, firstname, lastname, username, password')
        .eq('username', username)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None

def create_user(firstname, lastname, username, password):
    '''
    I am using djangos inbuilt make and check password hashes which uses random salts aswell and the raw password is not saved here
    '''
    supabase = get_supabase_client()
    response = supabase.table('users').insert({
        'firstname': firstname,
        'lastname': lastname,
        'username': username,
        'password': make_password(password),
    }).execute()
    return response.data[0]

def auth_user(username, password):
    '''
    Returns the user dict if username and password match otherwise it returns None
    '''
    user = get_user_by_username(username)
    if user and check_password(password, user['password']):
        return user
    return None


def upload_matarsidur_image(stad_id, image_file):
    """
    Uploads an image to the 'Images' bucket with the matarsidur id as the
    file name, then saves the public URL in matarsidur.img.
    Uploading again for the same id overwrites the old image.
    """
    supabase = get_supabase_client()
    file_name = str(stad_id)

    supabase.storage.from_(os.getenv("SUPABASE_BUCKET")).upload(
        path=file_name,
        file=image_file.read(),
        file_options={
            'content-type': image_file.content_type,
            'upsert': 'true',
        },
    )

    public_url = supabase.storage.from_(os.getenv("SUPABASE_BUCKET")).get_public_url(file_name)
    # ?v=... makes browsers load the new image after a replacement
    public_url = f"{public_url}?v={int(time.time())}"

    supabase.table('matarsidur').update({'img': public_url}).eq('id', stad_id).execute()
    return public_url

def fetch_users():
    supabase = get_supabase_client()
    response = supabase.table('users').select("*").execute()
    return response.data

def fetch_matarlisti():
    """
    Fetches all restaurants ordered by id. If the storage bucket has an image
    named after a restaurants id. That image is used instead of the img column 
    so images added straight to storage show up too.
    """
    supabase = get_supabase_client()
    response = supabase.table('matarsidur').select('*').order('id').execute()
    restaurants = response.data

    bucket = supabase.storage.from_(os.getenv("SUPABASE_BUCKET"))
    storage_images = {}
    for obj in bucket.list():
        file_id = obj['name'].split('.')[0]
        # updated_at changes when the file is replaced
        version = obj.get('updated_at') or ''
        storage_images[file_id] = f"{bucket.get_public_url(obj['name'])}?v={version}"

    for restaurant in restaurants:
        image_url = storage_images.get(str(restaurant['id']))
        if image_url:
            restaurant['img'] = image_url

    return restaurants

def fetch_stadir(start=0, amount=20):
    supabase = get_supabase_client()
    response = (
        supabase.table('matarsidur')
        .select('*')
        .gte('id', start)
        .lt('id', start+amount)
        .execute()
    )
    return response.data

def fetch_stad(stad_id):
    supabase = get_supabase_client()
    response = (
        supabase.table('matarsidur')
        .select('*')
        .eq('id', stad_id)
        .execute()
    )
    return response.data
