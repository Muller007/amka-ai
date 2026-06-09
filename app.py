"""
AMKA — Wake Up Your Money
AI-powered WhatsApp assistant for Africa's informal economy.

A conversational financial intelligence platform that enables informal economy workers
to track income, expenses, and receive AI-generated business insights via WhatsApp.

Author: Kwanele Mlalazi
GitHub: github.com/Muller007/amka-ai
License: MIT
"""

from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import logging
from datetime import datetime, timedelta
from ai_engine import AmkaAI
from database import init_db, get_session
from models import User, Transaction
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize Twilio client
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Initialize AMKA AI engine
amka_ai = AmkaAI()

# Initialize database
init_db()

# ─────────────────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for deployment monitoring."""
    return {
        'status': 'ok',
        'service': 'AMKA',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }, 200


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Main WhatsApp webhook endpoint.
    Receives messages from Twilio, processes them through AMKA AI engine,
    and returns responses.
    """
    try:
        # Extract incoming message data
        from_number = request.form.get('From')  # WhatsApp format: whatsapp:+27XXXXXXXXX
        user_message = request.form.get('Body', '').strip()
        media_url = request.form.get('MediaUrl0')  # For voice notes
        
        logger.info(f"Incoming message from {from_number}: {user_message[:50]}...")
        
        # Extract phone number (remove 'whatsapp:' prefix)
        phone_number = from_number.replace('whatsapp:', '')
        
        # Get or create user
        session = get_session()
        user = session.query(User).filter_by(phone_number=phone_number).first()
        
        if not user:
            # First-time user: create account and send onboarding
            user = User(phone_number=phone_number, language='en')
            session.add(user)
            session.commit()
            logger.info(f"New user created: {phone_number}")
            
            response_text = amka_ai.get_onboarding_message()
        else:
            # Update last active timestamp
            user.last_active = datetime.utcnow()
            session.commit()
            
            # Process the message through AI engine
            # If voice note, transcribe first
            if media_url:
                user_message = amka_ai.transcribe_voice_note(media_url, user.language)
                logger.info(f"Transcribed voice note: {user_message[:50]}...")
            
            # Classify intent and extract data
            intent, extracted_data = amka_ai.classify_intent(user_message, user.language)
            logger.info(f"Intent: {intent}, Data: {extracted_data}")
            
            # Route to appropriate handler
            if intent == 'INCOME':
                response_text = handle_income(user, extracted_data, session)
            elif intent == 'EXPENSE':
                response_text = handle_expense(user, extracted_data, session)
            elif intent == 'QUERY_DAY':
                response_text = handle_query_day(user, session)
            elif intent == 'QUERY_WEEK':
                response_text = handle_query_week(user, session)
            elif intent == 'QUERY_MONTH':
                response_text = handle_query_month(user, session)
            elif intent == 'REPORT':
                response_text = handle_report(user, session)
            elif intent == 'HELP':
                response_text = amka_ai.get_help_message(user.language)
            else:  # UNKNOWN
                response_text = amka_ai.get_confused_message(user.language)
        
        # Send response via Twilio
        send_whatsapp_message(phone_number, response_text)
        
        session.close()
        
        # Return empty TwiML response (Twilio expects XML)
        twiml = MessagingResponse()
        return str(twiml), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return {'error': 'Internal server error'}, 500


# ─────────────────────────────────────────────────────────────────────────────
# Intent Handlers
# ─────────────────────────────────────────────────────────────────────────────

def handle_income(user, extracted_data, session):
    """Record income transaction and return confirmation + summary."""
    try:
        amount = float(extracted_data.get('amount', 0))
        category = extracted_data.get('category', 'other')
        
        # Create transaction record
        transaction = Transaction(
            user_id=user.id,
            type='income',
            amount=amount,
            category=category,
            raw_message=extracted_data.get('raw_message', ''),
            created_at=datetime.utcnow()
        )
        session.add(transaction)
        session.commit()
        
        logger.info(f"Income recorded for user {user.phone_number}: R{amount}")
        
        # Get today's summary
        today = datetime.utcnow().date()
        today_income = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'income',
            Transaction.created_at >= datetime.combine(today, datetime.min.time())
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        today_expenses = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'expense',
            Transaction.created_at >= datetime.combine(today, datetime.min.time())
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        profit = today_income - today_expenses
        
        response = f"""✅ Income recorded: R{amount}

📊 Today so far:
Income:   R{today_income:.2f}
Expenses: R{today_expenses:.2f}
Profit:   R{profit:.2f} {'✨' if profit > 0 else ''}"""
        
        return response
        
    except Exception as e:
        logger.error(f"Error handling income: {str(e)}")
        return "❌ Could not record income. Try: 'I sold R150'"


def handle_expense(user, extracted_data, session):
    """Record expense transaction and return confirmation + summary."""
    try:
        amount = float(extracted_data.get('amount', 0))
        category = extracted_data.get('category', 'other')
        
        # Create transaction record
        transaction = Transaction(
            user_id=user.id,
            type='expense',
            amount=amount,
            category=category,
            raw_message=extracted_data.get('raw_message', ''),
            created_at=datetime.utcnow()
        )
        session.add(transaction)
        session.commit()
        
        logger.info(f"Expense recorded for user {user.phone_number}: R{amount}")
        
        # Get today's summary
        today = datetime.utcnow().date()
        today_income = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'income',
            Transaction.created_at >= datetime.combine(today, datetime.min.time())
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        today_expenses = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'expense',
            Transaction.created_at >= datetime.combine(today, datetime.min.time())
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        profit = today_income - today_expenses
        
        response = f"""✅ Expense recorded: R{amount}

📊 Today so far:
Income:   R{today_income:.2f}
Expenses: R{today_expenses:.2f}
Profit:   R{profit:.2f} {'✨' if profit > 0 else ''}"""
        
        return response
        
    except Exception as e:
        logger.error(f"Error handling expense: {str(e)}")
        return "❌ Could not record expense. Try: 'I spent R50'"


def handle_query_day(user, session):
    """Return today's financial summary."""
    try:
        today = datetime.utcnow().date()
        
        today_income = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'income',
            Transaction.created_at >= datetime.combine(today, datetime.min.time())
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        today_expenses = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'expense',
            Transaction.created_at >= datetime.combine(today, datetime.min.time())
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        profit = today_income - today_expenses
        
        response = f"""📊 Today's Summary:

Income:   R{today_income:.2f}
Expenses: R{today_expenses:.2f}
Profit:   R{profit:.2f} {'✨' if profit > 0 else '⚠️'}"""
        
        return response
        
    except Exception as e:
        logger.error(f"Error handling query_day: {str(e)}")
        return "❌ Could not get today's summary."


def handle_query_week(user, session):
    """Return this week's financial summary."""
    try:
        today = datetime.utcnow()
        week_start = today - timedelta(days=today.weekday())  # Monday
        
        week_income = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'income',
            Transaction.created_at >= week_start
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        week_expenses = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'expense',
            Transaction.created_at >= week_start
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        profit = week_income - week_expenses
        
        response = f"""📈 This Week's Summary:

Income:   R{week_income:.2f}
Expenses: R{week_expenses:.2f}
Profit:   R{profit:.2f} {'✨' if profit > 0 else '⚠️'}"""
        
        return response
        
    except Exception as e:
        logger.error(f"Error handling query_week: {str(e)}")
        return "❌ Could not get this week's summary."


def handle_query_month(user, session):
    """Return this month's financial summary."""
    try:
        today = datetime.utcnow()
        month_start = today.replace(day=1)
        
        month_income = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'income',
            Transaction.created_at >= month_start
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        month_expenses = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'expense',
            Transaction.created_at >= month_start
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        profit = month_income - month_expenses
        
        response = f"""📊 This Month's Summary:

Income:   R{month_income:.2f}
Expenses: R{month_expenses:.2f}
Profit:   R{profit:.2f} {'✨' if profit > 0 else '⚠️'}"""
        
        return response
        
    except Exception as e:
        logger.error(f"Error handling query_month: {str(e)}")
        return "❌ Could not get this month's summary."


def handle_report(user, session):
    """Generate a credit-ready 30-day financial report."""
    try:
        today = datetime.utcnow()
        month_start = today - timedelta(days=30)
        
        month_income = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'income',
            Transaction.created_at >= month_start
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        month_expenses = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.type == 'expense',
            Transaction.created_at >= month_start
        ).with_entities(
            lambda t: db.func.sum(t.amount)
        ).scalar() or 0
        
        profit = month_income - month_expenses
        
        # Count active days (days with at least one transaction)
        active_days = session.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.created_at >= month_start
        ).count()
        
        consistency_score = min(100, int((active_days / 30) * 100))
        
        response = f"""📋 AMKA Financial Report (30 Days)

Period: {month_start.date()} to {today.date()}

Income:            R{month_income:.2f}
Expenses:          R{month_expenses:.2f}
Net Profit:        R{profit:.2f}
Active Days:       {active_days}/30
Consistency Score: {consistency_score}/100

This report can be shared with microfinance lenders.
Reply 'send report' to receive it as a PDF."""
        
        return response
        
    except Exception as e:
        logger.error(f"Error handling report: {str(e)}")
        return "❌ Could not generate report."


# ─────────────────────────────────────────────────────────────────────────────
# Twilio Helper
# ─────────────────────────────────────────────────────────────────────────────

def send_whatsapp_message(to_number, message_body):
    """Send a WhatsApp message via Twilio."""
    try:
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=f'whatsapp:{to_number}'
        )
        logger.info(f"Message sent to {to_number}: {message.sid}")
        return message.sid
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {str(e)}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=os.getenv('FLASK_ENV') == 'development')