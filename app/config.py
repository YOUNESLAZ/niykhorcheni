import os

# The exact order of features expected by the model. 
# Based on UNSW-NB15 typical cleaned dataset.
EXPECTED_COLUMNS = [
    'dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes', 'dbytes', 
    'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sintpkt', 'dintpkt', 
    'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 
    'ackdat', 'smean', 'dmean', 'trans_depth', 'response_body_len', 
    'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm', 
    'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'is_ftp_login', 'ct_ftp_cmd', 
    'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst', 'is_sm_ips_ports'
]

# Features that undergo Log1p transformation
SKEWED_FEATURES = [
    'dur', 'sbytes', 'dbytes', 'sload', 'dload', 'sintpkt', 'dintpkt', 
    'sjit', 'djit', 'tcprtt', 'synack', 'ackdat'
]

# Categorical features requiring encoding
CATEGORICAL_FEATURES = ['proto', 'service', 'state']

# Path to artifacts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.dirname(BASE_DIR) # Root dir
