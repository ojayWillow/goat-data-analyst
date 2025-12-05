# Supabase API Keys - Reference

## Current Setup (Correct)

Your .env uses the **legacy anon key**:
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

This is the **correct key** to use for server-side operations.

## Key Types Explained

### 1. Legacy Anon Key (What you're using) ✅
- Long JWT token starting with eyJhbGc...
- Use for: Backend/server operations
- Use for: DatabaseManager, API endpoints
- Security: Safe for server-side code

### 2. Publishable Key (Don't use yet)
- Short key: sb_publishable_s2oTwWec...
- Use for: Client-side JavaScript (future)
- Use for: Browser-based apps, mobile apps
- Security: Safe to expose in frontend code

## When to Use Each

**Backend (Python) - Use Legacy Anon Key:**
- DatabaseManager operations
- FastAPI endpoints
- Server-side authentication
- Your current .env is correct ✅

**Frontend (JavaScript) - Use Publishable Key:**
- Browser JavaScript
- React/Vue apps
- Mobile apps
- Not needed yet for GOAT

## Security Best Practices

✅ **DO:**
- Keep legacy anon key in .env (server-side only)
- Never commit .env to git
- Use publishable key only for client-side code

❌ **DON'T:**
- Use publishable key in backend Python code
- Expose legacy anon key in browser/frontend
- Mix up the two keys

## Your Current .env (Correct)

SUPABASE_URL=https://ysheydqzwlfsbxsgrrcv.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (legacy anon - correct for backend)

## No Changes Needed

Your setup is correct. The publishable key is for future use when/if you add:
- Browser-based dashboard
- Mobile app
- Client-side features

For now, keep using the legacy anon key in your .env ✅

---

**Status**: Configuration verified
**Action**: No changes required
