import requests
import json

def emotion_detector(text_to_analyse):
    # Define the URL for the sentiment analysis API
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

    # Set the headers with the required model ID for the API
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Create a dictionary with the text to be analyzed
    payload = { "raw_document": { "text": text_to_analyse } }

    # Send a POST request to the API with the text and headers
    response = requests.post(url, json=payload, headers=headers)

    #return response.text  # Return the response text from the API

    # Convert the response text into a dictionary
    try:
        response_dict = json.loads(response.text)
    except json.JSONDecodeError:
        return {'error': 'Failed to parse JSON response'}

    # Print the response to debug
    # print("API Response:", response_dict)
        # Handle a 400 status code (Bad Request)
    if response.status_code == 400:
        # Return a dictionary with None values for all emotion scores
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Extract the emotions and their scores from the correct location
    emotions = response_dict.get('emotionPredictions', [])[0].get('emotion', {})

    # Ensure the required emotions are available (anger, disgust, fear, joy, sadness)
    anger_score = emotions.get('anger', 0)
    disgust_score = emotions.get('disgust', 0)
    fear_score = emotions.get('fear', 0)
    joy_score = emotions.get('joy', 0)
    sadness_score = emotions.get('sadness', 0)

    # Create a dictionary of the scores
    emotion_scores = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }

    # Find the dominant emotion (the one with the highest score)
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    # Add the dominant emotion to the dictionary
    emotion_scores['dominant_emotion'] = dominant_emotion

    return emotion_scores