from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime
import guess, rps, quest, riddle
import os
import base64
from PIL import Image
import io

app = Flask(__name__)

# Enable CORS
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyAUug9NDH9REr-5EZR9m90aSFb_VDqTVro"  # This is temporary for testing

def initialize_gemini():
    try:
        print("Initializing Gemini API...")
        print(f"API Key length: {len(GEMINI_API_KEY)}")
        
        # Configure the API
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Test the API key by listing models
        print("\nAvailable models:")
        models = genai.list_models()
        for m in models:
            print(f"- {m.name}")
        
        # Initialize models
        model = genai.GenerativeModel('gemini-pro')
        vision_model = genai.GenerativeModel('gemini-pro-vision')
        
        # Test the model with a simple prompt
        test_response = model.generate_content("Hello")
        if test_response and test_response.text:
            print("\nTest response successful!")
            return model, vision_model
        else:
            print("\nTest response failed!")
            return None, None
            
    except Exception as e:
        print(f"\nError during initialization: {str(e)}")
        return None, None

print("\nStarting application...")
model, vision_model = initialize_gemini()

def get_gemini_response(user_input):
    try:
        if not model:
            print("Model not initialized")
            return "I'm sorry, but I'm not properly configured. Please make sure the Gemini API key is set correctly."
        
        print(f"\nProcessing input: {user_input[:50]}...")
        
        # Add safety settings
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        response = model.generate_content(
            user_input,
            safety_settings=safety_settings,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40
            }
        )
        
        if not response or not response.text:
            print("Empty response received")
            return "I'm sorry, I couldn't generate a response. Please try again."
            
        print("Response generated successfully")
        return response.text
        
    except Exception as e:
        print(f"Error in get_gemini_response: {str(e)}")
        return "I'm having trouble processing your request. Please make sure the API key is valid and try again."

def analyze_image(image_data, prompt=""):
    try:
        if not vision_model:
            return "I'm sorry, but I'm not properly configured for image analysis. Please make sure the Gemini API key is set correctly."
            
        # Convert base64 to image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        
        # Generate response using vision model
        if prompt:
            response = vision_model.generate_content([prompt, image])
        else:
            response = vision_model.generate_content(["What do you see in this image? Please describe it in detail.", image])
        
        if not response or not response.text:
            return "I'm sorry, I couldn't analyze the image. Please try again."
        return response.text
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return "Sorry, I couldn't analyze the image. Please make sure the API key is valid and try again."

def get_time_based_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        data = request.json
        user_input = data.get('message')
        image_data = data.get('image')

        if not user_input and not image_data:
            return jsonify({'error': 'No message or image provided'}), 400

        # Handle exit command
        if user_input and user_input.lower() == 'exit':
            return jsonify({'response': 'Goodbye!'})

        # Handle stop command
        if user_input and any(keyword in user_input.lower() for keyword in ["stop", "enough"]):
            return jsonify({'response': "Okay, let me know if you want to 'chat' or 'play' again."})

        # Handle time-based greetings
        if user_input:
            greetings = ["good morning", "good afternoon", "good night"]
            if any(greeting in user_input.lower() for greeting in greetings):
                return jsonify({'response': f"{get_time_based_greeting()}! How can I help you today?"})

        # Handle image analysis
        if image_data:
            response = analyze_image(image_data, user_input)
            return jsonify({'response': response})

        # Check for game-related keywords
        if user_input and any(keyword in user_input.lower() for keyword in ["can we play?", "games", "let's play", "game"]):
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

            try:
                game_result = start_game(game_choice)
                return jsonify({'response': game_result})
            except Exception as e:
                print(f"Error in game: {e}")
                return jsonify({'response': "Sorry, there was an error starting the game. Please try again."})

        # Use Gemini API for all other responses
        if user_input:
            gemini_response = get_gemini_response(user_input)
            if gemini_response:
                return jsonify({'response': gemini_response})

        # Fallback response if Gemini API fails
        return jsonify({'response': "I'm having trouble processing your request. Please try again."})

    except Exception as e:
        print(f"Unexpected error in chat route: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
