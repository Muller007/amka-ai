"""
AMKA — AI Engine
Handles NLP intent classification, data extraction, and insight generation.

Intents:
- INCOME: User earned/sold something
- EXPENSE: User spent/bought something
- QUERY_DAY: User asks about today
- QUERY_WEEK: User asks about this week
- QUERY_MONTH: User asks about this month
- REPORT: User requests credit report
- HELP: User asks for help
- UNKNOWN: Message doesn't match any intent
"""

import os
import re
import json
from dotenv import load_dotenv
import anthropic
import requests
from datetime import datetime

load_dotenv()

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class AmkaAI:
    """AMKA AI Engine: Intent classification, data extraction, and insights."""
    
    def __init__(self):
        self.claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        self.openai_api_key = OPENAI_API_KEY
    
    def classify_intent(self, message: str, language: str = 'en') -> tuple:
        """
        Classify user message intent and extract financial data.
        
        Returns:
            (intent, extracted_data) where:
            - intent: str (INCOME|EXPENSE|QUERY_DAY|QUERY_WEEK|QUERY_MONTH|REPORT|HELP|UNKNOWN)
            - extracted_data: dict with amount, category, etc.
        """
        try:
            prompt = f"""You are AMKA, a financial intelligence assistant for African traders and small business owners.

User message: "{message}"
User language: {language}

Classify this message into ONE of these intents:
- INCOME: User earned/sold something (e.g., "sold R150", "I made money")
- EXPENSE: User spent/bought something (e.g., "spent R50", "bought stock")
- QUERY_DAY: User asks about today (e.g., "today", "how am I doing today")
- QUERY_WEEK: User asks about this week (e.g., "this week", "weekly")
- QUERY_MONTH: User asks about this month (e.g., "this month", "monthly")
- REPORT: User wants credit/financial report (e.g., "report", "credit", "loan report")
- HELP: User asks for help (e.g., "help", "?", "how do I")
- UNKNOWN: Message doesn't fit above categories

If intent is INCOME or EXPENSE:
1. Extract the AMOUNT (numerical value only, no currency symbol)
2. Guess the CATEGORY (stock, transport, food, equipment, rent, other)
3. Include the raw message

Respond as JSON only, no other text:
{{
    "intent": "INCOME|EXPENSE|QUERY_DAY|QUERY_WEEK|QUERY_MONTH|REPORT|HELP|UNKNOWN",
    "confidence": 0.0-1.0,
    "amount": 0.0,
    "category": "stock|transport|food|equipment|rent|other",
    "raw_message": "original user message"
}}
"""
            
            response = self.claude_client.messages.create(
                model="claude-opus-4-20250805",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text.strip()
            
            # Parse JSON response
            data = json.loads(response_text)
            
            return (
                data.get('intent', 'UNKNOWN'),
                {
                    'amount': data.get('amount', 0),
                    'category': data.get('category', 'other'),
                    'raw_message': data.get('raw_message', message),
                    'confidence': data.get('confidence', 0.5)
                }
            )
            
        except Exception as e:
            print(f"Error in classify_intent: {str(e)}")
            return ('UNKNOWN', {'amount': 0, 'category': 'other', 'raw_message': message})
    
    def transcribe_voice_note(self, media_url: str, language: str = 'en') -> str:
        """
        Transcribe a voice note using OpenAI Whisper API.
        
        Args:
            media_url: URL to the voice note from Twilio
            language: Language code for transcription
        
        Returns:
            Transcribed text
        """
        try:
            # Download the audio from Twilio URL
            audio_response = requests.get(media_url)
            audio_data = audio_response.content
            
            # Send to OpenAI Whisper
            headers = {"Authorization": f"Bearer {self.openai_api_key}"}
            files = {"file": ("audio.ogg", audio_data, "audio/ogg")}
            params = {"model": "whisper-1", "language": language}
            
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers=headers,
                files=files,
                data=params
            )
            
            if response.status_code == 200:
                return response.json()['text']
            else:
                print(f"Whisper API error: {response.status_code}")
                return "[Could not transcribe voice note]"
                
        except Exception as e:
            print(f"Error in transcribe_voice_note: {str(e)}")
            return "[Could not transcribe voice note]"
    
    def get_onboarding_message(self) -> str:
        """Return onboarding message for new users."""
        return """👋 Sawubona! I'm AMKA — *Wake Up Your Money*

I help you track your business and understand your finances using WhatsApp.

Just send me messages like:
💰 "I sold R150 of tomatoes"
💸 "I spent R50 on transport"
📊 "How am I doing?"

What language do you prefer?
1️⃣ English
2️⃣ isiZulu
3️⃣ Xhosa
4️⃣ Swahili
5️⃣ Hausa

Reply with the number of your choice!"""
    
    def get_help_message(self, language: str = 'en') -> str:
        """Return help message for users."""
        return """ℹ️ AMKA Help — How to use

📝 RECORD INCOME:
"I sold R150" or "I earned R200"

📝 RECORD EXPENSES:
"I spent R50" or "I bought R100 stock"

📊 CHECK YOUR BALANCE:
"How am I doing?" or "profit"
"today", "this week", "this month"

📋 GET YOUR REPORT:
"Give me my report" or "I need a credit report"

❓ More help?
Open an issue at: github.com/Muller007/amka-ai"""
    
    def get_confused_message(self, language: str = 'en') -> str:
        """Return message when intent is unknown."""
        return """🤔 I didn't quite catch that.

Try saying something like:
• "I sold R150" — to record income
• "I spent R50" — to record expenses
• "profit" — to see your balance
• "help" — for all commands

What would you like to do?"""


if __name__ == '__main__':
    # Test the AI engine
    amka = AmkaAI()
    
    test_messages = [
        "I sold R150 of tomatoes",
        "spent 40 on transport",
        "how am I doing today?",
        "I need my credit report",
        "help"
    ]
    
    for msg in test_messages:
        intent, data = amka.classify_intent(msg)
        print(f"Message: {msg}")
        print(f"Intent: {intent}, Data: {data}\n")