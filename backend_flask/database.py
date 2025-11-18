"""
Database configuration and initialization for MongoDB
"""
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
import os


class Database:
    """MongoDB database wrapper"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.participants = None
        self.questions = None
    
    def connect(self, mongo_uri):
        """
        Connect to MongoDB and initialize collections
        
        Args:
            mongo_uri (str): MongoDB connection URI
        """
        try:
            self.client = MongoClient(mongo_uri)
            # Test connection
            self.client.admin.command('ping')
            
            # Get database name from URI or use default
            db_name = mongo_uri.split('/')[-1].split('?')[0] if '/' in mongo_uri else 'zoom_questions'
            if not db_name or db_name == '':
                db_name = 'zoom_questions'
            
            self.db = self.client[db_name]
            
            # Initialize collections
            self.participants = self.db['participants']
            self.questions = self.db['questions']
            
            # Create indexes for better performance
            self._create_indexes()
            
            print(f"✅ Connected to MongoDB successfully!")
            print(f"   Database: {db_name}")
            print(f"   Collections: participants, questions")
            
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            raise
    
    def _create_indexes(self):
        """Create indexes for collections"""
        try:
            # Index on meeting_id and user_id for participants
            self.participants.create_index([
                ("meeting_id", ASCENDING),
                ("user_id", ASCENDING)
            ], unique=True)
            
            # Index on meeting_id for faster queries
            self.participants.create_index("meeting_id")
            
            # Index on user_id
            self.participants.create_index("user_id")
            
            # Index on questions for faster retrieval
            self.questions.create_index("created_at", ASCENDING)
            
            print("✅ Database indexes created")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not create indexes: {e}")
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")
    
    def get_participants_by_meeting(self, meeting_id):
        """
        Get all participants for a specific meeting
        
        Args:
            meeting_id (str): Zoom meeting ID
            
        Returns:
            list: List of participant documents
        """
        try:
            participants = list(self.participants.find({"meeting_id": str(meeting_id)}))
            return participants
        except Exception as e:
            print(f"❌ Error fetching participants: {e}")
            return []
    
    def add_participant(self, participant_data):
        """
        Add or update a participant
        
        Args:
            participant_data (dict): Participant information
            
        Returns:
            dict: Inserted/updated participant data
        """
        try:
            # Use upsert to avoid duplicates
            result = self.participants.update_one(
                {
                    "meeting_id": participant_data["meeting_id"],
                    "user_id": participant_data["user_id"]
                },
                {"$set": participant_data},
                upsert=True
            )
            
            if result.upserted_id:
                print(f"✅ New participant added: {participant_data.get('name', 'Unknown')}")
            else:
                print(f"✅ Participant updated: {participant_data.get('name', 'Unknown')}")
            
            return participant_data
            
        except Exception as e:
            print(f"❌ Error adding participant: {e}")
            raise
    
    def remove_participant(self, meeting_id, user_id):
        """
        Remove a participant (when they leave)
        
        Args:
            meeting_id (str): Zoom meeting ID
            user_id (str): Zoom user ID
            
        Returns:
            bool: True if removed, False otherwise
        """
        try:
            result = self.participants.delete_one({
                "meeting_id": str(meeting_id),
                "user_id": str(user_id)
            })
            
            if result.deleted_count > 0:
                print(f"✅ Participant removed: {user_id}")
                return True
            else:
                print(f"⚠️  Participant not found: {user_id}")
                return False
                
        except Exception as e:
            print(f"❌ Error removing participant: {e}")
            return False
    
    def create_question(self, question_data):
        """
        Create a new question
        
        Args:
            question_data (dict): Question information
            
        Returns:
            dict: Inserted question data with _id
        """
        try:
            from datetime import datetime
            question_data['created_at'] = datetime.utcnow()
            
            result = self.questions.insert_one(question_data)
            question_data['_id'] = str(result.inserted_id)
            
            print(f"✅ Question created: {question_data.get('title', 'Untitled')}")
            return question_data
            
        except Exception as e:
            print(f"❌ Error creating question: {e}")
            raise
    
    def get_all_questions(self):
        """
        Get all questions
        
        Returns:
            list: List of all questions
        """
        try:
            questions = list(self.questions.find().sort("created_at", -1))
            # Convert ObjectId to string
            for q in questions:
                q['_id'] = str(q['_id'])
            return questions
        except Exception as e:
            print(f"❌ Error fetching questions: {e}")
            return []


# Global database instance
db = Database()


def init_db(mongo_uri):
    """
    Initialize the database connection
    
    Args:
        mongo_uri (str): MongoDB connection URI
    """
    db.connect(mongo_uri)


def get_db():
    """
    Get the database instance
    
    Returns:
        Database: Database instance
    """
    return db

