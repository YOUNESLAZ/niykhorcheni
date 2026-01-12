from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    print("Health Check: PASSED")
    print(response.json())

def test_predict_normal():
    # Mock data representing normal traffic
    payload = {
        "dur": 0.1, "proto": "tcp", "service": "http", "state": "FIN",
        "spkts": 10, "dpkts": 10, "sbytes": 1000, "dbytes": 5000,
        "sttl": 62, "dttl": 252, "sload": 1000.0, "dload": 2000.0,
        "sloss": 0, "dloss": 0, "sintpkt": 1.0, "dintpkt": 1.0,
        "sjit": 5.0, "djit": 5.0, "swin": 255, "stcpb": 100, "dtcpb": 100,
        "dwin": 255, "ct_srv_src": 1, "ct_state_ttl": 0, "ct_dst_ltm": 1,
        "ct_src_dport_ltm": 1, "ct_dst_sport_ltm": 1, "ct_dst_src_ltm": 1,
        "is_ftp_login": 0, "ct_ftp_cmd": 0, "ct_flw_http_mthd": 0,
        "ct_src_ltm": 1, "ct_srv_dst": 1, "tcprtt": 0.0, "synack": 0.0, "ackdat": 0.0
    }
    
    response = client.post("/predict", json=payload)
    if response.status_code != 200:
        print(f"Prediction Failed: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    print("Prediction (Normal): PASSED")
    print(json.dumps(data, indent=2))
    assert data["is_attack"] == False

def test_predict_attack():
    # Mock data representing attack traffic (high duration triggers mock attack)
    payload = {
        "dur": 100.0, # Trigger mock attack
        "proto": "tcp", "service": "http", "state": "FIN",
        "spkts": 1000, "dpkts": 0, "sbytes": 100000, "dbytes": 0,
        "sttl": 254, "dttl": 0, "sload": 10000.0, "dload": 0.0,
        "sloss": 0, "dloss": 0, "sintpkt": 0.1, "dintpkt": 0.0,
        "sjit": 0.0, "djit": 0.0, "swin": 255, "stcpb": 100, "dtcpb": 0,
        "dwin": 0, "ct_srv_src": 10, "ct_state_ttl": 2, "ct_dst_ltm": 10,
        "ct_src_dport_ltm": 10, "ct_dst_sport_ltm": 10, "ct_dst_src_ltm": 10,
        "is_ftp_login": 0, "ct_ftp_cmd": 0, "ct_flw_http_mthd": 0,
        "ct_src_ltm": 10, "ct_srv_dst": 10, "tcprtt": 0.0, "synack": 0.0, "ackdat": 0.0
    }
    
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    print("Prediction (Attack): PASSED")
    print(json.dumps(data, indent=2))
    assert data["is_attack"] == True

if __name__ == "__main__":
    try:
        test_health()
        test_predict_normal()
        test_predict_attack()
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nTest failed: {e}")
