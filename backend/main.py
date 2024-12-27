from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

# Initialize the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Validate and configure the Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")
genai.configure(api_key=api_key)

# Configure generation settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

try:
    # Create the generative model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Initialize a chat session
    chat_session = model.start_chat(history=[])
except Exception as e:
    raise RuntimeError(f"Failed to initialize Gemini model or chat session: {str(e)}")

# Set up logging to save logs to a file
LOG_FILE = "chat_logs.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),  # Also log to console
    ],
)
logger = logging.getLogger(__name__)

# Request body model
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received message: {request.message}")

        # Validate the message
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty.")

        # Generate a response
        prompt = f"Provide a short response to the following question:\n\n{request.message}"
        response = chat_session.send_message(prompt)

        # Ensure the response is valid
        if not response or not response.text:
            raise HTTPException(status_code=500, detail="Received an empty response from Gemini API.")

        # Clean the response
        cleaned_response = response.text.strip("```html").strip("```").strip()
        logger.info(f"Cleaned response: {cleaned_response}")

        return {"response": cleaned_response}

    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Error in chat endpoint")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Run the application (use uvicorn to start the server)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
