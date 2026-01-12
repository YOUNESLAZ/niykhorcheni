import time
from fastapi import FastAPI, HTTPException
from app.schemas import NetworkFlowInput, PredictionOutput
from app.models import NIDSModel
from app.utils import preprocess_features

app = FastAPI(
    title="NIDS ML API",
    description="Network Intrusion Detection System API based on UNSW-NB15 dataset.",
    version="1.0.0"
)

# Initialize model (lazy loading or at startup)
model = NIDSModel()

@app.get("/")
def read_root():
    return {"status": "online", "message": "NIDS API is running. Use /predict to classify traffic."}

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": not model.is_mock}

@app.post("/predict", response_model=PredictionOutput)
def predict_flow(flow: NetworkFlowInput):
    start_time = time.time()
    
    try:
        # 1. Preprocess
        input_dict = flow.model_dump()
        features_df = preprocess_features(input_dict)
        
        # 2. Inference
        is_attack, category, confidence = model.predict(features_df)
        
        # 3. Response
        duration_ms = (time.time() - start_time) * 1000
        
        return PredictionOutput(
            is_attack=is_attack,
            attack_category=category,
            confidence=confidence,
            processing_time_ms=duration_ms
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
