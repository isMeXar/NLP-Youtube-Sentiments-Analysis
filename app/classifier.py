# app/classifier.py

from threading import Lock
import joblib
import tensorflow as tf
import pickle
import re
from itertools import islice
import collections
import matplotlib.pyplot as plt
import numpy as np
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR

class SingletonMeta(type):
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

COMMENTS_VOLUME = 50
MAX_LEN = 100  # Make sure this matches your model's expected sequence length

class ClassiferSingleton(metaclass=SingletonMeta):
    comment_scraper = YoutubeCommentDownloader()
    
    def __init__(self):
        self.model_type = None  # 'traditional' or 'deep'
        self.model = None
        self.vectorizer = None
        self.tokenizer = None

    def set_paths(self, model_path: str, vectorizer_path: str, model_type: str = 'traditional') -> None:
        """
        Set paths for model and vectorizer/tokenizer
        model_type: 'traditional' or 'deep'
        """
        self.model_type = model_type
        
        if model_type == 'traditional':
            self.model = joblib.load(filename=model_path)
            self.vectorizer = joblib.load(filename=vectorizer_path)
        else:  # deep learning model
            self.model = tf.keras.models.load_model(model_path)
            with open(vectorizer_path, 'rb') as handle:
                self.tokenizer = pickle.load(handle)

    def make_analysis(self, video_url):
        # Get comments
        comments_generator = self.comment_scraper.get_comments_from_url(
            youtube_url=video_url, sort_by=SORT_BY_POPULAR)

        # Get and clean comments
        dirty_comments = [comment['text'] for comment in islice(comments_generator, COMMENTS_VOLUME)]
        clean_comments = self._clean(dirty_comments)
        
        # Process based on model type
        if self.model_type == 'traditional':
            features = self.vectorizer.transform(clean_comments).toarray()
            predictions = self.model.predict(features)
            probabilities = None  # Traditional model might not have probabilities
        else:
            # Deep learning model
            sequences = self.tokenizer.texts_to_sequences(clean_comments)
            features = tf.keras.preprocessing.sequence.pad_sequences(
                sequences, maxlen=MAX_LEN)
            probabilities = self.model.predict(features)
            predictions = np.argmax(probabilities, axis=1)

        # Count predictions
        counter = collections.Counter(predictions)

        # Create visualization
        fig, ax = plt.subplots()
        ax.bar(
            x=['Negative', 'Neutral', 'Positive'],
            height=[counter[0] / COMMENTS_VOLUME * 100, 
                   counter[1] / COMMENTS_VOLUME * 100,
                   counter[2] / COMMENTS_VOLUME * 100],
            color=['red', 'yellow', 'green']
        )
        ax.set_title(f'Comments Sentiment Analysis ({self.model_type.title()} Model)')
        ax.set_xlabel('Category')
        ax.grid(axis='y', zorder=0)
        ax.set_ylim(0, 100)
        ax.set_ylabel('% of comments')

        # Save the plot
        plt.savefig('./app/static/plot.png')
        plt.close()

        return predictions, probabilities, counter

    def _clean(self, comments):
        processed_features = []
        for comment in comments:
            processed_feature = re.sub(r'\W', ' ', str(comment))
            processed_feature = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)
            processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature)
            processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)
            processed_feature = re.sub(r'^b\s+', '', processed_feature)
            processed_feature = processed_feature.lower()
            processed_features.append(processed_feature)
        return processed_features

    def make_analysis_single(self, comment):
        """Analyze a single comment"""
        if self.model_type == 'traditional':
            features = self.vectorizer.transform([comment]).toarray()
            prediction = self.model.predict(features)[0]
            probabilities = None
        else:
            sequence = self.tokenizer.texts_to_sequences([comment])
            features = tf.keras.preprocessing.sequence.pad_sequences(
                sequence, maxlen=MAX_LEN)
            probabilities = self.model.predict(features)
            prediction = np.argmax(probabilities[0])
        
        return prediction, probabilities, None