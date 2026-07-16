import os
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class UserRepository:
    
    def get_all_users(self):
        result = supabase.table("users").select("*").execute()

        users = {}

        for row in result.data:
            users[row["username"]] = {
                "password": row["password"],
                "role": row["role"],
                "staff_id": row["staff_id"],
                "job": row["job"],
                "child_name": row["child_name"]
            }
        
        return users
    
    def get_user(self, username):
        result = (
            supabase.table("users")
            .select("*")
            .eq("username", username)
            .execute()
        )

        if not result.data:
            return None
        
        return result.data[0]
    
    def create_user(self, username, password, role,
                    staff_id=None, job=None, child_name=None):
        
        supabase.table("users").insert({
            "username": username,
            "password": password,
            "role": role,
            "staff_id": staff_id,
            "job": job,
            "child_name": child_name
        }).execute()