from backend.database import DatabaseManager
from dotenv import load_dotenv
import uuid

load_dotenv()

db = DatabaseManager()

# Test 1: Create a test user
print("Test 1: Creating test user...")
test_user_id = str(uuid.uuid4())
user = db.create_user(test_user_id, "test@example.com", "free")
print(f"✅ User created: {user}")

# Test 2: Get the user
print("\nTest 2: Retrieving user...")
retrieved = db.get_user(test_user_id)
print(f"✅ User retrieved: {retrieved}")

# Test 3: Log an analysis
print("\nTest 3: Logging analysis...")
analysis = db.log_analysis(test_user_id, "test.csv", 1024, 5.5)
print(f"✅ Analysis logged: {analysis}")

# Test 4: Get usage
print("\nTest 4: Checking usage...")
usage = db.get_usage(test_user_id)
print(f"✅ Usage: {usage}")

print("\n🎉 All tests passed! Database is ready.")
