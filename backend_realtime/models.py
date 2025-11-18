"""
Database models and operations for live learning system
"""
from datetime import datetime
from bson import ObjectId
from database import get_db
import random


class QuestionModel:
    """Operations for questions collection"""
    
    @staticmethod
    def create_question(question_data):
        """Create a new question"""
        db = get_db()
        question_data['created_at'] = datetime.utcnow()
        result = db.questions.insert_one(question_data)
        question_data['_id'] = str(result.inserted_id)
        return question_data
    
    @staticmethod
    def get_all_questions():
        """Get all questions"""
        db = get_db()
        questions = list(db.questions.find())
        for q in questions:
            q['_id'] = str(q['_id'])
        return questions
    
    @staticmethod
    def get_random_questions(count):
        """Get random questions using MongoDB aggregation"""
        db = get_db()
        pipeline = [{'$sample': {'size': count}}]
        questions = list(db.questions.aggregate(pipeline))
        for q in questions:
            q['_id'] = str(q['_id'])
        return questions
    
    @staticmethod
    def get_question_by_id(question_id):
        """Get a specific question"""
        db = get_db()
        question = db.questions.find_one({'_id': ObjectId(question_id)})
        if question:
            question['_id'] = str(question['_id'])
        return question


class ParticipantModel:
    """Operations for participants collection"""
    
    @staticmethod
    def add_participant(student_id, meeting_id, socket_id, name=None):
        """Add or update participant"""
        db = get_db()
        participant_data = {
            'student_id': student_id,
            'meeting_id': meeting_id,
            'socket_id': socket_id,
            'name': name or f"Student {student_id}",
            'joined_at': datetime.utcnow(),
            'status': 'active'
        }
        
        result = db.participants.update_one(
            {'student_id': student_id, 'meeting_id': meeting_id},
            {'$set': participant_data},
            upsert=True
        )
        
        return participant_data
    
    @staticmethod
    def get_participants_by_meeting(meeting_id):
        """Get all active participants in a meeting"""
        db = get_db()
        participants = list(db.participants.find({
            'meeting_id': meeting_id,
            'status': 'active'
        }))
        for p in participants:
            p['_id'] = str(p['_id'])
        return participants
    
    @staticmethod
    def remove_participant(socket_id):
        """Remove participant by socket ID"""
        db = get_db()
        result = db.participants.update_one(
            {'socket_id': socket_id},
            {'$set': {'status': 'inactive', 'left_at': datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def get_participant_by_socket(socket_id):
        """Get participant by socket ID"""
        db = get_db()
        participant = db.participants.find_one({'socket_id': socket_id})
        if participant:
            participant['_id'] = str(participant['_id'])
        return participant


class StudentQuestionModel:
    """Operations for student_questions collection (assignment tracking)"""
    
    @staticmethod
    def assign_question(student_id, question_id, meeting_id):
        """Assign a question to a student"""
        db = get_db()
        assignment = {
            'student_id': student_id,
            'question_id': question_id,
            'meeting_id': meeting_id,
            'sent_time': datetime.utcnow(),
            'status': 'sent'
        }
        result = db.student_questions.insert_one(assignment)
        assignment['_id'] = str(result.inserted_id)
        return assignment
    
    @staticmethod
    def get_student_question(student_id, question_id):
        """Get specific assignment"""
        db = get_db()
        assignment = db.student_questions.find_one({
            'student_id': student_id,
            'question_id': question_id
        })
        if assignment:
            assignment['_id'] = str(assignment['_id'])
        return assignment
    
    @staticmethod
    def get_assignments_by_meeting(meeting_id):
        """Get all assignments for a meeting"""
        db = get_db()
        assignments = list(db.student_questions.find({'meeting_id': meeting_id}))
        for a in assignments:
            a['_id'] = str(a['_id'])
        return assignments


class ResponseModel:
    """Operations for responses collection"""
    
    @staticmethod
    def save_response(student_id, question_id, answer, correct, response_time=None):
        """Save student response"""
        db = get_db()
        response_data = {
            'student_id': student_id,
            'question_id': question_id,
            'answer': answer,
            'correct': correct,
            'timestamp': datetime.utcnow(),
            'response_time': response_time
        }
        result = db.responses.insert_one(response_data)
        response_data['_id'] = str(result.inserted_id)
        return response_data
    
    @staticmethod
    def get_response(student_id, question_id):
        """Get student response"""
        db = get_db()
        response = db.responses.find_one({
            'student_id': student_id,
            'question_id': question_id
        })
        if response:
            response['_id'] = str(response['_id'])
        return response
    
    @staticmethod
    def get_stats_by_question(question_id):
        """Get statistics for a question"""
        db = get_db()
        pipeline = [
            {'$match': {'question_id': question_id}},
            {'$group': {
                '_id': '$correct',
                'count': {'$sum': 1}
            }}
        ]
        stats = list(db.responses.aggregate(pipeline))
        
        total = 0
        correct = 0
        for stat in stats:
            count = stat['count']
            total += count
            if stat['_id']:  # if correct is True
                correct += count
        
        return {
            'question_id': question_id,
            'total': total,
            'correct': correct,
            'incorrect': total - correct,
            'accuracy': (correct / total * 100) if total > 0 else 0
        }
    
    @staticmethod
    def get_meeting_stats(meeting_id):
        """Get aggregated stats for entire meeting"""
        db = get_db()
        
        # Get all question IDs for this meeting
        assignments = list(db.student_questions.find({'meeting_id': meeting_id}))
        question_ids = list(set([a['question_id'] for a in assignments]))
        
        stats = []
        for qid in question_ids:
            stat = ResponseModel.get_stats_by_question(qid)
            stats.append(stat)
        
        return stats

