from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import random
import wikipediaapi
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from Bot_file import guess, rps, quest, riddle

app = Flask(__name__)

# Enable CORS
CORS(app)

# Define your user agent
user_agent = "Luna/1.0 (https://yourwebsite.com)"
headers = {'User-Agent': user_agent}
requests_session = requests.Session()
requests_session.headers.update(headers)
wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)
google_api_key = "AIzaSyAOcYzIe-CLGF0qLsjZpOAms26-zHMoznw"

with open('D:\Chatbot Luna\Bot_file/words.json') as file:
    intents = json.load(file)


def get_google_search_results(query):
    google_search_url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx=60f9e3d608b0843bd&q={query}"
    response = requests_session.get(google_search_url)
    return response.json() if response.status_code == 200 else None


def get_wikipedia_summary(query):
    try:
        page = wiki.page(query)
        if page.exists():
            summary = page.summary
            sentences = summary.split('. ')
            complete_summary = '. '.join(sentences[:5]) + '.'
            return complete_summary if len(complete_summary) > 100 else summary
        else:
            return "No Wikipedia page found for this query."
    except Exception as e:
        print(f"Error fetching Wikipedia summary: {e}")
        return "An unexpected error occurred. Please try again later."


def get_google_summary(query):
    try:
        search_results = get_google_search_results(query)
        if search_results:
            items = search_results.get("items", [])
            if items:
                for item in items:
                    link = item.get("link", "")
                    response = requests.get(link)
                    if response.status_code == 200:
                        page_content = response.text
                        soup = BeautifulSoup(page_content, 'html.parser')
                        paragraphs = soup.find_all("p")
                        if paragraphs:
                            full_text = ' '.join(p.get_text() for p in paragraphs[:3])
                            sentences = full_text.split('. ')
                            clean_summary = '. '.join(sentences[:5]) + '.'
                            return clean_summary + f"\n\nRead more: {link}"
    except Exception as e:
        print(f"Error retrieving Google summary: {e}")
    return "Sorry, I couldn't retrieve a summary from Google. Please try again."


def get_summary(query):
    wikipedia_summary = get_wikipedia_summary(query)
    if wikipedia_summary and "No Wikipedia page found" not in wikipedia_summary:
        return wikipedia_summary

    google_summary = get_google_summary(query)
    if google_summary and "Sorry" not in google_summary:
        return google_summary

    return "Sorry, I couldn't find relevant information. Please try again."


def start_game(game_choice):
    if game_choice.lower() == 'rock paper scissors':
        return rps.sample()
    elif game_choice.lower() == 'guessing game':
        return guess.guessing_game()
    elif game_choice.lower() == '20 questions':
        return quest.wordgame()
    elif game_choice.lower() == 'riddles':
        return riddle.riddlegame()
    else:
        return "I'm sorry, I didn't understand your choice."


def get_random_response(responses):
    return random.choice(responses)


def process_user_input(user_inputs):
    tokens = word_tokenize(user_inputs.lower())
    stop_words = set(stopwords.words('english'))
    keyword = [word.lower() for word in tokens if word.lower() not in stop_words]
    return keyword


@app.route('/')
def home():
    return render_template('index.html')  # Make sure 'index.html' is in the 'templates' folder


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if user_input.lower() == 'exit':
        return jsonify({'response': 'Goodbye!'})

    if any(keyword in user_input.lower() for keyword in ["stop", "enough"]):
        return jsonify({'response': "Okay, let me know if you want to 'chat' or 'play' again."})

    greetings = ["good morning", "good afternoon", "good night"]
    if any(greeting in user_input.lower() for greeting in greetings):
        return jsonify({'response': user_input})

    # Check for game-related keywords
    if any(keyword in user_input.lower() for keyword in ["can we play?", "games", "let's play", "game"]):
        if 'rock paper scissors' in user_input.lower():
            game_choice = 'rock paper scissors'
        elif 'guessing game' in user_input.lower():
            game_choice = 'guessing game'
        elif '20 questions' in user_input.lower():
            game_choice = '20 questions'
        elif 'riddles' in user_input.lower():
            game_choice = 'riddles'
        else:
            return jsonify({'response': "Please specify which game you want to play: 'rock paper scissors', 'guessing game', '20 questions', or 'riddles'."})

        game_result = start_game(game_choice)
        return jsonify({'response': game_result})

    matched_intent = None
    for intent in intents['intents']:
        for question in intent['question']:
            if question.lower() in user_input.lower():
                matched_intent = intent
                break

    if matched_intent:
        answer = get_random_response(matched_intent['answer'])
        return jsonify({'response': answer})
    else:
        keywords = process_user_input(user_input)
        query = " ".join(keywords)
        summary = get_summary(query)
        return jsonify({'response': summary})


if __name__ == '__main__':
    app.run(debug=True)
