from supabase import create_client, Client
from django.conf import settings
import os

def get_supabase_client() -> Client:
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def fetch_users():
    supabase = get_supabase_client()
    response = supabase.table('users').select("*").execute()
    return response.data

def fetch_matarlisti():
    supabase = get_supabase_client()
    response = supabase.table('matarsidur').select('*').execute()
    return response.data

def fetch_stad(stad_id):
    supabase = get_supabase_client()
    response = {
        supabase.table('matarsidur')
        .select('*')
        .eq('id', stad_id)
        .single()
        .execute()
    }
    return response.data
