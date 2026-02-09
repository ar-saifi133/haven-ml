"""Demo using pre-recorded video file instead of webcam.

Use this for testing without webcam or on cloud platforms.
"""

import sys
sys.path.insert(0, '.')

import asyncio
import cv2
import numpy as np
from loguru import logger

from agents.empathy_agent import EmpathyAgent
from utils.display_dashboard import Dashboard


async def main(video_path: str):
    """Run demo with video file."""
    
    print("=" * 70)
    print("EMPATHY SYSTEM - VIDEO FILE DEMO")
    print("=" * 70)
    
    # Initialize
    print("\nInitializing agent...")
    agent = EmpathyAgent('demo_user', persona='remote_worker', use_mock=False)
    await agent.start_session('video_demo_001')
    
    dashboard = Dashboard()
    
    # Open video
    print(f"\nOpening video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Could not open video: {video_path}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"✓ Video loaded: {total_frames} frames @ {fps} FPS")
    
    print("\nProcessing... (Press Q to quit)\n")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("\n✓ Video ended")
            break
        
        # Process frame
        result = await agent.video_pipeline.process_frame(frame)
        
        # Display
        if result.get('face_detected'):
            emotion = result.get('primary_emotion', 'unknown')
            conf = result.get('confidence', 0)
            cv2.putText(
                frame,
                f"{emotion} ({conf:.2f})",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
        
        cv2.imshow('Video Demo', frame)
        
        # Dashboard
        dashboard.display(
            vision=result,
            status=f"Frame {frame_count}/{total_frames}"
        )
        
        frame_count += 1
        
        # Keyboard
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', default='test_video.mp4', help='Path to video file')
    args = parser.parse_args()
    
    asyncio.run(main(args.video))
