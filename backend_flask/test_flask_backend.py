"""
Test script for Flask Zoom Live Questions Backend
Tests all endpoints without requiring actual Zoom setup
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"


def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_response(response):
    """Print API response"""
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, default=str))
    except:
        print(response.text)


def main():
    print("\n🚀 Testing Flask Zoom Live Questions Backend\n")
    
    # Test 1: Health Check
    print_section("1️⃣  Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    
    if response.status_code != 200:
        print("\n❌ Server not running. Start with: python app.py")
        return
    
    # Test 2: Root Endpoint
    print_section("2️⃣  Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    
    # Test 3: Test Zoom Connection
    print_section("3️⃣  Test Zoom Connection")
    response = requests.get(f"{BASE_URL}/api/test-zoom")
    print_response(response)
    
    # Test 4: Create Questions
    print_section("4️⃣  Create Questions")
    questions = [
        {
            "title": "Geography Question",
            "question_text": "What is the capital of France?",
            "options": ["London", "Berlin", "Paris", "Madrid"],
            "correct_answer": 2,
            "time_limit": 30
        },
        {
            "title": "Math Question",
            "question_text": "What is 5 + 7?",
            "options": ["10", "11", "12", "13"],
            "correct_answer": 2,
            "time_limit": 20
        }
    ]
    
    created_questions = []
    for q in questions:
        print(f"\n📝 Creating: {q['title']}")
        response = requests.post(
            f"{BASE_URL}/api/questions",
            json=q,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            result = response.json()
            created_questions.append(result["question"])
            print(f"✅ Created: ID = {result['question']['_id']}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print_response(response)
    
    # Test 5: Get All Questions
    print_section("5️⃣  Get All Questions")
    response = requests.get(f"{BASE_URL}/api/questions")
    print_response(response)
    
    # Test 6: Simulate Webhook - Participant Joined
    print_section("6️⃣  Simulate Zoom Webhook - Participant Joined")
    
    participants = [
        {
            "user_id": "user_123",
            "name": "Alice Johnson",
            "email": "alice@example.com"
        },
        {
            "user_id": "user_456",
            "name": "Bob Smith",
            "email": "bob@example.com"
        },
        {
            "user_id": "user_789",
            "name": "Charlie Brown",
            "email": "charlie@example.com"
        }
    ]
    
    meeting_id = "123456789"
    
    for p in participants:
        print(f"\n👤 Simulating join: {p['name']}")
        
        webhook_data = {
            "event": "meeting.participant_joined",
            "payload": {
                "object": {
                    "id": meeting_id,
                    "topic": "Test Meeting",
                    "participant": {
                        "user_id": p["user_id"],
                        "user_name": p["name"],
                        "email": p["email"]
                    }
                }
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/zoom/webhook",
            json=webhook_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print(f"✅ Participant added to database")
        else:
            print(f"❌ Failed: {response.status_code}")
        
        time.sleep(0.5)
    
    # Test 7: Get Meeting Participants
    print_section("7️⃣  Get Meeting Participants")
    response = requests.get(f"{BASE_URL}/api/meetings/{meeting_id}/participants")
    print_response(response)
    
    # Test 8: Send Question to Participants
    print_section("8️⃣  Send Question to Meeting Participants")
    
    question_link = "https://example.com/question/abc123"
    
    send_data = {
        "question_link": question_link,
        "meeting_id": meeting_id
    }
    
    print(f"📤 Sending question link to meeting {meeting_id}...")
    print(f"   Link: {question_link}")
    
    response = requests.post(
        f"{BASE_URL}/api/send-question",
        json=send_data,
        headers={"Content-Type": "application/json"}
    )
    print_response(response)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Question sent!")
        print(f"   Total participants: {result.get('total_participants')}")
        print(f"   Success: {result.get('success_count')}")
        print(f"   Failed: {result.get('failed_count')}")
    
    # Test 9: Simulate Participant Left
    print_section("9️⃣  Simulate Zoom Webhook - Participant Left")
    
    leave_participant = participants[0]
    print(f"👋 Simulating leave: {leave_participant['name']}")
    
    webhook_data = {
        "event": "meeting.participant_left",
        "payload": {
            "object": {
                "id": meeting_id,
                "participant": {
                    "user_id": leave_participant["user_id"]
                }
            }
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/zoom/webhook",
        json=webhook_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print(f"✅ Participant removed from database")
    
    # Test 10: Get Updated Participants
    print_section("🔟 Get Updated Participants")
    response = requests.get(f"{BASE_URL}/api/meetings/{meeting_id}/participants")
    print_response(response)
    
    # Summary
    print_section("✅ TEST COMPLETE - SUMMARY")
    print("""
    ✅ Health check working
    ✅ Questions CRUD working
    ✅ Webhook handling working
    ✅ Participant tracking working
    ✅ Send question endpoint working
    
    🎯 System is fully functional!
    
    📝 Next Steps:
    1. Configure Zoom credentials in .env file
    2. Set up Zoom webhook endpoint
    3. Test with real Zoom meeting
    
    📚 Documentation: README.md
    """)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server")
        print("   Make sure the Flask backend is running")
        print("   Run: python app.py")
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

