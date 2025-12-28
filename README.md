# Reel Music Generator 🎵

AI-powered music generation for your video reels. Upload a video and get back original, royalty-free music that perfectly matches your content.

## Features

- 🤖 **AI-Generated Music** - Powered by Meta's MusicGen
- 🎨 **16 Music Styles** - From ambient to epic, lo-fi to rock
- 🎼 **Reference Audio** - Upload inspiration songs or videos
- 📦 **Multiple Formats** - Download video with music, audio only, or both
- ✅ **100% Royalty-Free** - Use commercially without copyright issues

## Tech Stack

- **Backend**: FastAPI + Python 3.9+
- **AI Model**: Meta MusicGen via Replicate API
- **Video Processing**: FFmpeg
- **Frontend**: Pure HTML/CSS/JavaScript

## Deployment

This app is deployed on Railway and accessible at: https://your-app.railway.app

## Local Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
echo "REPLICATE_API_TOKEN=your_token_here" > .env

# Run the server
uvicorn main:app --reload
```

Visit http://localhost:8000

## Environment Variables

- `REPLICATE_API_TOKEN` - Your Replicate API token (get one at https://replicate.com)
- `APP_PASSWORD` - Password to access the app (default: `reelmusic2025`)

**Security Note**: Change the default password when deploying! Set `APP_PASSWORD` environment variable in Railway.

## License

MIT License - Feel free to use for personal and commercial projects!
