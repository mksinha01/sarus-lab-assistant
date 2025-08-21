#!/usr/bin/env python3
"""
Test script for Gemini API integration in Sarus Robot
"""
import asyncio
import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))
sys.path.insert(0, str(project_root))

# Set environment before importing
from dotenv import load_dotenv
load_dotenv()

from src.ai.llm_manager import LLMManager

async def test_gemini():
    """Test Gemini API integration"""
    print("🧠 Testing Gemini Integration for Sarus Robot")
    print("=" * 50)
    
    try:
        # Initialize LLM manager
        print("Initializing LLM Manager...")
        llm_manager = LLMManager()
        await llm_manager.initialize()
        
        # Test basic query
        print("\n🤖 Testing basic query...")
        test_query = "Hello! I'm Sarus, a lab assistant robot. Please introduce yourself briefly."
        
        response = await llm_manager.process_command(test_query)
        print(f"Gemini Response: {response}")
        
        # Test robot-specific query
        print("\n🔬 Testing robot-specific query...")
        robot_query = "What can you help me with as a lab assistant robot?"
        
        response2 = await llm_manager.process_command(robot_query)
        print(f"Robot Query Response: {response2}")
        
        print("\n✅ Gemini integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY environment variable not set!")
        print("Make sure your .env file contains: GEMINI_API_KEY=your_api_key")
        sys.exit(1)
    
    # Run the test
    asyncio.run(test_gemini())
