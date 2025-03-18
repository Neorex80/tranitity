import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import markdown
from markupsafe import Markup

# If you're using the Groq library:
from groq import Groq, APIError

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random secret key

# Flask-Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory storage for demo (no database)
users = {}        # { "email": { "username": "SomeName", "password_hash": "..." } }
itineraries = {}  # { "email": [ { "destination": "Paris", "details": "Itinerary in Markdown" } ] }

class User(UserMixin):
    def __init__(self, email, username):
        self.id = email
        self.username = username

@login_manager.user_loader
def load_user(email):
    """Loads user from the in-memory dictionary."""
    if email in users:
        return User(email, users[email]["username"])
    return None

# Jinja filter to convert Markdown to HTML
@app.template_filter('markdown')
def markdown_filter(text):
    """Converts Markdown text to HTML and marks it safe for rendering."""
    html_content = markdown.markdown(text)
    return Markup(html_content)

# --- Groq API Setup ---
# Replace "YOUR_GROQ_API_KEY_HERE" with your actual key, or load from environment:
groq_api_key = "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"
client = Groq(api_key=groq_api_key)

def generate_itinerary(destination, days, interests):
    """
    Sends a prompt to the Groq API requesting a multi-day travel itinerary in Markdown format.
    """
    prompt = (
        f"Create a {days}-day travel itinerary for {destination}, "
        f"focusing on {interests}. "
        "Format the output in Markdown with headings and bullet points."
    )
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except APIError as e:
        print(f"[Groq API Error] {e}")
        return "Error: Could not generate itinerary."
    except Exception as e:
        print(f"[Unexpected Error] {e}")
        return "Error: Could not generate itinerary."

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if email in users:
            return "User already exists!"

        # Store hashed password for security
        users[email] = {
            "username": username,
            "password_hash": generate_password_hash(password)
        }
        itineraries[email] = []
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and check_password_hash(users[email]["password_hash"], password):
            user = User(email, users[email]["username"])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_itineraries = itineraries.get(current_user.id, [])
    return render_template('dashboard.html', itineraries=user_itineraries)

@app.route('/generate_itinerary', methods=['POST'])
@login_required
def generate_ai_itinerary():
    destination = request.form['destination']
    days = request.form['days']
    interests = request.form['interests']

    # Generate itinerary using Groq
    itinerary_text = generate_itinerary(destination, days, interests)

    # Store the itinerary
    itineraries[current_user.id].append({
        "destination": destination,
        "details": itinerary_text
    })

    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
