from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import re  # Add this import at the top of app.py


def sanitise_input(message):
    """
    Clean and validate user input.
    Returns cleaned message or None if invalid.
    """
    if not message:
        return None

    # Remove leading/trailing whitespace
    message = message.strip()

    # Check if message is empty after stripping
    if not message:
        return None

    # Remove HTML tags (prevents script injection)
    message = re.sub(r"<[^>]+>", "", message)

    # Check length after cleaning
    if len(message) > 500:
        return None

    return message


# Create the Flask application
app = Flask(__name__)

# Initialize the chatbot
chatbot = ChatBot(
    "GlebBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///chatbot_database.sqlite3",
)

# Train the chatbot with English conversations
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

from chatterbot.trainers import ListTrainer

list_trainer = ListTrainer(chatbot)

# Train on school-related conversations
list_trainer.train(
    [
        "What subjects do you like?",
        "As an AI bot I do not have opinions" "Can you help with homework?",
        "I can try to help explain concepts, but you should do your own work!",
        "Who made you?",
        "I was created by a talented Year 9 student at Tempe High School!",
        "what is one plus one?",
        "Two",
        "what is 1 + 1",
        "Two",
        "what is your name?",
        "My name is Gleb AI, here to help!",
    ]
)

# Train on greetings
list_trainer.train(
    [
        "Good morning!",
        "Good morning! How can I help you today?",
        "Good afternoon!",
        "Good afternoon! What would you like to chat about?",
    ]
)

# Train on math
list_trainer.train(
    [
        "What is 2 + 2",
        "Four",
        "what is Two plus Two",
        "Four",
        "what is 2 times 2",
        "Four",
        "What is 8 times 8?",
        "64",
        "whats 3+5",
        "that would be 8",
        "what is 10 plus ten",
        "its 20",
        "what is 10 + 10",
        "20",
    ]
)

# Train on conversation
list_trainer.train(
    [
        "No",
        "Whats wrong?",
        "Just no",
        "can you tell me whats wrong?",
        "thats right!",
        "Thank you!",
    ]
)


@app.route("/")
def home():
    """Serve the main chat page."""
    return render_template("index.html")


CRISIS_KEYWORDS = [
    "suicide",
    "kill myself",
    "end my life",
    "self harm",
    "self-harm",
    "dont want to live",
    "don't want to live",
    "want to die",
    "I what to kill someone",
    "I what to kill",
    "I what to end it all",
    "Kill",
    "end it all",
    "Ima kill my self",
    "Kill my self",
    "I what to kill them",
    "I will kill myself",
    "I what to kill my self",
]

CRISIS_RESPONSE = """I'm concerned about what you've shared. Please know that you're not alone.

If you're in crisis, please reach out for support:

- Lifeline: 13 11 14 (24/7)
- Kids Helpline: 1800 55 1800
- Beyond Blue: 1300 22 4636

I'm just a chatbot and can't provide the support you need."""


def check_for_crisis(message):
    """Check if message contains crisis keywords."""
    message_lower = message.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in message_lower:
            return True
    return False


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages and return bot responses."""
    data = request.get_json()
    raw_message = data.get("message", "")

    # Sanitise and validate input
    user_message = sanitise_input(raw_message)

    if user_message is None:
        if not raw_message or not raw_message.strip():
            return jsonify({"response": "Please enter a message!"})
        else:
            return jsonify(
                {"response": "Message too long! Please keep it under 500 characters."}
            )

    # Safety check for crisis keywords (use original for better detection)
    if check_for_crisis(raw_message):
        return jsonify({"response": CRISIS_RESPONSE})

    # Get the chatbot's response
    bot_response = chatbot.get_response(user_message)

    return jsonify({"response": str(bot_response)})
