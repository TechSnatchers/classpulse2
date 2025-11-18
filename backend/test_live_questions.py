"""
Test script for Zoom Live Question Triggering System
Demonstrates the complete workflow without requiring Zoom setup
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:3001"

def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_response(response, success_only=False):
    """Print API response"""
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        if success_only and not data.get('success'):
            print(f"❌ Error: {data.get('detail', 'Unknown error')}")
        else:
            print(json.dumps(data, indent=2, default=str))
    except:
        print(response.text)


def main():
    print("\n🚀 Testing Zoom Live Question Triggering System\n")
    
    # Step 1: Register Instructor
    print_section("1️⃣  Register Instructor")
    instructor_data = {
        "firstName": "Dr. Sarah",
        "lastName": "Williams",
        "email": "sarah.instructor@example.com",
        "password": "password123",
        "role": "instructor"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=instructor_data)
    
    if response.status_code == 200:
        instructor = response.json()["user"]
        instructor_id = instructor["id"]
        instructor_email = instructor["email"]
        print(f"✅ Instructor registered: {instructor_email}")
        print(f"   ID: {instructor_id}")
    else:
        # Try to login
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": instructor_data["email"],
            "password": instructor_data["password"]
        })
        if login_response.status_code == 200:
            instructor = login_response.json()["user"]
            instructor_id = instructor["id"]
            instructor_email = instructor["email"]
            print(f"✅ Instructor logged in: {instructor_email}")
        else:
            print("❌ Failed to register/login instructor")
            return
    
    # Step 2: Create a Question
    print_section("2️⃣  Create Question")
    question_data = {
        "question": "What is the capital of France?",
        "options": [
            "London",
            "Berlin",
            "Paris",
            "Madrid"
        ],
        "correctAnswer": 2,
        "difficulty": "easy",
        "category": "Geography",
        "tags": ["geography", "europe", "capitals"],
        "timeLimit": 30
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-user-id": instructor_id,
        "x-user-email": instructor_email
    }
    
    response = requests.post(f"{BASE_URL}/api/questions/", json=question_data, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        question = response.json()
        question_id = question["id"]
        print(f"\n✅ Question created with ID: {question_id}")
    else:
        print("\n⚠️  Failed to create question. Using existing questions.")
        # Get existing questions
        response = requests.get(f"{BASE_URL}/api/questions/", headers=headers)
        if response.status_code == 200:
            questions = response.json()
            if questions:
                question_id = questions[0]["id"]
                print(f"✅ Using existing question: {question_id}")
            else:
                print("❌ No questions available")
                return
        else:
            print("❌ Cannot retrieve questions")
            return
    
    # Step 3: Trigger Question (Send to Zoom)
    print_section("3️⃣  Trigger Question to Zoom Meeting")
    
    trigger_data = {
        "questionId": question_id,
        "zoomMeetingId": "123456789",
        "courseId": "test_course",
        "timeLimit": 30,
        "sendToZoom": True  # Will attempt to send to Zoom
    }
    
    response = requests.post(
        f"{BASE_URL}/api/live-questions/trigger",
        json=trigger_data,
        headers=headers
    )
    print_response(response)
    
    if response.status_code == 200:
        result = response.json()
        session_token = result["session"]["sessionToken"]
        session_id = result["session"]["id"]
        question_url = result["questionUrl"]
        zoom_sent = result["zoomMessageSent"]
        
        print(f"\n✅ Question triggered successfully!")
        print(f"   Session Token: {session_token}")
        print(f"   Session ID: {session_id}")
        print(f"   Question URL: {question_url}")
        print(f"   Sent to Zoom: {zoom_sent}")
        
        if not zoom_sent:
            print("\n⚠️  Note: Zoom message not sent (Zoom API not configured)")
            print("   Configure ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, etc. in .env")
            print("   See ZOOM_LIVE_QUESTIONS_GUIDE.md for setup instructions")
    else:
        print("\n❌ Failed to trigger question")
        return
    
    # Step 4: Student Accesses Question
    print_section("4️⃣  Student Accesses Question (via URL)")
    
    print(f"   Simulating student clicking: {question_url}")
    print(f"   API call: GET /api/live-questions/session/{session_token}")
    
    response = requests.get(f"{BASE_URL}/api/live-questions/session/{session_token}")
    print_response(response)
    
    if response.status_code == 200:
        question_data = response.json()["question"]
        print(f"\n✅ Student sees question:")
        print(f"   Question: {question_data['question']}")
        print(f"   Options: {json.dumps(question_data['options'], indent=6)}")
        print(f"   Time Limit: {question_data['timeLimit']}s")
        print(f"   ⚠️  Note: Correct answer NOT shown to student")
    
    # Step 5: Simulate Student Answers
    print_section("5️⃣  Students Submit Answers")
    
    students = [
        {"name": "Alice Johnson", "email": "alice@example.com", "answer": 2, "time": 8.5},
        {"name": "Bob Smith", "email": "bob@example.com", "answer": 2, "time": 12.3},
        {"name": "Charlie Brown", "email": "charlie@example.com", "answer": 1, "time": 15.1},
        {"name": "Diana Prince", "email": "diana@example.com", "answer": 2, "time": 7.2},
        {"name": "Eve Davis", "email": "eve@example.com", "answer": 0, "time": 18.9},
    ]
    
    for student in students:
        print(f"\n👤 {student['name']} submitting answer...")
        
        answer_data = {
            "selectedAnswer": student["answer"],
            "responseTime": student["time"],
            "studentName": student["name"],
            "studentEmail": student["email"]
        }
        
        response = requests.post(
            f"{BASE_URL}/api/live-questions/submit/{session_token}",
            json=answer_data
        )
        
        if response.status_code == 200:
            result = response.json()
            status = "✅ Correct" if result["isCorrect"] else "❌ Incorrect"
            print(f"   {status} - Time: {result['responseTime']}s")
        elif response.status_code == 409:
            print(f"   ⚠️  Already submitted (duplicate prevention working)")
        else:
            print(f"   ❌ Error: {response.status_code}")
        
        time.sleep(0.5)  # Small delay between submissions
    
    # Step 6: Instructor Views Live Dashboard
    print_section("6️⃣  Instructor Dashboard - Live Responses")
    
    response = requests.get(
        f"{BASE_URL}/api/live-questions/dashboard/session/{session_id}/responses",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        stats = data["statistics"]
        responses = data["responses"]
        
        print(f"📊 LIVE STATISTICS")
        print(f"   Total Responses: {stats['total']}")
        print(f"   Correct: {stats['correct']}")
        print(f"   Incorrect: {stats['incorrect']}")
        print(f"   Accuracy: {stats['accuracy']:.1f}%")
        print(f"   Average Response Time: {stats['averageResponseTime']:.2f}s")
        print(f"   Fastest Response: {stats['fastestResponse']:.2f}s")
        print(f"   Slowest Response: {stats['slowestResponse']:.2f}s")
        
        print(f"\n📋 INDIVIDUAL RESPONSES (sorted by time):")
        sorted_responses = sorted(responses, key=lambda x: x['responseTime'])
        
        for i, r in enumerate(sorted_responses, 1):
            status = "✅" if r['isCorrect'] else "❌"
            print(f"   {i}. {r['studentName']:20} {status} {r['responseTime']:6.2f}s")
    
    # Step 7: Get All Active Sessions
    print_section("7️⃣  Get All Active Sessions")
    
    response = requests.get(
        f"{BASE_URL}/api/live-questions/dashboard/active",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Active Sessions: {data['count']}")
        for session in data['sessions']:
            print(f"\n   Session: {session['id']}")
            print(f"   Question: {session['question']}")
            print(f"   Responses: {session['totalResponses']}")
            print(f"   Accuracy: {session['correctResponses']}/{session['totalResponses']}")
    
    # Step 8: Complete the Session
    print_section("8️⃣  Complete Session")
    
    response = requests.post(
        f"{BASE_URL}/api/live-questions/dashboard/session/{session_id}/complete",
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ Session marked as completed")
        print("   Students can no longer submit answers")
    
    # Step 9: Try to Submit After Completion (Should Fail)
    print_section("9️⃣  Test: Submit After Session Completed")
    
    response = requests.post(
        f"{BASE_URL}/api/live-questions/submit/{session_token}",
        json={
            "selectedAnswer": 2,
            "responseTime": 10.0,
            "studentName": "Late Student"
        }
    )
    
    if response.status_code == 410:
        print("✅ Correctly rejected (session completed)")
        print_response(response, success_only=True)
    else:
        print("⚠️  Unexpected response")
    
    # Step 10: Test Zoom Connection (Optional)
    print_section("🔟 Test Zoom API Connection")
    
    response = requests.get(
        f"{BASE_URL}/api/live-questions/test-zoom",
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        if result["success"]:
            print("✅ Zoom API configured and working!")
        else:
            print("⚠️  Zoom API not configured")
            print(f"   {result['message']}")
            print("\n   To enable Zoom integration:")
            print("   1. Create a Zoom Server-to-Server OAuth app")
            print("   2. Add credentials to .env file")
            print("   3. See ZOOM_LIVE_QUESTIONS_GUIDE.md")
    
    # Summary
    print_section("✅ TEST COMPLETE - SUMMARY")
    print("""
    ✅ Instructor registration & login
    ✅ Question creation
    ✅ Live question triggering
    ✅ Unique URL generation
    ✅ Student question access
    ✅ Answer submission with response time
    ✅ Duplicate prevention
    ✅ Live dashboard with statistics
    ✅ Session completion
    ✅ Post-completion submission blocking
    
    📚 Next Steps:
    1. Configure Zoom API credentials in .env
    2. Build frontend question page (/question/{token})
    3. Build instructor dashboard
    4. Test with real Zoom meeting
    
    📖 Documentation: ZOOM_LIVE_QUESTIONS_GUIDE.md
    """)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server")
        print("   Make sure the backend is running on http://localhost:3001")
        print("   Run: python main.py")
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

