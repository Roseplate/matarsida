from supabase import create_client, Client
from django.conf import settings
import os

def get_supabase_client() -> Client:
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def fetch_users():
    supabase = get_supabase_client()
    response = supabase.table('Users').select("*").execute()
    return response.data