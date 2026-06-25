import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import logging

logger = logging.getLogger("welth.ml.pipeline")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)

class MLPipeline:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.model_path = os.path.join(MODEL_DIR, f"xgb_spending_{user_id}.joblib")

    def preprocess_data(self, transactions: list) -> pd.DataFrame:
        """Convert transaction JSON list to DataFrame and extract time-series aggregates."""
        if not transactions or len(transactions) < 5:
            logger.warning(f"Insufficient transactions for user {self.user_id} to run ML pipeline.")
            return pd.DataFrame()

        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        # Sort by date
        df = df.sort_values('date')
        
        # Group by day to compute total daily outflow
        outflows = df[df['type'].str.upper() == 'OUTFLOW']
        if outflows.empty:
            return pd.DataFrame()
            
        daily_spent = outflows.groupby(outflows['date'].dt.date)['amount'].sum().reset_index()
        daily_spent.columns = ['date', 'amount']
        
        # Feature Engineering: Lag features (prior 1-3 days spending)
        daily_spent['amount_lag_1'] = daily_spent['amount'].shift(1)
        daily_spent['amount_lag_2'] = daily_spent['amount'].shift(2)
        daily_spent['amount_lag_3'] = daily_spent['amount'].shift(3)
        
        # Drop rows with NaN lag values
        daily_spent = daily_spent.dropna().reset_index(drop=True)
        return daily_spent

    def train_model(self, processed_df: pd.DataFrame) -> dict:
        """Train XGBoost regressor model to predict daily expenses."""
        if processed_df.empty or len(processed_df) < 5:
            return {"status": "FAILED", "reason": "Insufficient data"}

        # Define Features and Target
        X = processed_df[['amount_lag_1', 'amount_lag_2', 'amount_lag_3']]
        y = processed_df['amount']

        # Simple train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
        
        # Fit model
        model = xgb.XGBRegressor(n_estimators=50, max_depth=3, learning_rate=0.1, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate model
        predictions = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)

        # Register/Save model
        joblib.dump(model, self.model_path)
        logger.info(f"Model saved successfully for user {self.user_id} at {self.model_path}")

        return {
            "status": "SUCCESS",
            "rmse": float(rmse),
            "r2": float(r2),
            "training_samples": len(X_train),
            "test_samples": len(X_test)
        }

    def predict_next_day(self, last_3_days_spending: list) -> float:
        """Predict tomorrow's spending given the list of spending from the last 3 days."""
        if not os.path.exists(self.model_path):
            logger.warning(f"No trained ML model found for user {self.user_id}. Using average fallback.")
            return float(np.mean(last_3_days_spending)) if last_3_days_spending else 0.0

        try:
            model = joblib.load(self.model_path)
            # Ensure shape is 2D: [[lag_1, lag_2, lag_3]]
            X_pred = np.array(last_3_days_spending).reshape(1, -1)
            prediction = model.predict(X_pred)
            return float(prediction[0])
        except Exception as e:
            logger.error(f"Prediction failed for user {self.user_id}: {e}")
            return float(np.mean(last_3_days_spending)) if last_3_days_spending else 0.0
