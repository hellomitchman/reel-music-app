"""Professional AI Music Generation using Real AI Services"""
import os
import requests
import time
from typing import Optional
import replicate
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class MusicGenerator:
    """Generate professional royalty-free music using real AI"""
    
    def __init__(self):
        """Initialize with API keys from environment"""
        # Reload .env to ensure we get latest values
        load_dotenv(override=True)
        self.replicate_key = os.getenv("REPLICATE_API_TOKEN", "")
        
        # Debug: Print if key is loaded (first 10 chars only)
        if self.replicate_key:
            print(f"✓ Replicate API key loaded: {self.replicate_key[:10]}...")
        else:
            print("✗ No Replicate API key found. Set REPLICATE_API_TOKEN environment variable.")
        else:
            print("✗ No Replicate API key found")
        
    def generate_music(
        self,
        duration: int,
        style: str = "ambient",
        prompt: Optional[str] = None,
        output_path: str = "generated_music.wav",
        reference_audio: Optional[str] = None
    ) -> str:
        """
        Generate professional AI music
        
        Args:
            duration: Duration in seconds
            style: Music style/mood
            prompt: Custom prompt with video analysis
            output_path: Where to save the audio
            reference_audio: Optional path to reference song for inspiration
            
        Returns:
            Path to the generated audio file
        """
        print(f"\n🎵 Generating professional {style} music ({duration}s)...")
        
        if prompt:
            print(f"📝 Prompt: {prompt}")
        
        if reference_audio:
            print(f"🎼 Using reference audio for inspiration...")
        
        # Try Replicate MusicGen (Meta's AI - state of the art)
        if self.replicate_key:
            try:
                print("🤖 Using Meta's MusicGen AI...")
                return self._generate_with_musicgen(duration, style, prompt, output_path, reference_audio)
            except Exception as e:
                print(f"⚠️  MusicGen error: {e}")
        else:
            print("ℹ️  Replicate API key not set, trying alternatives...")
        
        # Try Mubert API
        try:
            print("🤖 Trying Mubert AI...")
            return self._generate_with_mubert(duration, style, output_path)
        except Exception as e:
            print(f"⚠️  Mubert error: {e}")
        
        # If all fail, provide clear error
        raise Exception(
            "\n❌ No AI music service available!\n\n"
            "To get professional music, you need a free API key:\n\n"
            "1. Go to: https://replicate.com/account/api-tokens\n"
            "2. Sign up (free tier included)\n"
            "3. Copy your API token\n"
            "4. Run: export REPLICATE_API_TOKEN='your-token-here'\n"
            "5. Restart the server\n\n"
            "This gives you access to Meta's MusicGen - professional AI music!"
        )
    
    def _generate_with_musicgen(self, duration: int, style: str, prompt: str, output_path: str, reference_audio: Optional[str] = None) -> str:
        """
        Generate using Meta's MusicGen via Replicate API (direct HTTP)
        This is the BEST quality - same as professional music producers use
        """
        
        # Create detailed prompt
        if not prompt:
            prompt = self._create_detailed_prompt(style)
        
        print(f"   Generating with: {prompt[:100]}...")
        
        # Prepare input data
        input_data = {
            "prompt": prompt,
            "duration": min(duration, 30),
            "model_version": "stereo-melody-large" if reference_audio else "stereo-large",
            "output_format": "wav",
            "normalization_strategy": "loudness"
        }
        
        # If reference audio provided, convert to base64 and add
        if reference_audio:
            import base64
            with open(reference_audio, 'rb') as f:
                audio_data = f.read()
                audio_b64 = base64.b64encode(audio_data).decode('utf-8')
                
                # Determine format from file extension
                ext = reference_audio.split('.')[-1].lower()
                mime_type = f"audio/{ext if ext in ['wav', 'mp3'] else 'mpeg'}"
                
                input_data["melody"] = f"data:{mime_type};base64,{audio_b64}"
                print(f"   🎼 Reference audio included for melody conditioning")
        
        # Use direct API calls
        url = "https://api.replicate.com/v1/predictions"
        
        headers = {
            "Authorization": f"Token {self.replicate_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "version": "671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
            "input": input_data
        }
        
        # Start the prediction
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        prediction = response.json()
        prediction_id = prediction["id"]
        
        print(f"   ⏳ Prediction started: {prediction_id}")
        
        # Poll for completion
        get_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
        max_wait = 120  # 2 minutes max
        waited = 0
        
        while waited < max_wait:
            time.sleep(3)
            waited += 3
            
            status_response = requests.get(get_url, headers=headers, timeout=30)
            status_response.raise_for_status()
            result = status_response.json()
            
            status = result["status"]
            
            if status == "succeeded":
                # Download the generated audio
                audio_url = result["output"]
                if isinstance(audio_url, list):
                    audio_url = audio_url[0]
                
                print("   ⬇️  Downloading generated audio...")
                audio_response = requests.get(audio_url, timeout=60)
                audio_response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    f.write(audio_response.content)
                
                # If duration > 30s, extend it
                if duration > 30:
                    print(f"   🔄 Extending audio to {duration}s...")
                    self._extend_audio(output_path, duration)
                
                print("   ✅ Professional AI music generated!")
                return output_path
            
            elif status == "failed":
                error = result.get("error", "Unknown error")
                raise Exception(f"MusicGen failed: {error}")
            
            # Still processing...
            print(f"   ⏳ Generating... ({waited}s)")
        
        raise Exception("MusicGen timed out")
    
    def _generate_with_mubert(self, duration: int, style: str, output_path: str) -> str:
        """
        Generate using Mubert API (free tier available)
        """
        
        # Mubert style tags
        style_tags = {
            "energetic": "energetic,electronic,upbeat,modern",
            "epic": "epic,cinematic,powerful,dramatic",
            "ambient": "ambient,chill,atmospheric,calm",
            "happy": "happy,uplifting,positive,fun",
            "chill": "chill,lofi,relaxed,smooth",
            "dramatic": "dramatic,intense,emotional,dark",
            "upbeat": "upbeat,dance,energetic,fun",
            "inspiring": "inspiring,uplifting,motivational,hopeful",
            "cinematic": "cinematic,epic,orchestral,grand",
            "electronic": "electronic,edm,synth,modern",
            "hip-hop": "hiphop,urban,beats,modern",
            "lofi": "lofi,chill,jazzy,relaxed",
            "rock": "rock,energetic,powerful,electric"
        }
        
        tags = style_tags.get(style, f"{style},instrumental,modern")
        
        # Try Mubert's public API with proper authentication
        url = "https://api-b2b.mubert.com/v2/RecordTrack"
        
        # Use public PAT for testing
        payload = {
            "method": "RecordTrack",
            "params": {
                "pat": "hUQMSfqk7RGZ5X9fjvPqL",  # Public test token
                "mode": tags.split(',')[0],  # Use primary tag
                "duration": min(duration, 60),  # Max 60s for free
            }
        }
        
        print(f"   Requesting: {tags}")
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Mubert response: {data.get('status')}")
                
                if data.get("status") == 1 and "data" in data:
                    # Get download URL
                    track_data = data.get("data", {})
                    
                    # Try different possible fields
                    download_url = None
                    if "tasks" in track_data and len(track_data["tasks"]) > 0:
                        download_url = track_data["tasks"][0].get("download_link")
                    
                    if not download_url:
                        download_url = track_data.get("link") or track_data.get("url") or track_data.get("download_link")
                    
                    if download_url:
                        print(f"   ⬇️  Downloading from Mubert...")
                        
                        # Download the audio
                        audio_response = requests.get(download_url, timeout=90)
                        audio_response.raise_for_status()
                        
                        with open(output_path, 'wb') as f:
                            f.write(audio_response.content)
                        
                        # Extend if needed
                        if duration > 60:
                            self._extend_audio(output_path, duration)
                        
                        print("   ✅ Mubert AI music generated!")
                        return output_path
                    else:
                        print(f"   No download URL in response: {track_data}")
        
        except Exception as e:
            print(f"   Mubert exception: {e}")
        
        raise Exception(f"Mubert API failed")
    
    def _extend_audio(self, audio_path: str, target_duration: int):
        """
        Extend audio file by crossfading copies
        """
        try:
            from pydub import AudioSegment
            
            audio = AudioSegment.from_wav(audio_path)
            current_duration = len(audio) / 1000.0  # Convert to seconds
            
            if current_duration >= target_duration:
                return
            
            # Calculate how many times to repeat
            repeats = int(target_duration / current_duration) + 1
            
            # Create extended version with crossfades
            extended = audio
            crossfade_ms = 2000  # 2 second crossfade
            
            for _ in range(repeats - 1):
                extended = extended.append(audio, crossfade=crossfade_ms)
                if len(extended) / 1000.0 >= target_duration:
                    break
            
            # Trim to exact duration
            extended = extended[:target_duration * 1000]
            
            # Export
            extended.export(audio_path, format="wav")
            
        except ImportError:
            print("   ⚠️  pydub not available for audio extension")
    
    def _create_detailed_prompt(self, style: str) -> str:
        """
        Create professional prompts that work well with MusicGen
        Based on what actually generates good music
        """
        
        prompts = {
            "energetic": "upbeat electronic dance music, driving beat, energetic synths, modern EDM production, festival vibes, high energy, 128 BPM",
            
            "epic": "epic cinematic orchestral music, powerful dramatic strings, heroic brass section, thundering percussion, movie trailer style, inspiring and grandiose",
            
            "ambient": "ambient atmospheric soundscape, ethereal pads, gentle piano, calming textures, meditation music, peaceful and serene, floating melodies",
            
            "happy": "happy upbeat pop music, bright cheerful melody, acoustic guitars, clapping rhythm, feel-good vibes, sunny and optimistic, major key",
            
            "chill": "chill lofi hip hop beat, jazzy chords, vinyl crackle, mellow drums, lazy sunday afternoon, relaxed and smooth, 85 BPM",
            
            "dramatic": "dark dramatic music, intense strings, ominous bass, suspenseful atmosphere, thriller soundtrack, minor key, building tension",
            
            "upbeat": "upbeat dance pop, catchy melody, four on the floor beat, disco vibes, party anthem, energetic and fun, radio ready",
            
            "inspiring": "inspiring motivational music, uplifting piano, soaring strings, hopeful melody, achievement and success, emotional build up, major key",
            
            "cinematic": "cinematic film score, sweeping orchestra, emotional strings, grand piano, movie soundtrack, epic and beautiful, professional production",
            
            "electronic": "modern electronic music, pulsing synth bass, digital drums, futuristic sound design, club banger, energetic drops, progressive house",
            
            "hip-hop": "hip hop instrumental beat, 808 bass, trap drums, rolling hi hats, dark melody, modern rap beat, hard hitting, 140 BPM",
            
            "lofi": "lofi beats to study to, jazzy samples, dusty drums, warm vinyl sound, relaxing hip hop, chill vibes, perfect loop, 70 BPM",
            
            "rock": "energetic rock music, electric guitars, driving bass, powerful drums, anthemic chorus, stadium rock energy, distorted guitars"
        }
        
        return prompts.get(style, f"{style} instrumental music, professional production, no vocals, modern high quality")
    
    @staticmethod
    def get_available_styles():
        """Return list of available music styles"""
        return [
            "energetic", "epic", "ambient", "happy", "chill",
            "dramatic", "upbeat", "inspiring", "cinematic",
            "electronic", "hip-hop", "lofi", "rock"
        ]
