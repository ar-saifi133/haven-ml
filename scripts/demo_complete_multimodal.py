"""
Complete Multimodal Integration Demo

Demonstrates the full empathy system with:
- Real-time facial emotion detection (DeepFace)
- Voice transcription (Whisper)
- Voice emotion analysis (Wav2Vec2)
- LLM empathetic responses (Llama 3.1)
- Text-to-speech output (pyttsx3)
"""

import sys
sys.path.insert(0, '.')

import asyncio
import cv2
import numpy as np
import sounddevice as sd
from loguru import logger
from typing import Optional

from agents.empathy_agent import EmpathyAgent
from models.tts.pyttsx3_wrapper import Pyttsx3TTS
from utils.display_dashboard import Dashboard
from config import Config


class MultimodalDemo:
    """Complete multimodal empathy system demo."""
    
    def __init__(self):
        self.config = Config()
        self.dashboard = Dashboard()
        
        # State
        self.video_enabled = True
        self.audio_enabled = True
        self.tts_enabled = True
        self.running = True
        
        # Components
        self.agent: Optional[EmpathyAgent] = None
        self.tts: Optional[Pyttsx3TTS] = None
        self.cap: Optional[cv2.VideoCapture] = None
        
        # Audio buffer
        self.audio_buffer = []
        self.sample_rate = 16000
        self.chunk_size = 8000  # 0.5 seconds
    
    async def initialize(self):
        """Initialize all components."""
        print("\n" + "=" * 70)
        print("EMPATHY SYSTEM - INITIALIZING".center(70))
        print("=" * 70)
        
        # Initialize agent
        print("\n1. Loading AI models...")
        print("   (This may take 30-60 seconds on first run)")
        self.agent = EmpathyAgent(
            user_id='demo_user',
            persona='remote_worker',
            use_mock=False
        )
        
        # Check detector types
        detector_type = type(self.agent.video_pipeline.face_detector).__name__
        print(f"\n   Vision: {detector_type}")
        
        stt_type = type(self.agent.audio_pipeline.stt).__name__
        print(f"   STT: {stt_type}")
        
        await self.agent.start_session('multimodal_demo_001')
        print("   ✓ Agent initialized")
        
        # Initialize TTS
        print("\n2. Initializing text-to-speech...")
        try:
            self.tts = Pyttsx3TTS(voice_index=0, rate=170)
            print("   ✓ TTS ready (pyttsx3)")
        except Exception as e:
            print(f"   ⚠️  TTS failed: {e}")
            self.tts_enabled = False
        
        # Initialize video
        print("\n3. Opening webcam...")
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            print("   ✓ Webcam ready")
        else:
            print("   ⚠️  Webcam failed")
            self.video_enabled = False
        
        print("\n" + "=" * 70)
        print("✓ INITIALIZATION COMPLETE!".center(70))
        print("=" * 70)
        
        # Greet user
        if self.tts and self.tts_enabled:
            greeting = "Hello! I'm your empathy agent. I can see and hear you."
            print(f"\n🔊 {greeting}")
            self.tts.synthesize(greeting)
    
    async def process_frame(self) -> Optional[dict]:
        """Process one video frame."""
        if not self.video_enabled or not self.cap:
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Process through vision pipeline
        vision_result = await self.agent.video_pipeline.process_frame(frame)
        
        # Display frame with emotion overlay
        if vision_result.get('face_detected'):
            emotion = vision_result.get('primary_emotion', 'unknown')
            conf = vision_result.get('confidence', 0)
            
            # Draw emotion text
            cv2.putText(
                frame,
                f"{emotion} ({conf:.2f})",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
        
        cv2.imshow('Empathy System - Vision', frame)
        
        return vision_result
    
    async def process_audio(self) -> Optional[dict]:
        """Process audio chunk."""
        if not self.audio_enabled or not self.audio_buffer:
            return None
        
        # Get audio chunk
        audio_chunk = np.concatenate(self.audio_buffer)
        self.audio_buffer = []
        
        # Ensure float32
        if audio_chunk.dtype != np.float32:
            audio_chunk = audio_chunk.astype(np.float32)
        
        # Process through audio pipeline
        audio_result = await self.agent.audio_pipeline.process_audio(audio_chunk)
        
        return audio_result
    
    def audio_callback(self, indata, frames, time_info, status):
        """Audio input callback."""
        if self.audio_enabled and self.running:
            # Convert to mono if needed
            if indata.shape[1] > 1:
                audio = indata.mean(axis=1)
            else:
                audio = indata[:, 0]
            
            self.audio_buffer.append(audio.copy())
    
    async def generate_response(self, fused_state: dict, transcribed_text: str):
        """Generate and speak response."""
        if not transcribed_text or not transcribed_text.strip():
            return None
        
        # Generate LLM response
        response = await self.agent.generate_response(
            user_input=transcribed_text,
            visual_state=fused_state.get('visual_state'),
            audio_state=fused_state.get('audio_state'),
            fused_state=fused_state
        )
        
        # Speak response
        if self.tts and self.tts_enabled and response:
            emotion = fused_state.get('overall_emotion', None)
            self.tts.synthesize(response, emotion_override=emotion)
        
        return response
    
    async def main_loop(self):
        """Main processing loop."""
        frame_count = 0
        last_response = None
        last_transcript = ""
        
        # Start audio stream
        if self.audio_enabled:
            audio_stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=self.audio_callback,
                blocksize=self.chunk_size
            )
            audio_stream.start()
        
        while self.running:
            try:
                # Process vision (every frame)
                vision_result = await self.process_frame()
                
                # Process audio (when buffer has data)
                audio_result = None
                if len(self.audio_buffer) >= 2:  # ~1 second of audio
                    audio_result = await self.process_audio()
                
                # Fuse results
                fused_state = None
                if vision_result or audio_result:
                    visual_state = vision_result if vision_result else {}
                    audio_state = audio_result.get('audio_state', {}) if audio_result else {}
                    
                    fused_state = {
                        'visual_state': visual_state,
                        'audio_state': audio_state,
                        'overall_emotion': visual_state.get('primary_emotion', 'neutral'),
                        'valence': visual_state.get('valence', 0),
                        'arousal': visual_state.get('arousal', 0.5),
                        'stability': visual_state.get('emotional_stability', 1.0),
                        'emotional_masking': visual_state.get('emotional_masking', False)
                    }
                
                # Generate response if speech ended
                transcribed_text = ""
                if audio_result:
                    audio_state = audio_result.get('audio_state', {})
                    transcribed_text = audio_state.get('transcribed_text', '')
                    
                    if transcribed_text and transcribed_text != last_transcript:
                        last_transcript = transcribed_text
                        last_response = await self.generate_response(fused_state, transcribed_text)
                
                # Update dashboard
                self.dashboard.display(
                    vision=vision_result,
                    audio=audio_result,
                    fused=fused_state,
                    response=last_response,
                    status=f"Frame {frame_count} | Press Q to quit"
                )
                
                frame_count += 1
                
                # Handle keyboard
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    self.running = False
                elif key == ord('m') or key == ord('M'):
                    self.audio_enabled = not self.audio_enabled
                    logger.info(f"Audio: {'ON' if self.audio_enabled else 'OFF'}")
                elif key == ord('v') or key == ord('V'):
                    self.video_enabled = not self.video_enabled
                    logger.info(f"Video: {'ON' if self.video_enabled else 'OFF'}")
                elif key == ord('r') or key == ord('R'):
                    last_response = None
                    last_transcript = ""
                    logger.info("Reset conversation")
                
                # Small delay
                await asyncio.sleep(0.01)
                
            except KeyboardInterrupt:
                self.running = False
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                continue
        
        # Cleanup
        if self.audio_enabled:
            audio_stream.stop()
            audio_stream.close()
        
        if self.cap:
            self.cap.release()
        
        cv2.destroyAllWindows()
    
    async def run(self):
        """Run the demo."""
        try:
            await self.initialize()
            await self.main_loop()
        except Exception as e:
            logger.error(f"Demo error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("\n\n" + "=" * 70)
            print("DEMO ENDED".center(70))
            print("=" * 70)


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║          EMPATHY SYSTEM - COMPLETE MULTIMODAL DEMO                ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    
This demo shows:
  📹 Real-time facial emotion detection (DeepFace)
  🎵 Voice transcription and emotion analysis (Whisper + Wav2Vec2)
  🧠 Multimodal fusion and emotional understanding
  💬 Empathetic response generation (Llama 3.1)
  🔊 Text-to-speech output (pyttsx3)

Press ENTER to start...
    """)
    
    input()
    
    demo = MultimodalDemo()
    asyncio.run(demo.run())
