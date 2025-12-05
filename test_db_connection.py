from backend.database import DatabaseManager
from dotenv import load_dotenv

load_dotenv()

try:
    db = DatabaseManager()
    print("✅ Database connected successfully!")
    print(f"📊 Connection established to Supabase")
except Exception as e:
    print(f"❌ Connection failed: {e}")
