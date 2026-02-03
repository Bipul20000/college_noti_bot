import os
import requests
from dotenv import load_dotenv

# 1. Load the secrets from the .env file
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_test_message():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "🚀 Python is now connected to Telegram! We are ready to build."
    }
    
    # 2. Send the request
    print("Attempting to send message...")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() # Check for errors
        print("✅ Success! Check your Telegram.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_test_message()