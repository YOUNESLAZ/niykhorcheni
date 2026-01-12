import numpy as np
import pandas as pd
import json
import os
import joblib
from typing import Dict, Any
from app.config import EXPECTED_COLUMNS, SKEWED_FEATURES, CATEGORICAL_FEATURES, ARTIFACTS_DIR

# Global cache for encoders
_encoders = {}

def load_encoders():
    """Load label encoders from disk or create mock ones."""
    global _encoders
    if _encoders:
        return _encoders

    mappings_path = os.path.join(ARTIFACTS_DIR, "label_mappings.json")
    encoders_path = os.path.join(ARTIFACTS_DIR, "encoders.joblib")

    if os.path.exists(encoders_path):
        _encoders = joblib.load(encoders_path)
    elif os.path.exists(mappings_path):
        with open(mappings_path, 'r') as f:
            mappings = json.load(f)
        # Convert dict mappings to simple lookup or robust encoder simulation
        _encoders = mappings
    else:
        print("Warning: Encoders not found. Using simple hash/identity fallback.")
        _encoders = {} 
    
    return _encoders

def encode_feature(col_name: str, value: Any, encoders: Dict) -> int:
    """Helper to encode a single value safely."""
    # Real implementation would use scikit-learn LabelEncoder
    # Here we simulate or use the loaded dictionary
    if col_name in encoders:
        encoder = encoders[col_name]
        if hasattr(encoder, 'transform'): # It's a proper sklearn encoder
            try:
                return encoder.transform([value])[0]
            except ValueError:
                return -1 # Handle unseen labels
        elif isinstance(encoder, dict): # It's a dictionary mapping
             return encoder.get(value, -1)
    
    # Fallback if no encoder: hash it for consistency in mock mode
    return abs(hash(value)) % 100

def preprocess_features(input_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Transform input dictionary into a DataFrame compatible with the model.
    1. Validate fields
    2. Log Transform
    3. Encode Categoricals
    4. Enforce Column Order
    """
    df = pd.DataFrame([input_data])
    
    # 1. Log transform skewed features
    for col in SKEWED_FEATURES:
        if col in df.columns:
            # Ensure strictly positive for log
            val = df[col].clip(lower=0)
            df[col] = np.log1p(val)
            
    # 2. Encode categoricals
    encoders = load_encoders()
    for col in CATEGORICAL_FEATURES:
        if col in df.columns:
            val = df.iloc[0][col]
            df[col] = encode_feature(col, val, encoders)

    # 3. Add missing columns with 0
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = 0

    # 4. Enforce exact column order
    df = df[EXPECTED_COLUMNS]
    
    return df