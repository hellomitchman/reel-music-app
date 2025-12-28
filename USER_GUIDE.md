# Reel Music Generator - User Guide

## What This Does
This software adds original, royalty-free music to your Instagram reels. You upload a video without music, and it comes back with professional AI-generated music that you can use commercially without copyright issues.

## Setup Instructions (One-Time)

### Step 1: Install Python Packages
Open Terminal and run these commands:

```bash
cd /Users/Oldcomputer/Desktop/reel-music-app/backend
pip install -r requirements.txt
```

Wait for it to finish installing (may take 2-3 minutes).

### Step 2: Verify FFmpeg is Working
Run this command to check FFmpeg is installed:

```bash
ffmpeg -version
```

You should see version information. If not, install it with:

```bash
brew install ffmpeg
```

## How to Use

### Step 1: Start the Server
In Terminal, run:

```bash
cd /Users/Oldcomputer/Desktop/reel-music-app/backend
python -m uvicorn main:app --reload
```

You'll see: `Application startup complete` and `Uvicorn running on http://127.0.0.1:8000`

**Leave this Terminal window open while using the app!**

### Step 2: Upload Your Video

Open your web browser and go to: **http://127.0.0.1:8000/docs**

You'll see a web interface. Here's how to use it:

1. Click on **"POST /process-reel"** 
2. Click **"Try it out"**
3. Click **"Choose File"** and select your video
4. Select a music style from the dropdown (e.g., "ambient", "energetic", "epic")
5. Leave "remove_original_audio" checked (unless you want to keep original audio mixed with new music)
6. Click **"Execute"**

### Step 3: Download Your Video
Wait 20-60 seconds while it processes. When done, click **"Download file"** to get your video with music!

## Available Music Styles

- **ambient** - Calm, atmospheric background music
- **energetic** - Upbeat, high-energy tracks
- **epic** - Cinematic, dramatic music
- **happy** - Cheerful, positive vibes
- **inspiring** - Motivational, uplifting
- **chill** - Relaxed, lo-fi style
- **corporate** - Professional, business-appropriate
- **dramatic** - Intense, emotional
- **romantic** - Soft, loving themes
- **upbeat** - Fast-paced, exciting

## Important Notes

✅ **Copyright-Free**: All generated music is 100% royalty-free and can be used commercially
✅ **No Watermarks**: Clean output with no branding
✅ **File Limit**: Videos up to 100 MB
✅ **Formats Supported**: MP4, MOV, AVI, MKV

## Troubleshooting

**"ModuleNotFoundError"**
- Run: `pip install -r requirements.txt` in the backend folder

**"FFmpeg not found"**
- Run: `brew install ffmpeg`

**"Connection refused"**
- Make sure the server is running (Step 1 in "How to Use")

**Video takes too long**
- First-time generation may take longer
- Longer videos take more time to process

## Stopping the Server

When you're done, go back to the Terminal window and press:
- **Control + C** (Mac/Linux)
- Then close the Terminal

## Need Better Music Quality?

The app uses a fallback music generator by default. For higher quality AI music:

1. Get a free API key from https://mubert.com/render/api
2. Set it in Terminal before starting:
   ```bash
   export MUBERT_LICENSE="your-api-key-here"
   ```
3. Then start the server as usual

---

**That's it! You now have a fully functional reel music generator.**
