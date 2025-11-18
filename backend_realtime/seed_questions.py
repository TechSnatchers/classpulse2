"""
Seed script to populate sample questions for testing
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Sample questions
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct": 2
    },
    {
        "question": "What is 5 + 7?",
        "options": ["10", "11", "12", "13"],
        "correct": 2
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "correct": 1
    },
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "correct": 2
    },
    {
        "question": "In what year did World War II end?",
        "options": ["1943", "1944", "1945", "1946"],
        "correct": 2
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "correct": 2
    },
    {
        "question": "How many continents are there?",
        "options": ["5", "6", "7", "8"],
        "correct": 2
    },
    {
        "question": "What is the speed of light?",
        "options": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"],
        "correct": 0
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Michelangelo"],
        "correct": 1
    },
    {
        "question": "What is the smallest prime number?",
        "options": ["0", "1", "2", "3"],
        "correct": 2
    },
    {
        "question": "Which programming language is known for its use in web development?",
        "options": ["Python", "JavaScript", "C++", "Java"],
        "correct": 1
    },
    {
        "question": "What does HTML stand for?",
        "options": [
            "Hyper Text Markup Language",
            "High Tech Modern Language",
            "Home Tool Markup Language",
            "Hyperlinks and Text Markup Language"
        ],
        "correct": 0
    },
    {
        "question": "What is the boiling point of water at sea level?",
        "options": ["90°C", "100°C", "110°C", "120°C"],
        "correct": 1
    },
    {
        "question": "Who discovered penicillin?",
        "options": ["Marie Curie", "Alexander Fleming", "Louis Pasteur", "Isaac Newton"],
        "correct": 1
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "correct": 3
    }
]

def seed_questions():
    """Seed questions into MongoDB"""
    try:
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/live_learning')
        client = MongoClient(mongo_uri)
        
        db_name = mongo_uri.split('/')[-1].split('?')[0] if '/' in mongo_uri else 'live_learning'
        db = client[db_name]
        
        # Clear existing questions
        db.questions.delete_many({})
        print(f"✅ Cleared existing questions")
        
        # Insert new questions
        result = db.questions.insert_many(questions)
        print(f"✅ Inserted {len(result.inserted_ids)} questions")
        
        print(f"\n📊 Sample questions:")
        for i, q in enumerate(questions[:5], 1):
            print(f"   {i}. {q['question']}")
        
        print(f"\n✅ Seeding complete! Total questions: {len(questions)}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error seeding questions: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    print("\n🌱 Seeding questions...")
    print("="*60)
    seed_questions()
    print("="*60)

