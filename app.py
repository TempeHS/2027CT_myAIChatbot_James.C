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

# Train on more math
list_trainer.train(
    [
        "What is 1 + 1",
        "2",
        "What is 2 + 3",
        "5",
        "what is 4 + 9",
        "13",
        "what is 10 minus 7",
        "3",
        "what is 15 minus 5",
        "10",
        "what is 20 minus 13",
        "7",
        "what is 3 times 4",
        "12",
        "what is 5 times 9",
        "45",
        "what is 7 times 6",
        "42",
        "What is 8 times 12?",
        "96",
        "what is 9 times 11",
        "99",
        "what is 12 times 12",
        "144",
        "what is 100 divided by 10",
        "10",
        "What is 81 divided by 9?",
        "9",
        "what is 64 divided by 8",
        "8",
        "whats 14+16",
        "that would be 30",
        "whats 25+75",
        "100",
        "what is 200 minus 150",
        "50",
        "what is 300 minus 125",
        "175",
        "what is 2 squared",
        "4",
        "what is 3 squared",
        "9",
        "what is 4 squared",
        "16",
        "what is 5 squared",
        "25",
        "what is 10 squared",
        "100",
        "what is 2 cubed",
        "8",
        "what is 3 cubed",
        "27",
        "what is 4 cubed",
        "64",
        "what is 2 to the power of 6",
        "64",
        "what is 3 to the power of 4",
        "81",
        "what is 5 to the power of 3",
        "125",
        "what is 1/2 + 1/2",
        "1",
        "what is 3/4 + 1/4",
        "1",
        "what is 5/6 minus 1/6",
        "4/6",
        "what is 7/8 minus 3/8",
        "4/8",
        "what is 9 + 18",
        "27",
        "what is 45 + 55",
        "100",
        "what is 99 minus 44",
        "55",
        "what is 123 minus 23",
        "100",
        "what is 11 times 11",
        "121",
        "what is 13 times 7",
        "91",
        "what is 14 times 5",
        "70",
        "what is 16 times 4",
        "64",
        "what is 18 divided by 3",
        "6",
        "what is 49 divided by 7",
        "7",
        "what is 121 divided by 11",
        "11",
        "whats 6+17",
        "23",
        "whats 8+19",
        "27",
        "whats 33+67",
        "100",
        "what is 500 minus 250",
        "250",
        "what is 1000 minus 1",
        "999",
        "what is 9 times 12",
        "108",
        "what is 15 times 15",
        "225",
        "what is 20 times 20",
        "400",
        "what is 144 divided by 12",
        "12",
        "what is 225 divided by 15",
        "15",
        "what is 400 divided by 20",
        "20",
        "what is 30 + 45",
        "75",
        "what is 60 + 90",
        "150",
        "what is 100 + 250",
        "350",
        "what is 75 minus 25",
        "50",
        "what is 80 minus 30",
        "50",
        "what is 90 minus 45",
        "45",
        "what is 21 times 2",
        "42",
        "what is 22 times 3",
        "66",
        "what is 24 times 5",
        "120",
        "what is 36 divided by 6",
        "6",
        "what is 72 divided by 8",
        "9",
        "what is 90 divided by 9",
        "10",
        "what is 7 plus 14",
        "21",
        "what is 8 plus 24",
        "32",
        "what is 9 plus 36",
        "45",
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
