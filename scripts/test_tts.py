"""Simple TTS test script."""

import sys
sys.path.insert(0, '.')

from models.tts.voice_synthesis import CosyVoiceTTS, MockTTS
from loguru import logger
import sounddevice as sd
import numpy as np

print("=" * 70)
print("TEXT-TO-SPEECH TEST")
print("=" * 70)

# Test text
test_texts = [
    "Hello! I'm your empathy agent.",
    "I can detect your emotions and respond with care.",
    "How are you feeling today?",
]

print("\nAttempting to load TTS...")

try:
    # Try to load real TTS
    tts = CosyVoiceTTS(device='cpu')
    print("✅ Real TTS loaded successfully!")
    tts_type = "Real CosyVoice TTS"
except Exception as e:
    print(f"⚠️  Real TTS failed: {e}")
    print("Using MockTTS instead")
    tts = MockTTS()
    tts_type = "Mock TTS"

print(f"\nTTS Type: {tts_type}")
print(f"Sample Rate: {tts.sample_rate}Hz")

print("\n" + "=" * 70)
print("SYNTHESIZING SPEECH")
print("=" * 70)

for i, text in enumerate(test_texts, 1):
    print(f"\n{i}. Text: \"{text}\"")
    
    try:
        # Synthesize
        audio = tts.synthesize(text, emotion_override=None)
        
        print(f"   ✓ Generated {len(audio)} samples ({len(audio)/tts.sample_rate:.2f}s)")
        
        # Play audio
        print("   🔊 Playing audio...")
        sd.play(audio, tts.sample_rate)
        sd.wait()
        print("   ✓ Playback complete")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("TTS TEST COMPLETE!")
print("=" * 70)

if isinstance(tts, MockTTS):
    print("\n⚠️  Note: Using mock TTS (just beeps, no real speech)")
    print("   Real TTS requires: pip install TTS")
else:
    print("\n✅ Real TTS is working! You should have heard speech.")
