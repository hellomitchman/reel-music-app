# Reel Music App - AI Coding Agent Instructions

## Project Overview

This is a **FastAPI-based backend service** for a music/audio processing application. The project is in early development with a minimal API structure currently implementing only a health check endpoint.

## Architecture

**Backend Structure:**
- **FastAPI application** at [backend/main.py](../backend/main.py) - single-file API server
- Simple modular structure with `__init__.py` for package initialization
- Dependencies managed via [requirements.txt](../backend/requirements.txt)

**Key Dependencies:**
- `fastapi` - Web framework for building APIs
- `uvicorn` - ASGI server for running FastAPI
- `python-multipart` - For handling file uploads
- `ffmpeg-python` - Python bindings for FFmpeg (audio/video processing)
- `requests` - HTTP client for external API calls

## Development Workflows

**Running the Backend:**
```bash
cd backend
python -m uvicorn main:app --reload
```

**Installing Dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**Virtual Environment:**
- Project uses a `venv/` virtual environment in the root directory
- Activate before development: `source venv/bin/activate` (macOS/Linux)

## Patterns & Conventions

**API Structure:**
- Entry point: `app = FastAPI()` in [main.py](../backend/main.py)
- Health check endpoint: `GET /` returns `{"status": "ok"}`
- Currently single-file architecture - expect expansion into routers/modules for feature endpoints

**Expected Future Architecture:**
Given the `ffmpeg-python` dependency, this app likely will:
- Process audio/video files (reel content)
- Handle media uploads via `python-multipart`
- Make external API calls for music/audio metadata or services

**Python Style:**
- Standard FastAPI async patterns expected for I/O-heavy operations
- Type hints should be used for API route parameters and responses

## Integration Points

**Media Processing:**
- FFmpeg integration expected for audio extraction, format conversion, or transcoding
- File handling through FastAPI's `UploadFile` for multipart uploads

**External APIs:**
- `requests` library suggests integration with external music/audio services
- Potential integrations: music recognition APIs, audio analysis services, content platforms

## Important Notes

- This is an **early-stage project** - most endpoints and features are yet to be implemented
- The presence of FFmpeg suggests compute-intensive operations - consider async processing
- Backend-only structure currently - no frontend directory exists yet
- No database configuration present - API may be stateless or using external storage

## Next Steps for Development

When adding features, structure should evolve to:
- Separate routers for different API domains (e.g., `routers/upload.py`, `routers/process.py`)
- Service layer for business logic and FFmpeg operations
- Configuration management for FFmpeg paths and external API keys
- Error handling middleware for API responses
