#!/usr/bin/env python3
"""
🔊 VOICE SYSTEM TEST - Test Text-to-Speech
Simple test to verify voice output is working
"""

def test_voice_system():
    """Test if text-to-speech is working"""
    print("🔊 TESTING VOICE SYSTEM")
    print("="*40)
    
    try:
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
        
        # Initialize TTS engine
        engine = pyttsx3.init()
        print("✅ TTS engine initialized")
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"📢 Available voices: {len(voices) if voices else 0}")
        
        if voices:
            for i, voice in enumerate(voices):
                print(f"  Voice {i}: {voice.name} ({voice.id})")
        
        # Test speech
        print("\n🎤 Testing speech output...")
        print("You should hear: 'Hello, this is Sarus robot speaking!'")
        
        engine.say("Hello, this is Sarus robot speaking!")
        engine.runAndWait()
        
        print("✅ Voice test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Voice test failed: {e}")
        return False

def test_speech_recognition():
    """Test if speech recognition is working"""
    print("\n🎤 TESTING SPEECH RECOGNITION")
    print("="*40)
    
    try:
        import speech_recognition as sr
        print("✅ speech_recognition imported successfully")
        
        # Initialize recognizer
        r = sr.Recognizer()
        mic = sr.Microphone()
        print("✅ Speech recognition initialized")
        
        print("🎤 Say something (you have 3 seconds)...")
        
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=3)
        
        try:
            text = r.recognize_google(audio)
            print(f"✅ You said: {text}")
            return True
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return False
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Speech recognition test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 SARUS VOICE SYSTEM DIAGNOSTIC TEST")
    print("="*50)
    
    # Test TTS first
    tts_working = test_voice_system()
    
    # Test speech recognition
    sr_working = test_speech_recognition()
    
    print("\n📊 DIAGNOSTIC RESULTS:")
    print("="*30)
    print(f"🔊 Text-to-Speech: {'✅ Working' if tts_working else '❌ Failed'}")
    print(f"🎤 Speech Recognition: {'✅ Working' if sr_working else '❌ Failed'}")
    
    if tts_working and sr_working:
        print("\n🎉 Both voice systems are working!")
    else:
        print("\n⚠️ Some voice systems need fixing")
    
    input("\nPress Enter to exit...")
