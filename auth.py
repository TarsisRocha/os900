# app/modules/auth.py
import bcrypt
from typing import Optional
from app.modules.supabase_client import supabase

def authenticate(username: str, password: str) -> bool:
    try:
        resp = supabase.table("usuarios").select("password").eq("username", username).execute()
        if resp.data:
            stored = resp.data[0]["password"]
            if isinstance(stored, str):
                stored = stored.encode("utf-8")
            return bcrypt.checkpw(password.encode("utf-8"), stored)
        return False
    except Exception as e:
        print(f"Erro autenticação: {e}")
        return False

def add_user(username: str, password: str, is_admin: bool = False) -> bool:
    try:
        resp = supabase.table("usuarios").select("username").eq("username", username).execute()
        if resp.data:
            return False
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        role = "admin" if is_admin else "user"
        supabase.table("usuarios").insert({"username": username, "password": hashed, "role": role}).execute()
        return True
    except Exception as e:
        print(f"Erro add_user: {e}")
        return False

def is_admin(username: str) -> bool:
    try:
        resp = supabase.table("usuarios").select("role").eq("username", username).execute()
        return bool(resp.data and resp.data[0].get("role") == "admin")
    except Exception as e:
        print(f"Erro is_admin: {e}")
        return False

def list_users():
    try:
        resp = supabase.table("usuarios").select("username, role").execute()
        return resp.data or []
    except Exception as e:
        print(f"Erro list_users: {e}")
        return []

def force_change_password(admin_username: str, target_username: str, new_password: str) -> bool:
    if not is_admin(admin_username):
        return False
    try:
        hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        supabase.table("usuarios").update({"password": hashed}).eq("username", target_username).execute()
        return True
    except Exception as e:
        print(f"Erro force_change_password: {e}")
        return False
