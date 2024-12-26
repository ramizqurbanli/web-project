Web Project - FastAPI Chatbot with Gemini API Integration

This project is a simple backend chatbot using FastAPI and the Gemini API (Google Generative AI).
It allows users to send a message, and the chatbot responds with HTML-formatted text.
The project also logs user messages and chatbot responses to a log file for debugging purposes.

Features:
- Handles user chat messages and sends requests to the Gemini API.
- Responds with HTML-formatted content.
- Strips unnecessary markdown (e.g., \```html and \```).
- Logs all chat messages and responses to a file (chat_logs.log).
- CORS support for client-side integration.

Requirements:
- Python 3.8 or higher
- Gemini API key (Google Generative AI)

Setup:

1. Clone the repository:
   git clone https://github.com/ramizqurbanli/web-project.git
   cd web-project

2. Install dependencies:
   Create a virtual environment (optional but recommended) and install the required Python packages:
   
   python -m venv venv
   source venv/bin/activate  # For Windows use `venv\Scripts\activate`
   pip install -r requirements.txt

Here is the content of `requirements.txt`:
fastapi
uvicorn
google-generativeai
pydantic

3. Set up Gemini API Key:
   To use the Gemini API, you need an API key from Google.
   1. Sign up and get your Gemini API key from Google's Generative AI documentation: https://ai.google.dev
   2. Replace the empty GEMINI_API_KEY in the code with your API key:
      GEMINI_API_KEY = "your-api-key-here"

4. Running the Application:
   To run the FastAPI server, use `uvicorn`:
   
   uvicorn main:app --reload

   This will start the FastAPI application on http://127.0.0.1:8000 (default).

5. Testing the Chatbot API:
   You can interact with the chatbot API using any HTTP client (e.g., Postman, cURL, or your frontend).
   
   Request:
   Send a POST request to http://127.0.0.1:8000/chat with a JSON body:
   
   {
     "message": "Why don't scientists trust atoms?"
   }

   Response:
   The API will return a JSON object with the chatbot's HTML-formatted response:
   
   {
     "response": "<p>Because they make up everything!</p>"
   }

6. Logs:
   The application logs all user messages and chatbot responses to the chat_logs.log file in the project directory.
   
   You can open the `chat_logs.log` file to check the logged data:
   2024-12-24 12:34:56,789 - INFO - User message: Why don't scientists trust atoms?
   2024-12-24 12:34:57,123 - INFO - Raw response: ```html <p>Because they make up everything!</p> ```
   2024-12-24 12:34:57,124 - INFO - Cleaned bot response: <p>Because they make up everything!</p>

7. Accessing API Documentation:
   FastAPI automatically generates interactive API documentation using Swagger UI. You can view it by navigating to:
   
   http://127.0.0.1:8000/docs
   
   Alternatively, you can access the ReDoc documentation at:
   
   http://127.0.0.1:8000/redoc

Troubleshooting:
- Error communicating with Gemini API: Ensure that your Gemini API key is valid and correctly set in the code.
- CORS issues: If you are making requests from a different domain (e.g., a frontend app), ensure that CORS is correctly configured. This project uses CORSMiddleware to allow all origins by default.

License:
This project is licensed under the MIT License - see the LICENSE file for details.
