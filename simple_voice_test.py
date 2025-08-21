#!/usr/bin/env python3
"""
🗣️ SIMPLE VOICE RESPONSE TEST
Test the voice agent's speak functionality
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_voice_response():
    """Test voice response functionality"""
    print("🗣️ TESTING VOICE RESPONSE")
    print("="*40)
    
    try:
        from src.ai.voice_agent import VoiceAgent
        
        print("🔧 Creating voice agent...")
        voice_agent = VoiceAgent()
        
        print("🔧 Initializing voice system...")
        if voice_agent.initialize():
            print("✅ Voice system ready!")
            
            # Test responses
            test_messages = [
                "Hello! I am Sarus, your autonomous lab assistant robot.",
                "Voice output is working correctly.",
                "This is a test of the speech system."
            ]
            
            for i, message in enumerate(test_messages, 1):
                print(f"\n🔊 Test {i}/3:")
                voice_agent.speak_response(message)
                
                # Small pause between messages
                import time
                time.sleep(1)
            
            print("\n✅ Voice response test completed!")
            print("   You should have heard 3 spoken messages.")
            
        else:
            print("❌ Failed to initialize voice system")
            
    except Exception as e:
        print(f"❌ Error during voice test: {e}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    test_voice_response()
