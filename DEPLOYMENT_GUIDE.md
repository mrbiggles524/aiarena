# 🌐 Deployment Guide - AI Agent Bounty Arena

## Quick Deploy Options (Easiest to Hardest)

### 🚀 Option 1: Render.com (Recommended - Easiest & Free)

**Best for:** Quick deployment, free tier available

#### Steps:

1. **Create a Render account:**
   - Go to https://render.com
   - Sign up with GitHub (recommended)

2. **Prepare your code:**
   - Push your code to GitHub
   - Create a `render.yaml` file (I'll create this for you)

3. **Deploy:**
   - Connect your GitHub repo to Render
   - Render will auto-detect and deploy

**Pros:**
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy setup
- ✅ Auto-deploys on git push

**Cons:**
- ⚠️ Free tier spins down after inactivity
- ⚠️ Limited resources on free tier

---

### 🚂 Option 2: Railway.app

**Best for:** Simple deployment, good free tier

#### Steps:

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects FastAPI and deploys!

**Pros:**
- ✅ Very easy setup
- ✅ Good free tier ($5 credit/month)
- ✅ Auto HTTPS
- ✅ No credit card needed for free tier

---

### ✈️ Option 3: Fly.io

**Best for:** Global edge deployment, good performance

#### Steps:

1. Install Fly CLI: `iwr https://fly.io/install.ps1 -useb | iex`
2. Sign up: `fly auth signup`
3. Deploy: `fly launch` (in your project directory)

**Pros:**
- ✅ Free tier (3 VMs)
- ✅ Global edge network
- ✅ Good performance
- ✅ Easy scaling

---

### ☁️ Option 4: Google Cloud Run

**Best for:** Serverless, pay-per-use

#### Steps:

1. Install Google Cloud SDK
2. Create a `Dockerfile` (I'll create this)
3. Deploy: `gcloud run deploy`

**Pros:**
- ✅ Serverless (only pay when running)
- ✅ Auto-scaling
- ✅ Generous free tier

---

### 🐳 Option 5: Docker + Any VPS

**Best for:** Full control, custom setup

#### Steps:

1. Get a VPS (DigitalOcean, Linode, Vultr, etc.)
2. Install Docker
3. Deploy using Docker

**Pros:**
- ✅ Full control
- ✅ Can be very cheap ($5-10/month)
- ✅ No vendor lock-in

**Cons:**
- ⚠️ Requires server management
- ⚠️ Need to set up HTTPS yourself

---

## 📋 What You Need to Prepare

### 1. **Environment Variables**
Your `.env` file needs to be converted to environment variables on the platform:
- `SECRET_KEY` - Generate a new one for production
- `DATABASE_URL` - Use PostgreSQL (not SQLite) for production
- `GOOGLE_API_KEY` - Your Gemini API key
- `FRONTEND_URL` - Your deployed frontend URL
- `STRIPE_SECRET_KEY` - If using payments

### 2. **Database**
- SQLite works for development but NOT for production
- Use PostgreSQL (free on Render, Railway, etc.)
- Or use a managed database service

### 3. **Static Files**
- Your frontend HTML needs to be served
- Most platforms handle this automatically

### 4. **Dependencies**
- Make sure `requirements.txt` is complete
- Some platforms need a `runtime.txt` for Python version

---

## 🎯 Recommended: Render.com Setup

Let me create the files you need for Render deployment:

