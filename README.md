﻿# YouTube Sentiments Analysis using NLP

<p align="center" >
   <img src="http://estruyf-github.azurewebsites.net/api/VisitorHit?user=isMeXar&repo=NLP-Youtube-Sentiments-Analysis&countColorcountColor&countColor=%237B1E7B"/>
</p>


![Interface](app/static/image.png)

## About
This project aims to analyze YouTube video comments using Natural Language Processing (NLP) and Machine Learning (ML) techniques to determine the sentiment of the comments. The application allows users to input a YouTube video link, and it scrapes the comments from the video. Then, it analyzes the comments using NLP to classify them into positive, negative, or neutral sentiments. The results are then presented to the user in the form of a graph, showing the distribution of sentiment categories in the comments.

## Features
- Scrapes YouTube comments from a specified video.
- Analyzes comments using NLP to determine sentiment.
- Presents sentiment analysis results in a graph.
- Supports adjustable volume of comments scraped per video.
- Utilizes a XGBoost ML model for sentiment analysis.
- Support for both Deep Learning and Traditional ML models

## NLP Techniques in Sentiment Analysis
Natural Language Processing (NLP) plays a crucial role in this project by enabling the analysis of textual data from YouTube comments. NLP techniques are used to preprocess the comments, extract relevant features, and train machine learning models for sentiment analysis.

In this use case, the following NLP tasks are performed:
- Text preprocessing: Cleaning the text by removing special characters, punctuation, and stopwords to prepare it for analysis.
- Tokenization: Breaking down the text into individual words or tokens to analyze each word's sentiment.
- Feature extraction: Transforming the textual data into numerical features that can be used as input to machine learning algorithms.
- Sentiment analysis: Using machine learning models to classify the sentiment of the comments into positive, negative, or neutral categories based on their features.

NLP techniques enable the system to understand the underlying sentiment of the comments and provide valuable insights into the overall feedback received by the YouTube video.

## Importing the dataset

The dataset used for training the sentiment analysis model is the "Generic Sentiment | Multidomain Sentiment Dataset". It contains 50,000 sentiments merged from multiple domains, including Yelp, Twitter, and mobile reviews.

Dataset Link: [Generic Sentiment | Multidomain Sentiment Dataset](https://www.kaggle.com/datasets/akgeni/generic-sentiment-multidomain-sentiment-dataset)

**Context**

The dataset provides sentiments from various domains. To gain a general understanding of sentiment, it covers a wide range of semantics related to sentiment analysis.

- 0 -> Negative
- 1 -> Neutral
- 2 -> Positive


## Installation

1. Clone the repository:
```bash
git clone https://github.com/isMeXar/NLP-Youtube-Comments-Analysis.git
cd NLP-Youtube-Comments-Analysis
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter a YouTube video URL in the input field
2. Select your preferred model type (Deep Learning or Traditional ML)
3. Click "Analyze" to start the analysis
4. Watch as the sentiment distribution updates in real-time
5. View individual comments and their sentiments as they're processed


## Models

The application supports two types of models:
1. Deep Learning Model:
   - Uses TensorFlow/Keras
   - Better for nuanced sentiment detection
   - Slower but more accurate

2. Traditional ML Model:
   - Uses scikit-learn
   - Faster processing
   - Good for basic sentiment classification


## Future Improvements
- Add support for more languages
- Implement sentiment trend analysis over time
- improve model accuracy
- Add export functionality for analysis results
- Support for batch processing of multiple videos
- Enhanced visualization options

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
