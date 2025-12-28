# Reference Song Feature - Melody Conditioning

## Overview

Users can now upload a reference song that the AI will use as **inspiration** to generate similar-sounding but **100% original** music. This uses Meta MusicGen's "melody conditioning" technology.

## How It Works

1. **Upload Reference Song**: User uploads any audio file (MP3, WAV, etc.) they like
2. **AI Analyzes Melody**: MusicGen extracts the melodic structure and vibe
3. **Generate Similar Music**: AI creates new music with similar feel but completely original
4. **No Copyright Issues**: Output is fully original and royalty-free

## API Usage

### Endpoint: `POST /process-reel`

**Parameters:**
- `video` (required): Your video file
- `style` (optional): Music style enum (ambient, epic, energetic, etc.)
- `remove_original_audio` (optional): Remove existing audio from video (default: true)
- `reference_audio` (optional): **NEW!** Reference song for inspiration

### Example with cURL:

```bash
curl -X POST http://localhost:8000/process-reel \
  -F "video=@my_reel.mp4" \
  -F "style=energetic" \
  -F "reference_audio=@favorite_song.mp3"
```

## Technical Implementation

### Backend Changes

**main.py:**
- Added `reference_audio: Optional[UploadFile]` parameter
- Saves uploaded reference file with unique job_id
- Passes reference path to music generator
- Cleans up reference file after processing

**music_generator.py:**
- Updated `generate_music()` to accept `reference_audio` parameter
- Switches to `stereo-melody-large` model when reference provided
- Converts reference audio to base64
- Adds as `melody` parameter in Replicate API call
- Automatically adapts generated music to reference melody structure

### Key Code Snippet:

```python
if reference_audio:
    import base64
    with open(reference_audio, 'rb') as f:
        audio_data = f.read()
        audio_b64 = base64.b64encode(audio_data).decode('utf-8')
        
        ext = reference_audio.split('.')[-1].lower()
        mime_type = f"audio/{ext if ext in ['wav', 'mp3'] else 'mpeg'}"
        
        input_data["melody"] = f"data:{mime_type};base64,{audio_b64}"
        input_data["model_version"] = "stereo-melody-large"
```

## User Benefits

✅ **Creative Control**: Get music that matches specific vibes you have in mind
✅ **Royalty-Free**: Generated music is 100% original and commercially usable
✅ **No Copying**: AI creates new music inspired by reference, not a copy
✅ **Works with Any Audio**: MP3, WAV, M4A - any format supported by FFmpeg

## Use Cases

- "I want something like this trending TikTok sound"
- "Make music inspired by this lofi beat"
- "Create epic music similar to this movie trailer"
- "Generate hip-hop vibes like this reference track"

## Limitations

- Reference songs help guide **melody and vibe**, not exact reproduction
- Generated music may vary slightly from reference (intentional - ensures originality)
- Reference audio quality affects results (higher quality = better inspiration)
- Works best with instrumental references (vocals may confuse melody extraction)

## Cost

Same as regular generation: ~$0.10-0.15 per video using Replicate API with MusicGen melody model.
