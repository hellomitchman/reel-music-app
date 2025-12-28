"""Video processing utilities using FFmpeg"""
import ffmpeg
import os
from pathlib import Path
from typing import Dict, Optional


class VideoProcessor:
    """Handle video analysis and audio-video merging"""
    
    @staticmethod
    def get_video_info(video_path: str) -> Dict:
        """
        Extract video information like duration, resolution, fps
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Dictionary with video metadata
        """
        try:
            probe = ffmpeg.probe(video_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            
            duration = float(probe['format']['duration'])
            width = int(video_info['width'])
            height = int(video_info['height'])
            fps = eval(video_info['r_frame_rate'])  # Convert "30/1" to 30.0
            
            return {
                "duration": duration,
                "width": width,
                "height": height,
                "fps": fps,
                "has_audio": any(s['codec_type'] == 'audio' for s in probe['streams'])
            }
        except Exception as e:
            raise Exception(f"Failed to get video info: {str(e)}")
    
    @staticmethod
    def merge_audio_video(
        video_path: str,
        audio_path: str,
        output_path: str,
        remove_original_audio: bool = True
    ) -> str:
        """
        Merge audio file with video file
        
        Args:
            video_path: Path to input video
            audio_path: Path to audio file (music)
            output_path: Path for the output video
            remove_original_audio: If True, removes original audio from video
            
        Returns:
            Path to the output video file
        """
        try:
            video = ffmpeg.input(video_path)
            audio = ffmpeg.input(audio_path)
            
            if remove_original_audio:
                # Use only the new audio
                output = ffmpeg.output(
                    video.video,
                    audio.audio,
                    output_path,
                    vcodec='copy',  # Don't re-encode video (faster)
                    acodec='aac',   # Use AAC audio codec
                    audio_bitrate='192k',
                    shortest=None   # Cut to shortest stream (video or audio)
                )
            else:
                # Mix original audio with new audio
                output = ffmpeg.output(
                    video,
                    audio,
                    output_path,
                    vcodec='copy',
                    acodec='aac',
                    audio_bitrate='192k'
                )
            
            # Overwrite output file if it exists
            output = ffmpeg.overwrite_output(output)
            
            # Run the ffmpeg command
            ffmpeg.run(output, capture_stdout=True, capture_stderr=True)
            
            return output_path
            
        except ffmpeg.Error as e:
            error_message = e.stderr.decode() if e.stderr else str(e)
            raise Exception(f"FFmpeg error: {error_message}")
        except Exception as e:
            raise Exception(f"Failed to merge audio and video: {str(e)}")
    
    @staticmethod
    def extract_audio(video_path: str, output_path: str) -> str:
        """
        Extract audio from video file
        
        Args:
            video_path: Path to video file
            output_path: Path for extracted audio
            
        Returns:
            Path to extracted audio file
        """
        try:
            stream = ffmpeg.input(video_path)
            audio = stream.audio
            output = ffmpeg.output(audio, output_path, acodec='mp3', audio_bitrate='192k')
            output = ffmpeg.overwrite_output(output)
            ffmpeg.run(output, capture_stdout=True, capture_stderr=True)
            return output_path
        except Exception as e:
            raise Exception(f"Failed to extract audio: {str(e)}")
