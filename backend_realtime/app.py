"""
Real-time Live Learning System with Flask-SocketIO
Each student receives a different question when instructor triggers
"""
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from dotenv import load_dotenv
import os
import eventlet

# Monkey patch for eventlet
eventlet.monkey_patch()

# Load environment variables
load_dotenv()

# Import database and models
from database import init_db, get_db
from models import ParticipantModel, QuestionModel, ResponseModel
from routes.live import live_bp

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Initialize MongoDB
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/live_learning')
init_db(mongo_uri)

# Register blueprints
app.register_blueprint(live_bp)

# Socket ID to Student ID mapping
socket_to_student = {}


@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Real-time Live Learning System',
        'version': '1.0.0',
        'endpoints': {
            'student': '/student',
            'instructor': '/instructor',
            'api': '/api/live'
        }
    })


@app.route('/student')
def student_page():
    """Student page"""
    return render_template('student.html')


@app.route('/instructor')
def instructor_page():
    """Instructor page"""
    return render_template('instructor.html')


@app.route('/health')
def health():
    """Health check"""
    try:
        db = get_db()
        db.client.admin.command('ping')
        db_status = 'connected'
    except:
        db_status = 'disconnected'
    
    return jsonify({
        'status': 'ok',
        'database': db_status,
        'socketio': 'active'
    })


# Socket.IO Event Handlers

@socketio.on('connect')
def handle_connect():
    """Client connected"""
    print(f"🔌 Client connected: {request.sid}")
    emit('connected', {'socket_id': request.sid})


@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    print(f"🔌 Client disconnected: {request.sid}")
    
    # Remove from participants
    student_id = socket_to_student.get(request.sid)
    if student_id:
        ParticipantModel.remove_participant(request.sid)
        del socket_to_student[request.sid]
        print(f"   Removed student: {student_id}")


@socketio.on('join_student')
def handle_join_student(data):
    """
    Student joins the system
    Data: { student_id, meeting_id, name }
    """
    try:
        student_id = data.get('student_id')
        meeting_id = data.get('meeting_id')
        name = data.get('name', f'Student {student_id}')
        
        if not student_id or not meeting_id:
            emit('error', {'message': 'student_id and meeting_id required'})
            return
        
        # Add to participants collection
        participant = ParticipantModel.add_participant(
            student_id=student_id,
            meeting_id=meeting_id,
            socket_id=request.sid,
            name=name
        )
        
        # Store mapping
        socket_to_student[request.sid] = student_id
        
        # Join student's personal room (for targeted messages)
        join_room(request.sid)
        
        # Join meeting room
        join_room(f"meeting_{meeting_id}")
        
        # Join instructor room (for receiving updates)
        join_room(f"instructor_{meeting_id}")
        
        print(f"✅ Student joined: {name} ({student_id}) in meeting {meeting_id}")
        print(f"   Socket: {request.sid}")
        
        emit('joined', {
            'success': True,
            'student_id': student_id,
            'meeting_id': meeting_id,
            'socket_id': request.sid
        })
        
        # Notify instructor
        emit('student_joined', {
            'student_id': student_id,
            'name': name,
            'meeting_id': meeting_id
        }, room=f"instructor_{meeting_id}")
        
    except Exception as e:
        print(f"❌ Error in join_student: {e}")
        emit('error', {'message': str(e)})


@socketio.on('join_instructor')
def handle_join_instructor(data):
    """
    Instructor joins the system
    Data: { instructor_id, meeting_id }
    """
    try:
        instructor_id = data.get('instructor_id')
        meeting_id = data.get('meeting_id')
        
        if not instructor_id or not meeting_id:
            emit('error', {'message': 'instructor_id and meeting_id required'})
            return
        
        # Join instructor room
        join_room(f"instructor_{meeting_id}")
        
        print(f"✅ Instructor joined: {instructor_id} for meeting {meeting_id}")
        
        emit('instructor_joined', {
            'success': True,
            'instructor_id': instructor_id,
            'meeting_id': meeting_id
        })
        
    except Exception as e:
        print(f"❌ Error in join_instructor: {e}")
        emit('error', {'message': str(e)})


@socketio.on('trigger_questions')
def handle_trigger_questions(data):
    """
    Instructor triggers sending random questions to all students
    Data: { meeting_id }
    """
    try:
        meeting_id = data.get('meeting_id')
        
        if not meeting_id:
            emit('error', {'message': 'meeting_id required'})
            return
        
        print(f"\n🚀 Triggering questions for meeting: {meeting_id}")
        
        # Get all participants
        participants = ParticipantModel.get_participants_by_meeting(meeting_id)
        
        if not participants:
            emit('error', {'message': 'No participants found'})
            return
        
        num_students = len(participants)
        print(f"   Found {num_students} students")
        
        # Get random questions
        questions = QuestionModel.get_random_questions(num_students)
        
        if len(questions) < num_students:
            emit('error', {
                'message': f'Not enough questions. Need {num_students}, have {len(questions)}'
            })
            return
        
        # Assign and send different question to each student
        from models import StudentQuestionModel
        
        assignments = []
        for i, participant in enumerate(participants):
            question = questions[i]
            
            # Save assignment
            StudentQuestionModel.assign_question(
                student_id=participant['student_id'],
                question_id=question['_id'],
                meeting_id=meeting_id
            )
            
            # Send question to this specific student
            question_data = {
                'question_id': question['_id'],
                'question': question['question'],
                'options': question['options'],
                'sent_time': str(datetime.utcnow())
            }
            
            # Emit to specific student's socket
            socketio.emit('NEW_QUESTION', question_data, room=participant['socket_id'])
            
            print(f"   ✅ Sent Q#{i+1} to {participant['name']} ({participant['student_id']})")
            
            assignments.append({
                'student_id': participant['student_id'],
                'student_name': participant['name'],
                'question_id': question['_id']
            })
        
        print(f"\n✅ All questions sent to {num_students} students!\n")
        
        # Notify instructor
        emit('questions_sent', {
            'success': True,
            'count': num_students,
            'assignments': assignments
        }, room=f"instructor_{meeting_id}")
        
    except Exception as e:
        print(f"❌ Error triggering questions: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': str(e)})


@socketio.on('submit_answer_ws')
def handle_submit_answer_ws(data):
    """
    Student submits answer via WebSocket
    Data: { student_id, question_id, answer, response_time }
    """
    try:
        student_id = data.get('student_id')
        question_id = data.get('question_id')
        answer = data.get('answer')
        response_time = data.get('response_time')
        
        if not all([student_id, question_id, answer is not None]):
            emit('error', {'message': 'Missing required fields'})
            return
        
        # Get question
        question = QuestionModel.get_question_by_id(question_id)
        
        if not question:
            emit('error', {'message': 'Question not found'})
            return
        
        # Check correctness
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
        
        print(f"✅ Answer: Student {student_id} -> {'✓ Correct' if is_correct else '✗ Wrong'}")
        
        # Send result back to student
        emit('answer_result', {
            'correct': is_correct,
            'correct_answer': correct_answer,
            'your_answer': answer
        })
        
        # Get updated stats
        stats = ResponseModel.get_stats_by_question(question_id)
        
        # Get participant info
        participant = ParticipantModel.get_participant_by_socket(request.sid)
        meeting_id = participant.get('meeting_id') if participant else None
        
        # Send update to instructor
        if meeting_id:
            emit('ANSWER_UPDATE', {
                'student_id': student_id,
                'student_name': participant.get('name', student_id),
                'question_id': question_id,
                'answer': answer,
                'correct': is_correct,
                'stats': stats,
                'timestamp': str(datetime.utcnow())
            }, room=f"instructor_{meeting_id}")
        
    except Exception as e:
        print(f"❌ Error submitting answer: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': str(e)})


if __name__ == '__main__':
    from datetime import datetime
    
    port = int(os.getenv('PORT', 5000))
    
    print("\n" + "="*60)
    print("🚀 Real-time Live Learning System Starting...")
    print("="*60)
    print(f"   Port: {port}")
    print(f"   Student UI: http://localhost:{port}/student")
    print(f"   Instructor UI: http://localhost:{port}/instructor")
    print(f"   WebSocket: Active (Socket.IO)")
    print("="*60 + "\n")
    
    # Run with eventlet
    socketio.run(app, host='0.0.0.0', port=port, debug=True)

