import logging
from flask import Flask
from app.routes import routes
from app.classifier import ClassiferSingleton

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(routes)
    configure_logging()
    load_classifier()
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
