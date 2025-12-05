import os
from supabase import create_client, Client
from typing import Optional, Dict, Any
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.client: Client = create_client(supabase_url, supabase_key)
    
    # User operations
    def create_user(self, user_id: str, email: str, plan: str = "free") -> Dict[str, Any]:
        data = {
            "id": user_id,
            "email": email,
            "plan": plan
        }
        result = self.client.table("users").insert(data).execute()
        return result.data[0] if result.data else None
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        result = self.client.table("users").select("*").eq("id", user_id).execute()
        return result.data[0] if result.data else None
    
    def update_user_plan(self, user_id: str, plan: str) -> Dict[str, Any]:
        result = self.client.table("users").update({"plan": plan}).eq("id", user_id).execute()
        return result.data[0] if result.data else None
    
    # Analysis operations
    def log_analysis(self, user_id: str, file_name: str, file_size: int, duration: float) -> Dict[str, Any]:
        data = {
            "user_id": user_id,
            "file_name": file_name,
            "file_size_bytes": file_size,
            "analysis_duration_seconds": duration
        }
        result = self.client.table("analyses").insert(data).execute()
        
        # Update usage counter
        self._update_usage(user_id, analyses_increment=1, storage_increment=file_size)
        
        return result.data[0] if result.data else None
    
    def get_user_analyses(self, user_id: str, limit: int = 50) -> list:
        result = self.client.table("analyses").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
        return result.data
    
    # Usage operations
    def get_usage(self, user_id: str) -> Optional[Dict[str, Any]]:
        result = self.client.table("usage").select("*").eq("user_id", user_id).execute()
        return result.data[0] if result.data else None
    
    def _update_usage(self, user_id: str, analyses_increment: int = 0, storage_increment: int = 0):
        # Get current usage
        current = self.get_usage(user_id)
        
        if current:
            # Update existing
            new_count = current["analyses_count"] + analyses_increment
            new_storage = current["storage_used_bytes"] + storage_increment
            self.client.table("usage").update({
                "analyses_count": new_count,
                "storage_used_bytes": new_storage,
                "last_updated": datetime.utcnow().isoformat()
            }).eq("user_id", user_id).execute()
        else:
            # Create new
            self.client.table("usage").insert({
                "user_id": user_id,
                "analyses_count": analyses_increment,
                "storage_used_bytes": storage_increment
            }).execute()
