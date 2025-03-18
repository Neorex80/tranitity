
# Travel Itinerary Planner (Flask + Groq)
![image](https://github.com/user-attachments/assets/51fad89c-74cf-48e1-b813-a5dea9699733)

This is a demo Flask application that uses the **Groq API** to generate multi-day travel itineraries in Markdown format, then renders them on the dashboard page.

## Features
- **User registration and login** (in-memory, no database).
- **AI-based itinerary generation** using the Groq API.
- **Markdown-formatted** itineraries displayed in a styled dashboard.
- **Logout functionality** for user sessions.

## Requirements
See [requirements.txt](./requirements.txt) for the list of required Python packages:
```
Flask
Flask-Login
groq
markdown
Werkzeug
```

## Setup & Installation

1. **Clone this repository** or download the files.

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   # or:
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your Groq API Key**:
   - In `app.py`, replace `"YOUR_GROQ_API_KEY_HERE"` with your actual key.
   - Alternatively, set the environment variable `GROQ_API_KEY` and modify the code in `app.py` to load from `os.getenv("GROQ_API_KEY")`.

5. **Run the application**:
   ```bash
   python app.py
   ```
6. **Access the app**:
   - Open your browser and go to `http://127.0.0.1:5000/`

## Usage
1. **Register** a new user at `/register`.
2. **Log in** at `/login`.
3. **Generate** an itinerary from the Dashboard by entering:
   - Destination
   - Number of Days
   - Interests (e.g., "food, adventure")
4. **View** your itineraries, which will appear in Markdown format.

## Troubleshooting
- If the server crashes upon generating an itinerary, check the console for **Groq API errors**:
  - Ensure your API key is valid.
  - Verify the model name (`"llama-3.3-70b-versatile"`) is correct and available to you.
- If templates are not found, confirm that you have a `templates` folder with all `.html` files.

## License
This project is for demonstration purposes. Feel free to adapt it to your own needs.
