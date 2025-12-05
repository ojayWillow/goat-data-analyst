# GOAT Data Analyst - Database Setup Guide

## Overview
This guide will help you set up the production database for GOAT Data Analyst using Supabase.

---

## What This Database Does

The database stores:
- **Users**: Email, subscription plan (free/pro), signup date
- **Analyses**: History of all file analyses (file name, size, duration)
- **Usage**: Tracking metrics (total analyses, storage used)

---

## Prerequisites

- Supabase account (free tier works)
- Python 3.10+
- Active internet connection

---

## Step-by-Step Setup

### Step 1: Verify Your Supabase Credentials

Your .env file should have these variables:
SUPABASE_URL=https://ysheydqzwlfsbxsgrrcv.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

### Step 2: Test Database Connection

Run: python test_db_connection.py

Expected output:
- Database connected successfully!
- Connection established to Supabase

### Step 3: Create Database Tables

1. Open browser: https://ysheydqzwlfsbxsgrrcv.supabase.co
2. Log in to Supabase
3. Click SQL Editor (left sidebar)
4. Click + New query button
5. Copy and paste this SQL:

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    plan VARCHAR(50) DEFAULT 'free'
);

CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    file_name VARCHAR(255) NOT NULL,
    file_size_bytes BIGINT,
    analysis_duration_seconds DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    analyses_count INT DEFAULT 0,
    storage_used_bytes BIGINT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT NOW()
);

6. Click RUN button
7. Wait for Success message

### Step 4: Verify Tables

1. Click Table Editor in left sidebar
2. You should see: users, analyses, usage

---

## Database Schema

### users table
- id: UUID (auto-generated)
- email: VARCHAR(255) (unique)
- created_at: TIMESTAMP
- plan: VARCHAR(50) - 'free' or 'pro'

### analyses table
- id: UUID (auto-generated)
- user_id: UUID (links to users)
- file_name: VARCHAR(255)
- file_size_bytes: BIGINT
- analysis_duration_seconds: DECIMAL(10,2)
- created_at: TIMESTAMP

### usage table
- id: UUID (auto-generated)
- user_id: UUID (links to users)
- analyses_count: INT
- storage_used_bytes: BIGINT
- last_updated: TIMESTAMP

---

## Troubleshooting

### Error: Could not connect to database
- Check .env has correct SUPABASE_URL and SUPABASE_KEY
- Verify internet connection

### Error: Table does not exist
- Run the SQL schema in Step 3
- Go to Supabase SQL Editor and run CREATE TABLE commands

---

Last Updated: December 5, 2025
Version: 1.0
