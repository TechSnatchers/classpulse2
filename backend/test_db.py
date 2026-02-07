"""Test script to verify MongoDB Atlas connection and database operations"""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Load .env file
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

from src.database.connection import connect_to_mongo, get_database, close_mongo_connection
from src.models.user import UserModel
from src.models.question import Question


async def test_database():
    """Test database connection and operations"""
    print("=" * 60)
    print("MongoDB Atlas Database Test")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Connect to database
        print("1️⃣ Testing database connection...")
        await connect_to_mongo()
        print("   ✅ Connection successful!")
        print()
        
        # Test 2: Check database object
        print("2️⃣ Checking database object...")
        database = get_database()
        if database is None:
            print("   ❌ Database object is None")
            return
        print(f"   ✅ Database object: {database.name}")
        print()
        
        # Test 3: List collections
        print("3️⃣ Listing collections...")
        collections = await database.list_collection_names()
        print(f"   ✅ Found {len(collections)} collections:")
        for col in collections:
            count = await database[col].count_documents({})
            print(f"      - {col}: {count} documents")
        print()
        
        # Test 4: Test User queries
        print("4️⃣ Testing User queries...")
        user = await UserModel.find_by_email("student@example.com")
        if user:
            print(f"   ✅ Found user: {user.get('firstName')} {user.get('lastName')} ({user.get('email')})")
        else:
            print("   ⚠️  No user found with email: student@example.com")
        print()
        
        # Test 5: Test Question queries
        print("5️⃣ Testing Question queries...")
        questions = await Question.find_all()
        print(f"   ✅ Found {len(questions)} questions")
        if questions:
            print(f"      Example: {questions[0].get('question', 'N/A')[:50]}...")
        print()
        
        # Test 6: Test database ping
        print("6️⃣ Testing database ping...")
        result = await database.client.admin.command('ping')
        print(f"   ✅ Ping successful: {result}")
        print()
        
        print("=" * 60)
        print("✅ All database tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(test_database())

