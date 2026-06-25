import argparse
import asyncio
from backend.app.ml.pipeline import MLPipeline

async def run_training(user_id: str):
    print(f"Starting ML training pipeline for User {user_id}...")
    
    # Mock some transaction data to run the pipeline
    import datetime
    mock_transactions = []
    base_date = datetime.datetime.now() - datetime.timedelta(days=30)
    
    # Generate 30 days of transactions (some inflows, mostly outflows)
    for i in range(30):
        # Outflow
        mock_transactions.append({
            "amount": float(10 + (i % 5) * 15 + (i % 3) * 5),
            "type": "OUTFLOW",
            "date": (base_date + datetime.timedelta(days=i)).isoformat()
        })
        
    pipeline = MLPipeline(user_id)
    df = pipeline.preprocess_data(mock_transactions)
    results = pipeline.train_model(df)
    print(f"ML Pipeline results: {results}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train ML model for user spending.")
    parser.add_argument("--user_id", type=str, required=True, help="User ID to train model for")
    args = parser.parse_args()
    
    asyncio.run(run_training(args.user_id))
