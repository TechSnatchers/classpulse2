"""Quick script to check if Zoom data exists in MongoDB"""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

from src.database.connection import connect_to_mongo, get_database, close_mongo_connection


async def check_data():
    """Check what Zoom data exists in MongoDB"""
    await connect_to_mongo()
    database = get_database()
    
    if database is None:
        print("❌ Database not connected!")
        return
    
    print("🔍 Checking Zoom data in MongoDB...")
    print("")
    
    # Check meetings
    meetings_count = await database.zoom_meetings.count_documents({})
    print(f"📊 Meetings: {meetings_count}")
    if meetings_count > 0:
        meetings = []
        async for meeting in database.zoom_meetings.find().sort("created_at", -1).limit(5):
            meetings.append(meeting)
        for m in meetings:
            print(f"   - {m.get('topic', 'N/A')} (ID: {m.get('zoom_meeting_id', 'N/A')})")
    
    # Check participants
    participants_count = await database.zoom_participants.count_documents({})
    print(f"👥 Participants: {participants_count}")
    
    # Check recordings
    recordings_count = await database.zoom_recordings.count_documents({})
    print(f"🎥 Recordings: {recordings_count}")
    
    print("")
    
    # List all collections
    collections = await database.list_collection_names()
    print(f"📋 Collections: {', '.join(collections)}")
    
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(check_data())

