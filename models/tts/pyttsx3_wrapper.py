"""pyttsx3 TTS wrapper for empathy system."""

import numpy as np
from typing import Optional
from loguru import logger

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class Pyttsx3TTS:
    """
    Text-to-speech using pyttsx3 (Windows system voices).
    
    Compatible with Python 3.13, works offline.
    """
    
    def __init__(self, voice_index: int = 0, rate: int = 170, volume: float = 0.9):
        """
        Initialize pyttsx3 TTS.
        
        Args:
            voice_index: Index of voice to use (0=David, 1=Zira)
            rate: Speech rate in words per minute
            volume: Volume (0.0-1.0)
        """
        if not PYTTSX3_AVAILABLE:
            raise ImportError("pyttsx3 not installed")
        
        self.engine = pyttsx3.init()
        self.sample_rate = 22050  # Standard for compatibility
        
        # Get voices
        voices = self.engine.getProperty('voices')
        if voices and 0 <= voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)
            logger.info(f"Using voice: {voices[voice_index].name}")
        
        # Set properties
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        logger.info(f"Pyttsx3TTS initialized (rate={rate}, volume={volume})")
    
    def synthesize(self, text: str, emotion_override: Optional[str] = None) -> np.ndarray:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            emotion_override: Optional emotion hint (not used by pyttsx3)
            
        Returns:
            Empty array (pyttsx3 plays directly, doesn't return audio)
        """
        if not text or not text.strip():
            return np.array([], dtype=np.float32)
        
        try:
            # Adjust rate based on emotion (simple heuristic)
            if emotion_override:
                base_rate = self.engine.getProperty('rate')
                if emotion_override in ['excited', 'happy']:
                    self.engine.setProperty('rate', base_rate + 20)
                elif emotion_override in ['sad', 'calm']:
                    self.engine.setProperty('rate', base_rate - 20)
            
            # Speak
            self.engine.say(text)
            self.engine.runAndWait()
            
            # Reset rate
            if emotion_override:
                self.engine.setProperty('rate', 170)
            
            logger.debug(f"Synthesized: {text[:50]}...")
            return np.array([], dtype=np.float32)
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return np.array([], dtype=np.float32)
    
    def synthesize_async(self, text: str):
        """
        Synthesize speech asynchronously (non-blocking).
        
        Args:
            text: Text to synthesize
        """
        if not text or not text.strip():
            return
        
        try:
            self.engine.say(text)
            # Don't call runAndWait - let it queue
        except Exception as e:
            logger.error(f"Async TTS error: {e}")
    
    def flush(self):
        """Process queued speech."""
        try:
            self.engine.runAndWait()
        except:
            pass
