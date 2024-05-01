from flask import Blueprint, render_template, request
from app.classifier import ClassiferSingleton

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.form.get('video_url')
    classifier = ClassiferSingleton()
    predictions = classifier.make_analysis(video_url)
    video_embed = get_video_embed(video_url)
    return render_template('index.html', video_embed=video_embed)

def get_video_embed(video_url):
    video_id = video_url.split('v=')[1].split('&')[0]
    embed_link = f'https://www.youtube.com/embed/{video_id}'
    return embed_link