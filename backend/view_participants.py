"""View detailed participant information from MongoDB"""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

from src.database.connection import connect_to_mongo, get_database, close_mongo_connection
import json


async def view_participants():
    """View all participants with details"""
    await connect_to_mongo()
    database = get_database()
    
    if database is None:
        print("❌ Database not connected!")
        return
    
    print("👥 Zoom Participants in MongoDB")
    print("=" * 60)
    print("")
    
    # Get all participants
    participants_count = await database.zoom_participants.count_documents({})
    print(f"📊 Total Participants: {participants_count}")
    print("")
    
    if participants_count == 0:
        print("⚠️  No participants found in database")
        print("")
        print("💡 This means:")
        print("   - Participant events not being received")
        print("   - Or events not being stored")
        print("   - Check backend terminal for participant.joined events")
        print("")
        await close_mongo_connection()
        return
    
    # Get all participants with details
    participants = []
    async for p in database.zoom_participants.find():
        participants.append(p)
    
    print("📋 Participant Details:")
    print("")
    
    for i, p in enumerate(participants, 1):
        print(f"{i}. Participant:")
        print(f"   Name: {p.get('user_name', 'N/A')}")
        print(f"   User ID: {p.get('user_id', 'N/A')}")
        print(f"   Email: {p.get('email', 'N/A')}")
        print(f"   Meeting ID: {p.get('zoom_meeting_id', 'N/A')}")
        print(f"   Join Time: {p.get('join_time', 'N/A')}")
        print(f"   Leave Time: {p.get('leave_time', 'N/A')}")
        print(f"   Created: {p.get('created_at', 'N/A')}")
        print("")
    
    # Group by meeting
    print("=" * 60)
    print("📊 Participants by Meeting:")
    print("")
    
    meetings = {}
    for p in participants:
        meeting_id = p.get('zoom_meeting_id', 'Unknown')
        if meeting_id not in meetings:
            meetings[meeting_id] = []
        meetings[meeting_id].append(p)
    
    for meeting_id, meeting_participants in meetings.items():
        print(f"Meeting ID: {meeting_id}")
        print(f"   Participants: {len(meeting_participants)}")
        for p in meeting_participants:
            print(f"   - {p.get('user_name', 'N/A')} ({p.get('user_id', 'N/A')})")
        print("")
    
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(view_participants())

