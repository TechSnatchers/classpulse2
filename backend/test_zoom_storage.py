"""Test script to check if Zoom data is being stored in MongoDB"""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Load .env
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

from src.database.connection import connect_to_mongo, get_database, close_mongo_connection
from src.services.zoom_webhook_service import ZoomWebhookService


async def test_zoom_storage():
    """Test if Zoom webhook service can store data"""
    print("🔍 Testing Zoom webhook data storage...")
    print("")
    
    # Connect to database
    await connect_to_mongo()
    database = get_database()
    
    if database is None:
        print("❌ Database not connected!")
        return
    
    print("✅ Database connected")
    print("")
    
    # Test event
    test_event = {
        "event": "meeting.started",
        "event_ts": 1697461200000,
        "payload": {
            "account_id": "test_account",
            "object": {
                "id": "123456789",
                "uuid": "test-uuid-12345",
                "topic": "Test Learning Session",
                "host_id": "test_host_123"
            }
        }
    }
    
    print("📤 Sending test event...")
    print(f"   Event: {test_event['event']}")
    print(f"   Meeting ID: {test_event['payload']['object']['id']}")
    print("")
    
    # Process event
    service = ZoomWebhookService()
    result = await service.handle_event(test_event)
    
    print("📥 Result:")
    print(f"   Status: {result.get('status')}")
    print(f"   Message: {result.get('message')}")
    print("")
    
    # Check if data was stored
    print("🔍 Checking database...")
    
    # Check zoom_meetings collection
    meetings_count = await database.zoom_meetings.count_documents({})
    print(f"   Total meetings in database: {meetings_count}")
    
    if meetings_count > 0:
        latest_meeting = await database.zoom_meetings.find_one(
            sort=[("created_at", -1)]
        )
        print(f"   Latest meeting: {latest_meeting.get('topic', 'N/A')}")
        print(f"   Meeting ID: {latest_meeting.get('zoom_meeting_id', 'N/A')}")
    
    # Check zoom_participants collection
    participants_count = await database.zoom_participants.count_documents({})
    print(f"   Total participants in database: {participants_count}")
    
    # Check zoom_recordings collection
    recordings_count = await database.zoom_recordings.count_documents({})
    print(f"   Total recordings in database: {recordings_count}")
    
    print("")
    
    # List all collections
    collections = await database.list_collection_names()
    print(f"📋 All collections: {', '.join(collections)}")
    
    await close_mongo_connection()
    
    if result.get("status") == "success":
        print("")
        print("✅ Test passed! Data should be stored.")
    else:
        print("")
        print(f"❌ Test failed: {result.get('message', 'Unknown error')}")


if __name__ == "__main__":
    asyncio.run(test_zoom_storage())

