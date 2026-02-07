"""Seed database with initial data"""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path so we can import src
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

# Load .env file
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

from src.database.connection import connect_to_mongo, get_database
from src.models.user import UserModel
from src.models.question import Question
import hashlib


def hash_password(password: str) -> str:
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()


async def seed_users():
    """Seed default users"""
    database = get_database()
    if database is None:
        return

    # Check if users already exist
    existing_users = await database.users.count_documents({})
    if existing_users > 0:
        print("Users already exist, skipping seed")
        return

    # Create default users
    users = [
        {
            "firstName": "John",
            "lastName": "Student",
            "email": "student@example.com",
            "password": hash_password("password123"),
            "role": "student",
            "status": 1,
        },
        {
            "firstName": "Jane",
            "lastName": "Instructor",
            "email": "instructor@example.com",
            "password": hash_password("password123"),
            "role": "instructor",
            "status": 1,
        },
        {
            "firstName": "Admin",
            "lastName": "User",
            "email": "admin@example.com",
            "password": hash_password("password123"),
            "role": "admin",
            "status": 1,
        },
    ]

    for user_data in users:
        await UserModel.create(user_data)
        print(f"Created user: {user_data['email']}")


async def seed_questions():
    """Seed default questions"""
    database = get_database()
    if database is None:
        return

    # Check if questions already exist
    existing_questions = await database.questions.count_documents({})
    if existing_questions > 0:
        print("Questions already exist, skipping seed")
        return

    questions = [
        {
            "question": "What is the primary purpose of backpropagation in neural networks?",
            "options": [
                "To initialize weights randomly",
                "To update weights based on error gradients",
                "To add more layers to the network",
                "To visualize the network structure"
            ],
            "correctAnswer": 1,
            "difficulty": "medium",
            "category": "Neural Networks",
        },
        {
            "question": "Which activation function is commonly used in hidden layers?",
            "options": [
                "Sigmoid",
                "ReLU",
                "Linear",
                "Step function"
            ],
            "correctAnswer": 1,
            "difficulty": "easy",
            "category": "Neural Networks",
        },
        {
            "question": "What is the main advantage of using dropout in neural networks?",
            "options": [
                "Increases training speed",
                "Prevents overfitting",
                "Reduces model size",
                "Improves accuracy on all datasets"
            ],
            "correctAnswer": 1,
            "difficulty": "hard",
            "category": "Neural Networks",
        },
    ]

    for question_data in questions:
        await Question.create(question_data)
        print(f"Created question: {question_data['question'][:50]}...")


async def seed_database():
    """Seed all data"""
    await connect_to_mongo()
    try:
        await seed_users()
        await seed_questions()
        print("\n✅ Database seeded successfully!")
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
    finally:
        from src.database.connection import close_mongo_connection
        await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_database())

