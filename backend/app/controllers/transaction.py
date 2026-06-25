from fastapi import APIRouter, Depends, status, UploadFile, File
from backend.app.services.transaction_service import TransactionService
from backend.app.api.deps import get_current_user
from backend.app.storage.uploads import save_upload_file
from pydantic import BaseModel
from typing import Optional, Any, List

router = APIRouter()
tx_service = TransactionService()

class TransactionCreate(BaseModel):
    accountId: str
    amount: float
    currency: Optional[str] = "USD"
    category: Optional[str] = "OTHER"
    description: Optional[str] = ""
    type: str  # INFLOW or OUTFLOW
    date: Optional[str] = None
    status: Optional[str] = "COMPLETED"

@router.get("/", response_model=List[Any])
async def get_transactions(current_user: Any = Depends(get_current_user), limit: int = 100):
    txs = await tx_service.list_transactions(current_user.id, limit=limit)
    return txs

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(tx_in: TransactionCreate, current_user: Any = Depends(get_current_user)):
    tx = await tx_service.create_transaction(current_user.id, tx_in.model_dump())
    return tx

@router.get("/cashflow")
async def get_cashflow(current_user: Any = Depends(get_current_user)):
    analysis = await tx_service.get_cashflow_analysis(current_user.id)
    return analysis

@router.post("/upload-receipt")
async def upload_receipt(file: UploadFile = File(...), current_user: Any = Depends(get_current_user)):
    file_url = await save_upload_file(file)
    # Parse OCR using AI
    from backend.app.ai.gemini_client import GeminiClient
    ai = GeminiClient()
    ocr_result = await ai.parse_receipt_ocr(f"Receipt image upload: {file_url}")
    
    # Save the receipt log to the database
    from backend.app.core.db import db
    import datetime
    receipt_record = await db.receipt.create(
        data={
            "userId": current_user.id,
            "fileName": file.filename or "receipt.jpg",
            "filePath": file_url,
            "rawText": "Processed by Gemini AI OCR",
            "parsedAmount": float(ocr_result.get("total_amount", 0.0)),
            "parsedMerchant": ocr_result.get("merchant", "Unknown Merchant"),
            "parsedDate": datetime.datetime.fromisoformat(ocr_result.get("date", datetime.date.today().isoformat())),
            "status": "PROCESSED"
        }
    )
    
    return {
        "receipt_id": receipt_record.id,
        "ocr_data": ocr_result,
        "file_url": file_url
    }
