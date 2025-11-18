"""
Database configuration and connection for MongoDB
"""
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
import os


class Database:
    """MongoDB database wrapper for live learning system"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.questions = None
        self.participants = None
        self.student_questions = None
        self.responses = None
    
    def connect(self, mongo_uri):
        """Connect to MongoDB and initialize collections"""
        try:
            self.client = MongoClient(mongo_uri)
            # Test connection
            self.client.admin.command('ping')
            
            # Get database name from URI or use default
            db_name = mongo_uri.split('/')[-1].split('?')[0] if '/' in mongo_uri else 'live_learning'
            if not db_name:
                db_name = 'live_learning'
            
            self.db = self.client[db_name]
            
            # Initialize collections
            self.questions = self.db['questions']
            self.participants = self.db['participants']
            self.student_questions = self.db['student_questions']
            self.responses = self.db['responses']
            
            # Create indexes
            self._create_indexes()
            
            print(f"✅ Connected to MongoDB: {db_name}")
            print(f"   Collections: questions, participants, student_questions, responses")
            
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    def _create_indexes(self):
        """Create indexes for better performance"""
        try:
            # Participants indexes
            self.participants.create_index([("student_id", ASCENDING), ("meeting_id", ASCENDING)], unique=True)
            self.participants.create_index("meeting_id")
            self.participants.create_index("socket_id")
            
            # Student questions indexes
            self.student_questions.create_index([("student_id", ASCENDING), ("question_id", ASCENDING)])
            self.student_questions.create_index("meeting_id")
            self.student_questions.create_index("sent_time", DESCENDING)
            
            # Responses indexes
            self.responses.create_index([("student_id", ASCENDING), ("question_id", ASCENDING)])
            self.responses.create_index("question_id")
            self.responses.create_index("timestamp", DESCENDING)
            
            print("✅ Database indexes created")
        except Exception as e:
            print(f"⚠️  Warning: Could not create indexes: {e}")
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")


# Global database instance
db = Database()


def init_db(mongo_uri):
    """Initialize database connection"""
    db.connect(mongo_uri)


def get_db():
    """Get database instance"""
    return db

