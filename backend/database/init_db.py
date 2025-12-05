"""
Database initialization script.
Run this after setting up Supabase to create tables.
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_database():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        return
    
    print(f"🔗 Connecting to Supabase: {supabase_url}")
    client = create_client(supabase_url, supabase_key)
    
    # Read schema file
    with open("backend/database/schema.sql", "r") as f:
        schema = f.read()
    
    print("📄 Schema loaded from backend/database/schema.sql")
    print("\n⚠️  MANUAL STEP REQUIRED:")
    print("1. Go to your Supabase project dashboard")
    print("2. Navigate to SQL Editor")
    print("3. Copy and paste the schema below:")
    print("=" * 60)
    print(schema)
    print("=" * 60)
    print("\n4. Click 'RUN' to create the tables")
    print("\n✅ After running the schema, your database will be ready!")

if __name__ == "__main__":
    init_database()
