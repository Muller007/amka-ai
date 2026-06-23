#!/usr/bin/env python3
"""
AMKA AI Engine v3 - Fine-tuned DistilBERT
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import re
from typing import Dict, Tuple

class AMKAFinetuneEngine:
    """AMKA AI Engine using fine-tuned DistilBERT"""
    
    def __init__(self, model_path="./amka_finetuned_model", use_fallback=True):
        """
        Initialize fine-tuned model
        
        Args:
            model_path: Path to fine-tuned model directory
            use_fallback: Use regex fallback if model fails
        """
        self.use_fallback = use_fallback
        
        try:
            print("[AI] Loading fine-tuned model...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            self.model_loaded = True
            print("[AI] ✅ Fine-tuned model loaded")
        except Exception as e:
            print(f"[AI] ⚠️  Model load failed: {e}")
            self.model_loaded = False
            if not use_fallback:
                raise
        
        # Label mappings
        self.intent_labels = {
            0: "income",
            1: "expense",
            2: "query",
            3: "report",
            4: "help"
        }
        
        # Category patterns (for regex fallback)
        self.income_keywords = [
            r'\b(sold|earned|made|got|income|revenue|sales|profit)\b',
            r'\b(R?\d+)\b.*\b(sold|earned|made|income)\b',
        ]
        
        self.expense_keywords = [
            r'\b(spent|paid|bought|cost|expense|purchase)\b',
            r'\b(R?\d+)\b.*\b(spent|paid|bought|cost)\b',
        ]
    
    def classify_with_finetuned(self, text: str) -> Tuple[str, float]:
        """
        Classify using fine-tuned model
        
        Args:
            text: User message
            
        Returns:
            Tuple of (intent, confidence)
        """
        if not self.model_loaded:
            return None, 0.0
        
        try:
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=128
            )
            
            # Get prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Get probabilities and label
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidence, predicted_class = torch.max(probabilities, dim=-1)
            
            intent = self.intent_labels[predicted_class.item()]
            confidence_score = confidence.item()
            
            return intent, confidence_score
        except Exception as e:
            print(f"[AI] Error in fine-tuned classification: {e}")
            return None, 0.0
    
    def classify_with_regex(self, text: str) -> Tuple[str, float]:
        """
        Fallback regex-based classification
        
        Args:
            text: User message
            
        Returns:
            Tuple of (intent, confidence)
        """
        text_lower = text.lower()
        
        # Check for queries first (distinct patterns)
        if any(word in text_lower for word in ['what', 'how', 'show', 'tell', 'can i', 'am i', 'do i']):
            if any(word in text_lower for word in ['profit', 'earned', 'earn', 'income', 'make', 'made']):
                return "query", 0.85
            elif any(word in text_lower for word in ['loan', 'borrow', 'credit', 'qualify']):
                return "query", 0.85
            elif any(word in text_lower for word in ['score', 'rating', 'rank']):
                return "query", 0.85
            elif any(word in text_lower for word in ['balance', 'total', 'sum']):
                return "query", 0.85
            else:
                return "query", 0.75
        
        # Check for reports
        if any(word in text_lower for word in ['summary', 'report', 'week', 'month', 'day', 'show']):
            if any(word in text_lower for word in ['week', 'weekly']):
                return "report", 0.9
            elif any(word in text_lower for word in ['month', 'monthly']):
                return "report", 0.9
            elif any(word in text_lower for word in ['day', 'daily']):
                return "report", 0.9
            else:
                return "report", 0.8
        
        # Check for help
        if any(word in text_lower for word in ['help', 'explain', 'understand', 'confused', 'how do i', "don't know"]):
            return "help", 0.85
        
        # Check for income (look for amount + income keywords)
        amount_match = re.search(r'R?(\d+(?:,\d{3})*(?:\.\d{2})?)', text_lower)
        has_income_keyword = any(re.search(pattern, text_lower) for pattern in self.income_keywords)
        
        if has_income_keyword or (amount_match and any(word in text_lower for word in ['sold', 'earned', 'made', 'income', 'sales'])):
            return "income", 0.9
        
        # Check for expense (look for amount + expense keywords)
        has_expense_keyword = any(re.search(pattern, text_lower) for pattern in self.expense_keywords)
        
        if has_expense_keyword or (amount_match and any(word in text_lower for word in ['spent', 'paid', 'bought', 'cost', 'purchase'])):
            return "expense", 0.9
        
        # Default: unknown (very low confidence)
        return "unknown", 0.3
    
    def process_message(self, text: str) -> Dict:
        """
        Process user message and extract transaction data
        
        Args:
            text: User message
            
        Returns:
            Dict with intent, confidence, extracted data
        """
        # Try fine-tuned model first
        intent, confidence = self.classify_with_finetuned(text)
        
        # Fallback to regex if model failed
        if intent is None and self.use_fallback:
            intent, confidence = self.classify_with_regex(text)
        
        # If still no intent, classify with regex anyway
        if intent is None:
            intent, confidence = self.classify_with_regex(text)
        
        # Extract amount
        amount_match = re.search(r'R?(\d+(?:,\d{3})*(?:\.\d{2})?)', text)
        amount = int(amount_match.group(1).replace(',', '')) if amount_match else 0
        
        result = {
            "text": text,
            "intent": intent,
            "confidence": confidence,
            "amount": amount,
            "method": "finetuned" if self.model_loaded else "regex",
        }
        
        # Add categorical info based on intent
        if intent == "income":
            result["type"] = "income"
            result["description"] = f"Income recorded: R{amount}"
        elif intent == "expense":
            result["type"] = "expense"
            result["description"] = f"Expense recorded: R{amount}"
        elif intent == "query":
            result["type"] = "query"
            result["description"] = f"Query: {text}"
        elif intent == "report":
            result["type"] = "report"
            result["description"] = f"Report requested"
        elif intent == "help":
            result["type"] = "help"
            result["description"] = f"Help request"
        else:
            result["type"] = "unknown"
            result["description"] = f"Unknown message type"
        
        return result
    
    def get_status(self) -> Dict:
        """Get AI engine status"""
        return {
            "model_loaded": self.model_loaded,
            "method": "fine-tuned DistilBERT" if self.model_loaded else "regex fallback",
            "num_labels": len(self.intent_labels),
            "max_input_length": 128
        }


if __name__ == "__main__":
    # Test the engine
    engine = AMKAFinetuneEngine()
    
    print("\n[TEST] AMKA Fine-tuned AI Engine")
    print(f"Status: {engine.get_status()}\n")
    
    # Test cases
    test_messages = [
        "I sold R300 on tomatoes",
        "Spent R50 on transport",
        "What's my profit today?",
        "Show me weekly summary",
        "How do I use AMKA?",
        "I earned R500",
        "Bought stock for R2000",
        "Can I get a loan?",
    ]
    
    print("[TEST] Processing sample messages:\n")
    for msg in test_messages:
        result = engine.process_message(msg)
        print(f"Message: {msg}")
        print(f"Intent: {result['intent']} (confidence: {result['confidence']:.2%})")
        print(f"Method: {result['method']}")
        print(f"Description: {result['description']}\n")