import logging
from flask import Flask
from flask_socketio import SocketIO
from app.classifier import ClassiferSingleton

# Create the SocketIO instance at module level
socketio = SocketIO()

def create_app():
    app = Flask(__name__, template_folder='templates')
    configure_logging()
    load_classifier()
    
    # Import the routes Blueprint
    from app.routes import routes
    app.register_blueprint(routes)
    
    # Initialize SocketIO with the app
    socketio.init_app(app, cors_allowed_origins="*")
    return app

def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

def load_classifier():
    cs = ClassiferSingleton()
    cs.set_paths(model_path='./app/finalized_model.sav', vectorizer_path='./app/vectorizer.sav')

# Initialize the classifier (it will load models on demand)
classifier = ClassiferSingleton()

# Make sure to export socketio
__all__ = ['create_app', 'socketio']
