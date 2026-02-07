"""Test webhook endpoint directly to see if it's receiving requests"""
import requests
import json

url = "http://localhost:3001/api/zoom/webhook"

# Test event
test_event = {
    "event": "meeting.started",
    "event_ts": 1697461200000,
    "payload": {
        "account_id": "test_account",
        "object": {
            "id": "999888777",
            "uuid": "test-direct-uuid",
            "topic": "Direct Test Meeting",
            "host_id": "test_host_direct"
        }
    }
}

print("🧪 Testing webhook endpoint directly...")
print(f"   URL: {url}")
print(f"   Event: {test_event['event']}")
print("")

try:
    response = requests.post(
        url,
        json=test_event,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"✅ Response Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
except requests.exceptions.ConnectionError:
    print("❌ Connection Error: Backend not running!")
    print("   Start backend: python main.py")
except Exception as e:
    print(f"❌ Error: {e}")

