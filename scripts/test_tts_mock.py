"""Test TTS using the current mock implementation with audio playback."""

import sys
sys.path.insert(0, '.')

from models.tts.voice_synthesis import MockTTS
from loguru import logger
import sounddevice as sd
import numpy as np

print("=" * 70)
print("TEXT-TO-SPEECH TEST (Mock Version)")
print("=" * 70)

# Test text
test_texts = [
    "Hello! I'm your empathy agent.",
    "I can detect your emotions and respond with care.",
    "How are you feeling today?",
]

print("\nInitializing Mock TTS...")
tts = MockTTS()

print(f"✓ TTS Type: Mock TTS (generates beeps)")
print(f"  Sample Rate: {tts.sample_rate}Hz")
print(f"  Note: This is a placeholder until real TTS is installed")

print("\n" + "=" * 70)
print("GENERATING AND PLAYING AUDIO")
print("=" * 70)

for i, text in enumerate(test_texts, 1):
    print(f"\n{i}. Text: \"{text}\"")
    
    try:
        # Synthesize
        audio = tts.synthesize(text, emotion_override=None)
        
        duration = len(audio) / tts.sample_rate
        print(f"   ✓ Generated {len(audio)} samples ({duration:.2f}s)")
        
        # Play audio (will be beeps with MockTTS)
        print("   🔊 Playing audio...")
        sd.play(audio, tts.sample_rate)
        sd.wait()
        print("   ✓ Playback complete")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
print("TEST COMPLETE!")
print("=" * 70)

print("\n📝 NOTES:")
print("  • Mock TTS generates sine wave beeps instead of speech")
print("  • Each word generates a short beep tone")
print("  • Real TTS requires Python 3.9-3.11 (Coqui TTS limitation)")
print("  • For real speech: consider pyttsx3 or edge-tts as alternatives")

print("\n🔧 Alternative TTS Options:")
print("  1. pyttsx3 - Offline, uses system TTS")
print("     Install: pip install pyttsx3")
print("  2. edge-tts - Microsoft Edge TTS (requires internet)")
print("     Install: pip install edge-tts")
print("  3. gTTS - Google TTS (requires internet)")
print("     Install: pip install gTTS")
