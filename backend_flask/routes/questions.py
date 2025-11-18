"""
Questions CRUD endpoints
Create and manage questions
"""
from flask import Blueprint, request, jsonify
from database import get_db


# Create Blueprint
questions_bp = Blueprint('questions', __name__, url_prefix='/api')


@questions_bp.route('/questions', methods=['POST'])
def create_question():
    """
    Create a new question
    
    Request JSON:
    {
        "title": "Question Title",
        "question_text": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct_answer": 2,
        "time_limit": 30,
        "points": 10
    }
    
    Returns:
        JSON response with created question
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['title', 'question_text']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create question document
        question_data = {
            'title': data.get('title'),
            'question_text': data.get('question_text'),
            'options': data.get('options', []),
            'correct_answer': data.get('correct_answer'),
            'time_limit': data.get('time_limit', 30),
            'points': data.get('points', 10),
            'difficulty': data.get('difficulty', 'medium'),
            'category': data.get('category', 'general'),
            'tags': data.get('tags', [])
        }
        
        # Save to database
        db = get_db()
        created_question = db.create_question(question_data)
        
        return jsonify({
            'success': True,
            'message': 'Question created successfully',
            'question': created_question
        }), 201
    
    except Exception as e:
        print(f"❌ Error creating question: {e}")
        return jsonify({'error': str(e)}), 500


@questions_bp.route('/questions', methods=['GET'])
def get_all_questions():
    """
    Get all questions
    
    Returns:
        JSON response with list of all questions
    """
    try:
        db = get_db()
        questions = db.get_all_questions()
        
        return jsonify({
            'success': True,
            'count': len(questions),
            'questions': questions
        }), 200
    
    except Exception as e:
        print(f"❌ Error getting questions: {e}")
        return jsonify({'error': str(e)}), 500


@questions_bp.route('/questions/<question_id>', methods=['GET'])
def get_question_by_id(question_id):
    """
    Get a specific question by ID
    
    Args:
        question_id (str): Question ID
        
    Returns:
        JSON response with question details
    """
    try:
        from bson import ObjectId
        
        db = get_db()
        question = db.questions.find_one({'_id': ObjectId(question_id)})
        
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        # Convert ObjectId to string
        question['_id'] = str(question['_id'])
        
        return jsonify({
            'success': True,
            'question': question
        }), 200
    
    except Exception as e:
        print(f"❌ Error getting question: {e}")
        return jsonify({'error': str(e)}), 500


@questions_bp.route('/questions/<question_id>', methods=['PUT'])
def update_question(question_id):
    """
    Update a question
    
    Args:
        question_id (str): Question ID
        
    Request JSON:
        Updated question fields
        
    Returns:
        JSON response with updated question
    """
    try:
        from bson import ObjectId
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        db = get_db()
        
        # Update question
        result = db.questions.update_one(
            {'_id': ObjectId(question_id)},
            {'$set': data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'Question not found'}), 404
        
        # Get updated question
        question = db.questions.find_one({'_id': ObjectId(question_id)})
        question['_id'] = str(question['_id'])
        
        return jsonify({
            'success': True,
            'message': 'Question updated successfully',
            'question': question
        }), 200
    
    except Exception as e:
        print(f"❌ Error updating question: {e}")
        return jsonify({'error': str(e)}), 500


@questions_bp.route('/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    """
    Delete a question
    
    Args:
        question_id (str): Question ID
        
    Returns:
        JSON response confirming deletion
    """
    try:
        from bson import ObjectId
        
        db = get_db()
        
        result = db.questions.delete_one({'_id': ObjectId(question_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Question not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Question deleted successfully'
        }), 200
    
    except Exception as e:
        print(f"❌ Error deleting question: {e}")
        return jsonify({'error': str(e)}), 500

