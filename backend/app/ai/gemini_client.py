import os
import json
import logging
from typing import Dict, Any, Optional
import google.generativeai as genai
from backend.app.core.config import settings

logger = logging.getLogger("welth.ai.gemini")

# Initialize Gemini SDK
if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "MOCK_GEMINI_KEY":
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use Gemini 1.5 Flash as standard fast multimodal model
        model = genai.GenerativeModel("gemini-1.5-flash")
        gemini_ready = True
        logger.info("Gemini Client: Configured and ready.")
    except Exception as e:
        logger.error(f"Gemini Client config error: {e}")
        gemini_ready = False
else:
    gemini_ready = False
    logger.info("Gemini Client: API key not provided or mock. Running in offline/mock mode.")

def load_prompt_template(filename: str) -> str:
    """Read a markdown prompt template from the filesystem."""
    try:
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", filename)
        with open(prompt_path, "r") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to load prompt template {filename}: {e}")
        return ""

def clean_json_response(text: str) -> str:
    """Strip markdown code block wrappers (e.g. ```json ... ```) from LLM output."""
    clean = text.strip()
    if clean.startswith("```json"):
        clean = clean[7:]
    elif clean.startswith("```"):
        clean = clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    return clean.strip()

async def call_gemini(prompt: str) -> Optional[str]:
    """Execute generative call against Gemini API, logging exceptions."""
    if not gemini_ready:
        return None
    try:
        # Generate response using thread pool as SDK calls are blocking/sync
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: model.generate_content(prompt)
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini API call failed: {e}")
        return None

class GeminiClient:
    async def categorize_transaction(self, description: str) -> Dict[str, Any]:
        """Categorize a transaction description using LLM."""
        template = load_prompt_template("categorize.md")
        prompt = f"{template}\n\nTransaction description: '{description}'"
        
        response_text = await call_gemini(prompt)
        if response_text:
            try:
                cleaned = clean_json_response(response_text)
                return json.loads(cleaned)
            except Exception as e:
                logger.error(f"Failed to parse categorization JSON: {e}")
                
        # Mock/Fallback logic
        description_lower = description.lower()
        if any(w in description_lower for w in ["uber", "lyft", "taxi", "flight", "airlines"]):
            return {"category": "TRAVEL", "merchant": description.split()[0]}
        if any(w in description_lower for w in ["netflix", "spotify", "hulu", "steam", "disney"]):
            return {"category": "ENTERTAINMENT", "merchant": description.split()[0]}
        if any(w in description_lower for w in ["whole foods", "walmart", "grocery", "restaurant", "starbucks", "food"]):
            return {"category": "FOOD", "merchant": description.split()[0]}
        return {"category": "OTHER", "merchant": description}

    async def parse_receipt_ocr(self, raw_text: str) -> Dict[str, Any]:
        """Parse raw OCR text into structured receipt JSON."""
        template = load_prompt_template("receipt.md")
        prompt = f"{template}\n\nRaw OCR text:\n{raw_text}"
        
        response_text = await call_gemini(prompt)
        if response_text:
            try:
                cleaned = clean_json_response(response_text)
                return json.loads(cleaned)
            except Exception as e:
                logger.error(f"Failed to parse receipt OCR JSON: {e}")

        # Fallback Mock
        return {
            "merchant": "Target Stores",
            "total_amount": 42.15,
            "date": "2026-06-25",
            "category": "OTHER",
            "confidence": 0.85
        }

    async def get_financial_advice(self, query: str, context: str) -> Dict[str, Any]:
        """Query AI financial advisor with custom user context."""
        template = load_prompt_template("advisor.md")
        prompt = f"{template}\n\nUser Context:\n{context}\n\nQuestion: {query}"
        
        response_text = await call_gemini(prompt)
        if response_text:
            try:
                cleaned = clean_json_response(response_text)
                return json.loads(cleaned)
            except Exception as e:
                logger.error(f"Failed to parse financial advice JSON: {e}")

        return {
            "advice": "Keep an eye on your miscellaneous spending. Consider establishing a larger emergency fund covering 3 to 6 months of expenses.",
            "recommended_actions": ["Increase savings target to 20%", "Review subscription list"]
        }

    async def detect_fraud_anomalies(self, transaction: Dict[str, Any], user_history_summary: str) -> Dict[str, Any]:
        """Assess transaction for fraud markers using Gemini prompt."""
        template = load_prompt_template("fraud.md")
        prompt = f"{template}\n\nTransaction:\n{json.dumps(transaction)}\n\nUser History Context:\n{user_history_summary}"
        
        response_text = await call_gemini(prompt)
        if response_text:
            try:
                cleaned = clean_json_response(response_text)
                return json.loads(cleaned)
            except Exception as e:
                logger.error(f"Failed to parse fraud JSON: {e}")

        return {
            "is_fraud": False,
            "confidence_score": 0.05,
            "flagged_reasons": []
        }

    async def generate_monthly_report(self, cash_flow: Dict[str, Any], budget_summary: str) -> Dict[str, Any]:
        """Summarize monthly performance and goals."""
        template = load_prompt_template("monthly_report.md")
        prompt = f"{template}\n\nCash Flow:\n{json.dumps(cash_flow)}\n\nBudgets:\n{budget_summary}"
        
        response_text = await call_gemini(prompt)
        if response_text:
            try:
                cleaned = clean_json_response(response_text)
                return json.loads(cleaned)
            except Exception as e:
                logger.error(f"Failed to parse monthly report JSON: {e}")

        return {
            "summary": "You maintained a positive cash flow this month. Great job sticking to your utilities and travel budgets.",
            "achievements": ["Remained under budget in Entertainment", "Saved 15% of net income"],
            "focus_areas": ["Food costs rose by 10%", "Boost stock market investments"]
        }

    async def recommend_investments(self, risk_profile: str, age: int, net_worth: float) -> Dict[str, Any]:
        """Request recommended assets based on user risk tolerance."""
        template = load_prompt_template("investment.md")
        prompt = f"{template}\n\nAge: {age}\nRisk Profile: {risk_profile}\nNet Worth: {net_worth}"
        
        response_text = await call_gemini(prompt)
        if response_text:
            try:
                cleaned = clean_json_response(response_text)
                return json.loads(cleaned)
            except Exception as e:
                logger.error(f"Failed to parse investment JSON: {e}")

        return {
            "risk_rating": risk_profile,
            "recommendations": [
                {
                    "symbol": "VOO",
                    "name": "Vanguard S&P 500 ETF",
                    "type": "MUTUAL_FUND",
                    "allocation_percent": 60,
                    "reason": "Diversified low-cost index tracking perfect for long term wealth compounding."
                },
                {
                    "symbol": "BTC",
                    "name": "Bitcoin",
                    "type": "CRYPTO",
                    "allocation_percent": 10,
                    "reason": "Speculative asset for higher growth potential matching risk profile."
                }
            ]
        }
