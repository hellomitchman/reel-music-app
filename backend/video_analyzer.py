"""Video analysis for detecting transitions and pacing"""
import cv2
import numpy as np
from typing import List, Dict, Tuple


class VideoAnalyzer:
    """Analyze video content to understand pacing and transitions"""
    
    @staticmethod
    def analyze_video_dynamics(video_path: str) -> Dict:
        """
        Analyze video for scene changes, motion, and pacing
        
        Returns dict with:
        - scene_changes: timestamps of major transitions
        - intensity_profile: motion intensity over time
        - overall_pace: slow/medium/fast
        """
        cap = cv2.VideoCapture(video_path)
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        
        scene_changes = []
        motion_scores = []
        prev_frame = None
        frame_idx = 0
        
        # Sample frames (analyze every 5th frame for performance)
        sample_rate = 5
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_idx % sample_rate == 0:
                # Convert to grayscale and resize for faster processing
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, (320, 240))
                
                if prev_frame is not None:
                    # Detect scene changes using frame difference
                    diff = cv2.absdiff(gray, prev_frame)
                    diff_score = np.mean(diff)
                    
                    # High difference = scene change or high motion
                    motion_scores.append(diff_score)
                    
                    # Detect significant scene changes
                    if diff_score > 30:  # Threshold for scene change
                        timestamp = frame_idx / fps
                        scene_changes.append(timestamp)
                
                prev_frame = gray.copy()
            
            frame_idx += 1
        
        cap.release()
        
        # Calculate overall pace based on motion
        if motion_scores:
            avg_motion = np.mean(motion_scores)
            if avg_motion > 25:
                pace = "fast"
            elif avg_motion > 15:
                pace = "medium"
            else:
                pace = "slow"
        else:
            pace = "medium"
        
        # Remove duplicate scene changes (within 1 second)
        filtered_changes = []
        for timestamp in scene_changes:
            if not filtered_changes or timestamp - filtered_changes[-1] > 1.0:
                filtered_changes.append(timestamp)
        
        return {
            "duration": duration,
            "scene_changes": filtered_changes[:10],  # Limit to top 10
            "num_scenes": len(filtered_changes),
            "overall_pace": pace,
            "motion_intensity": "high" if avg_motion > 20 else "medium" if avg_motion > 10 else "low"
        }
    
    @staticmethod
    def get_music_prompt(analysis: Dict, style: str) -> str:
        """
        Generate a detailed music generation prompt based on video analysis
        
        Args:
            analysis: Video analysis results
            style: User-selected style
            
        Returns:
            Detailed prompt for AI music generation
        """
        pace = analysis["overall_pace"]
        intensity = analysis["motion_intensity"]
        num_scenes = analysis["num_scenes"]
        
        # Build dynamic prompt based on video characteristics
        tempo_map = {
            "slow": "slow tempo, calm",
            "medium": "moderate tempo",
            "fast": "fast tempo, energetic"
        }
        
        intensity_map = {
            "low": "gentle, subtle",
            "medium": "balanced, moderate energy",
            "high": "intense, powerful"
        }
        
        # Dynamic structure based on scenes
        if num_scenes > 5:
            structure = "dynamic with build-ups and transitions"
        elif num_scenes > 2:
            structure = "with some variation and progression"
        else:
            structure = "steady and consistent"
        
        prompt = (
            f"{style} instrumental music, {tempo_map[pace]}, "
            f"{intensity_map[intensity]}, {structure}, "
            f"professional production, no vocals, cinematic"
        )
        
        return prompt
