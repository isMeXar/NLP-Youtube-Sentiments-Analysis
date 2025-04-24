// app/static/script.js
// Add this to your existing JavaScript

document.getElementById('analysis-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const videoUrl = document.getElementById('video-url').value;
    const modelType = document.getElementById('model-type').value;
    const results = document.getElementById('results');
    const error = document.getElementById('error');
    
    // Show loading state
    results.style.display = 'none';
    error.style.display = 'none';
    
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `video_url=${encodeURIComponent(videoUrl)}&model_type=${encodeURIComponent(modelType)}`
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            error.textContent = data.error;
            error.style.display = 'block';
            return;
        }
        
        // Update results
        document.getElementById('sentiment').textContent = data.sentiment;
        document.getElementById('video-embed').src = data.video_embed;
        document.getElementById('sentiment-plot').src = data.plot_url + '?t=' + new Date().getTime();
        
        // Update percentages
        document.getElementById('negative-percent').textContent = data.percentages.Negative.toFixed(1) + '%';
        document.getElementById('neutral-percent').textContent = data.percentages.Neutral.toFixed(1) + '%';
        document.getElementById('positive-percent').textContent = data.percentages.Positive.toFixed(1) + '%';
        
        results.style.display = 'block';
    })
    .catch(err => {
        error.textContent = 'An error occurred during analysis.';
        error.style.display = 'block';
    });
});

socket.on('sentiment_update', function(data) {
    console.log('Received update:', data);  // Debug log
    
    // Update chart immediately
    if (chart) {
        chart.data.datasets[0].data = [
            data.percentages.Negative,
            data.percentages.Neutral,
            data.percentages.Positive
        ];
        chart.update('none');  // Update without animation
    }

    // Update progress counter
    document.getElementById('progress-counter').textContent = 
        `(${data.total}/50 comments)`;

    // Update current comment display
    const commentDiv = document.getElementById('current-comment');
    commentDiv.classList.remove('hidden');
    document.getElementById('comment-text').textContent = data.current_comment;
    document.getElementById('comment-sentiment').textContent = 
        `Sentiment: ${data.current_sentiment}`;
});

function initChart() {
    const ctx = document.getElementById('sentimentChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Negative', 'Neutral', 'Positive'],
            datasets: [{
                label: 'Sentiment Distribution',
                data: [0, 0, 0],
                backgroundColor: ['#ef4444', '#eab308', '#22c55e']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 14 // Larger font size
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        },
                        font: {
                            size: 14 // Larger font size
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            family: 'Poppins',
                            size: 14 // Larger font size
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Sentiment Distribution',
                    font: {
                        family: 'Poppins',
                        size: 20, // Larger title
                        weight: 'bold'
                    },
                    padding: {
                        bottom: 30
                    }
                }
            }
        }
    });
}

async function startAnalysis() {
    const videoUrl = document.getElementById('video_url').value;
    const modelType = document.getElementById('model-type').value;
    const videoId = getVideoId(videoUrl);

    if (!videoId) {
        alert('Please enter a valid YouTube URL');
        return;
    }

    // Show video and hide empty state
    const videoFrame = document.getElementById('video-frame');
    const emptyState = document.getElementById('empty-state');
    
    videoFrame.src = `https://www.youtube.com/embed/${videoId}`;
    videoFrame.classList.remove('hidden');
    emptyState.classList.add('hidden');

    // Rest of your analysis code...
}