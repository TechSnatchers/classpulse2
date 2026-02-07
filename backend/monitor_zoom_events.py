"""Monitor Zoom webhook events in real-time"""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

from src.database.connection import connect_to_mongo, get_database, close_mongo_connection


async def monitor_events():
    """Monitor Zoom events in database"""
    await connect_to_mongo()
    database = get_database()
    
    if database is None:
        print("❌ Database not connected!")
        return
    
    print("🔍 Monitoring Zoom Events in MongoDB...")
    print("   (Press Ctrl+C to stop)")
    print("")
    
    last_meeting_count = 0
    last_participant_count = 0
    
    try:
        while True:
            # Check meetings
            meetings_count = await database.zoom_meetings.count_documents({})
            if meetings_count != last_meeting_count:
                print(f"📊 New meeting! Total: {meetings_count}")
                last_meeting = await database.zoom_meetings.find_one(sort=[("created_at", -1)])
                if last_meeting:
                    print(f"   Topic: {last_meeting.get('topic', 'N/A')}")
                    print(f"   Meeting ID: {last_meeting.get('zoom_meeting_id', 'N/A')}")
                    print(f"   Status: {last_meeting.get('status', 'N/A')}")
                last_meeting_count = meetings_count
                print("")
            
            # Check participants
            participants_count = await database.zoom_participants.count_documents({})
            if participants_count != last_participant_count:
                print(f"👥 New participant! Total: {participants_count}")
                last_participant = await database.zoom_participants.find_one(sort=[("created_at", -1)])
                if last_participant:
                    print(f"   Name: {last_participant.get('user_name', 'N/A')}")
                    print(f"   Meeting ID: {last_participant.get('zoom_meeting_id', 'N/A')}")
                    print(f"   Join Time: {last_participant.get('join_time', 'N/A')}")
                last_participant_count = participants_count
                print("")
            
            await asyncio.sleep(2)  # Check every 2 seconds
            
    except KeyboardInterrupt:
        print("\n✅ Monitoring stopped")
        await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(monitor_events())

