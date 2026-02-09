"""Console dashboard display utilities."""

from typing import Dict, Optional
import sys


class Dashboard:
    """Clean console dashboard for multimodal demo."""
    
    def __init__(self):
        self.width = 70
    
    def clear(self):
        """Clear console (cross-platform)."""
        print('\033[2J\033[H', end='')
    
    def _section(self, title: str, icon: str = "") -> str:
        """Create section header."""
        header = f"{icon} {title}" if icon else title
        return f"\n{'─' * self.width}\n{header}\n{'─' * self.width}"
    
    def display(
        self,
        vision: Optional[Dict] = None,
        audio: Optional[Dict] = None,
        fused: Optional[Dict] = None,
        response: Optional[str] = None,
        status: str = "Running..."
    ):
        """
        Display complete dashboard.
        
        Args:
            vision: Vision pipeline results
            audio: Audio pipeline results
            fused: Fused emotional state
            response: LLM response text
            status: Current status message
        """
        self.clear()
        
        # Header
        print("=" * self.width)
        print("EMPATHY SYSTEM - MULTIMODAL DEMO".center(self.width))
        print("=" * self.width)
        print(f"Status: {status}")
        
        # Vision section
        if vision:
            print(self._section("VISION", "📹"))
            face_detected = vision.get('face_detected', False)
            if face_detected:
                emotion = vision.get('primary_emotion', 'unknown')
                conf = vision.get('confidence', 0)
                valence = vision.get('valence', 0)
                arousal = vision.get('arousal', 0)
                print(f"  Face: {emotion} (confidence: {conf:.2f})")
                print(f"  Valence: {valence:+.2f}, Arousal: {arousal:.2f}")
            else:
                print("  No face detected")
            
            if vision.get('posture'):
                posture = vision['posture']
                print(f"  Posture: {posture.get('openness', 'N/A')}")
            
            if vision.get('gaze'):
                gaze = vision['gaze']
                print(f"  Gaze: {gaze.get('status', 'N/A')}")
        
        # Audio section
        if audio:
            print(self._section("AUDIO", "🎵"))
            audio_state = audio.get('audio_state', {})
            is_speaking = audio_state.get('is_speaking', False)
            print(f"  Speaking: {'Yes' if is_speaking else 'No'}")
            
            transcript = audio_state.get('transcribed_text', '')
            if transcript:
                print(f"  Transcript: \"{transcript}\"")
            
            audio_emotion = audio_state.get('audio_emotion', 'unknown')
            arousal = audio_state.get('arousal', 0)
            valence = audio_state.get('valence', 0)
            print(f"  Voice tone: {audio_emotion}")
            print(f"  Valence: {valence:+.2f}, Arousal: {arousal:.2f}")
            
            events = audio_state.get('detected_events', [])
            if events:
                print(f"  Events: {', '.join(events)}")
        
        # Fused state
        if fused:
            print(self._section("FUSED STATE", "🧠"))
            emotion = fused.get('overall_emotion', 'unknown')
            valence = fused.get('valence', 0)
            arousal = fused.get('arousal', 0)
            stability = fused.get('stability', 0)
            
            print(f"  Emotion: {emotion}")
            print(f"  Valence: {valence:+.2f}, Arousal: {arousal:.2f}")
            print(f"  Stability: {stability:.2f}")
            
            masking = fused.get('emotional_masking', False)
            if masking:
                print(f"  ⚠️  Emotional masking detected")
        
        # Response
        if response:
            print(self._section("RESPONSE", "💬"))
            # Word wrap response
            words = response.split()
            line = "  "
            for word in words:
                if len(line) + len(word) + 1 > self.width:
                    print(line)
                    line = "  " + word
                else:
                    line += " " + word if line != "  " else word
            if line != "  ":
                print(line)
        
        # Footer
        print("\n" + "=" * self.width)
        print("Controls: [Q]uit | [M]ic toggle | [V]ideo toggle | [R]eset")
        print("=" * self.width)
        sys.stdout.flush()


class SimpleProgressBar:
    """Simple progress indicator."""
    
    def __init__(self, message: str):
        self.message = message
    
    def __enter__(self):
        print(f"{self.message}...", end='', flush=True)
        return self
    
    def __exit__(self, *args):
        print(" ✓")
