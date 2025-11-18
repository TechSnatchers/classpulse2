"""
Live learning routes for real-time question delivery
"""
from flask import Blueprint, request, jsonify
from models import QuestionModel, ParticipantModel, StudentQuestionModel, ResponseModel
from bson import ObjectId

live_bp = Blueprint('live', __name__, url_prefix='/api/live')


@live_bp.route('/send-random-questions', methods=['POST'])
def send_random_questions():
    """
    Trigger sending random (different) questions to all students in a meeting
    
    Request: { "meeting_id": "123" }
    Response: { "success": true, "assignments": [...] }
    """
    try:
        data = request.get_json()
        meeting_id = data.get('meeting_id')
        
        if not meeting_id:
            return jsonify({'error': 'meeting_id is required'}), 400
        
        # Get all active participants
        participants = ParticipantModel.get_participants_by_meeting(meeting_id)
        
        if not participants:
            return jsonify({'error': 'No participants found in meeting'}), 404
        
        num_students = len(participants)
        print(f"📤 Sending questions to {num_students} students...")
        
        # Get random questions (at least as many as students)
        questions = QuestionModel.get_random_questions(num_students)
        
        if len(questions) < num_students:
            return jsonify({
                'error': f'Not enough questions. Need {num_students}, have {len(questions)}'
            }), 400
        
        # Assign different question to each student
        assignments = []
        for i, participant in enumerate(participants):
            question = questions[i]
            
            # Save assignment
            assignment = StudentQuestionModel.assign_question(
                student_id=participant['student_id'],
                question_id=question['_id'],
                meeting_id=meeting_id
            )
            
            assignments.append({
                'student_id': participant['student_id'],
                'socket_id': participant['socket_id'],
                'question_id': question['_id'],
                'question': question
            })
        
        print(f"✅ Created {len(assignments)} question assignments")
        
        return jsonify({
            'success': True,
            'message': f'Questions assigned to {num_students} students',
            'assignments': assignments
        }), 200
        
    except Exception as e:
        print(f"❌ Error sending questions: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@live_bp.route('/submit-answer', methods=['POST'])
def submit_answer():
    """
    Submit student answer
    
    Request: { "student_id": "123", "question_id": "abc", "answer": 1 }
    Response: { "success": true, "correct": true }
    """
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        question_id = data.get('question_id')
        answer = data.get('answer')
        response_time = data.get('response_time')
        
        if not all([student_id, question_id, answer is not None]):
            return jsonify({'error': 'student_id, question_id, and answer are required'}), 400
        
        # Get question to check correct answer
        question = QuestionModel.get_question_by_id(question_id)
        
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        # Check if answer is correct
        correct_answer = question.get('correct')
        is_correct = (answer == correct_answer)
        
        # Save response
        response = ResponseModel.save_response(
            student_id=student_id,
            question_id=question_id,
            answer=answer,
            correct=is_correct,
            response_time=response_time
        )
        
        print(f"✅ Answer submitted: Student {student_id} -> {'✓' if is_correct else '✗'}")
        
        # Get updated stats for this question
        stats = ResponseModel.get_stats_by_question(question_id)
        
        return jsonify({
            'success': True,
            'correct': is_correct,
            'correct_answer': correct_answer,
            'response': response,
            'stats': stats
        }), 200
        
    except Exception as e:
        print(f"❌ Error submitting answer: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@live_bp.route('/stats/<meeting_id>', methods=['GET'])
def get_meeting_stats(meeting_id):
    """Get live stats for a meeting"""
    try:
        stats = ResponseModel.get_meeting_stats(meeting_id)
        
        return jsonify({
            'success': True,
            'meeting_id': meeting_id,
            'stats': stats
        }), 200
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500


@live_bp.route('/questions', methods=['POST'])
def create_question():
    """Create a new question"""
    try:
        data = request.get_json()
        
        required_fields = ['question', 'options', 'correct']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'question, options, and correct are required'}), 400
        
        question = QuestionModel.create_question(data)
        
        return jsonify({
            'success': True,
            'question': question
        }), 201
        
    except Exception as e:
        print(f"❌ Error creating question: {e}")
        return jsonify({'error': str(e)}), 500


@live_bp.route('/questions', methods=['GET'])
def get_questions():
    """Get all questions"""
    try:
        questions = QuestionModel.get_all_questions()
        
        return jsonify({
            'success': True,
            'count': len(questions),
            'questions': questions
        }), 200
        
    except Exception as e:
        print(f"❌ Error getting questions: {e}")
        return jsonify({'error': str(e)}), 500

