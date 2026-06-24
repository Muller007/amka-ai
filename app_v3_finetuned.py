#!/usr/bin/env python3
"""
AMKA WhatsApp Financial Assistant - MVP v3 (Fine-tuned AI)
"""

from flask import Flask, request, jsonify
from twilio.rest import Client
from ai_engine_v3_finetuned import AMKAFinetuneEngine
import os
from datetime import datetime
import json
from collections import defaultdict

# Initialize Flask app
app = Flask(__name__)


from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Initialize AI Engine with fine-tuned model
ai_engine = AMKAFinetuneEngine(use_fallback=True)

# In-memory storage (replace with database in production)
user_transactions = defaultdict(list)
user_profiles = {}

class TransactionManager:
    """Manage user transactions"""
    
    @staticmethod
    def add_transaction(phone, transaction_type, amount, description):
        """Add transaction to user history"""
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "type": transaction_type,
            "amount": amount,
            "description": description
        }
        user_transactions[phone].append(transaction)
        return transaction
    
    @staticmethod
    def get_daily_summary(phone):
        """Get today's summary"""
        today = datetime.now().date()
        today_txns = [t for t in user_transactions[phone] 
                     if datetime.fromisoformat(t['timestamp']).date() == today]
        
        income = sum(t['amount'] for t in today_txns if t['type'] == 'income')
        expenses = sum(t['amount'] for t in today_txns if t['type'] == 'expense')
        
        return {
            "date": str(today),
            "transactions": len(today_txns),
            "income": income,
            "expenses": expenses,
            "profit": income - expenses
        }
    
    @staticmethod
    def get_weekly_summary(phone):
        """Get week's summary"""
        from datetime import timedelta
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        
        week_txns = [t for t in user_transactions[phone] 
                    if week_ago <= datetime.fromisoformat(t['timestamp']).date() <= today]
        
        income = sum(t['amount'] for t in week_txns if t['type'] == 'income')
        expenses = sum(t['amount'] for t in week_txns if t['type'] == 'expense')
        
        return {
            "period": f"{week_ago} to {today}",
            "transactions": len(week_txns),
            "income": income,
            "expenses": expenses,
            "profit": income - expenses,
            "avg_daily": income / 7 if income > 0 else 0
        }

def generate_response(result, phone):
    """Generate WhatsApp response based on AI classification"""
    
    intent = result['intent']
    amount = result['amount']
    confidence = result['confidence']
    
    # Track confidence
    model_type = "Fine-tuned" if result['method'] == 'finetuned' else 'Regex'
    
    if intent == "income":
        # Record income
        TransactionManager.add_transaction(phone, "income", amount, result['text'])
        response = f"✅ Income recorded\n" \
                  f"Amount: R{amount:,}\n" \
                  f"Method: {model_type} | Confidence: {confidence:.0%}"
    
    elif intent == "expense":
        # Record expense
        TransactionManager.add_transaction(phone, "expense", amount, result['text'])
        response = f"✅ Expense recorded\n" \
                  f"Amount: R{amount:,}\n" \
                  f"Method: {model_type} | Confidence: {confidence:.0%}"
    
    elif intent == "query":
        # Handle query
        if 'profit' in result['text'].lower():
            summary = TransactionManager.get_daily_summary(phone)
            response = f"📊 Daily Summary\n" \
                      f"Income: R{summary['income']:,}\n" \
                      f"Expenses: R{summary['expenses']:,}\n" \
                      f"Profit: R{summary['profit']:,}"
        elif 'week' in result['text'].lower():
            summary = TransactionManager.get_weekly_summary(phone)
            response = f"📈 Weekly Summary\n" \
                      f"Income: R{summary['income']:,}\n" \
                      f"Expenses: R{summary['expenses']:,}\n" \
                      f"Profit: R{summary['profit']:,}\n" \
                      f"Avg Daily: R{summary['avg_daily']:,.0f}"
        elif 'loan' in result['text'].lower():
            summary = TransactionManager.get_weekly_summary(phone)
            credit_score = min(100, (summary['profit'] / 100))
            response = f"💳 Loan Eligibility\n" \
                      f"Your Score: {credit_score:.0f}/100\n" \
                      f"You qualify for: R{credit_score * 50:,.0f}"
        else:
            response = f"📝 I understood your query\n" \
                      f"Method: {model_type} | Confidence: {confidence:.0%}\n" \
                      f"Try: 'What's my profit?' or 'Show weekly'"
    
    elif intent == "report":
        summary = TransactionManager.get_weekly_summary(phone)
        response = f"📋 Your Report\n" \
                  f"Period: {summary['period']}\n" \
                  f"Total Transactions: {summary['transactions']}\n" \
                  f"Income: R{summary['income']:,}\n" \
                  f"Expenses: R{summary['expenses']:,}\n" \
                  f"Net Profit: R{summary['profit']:,}"
    
    elif intent == "help":
        response = f"📚 AMKA Help\n" \
                  f"Try:\n" \
                  f"• 'I earned R500' (record income)\n" \
                  f"• 'Spent R100' (record expense)\n" \
                  f"• 'What's my profit?' (daily summary)\n" \
                  f"• 'Show weekly' (weekly report)\n" \
                  f"Model: {model_type} AI"
    
    else:
        response = f"❓ I didn't quite understand\n" \
                  f"Please try:\n" \
                  f"• 'I earned R500'\n" \
                  f"• 'What's my profit?'\n" \
                  f"Method: {model_type} | Confidence: {confidence:.0%}"
    
    return response

@app.route('/webhook', methods=['POST'])
def webhook():
    """Twilio WhatsApp webhook"""
    
    try:
        # Get message from Twilio
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        
        if not incoming_msg:
            return ('', 204)
        
        # Log message
        print(f"[{sender}] {incoming_msg}")
        
        # Process with AI engine
        result = ai_engine.process_message(incoming_msg)
        print(f"[AI] Intent: {result['intent']} | Confidence: {result['confidence']:.2%} | Method: {result['method']}")
        
        # Generate response
        response_text = generate_response(result, sender)
        
        # Send response via Twilio
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=response_text,
            to=sender
        )
        
        print(f"[✅] Response sent: {message.sid}")
        
        return ('', 200)
    
    except Exception as e:
        print(f"[ERROR] {e}")
        return (str(e), 500)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "ai_engine": ai_engine.get_status(),
        "users": len(user_transactions)
    })

@app.route('/user/<phone>/summary', methods=['GET'])
def user_summary(phone):
    """Get user summary"""
    daily = TransactionManager.get_daily_summary(phone)
    weekly = TransactionManager.get_weekly_summary(phone)
    
    return jsonify({
        "phone": phone,
        "daily": daily,
        "weekly": weekly,
        "total_transactions": len(user_transactions[phone])
    })

if __name__ == '__main__':
    print("🚀 AMKA MVP v3 (Fine-tuned AI)")
    print(f"AI Engine Status: {ai_engine.get_status()}")
    print("Starting Flask server on port 5000...")
    
    app.run(debug=True, port=5000)