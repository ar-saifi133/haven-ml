"""Real TTS test using pyttsx3 (Windows system voices)."""

import sys
sys.path.insert(0, '.')

from loguru import logger

print("=" * 70)
print("REAL TEXT-TO-SPEECH TEST (pyttsx3)")
print("=" * 70)

try:
    import pyttsx3
    
    print("\n✅ pyttsx3 installed successfully!")
    
    # Initialize TTS engine
    print("\nInitializing TTS engine...")
    engine = pyttsx3.init()
    
    # Get available voices
    voices = engine.getProperty('voices')
    print(f"\n📢 Available voices: {len(voices)}")
    for i, voice in enumerate(voices[:5]):  # Show first 5
        print(f"   {i+1}. {voice.name} ({voice.languages})")
    
    # Configure voice settings
    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')
    
    print(f"\n⚙️  Current settings:")
    print(f"   Speech rate: {rate} words/min")
    print(f"   Volume: {volume}")
    
    # Adjust settings for better quality
    engine.setProperty('rate', 170)  # Slightly slower for clarity
    engine.setProperty('volume', 0.9)
    
    # Test sentences with emotional context
    test_texts = [
        "Hello! I'm your empathy agent.",
        "I can detect your emotions through your facial expressions and voice.",
        "How are you feeling today?",
        "I'm here to support you with care and understanding.",
    ]
    
    print("\n" + "=" * 70)
    print("SYNTHESIZING AND PLAYING SPEECH")
    print("=" * 70)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. Speaking: \"{text}\"")
        print("   🔊 Playing...")
        
        engine.say(text)
        engine.runAndWait()
        
        print("   ✓ Complete")
    
    print("\n" + "=" * 70)
    print("✅ REAL TTS TEST COMPLETE!")
    print("=" * 70)
    
    print("\n📝 Summary:")
    print("  • Using Windows system TTS voices")
    print("  • Works offline (no internet needed)")
    print("  • Fast and reliable")
    print("  • You should have heard real speech!")
    
    print("\n💡 To change voice:")
    print("  engine.setProperty('voice', voices[index].id)")
    
except ImportError:
    print("\n❌ pyttsx3 not installed")
    print("   Install with: pip install pyttsx3")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
