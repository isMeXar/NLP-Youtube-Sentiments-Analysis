from flask import Blueprint, render_template, request, jsonify
from app.classifier import ClassiferSingleton
from app import socketio
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
import time

routes = Blueprint('routes', __name__)
classifier = ClassiferSingleton()

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.form.get('video_url')
    model_type = request.form.get('model_type', 'deep')
    
    if model_type == 'traditional':
        classifier.set_paths('./app/finalized_model.sav', './app/vectorizer.sav', 'traditional')
    else:
        classifier.set_paths('./app/sentiment_analysis_model.h5', './app/tokenizer.pickle', 'deep')
    
    # Start the analysis in a background thread
    socketio.start_background_task(process_comments, video_url)
    
    return jsonify({'status': 'started', 'message': 'Analysis started'})

def process_comments(video_url):
    comment_scraper = YoutubeCommentDownloader()
    comments_generator = comment_scraper.get_comments_from_url(
        youtube_url=video_url, sort_by=SORT_BY_POPULAR)
    
    sentiment_counts = {'Negative': 0, 'Neutral': 0, 'Positive': 0}
    total_processed = 0
    
    for comment in comments_generator:
        if total_processed >= 50:  # Process 50 comments max
            break
            
        # Process single comment
        clean_comment = classifier._clean([comment['text']])
        prediction, _, _ = classifier.make_analysis_single(clean_comment[0])
        
        # Update counts
        sentiment_label = ['Negative', 'Neutral', 'Positive'][prediction]
        sentiment_counts[sentiment_label] += 1
        total_processed += 1
        
        # Emit update to client
        socketio.emit('sentiment_update', {
            'counts': sentiment_counts,
            'total': total_processed,
            'current_comment': comment['text'],
            'current_sentiment': sentiment_label
        })
        
        time.sleep(0.5)  # Add small delay for visualization

def get_video_embed(video_url):
    video_id = video_url.split('v=')[1].split('&')[0]
    embed_link = f'https://www.youtube.com/embed/{video_id}'
    return embed_link