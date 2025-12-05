# Database Setup Guide

## Prerequisites
- Supabase account (free tier is fine)
- Project created on Supabase

## Step 1: Create Supabase Project
1. Go to https://supabase.com
2. Sign up or log in
3. Click "New Project"
4. Fill in project details
5. Wait for project to be created (~2 minutes)

## Step 2: Get Connection Details
1. In your Supabase project dashboard, go to **Settings** → **API**
2. Copy the following:
   - **Project URL** (e.g., https://xxxxx.supabase.co)
   - **anon/public key** (starts with eyJ...)

## Step 3: Configure Environment Variables
1. Copy .env.example to .env:

## Step 4: Create Database Tables
1. Run the initialization script:
python backend/database/init_db.py
2. Follow the instructions to copy the SQL schema
3. Go to Supabase SQL Editor and paste the schema
4. Click **RUN** to create the tables

## Step 5: Verify Setup
from backend.database import DatabaseManager

This should connect without errors
db = DatabaseManager()
print("✅ Database connected successfully!")

## Database Schema

### users
- id (UUID, primary key)
- email (VARCHAR, unique)
- created_at (TIMESTAMP)
- plan (VARCHAR, default: 'free')

### analyses
- id (UUID, primary key)
- user_id (UUID, foreign key)
- ile_name (VARCHAR)
- ile_size_bytes (BIGINT)
- nalysis_duration_seconds (DECIMAL)
- created_at (TIMESTAMP)

### usage
- id (UUID, primary key)
- user_id (UUID, foreign key)
- nalyses_count (INT)
- storage_used_bytes (BIGINT)
- last_updated (TIMESTAMP)

## Backup Strategy
- Supabase automatically backs up your database daily
- To manually backup: Go to **Database** → **Backups** in Supabase dashboard
- Download backup: Click on backup and select "Download"

## Next Steps
- [ ] Set up authentication (Day 21-23)
- [ ] Integrate database logging into analysis workflow
- [ ] Create admin dashboard to view usage stats
