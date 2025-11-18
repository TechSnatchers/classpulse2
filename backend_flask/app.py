"""
Flask Backend for Zoom Live Questions
Sends live questions to Zoom participants using Zoom Chat API
"""
from flask import Flask, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import modules
from database import init_db, get_db
from zoom_webhook import webhook_bp
from routes.send_question import send_question_bp
from routes.questions import questions_bp


def create_app():
    """Create and configure Flask application"""
    
    app = Flask(__name__)
    
    # Configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # Initialize MongoDB
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/zoom_questions')
    print(f"\n🚀 Starting Flask Backend for Zoom Live Questions")
    print(f"{'='*60}")
    
    try:
        init_db(mongo_uri)
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        print(f"   Make sure MongoDB is running")
        print(f"   Connection URI: {mongo_uri}")
    
    # Register Blueprints
    app.register_blueprint(webhook_bp)
    app.register_blueprint(send_question_bp)
    app.register_blueprint(questions_bp)
    
    print(f"\n📡 Registered API Routes:")
    print(f"   - POST   /api/zoom/webhook          (Zoom webhooks)")
    print(f"   - POST   /api/send-question         (Send question to participants)")
    print(f"   - GET    /api/meetings/<id>/participants  (Get participants)")
    print(f"   - POST   /api/questions             (Create question)")
    print(f"   - GET    /api/questions             (List questions)")
    print(f"   - GET    /health                    (Health check)")
    print(f"{'='*60}\n")
    
    # Health check route
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        try:
            # Check database connection
            db = get_db()
            db.client.admin.command('ping')
            db_status = 'connected'
        except:
            db_status = 'disconnected'
        
        # Check Zoom credentials
        zoom_configured = all([
            os.getenv('ZOOM_CLIENT_ID'),
            os.getenv('ZOOM_CLIENT_SECRET'),
            os.getenv('ZOOM_ACCOUNT_ID')
        ])
        
        return jsonify({
            'status': 'ok',
            'message': 'Flask backend is running',
            'database': db_status,
            'zoom_configured': zoom_configured,
            'base_url': os.getenv('BASE_URL', 'http://localhost:5000'),
            'endpoints': {
                'webhook': '/api/zoom/webhook',
                'send_question': '/api/send-question',
                'questions': '/api/questions',
                'participants': '/api/meetings/{meeting_id}/participants'
            }
        }), 200
    
    # Root route
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint"""
        return jsonify({
            'message': 'Zoom Live Questions API',
            'version': '1.0.0',
            'documentation': {
                'health': 'GET /health',
                'webhook': 'POST /api/zoom/webhook',
                'send_question': 'POST /api/send-question',
                'questions': 'GET/POST /api/questions',
                'participants': 'GET /api/meetings/{meeting_id}/participants'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """404 error handler"""
        return jsonify({
            'error': 'Not found',
            'message': 'The requested endpoint does not exist',
            'available_endpoints': [
                'GET /health',
                'POST /api/zoom/webhook',
                'POST /api/send-question',
                'GET /api/questions',
                'POST /api/questions'
            ]
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 error handler"""
        return jsonify({
            'error': 'Internal server error',
            'message': str(error)
        }), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Get port from environment or use default
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"\n✅ Server starting on http://localhost:{port}")
    print(f"   Debug mode: {debug}")
    print(f"   Health check: http://localhost:{port}/health")
    print(f"   Webhook endpoint: http://localhost:{port}/api/zoom/webhook")
    print(f"\n💡 Configure Zoom webhook to point to:")
    print(f"   {os.getenv('BASE_URL', 'http://localhost:5000')}/api/zoom/webhook")
    print(f"\n🎯 Ready to send questions to Zoom participants!\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

