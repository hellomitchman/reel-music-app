# 🚀 Deployment Guide - Railway

Follow these steps to deploy your Reel Music Generator to the cloud!

## Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app with GitHub)
- Your Replicate API token

## Step 1: Push to GitHub

```bash
cd /Users/Oldcomputer/Desktop/reel-music-app

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Reel Music Generator"

# Create a new repository on GitHub (github.com/new)
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/reel-music-app.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy on Railway

1. **Go to Railway**: https://railway.app
2. **Sign in** with GitHub
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your `reel-music-app` repository**
6. Railway will automatically detect and deploy your app!

## Step 3: Set Environment Variables

1. In Railway, click on your project
2. Go to **"Variables"** tab
3. Click **"Add Variable"**
4. Add these variables:
   - **Key**: `REPLICATE_API_TOKEN`
   - **Value**: `YOUR_REPLICATE_API_TOKEN_HERE`
   
   - **Key**: `APP_PASSWORD`
   - **Value**: Choose a strong password (e.g., `MySecretPass123!`)
5. Click **"Add"** for each

**⚠️ IMPORTANT**: Choose a strong password! This protects your app and prevents strangers from using your Replicate API credits.

## Step 4: Install FFmpeg (Required)

Railway needs FFmpeg for video processing:

1. In your Railway project, go to **"Settings"**
2. Under **"Nixpacks"**, add this to the config:
3. Railway should auto-detect the `nixpacks.toml` file we created

## Step 5: Get Your Live URL

1. In Railway, go to **"Settings"**
2. Click **"Generate Domain"**
3. You'll get a URL like: `https://reel-music-app-production.up.railway.app`
4. **That's your live link!** Share it with anyone!

## Step 6: Test It!

Visit your Railway URL and try uploading a video!

## Cost Estimate

- **Railway**: Free tier includes $5/month credit (enough for light use)
- **Replicate API**: ~$0.10-0.15 per video generated
- **Total**: Nearly free for personal use!

## Troubleshooting

### Build fails?
- Check the build logs in Railway
- Ensure all files were pushed to GitHub
- Verify FFmpeg is installed (check nixpacks.toml)

### "API key not found" error?
- Go to Railway Variables and add `REPLICATE_API_TOKEN`
- Redeploy after adding the variable

### Videos not processing?
- Check FFmpeg is installed in Railway settings
- View logs in Railway dashboard

## Alternative: Render.com

If Railway doesn't work, try Render:

1. Go to https://render.com
2. Create a new "Web Service"
3. Connect your GitHub repo
4. Set build command: `pip install -r backend/requirements.txt`
5. Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variable: `REPLICATE_API_TOKEN`
7. Deploy!

---

## 🎉 You're Live!

Once deployed, your app will be accessible 24/7 from anywhere in the world. No need to keep your computer on!

Share your link: `https://your-app.railway.app`
