from threading import Lock
import joblib
import re
from itertools import islice
import collections
import matplotlib.pyplot as plt

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

class ClassiferSingleton(metaclass=SingletonMeta):
    comment_scraper = YoutubeCommentDownloader()

    def set_paths(self, model_path: str, vectorizer_path: str) -> None:
        self.model = joblib.load(filename=model_path)
        self.vectorizer = joblib.load(filename=vectorizer_path)

    def make_analysis(self, video_url):
        comments_generator = self.comment_scraper.get_comments_from_url(
            youtube_url=video_url, sort_by=SORT_BY_POPULAR)

        dirty_comments = [comment['text'] for comment in islice(comments_generator, COMMENTS_VOLUME)]
        clean_comments = self._clean(dirty_comments)
        features = self.vectorizer.transform(clean_comments).toarray()
        predictions = self.model.predict(features)
        counter = collections.Counter(predictions)

        fig, ax = plt.subplots()
        ax.bar(
            x=['Negative', 'Neutral', 'Positive'],
            height=[counter[0] / COMMENTS_VOLUME * 100, counter[1] / COMMENTS_VOLUME * 100,
                    counter[2] / COMMENTS_VOLUME * 100],
            color=['red', 'yellow', 'green']
        )
        ax.set_title(f'Comments Sentiment Analysis')
        ax.set_xlabel('Category')
        ax.grid(axis='y', zorder=0)
        ax.set_ylim(0, 100)
        ax.set_ylabel('% of comments')

        # Save the figure using FigureCanvasAgg
        plt.savefig('./app/static/plot.png')

        return predictions


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
