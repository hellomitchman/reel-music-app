from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends, Header
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
import uuid
from pathlib import Path
from typing import Optional
import shutil
from enum import Enum
import zipfile
import secrets
import hashlib

from config import UPLOAD_DIR, OUTPUT_DIR, ALLOWED_VIDEO_EXTENSIONS, MAX_FILE_SIZE
from video_processor import VideoProcessor
from music_generator import MusicGenerator
from video_analyzer import VideoAnalyzer


class OutputFormat(str, Enum):
    """Output format options"""
    video = "video"  # Video with music
    audio = "audio"  # Audio only
    both = "both"    # ZIP with both files


class MusicStyle(str, Enum):
    """Available music styles"""
    energetic = "energetic"
    epic = "epic"
    ambient = "ambient"
    happy = "happy"
    chill = "chill"
    dramatic = "dramatic"
    upbeat = "upbeat"
    inspiring = "inspiring"
    cinematic = "cinematic"
    electronic = "electronic"
    hip_hop = "hip-hop"
    lofi = "lofi"
    rock = "rock"


app = FastAPI(
    title="Reel Music Generator",
    description="Upload a video reel and get it back with AI-generated royalty-free music",
    version="1.0.0"
)

# Authentication setup
security = HTTPBasic()
APP_PASSWORD = os.getenv("APP_PASSWORD", "sam")  # Default password, change via env var

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify the password for protected endpoints"""
    correct_password = APP_PASSWORD.encode("utf8")
    provided_password = credentials.password.encode("utf8")
    
    is_correct = secrets.compare_digest(provided_password, correct_password)
    
    if not is_correct:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend HTML"""
    html_file = frontend_path / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(), status_code=200)
    return {"status": "ok", "message": "Reel Music Generator API is running"}


@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Reel Music Generator API is running",
        "version": "1.0.0"
    }


# Initialize services
video_processor = VideoProcessor()
music_generator = MusicGenerator()
video_analyzer = VideoAnalyzer()


@app.get("/styles")
def get_music_styles():
    """Get available music styles"""
    return {
        "styles": music_generator.get_available_styles(),
        "description": "Choose a style that matches your video mood"
    }


@app.post("/process-reel")
async def process_reel(
    video: UploadFile = File(..., description="Video file (MP4, MOV, AVI, MKV)"),
    style: MusicStyle = Form(MusicStyle.ambient, description="Music style/mood"),
    remove_original_audio: bool = Form(True, description="Remove original audio from video"),
    reference_audio: Optional[UploadFile] = File(None, description="Optional: Upload a song OR video with music for AI to use as inspiration (MP3, WAV, MP4, MOV)"),
    output_format: OutputFormat = Form(OutputFormat.video, description="Download format: video (video with music), audio (music only), or both (ZIP file)"),
    username: str = Depends(verify_password)
):
    """
    Upload a video reel and get it back with AI-generated music
    
    - **video**: Your video file without music (or with audio you want replaced)
    - **style**: Music style from dropdown (epic, energetic, lofi, etc.)
    - **remove_original_audio**: Whether to remove existing audio from video
    - **reference_audio**: Optional reference song OR video with music for the AI to take inspiration from
    - **output_format**: Choose what to download: video (video with music), audio (music only), or both (ZIP file)
    """
    
    # Validate file extension
    file_ext = Path(video.filename).suffix.lower()
    if file_ext not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_VIDEO_EXTENSIONS)}"
        )
    
    # Convert enum to string value
    style_str = style.value
    
    # Generate unique ID for this processing job
    job_id = str(uuid.uuid4())
    
    # Create paths
    upload_path = UPLOAD_DIR / f"{job_id}_{video.filename}"
    music_path = OUTPUT_DIR / f"{job_id}_music.wav"
    output_path = OUTPUT_DIR / f"{job_id}_final.mp4"
    reference_path = None
    reference_audio_path = None
    
    if reference_audio:
        reference_path = UPLOAD_DIR / f"{job_id}_reference_{reference_audio.filename}"
    
    try:
        # Save uploaded video
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        # Save reference audio/video if provided
        if reference_audio and reference_path:
            with open(reference_path, "wb") as buffer:
                shutil.copyfileobj(reference_audio.file, buffer)
            
            # Check if reference is a video - extract audio from it
            ref_ext = Path(reference_audio.filename).suffix.lower()
            if ref_ext in ALLOWED_VIDEO_EXTENSIONS:
                print(f"🎬 Reference video uploaded: {reference_audio.filename}")
                print(f"🎵 Extracting audio from reference video...")
                reference_audio_path = UPLOAD_DIR / f"{job_id}_reference_audio.wav"
                video_processor.extract_audio(str(reference_path), str(reference_audio_path))
                print(f"✅ Audio extracted from video")
            else:
                print(f"📀 Reference audio uploaded: {reference_audio.filename}")
                reference_audio_path = reference_path
        
        # Check file size
        file_size = os.path.getsize(upload_path)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.0f}MB"
            )
        
        # Get video information
        video_info = video_processor.get_video_info(str(upload_path))
        duration = int(video_info["duration"]) + 1  # Add 1 second buffer
        
        # Analyze video for transitions and pacing
        print("Analyzing video dynamics...")
        video_analysis = video_analyzer.analyze_video_dynamics(str(upload_path))
        
        # Create intelligent music prompt based on video
        music_prompt = video_analyzer.get_music_prompt(video_analysis, style_str)
        print(f"Video analysis: {video_analysis['overall_pace']} pace, "
              f"{video_analysis['num_scenes']} scene changes")
        
        # Generate AI music
        print(f"Generating {style_str} music for {duration} seconds...")
        print(f"Using prompt: {music_prompt}")
        try:
            music_generator.generate_music(
                duration=duration,
                style=style_str,
                prompt=music_prompt,
                output_path=str(music_path),
                reference_audio=str(reference_audio_path) if reference_audio_path else None
            )
        except Exception as music_error:
            print(f"Music generation error: {music_error}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Music generation failed: {str(music_error)}")
        
        # Merge video with generated music
        print("Merging video with music...")
        video_processor.merge_audio_video(
            video_path=str(upload_path),
            audio_path=str(music_path),
            output_path=str(output_path),
            remove_original_audio=remove_original_audio
        )
        
        # Clean up temporary upload files
        os.remove(upload_path)
        if reference_path and reference_path.exists():
            os.remove(reference_path)
        if reference_audio_path and reference_audio_path.exists() and reference_audio_path != reference_path:
            os.remove(reference_audio_path)
        
        # Return based on requested format
        if output_format == OutputFormat.video:
            # Return video with music
            os.remove(music_path)  # Clean up standalone music file
            return FileResponse(
                path=str(output_path),
                media_type="video/mp4",
                filename=f"reel_with_music_{video.filename}",
                headers={
                    "Content-Disposition": f"attachment; filename=reel_with_music_{video.filename}"
                }
            )
        
        elif output_format == OutputFormat.audio:
            # Return only the music
            os.remove(output_path)  # Clean up video file
            return FileResponse(
                path=str(music_path),
                media_type="audio/wav",
                filename=f"reel_music_{Path(video.filename).stem}.wav",
                headers={
                    "Content-Disposition": f"attachment; filename=reel_music_{Path(video.filename).stem}.wav"
                }
            )
        
        else:  # OutputFormat.both
            # Create ZIP file with both video and audio
            zip_path = OUTPUT_DIR / f"{job_id}_package.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(output_path, f"reel_with_music_{video.filename}")
                zipf.write(music_path, f"reel_music_{Path(video.filename).stem}.wav")
            
            # Clean up individual files
            os.remove(output_path)
            os.remove(music_path)
            
            return FileResponse(
                path=str(zip_path),
                media_type="application/zip",
                filename=f"reel_package_{Path(video.filename).stem}.zip",
                headers={
                    "Content-Disposition": f"attachment; filename=reel_package_{Path(video.filename).stem}.zip"
                }
            )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Clean up files on error
        zip_path = OUTPUT_DIR / f"{job_id}_package.zip"
        for path in [upload_path, music_path, output_path, reference_path, reference_audio_path, zip_path]:
            if path and path.exists():
                os.remove(path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )


@app.get("/info")
def get_info():
    """Get information about the service"""
    return {
        "name": "Reel Music Generator",
        "description": "Upload Instagram reels and get them back with AI-generated royalty-free music",
        "features": [
            "AI-generated instrumental music",
            "Royalty-free and commercially usable",
            "Multiple music styles available",
            "Automatic video-audio synchronization",
            "No watermarks or limitations"
        ],
        "supported_formats": list(ALLOWED_VIDEO_EXTENSIONS),
        "max_file_size_mb": MAX_FILE_SIZE / (1024 * 1024),
        "music_styles": music_generator.get_available_styles()
    }