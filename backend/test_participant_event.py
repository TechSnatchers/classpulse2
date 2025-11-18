"""Test participant event handling"""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

from src.database.connection import connect_to_mongo, get_database, close_mongo_connection
from src.services.zoom_webhook_service import ZoomWebhookService


async def test_participant_events():
    """Test participant event handling"""
    print("🧪 Testing Participant Events...")
    print("")
    
    await connect_to_mongo()
    
    service = ZoomWebhookService()
    
    # Test participant.joined
    print("1️⃣ Testing participant.joined...")
    joined_event = {
        "event": "participant.joined",
        "event_ts": 1697461200000,
        "payload": {
            "account_id": "test_account",
            "object": {
                "id": "123456789",
                "uuid": "test-uuid",
                "participant": {
                    "user_id": "user123",
                    "user_name": "John Doe",
                    "email": "john@example.com"
                }
            }
        }
    }
    
    result = await service.handle_event(joined_event)
    print(f"   Result: {result}")
    print("")
    
    # Test participant.left
    print("2️⃣ Testing participant.left...")
    left_event = {
        "event": "participant.left",
        "event_ts": 1697461300000,
        "payload": {
            "account_id": "test_account",
            "object": {
                "id": "123456789",
                "uuid": "test-uuid",
                "participant": {
                    "user_id": "user123",
                    "user_name": "John Doe",
                    "email": "john@example.com"
                }
            }
        }
    }
    
    result = await service.handle_event(left_event)
    print(f"   Result: {result}")
    print("")
    
    # Check database
    database = get_database()
    if database is not None:
        participants_count = await database.zoom_participants.count_documents({})
        print(f"📊 Total participants in database: {participants_count}")
        
        if participants_count > 0:
            participants = []
            async for p in database.zoom_participants.find().limit(5):
                participants.append(p)
            for p in participants:
                print(f"   - {p.get('user_name', 'N/A')} (Meeting: {p.get('zoom_meeting_id', 'N/A')})")
    
    await close_mongo_connection()
    print("")
    print("✅ Test complete!")


if __name__ == "__main__":
    asyncio.run(test_participant_events())

