from fastapi import FastAPI, HTTPException  # type: ignore
from pydantic import BaseModel  # type: ignore
import google.generativeai as genai  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
import logging

# Initialize the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace with your Gemini API key
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Set up logging to save logs to a file
LOG_FILE = "chat_logs.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Save logs to the specified file
    ]
)
logger = logging.getLogger(__name__)

# Request body model
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    
    #Handles chat requests, logs all messages, and removes unnecessary markers from the response.

    try:
        # Log the user's message
        logger.info(f"User message: {request.message}")
        
        # Create a model instance
        model = genai.GenerativeModel("gemini-1.5-flash")

        if request.message.strip():
        # Generate a response and request an HTML format
            prompt = f"Provide a short response to the following question, formatted for web display:\n\n{request.message}"

            response = model.generate_content(prompt)
        
        # Get raw response
        raw_response = response.text

        
        # Clean the response by removing unwanted markers from the start and end
        cleaned_response = raw_response.strip("```html").strip("```").strip()

        # Log the cleaned response
        logger.info(f"Cleaned bot response: {cleaned_response}")
        
        # Return the cleaned response
        return {"response": cleaned_response}
    
    except Exception as e:
        # Log the error
        logger.error(f"Error communicating with Gemini API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error communicating with Gemini API: {str(e)}")
