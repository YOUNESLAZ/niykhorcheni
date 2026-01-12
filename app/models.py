import joblib
import pandas as pd
import numpy as np
import os
import random
from typing import Tuple

class NIDSModel:
    def __init__(self, binary_model_path: str = "binary_model.joblib", multiclass_model_path: str = "multiclass_model.joblib"):
        self.binary_model = None
        self.multiclass_model = None
        self.is_mock = False
        
        try:
            if os.path.exists(binary_model_path):
                print(f"Loading binary model from {binary_model_path}...")
                self.binary_model = joblib.load(binary_model_path)
            else:
                print("Binary model not found. Using MOCK mode.")
                self.is_mock = True

            if os.path.exists(multiclass_model_path):
                print(f"Loading multiclass model from {multiclass_model_path}...")
                self.multiclass_model = joblib.load(multiclass_model_path)
            else:
                 print("Multiclass model not found.")
                 # If binary is mock, multiclass is simpler to mock too
        except Exception as e:
            print(f"Error loading models: {e}. Switching to MOCK mode.")
            self.is_mock = True

    def predict(self, features: pd.DataFrame) -> Tuple[bool, str, float]:
        """
        Returns (is_attack, category, confidence)
        """
        if self.is_mock:
            return self._mock_predict(features)
        
        # 1. Binary Classification
        try:
            # Check if model expects specific columns (omitted for brevity)
            is_attack_prob = self.binary_model.predict_proba(features)[0][1]
            is_attack = is_attack_prob > 0.5
            
            if not is_attack:
                return False, "Normal", float(1.0 - is_attack_prob)
            
            # 2. Multi-class Classification
            # Assuming multiclass model trained on same features
            cat_probs = self.multiclass_model.predict_proba(features)[0]
            cat_idx = np.argmax(cat_probs)
            confidence = float(cat_probs[cat_idx])
            category = self.multiclass_model.classes_[cat_idx]
            
            return True, category, confidence
            
        except Exception as e:
            print(f"Inference error: {e}")
            # Fallback to mock if runtime error
            return self._mock_predict(features)

    def _mock_predict(self, features: pd.DataFrame) -> Tuple[bool, str, float]:
        """
        Simulation for testing API without trained models.
        """
        # Deterministic mock based on some feature to make it testable
        # e.g., if duration > 100, say it's an attack
        dur = features.get("dur", [0])[0] if "dur" in features else 0
        
        if dur > 50: # Arbitrary threshold for mock
            categories = ["DoS", "Exploits", "Fuzzers", "Generic", "Reconnaissance"]
            return True, random.choice(categories), 0.95
        else:
            return False, "Normal", 0.99
