import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Environment Variables Check\n")

required_vars = [
    "PERPLEXITY_API_KEY",
    "GROQ_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "SECRET_KEY",
    "SENTRY_DSN",
    "POSTHOG_API_KEY",
    "POSTHOG_HOST"
]

missing = []
for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"✅ {var}: Set")
    else:
        print(f"❌ {var}: MISSING")
        missing.append(var)

print(f"\n{'✅ All required variables set!' if not missing else '❌ Missing variables: ' + ', '.join(missing)}")
