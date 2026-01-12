from pydantic import BaseModel, Field
from typing import Optional

class NetworkFlowInput(BaseModel):
    # Basic Flow Features
    dur: float = Field(..., description="Record total duration")
    proto: str = Field(..., description="Transaction protocol (e.g., tcp, udp)")
    service: str = Field(..., description="http, ftp, smtp, ssh, dns, etc.")
    state: str = Field(..., description="Indicates to the state and its dependent protocol, e.g. ACC, CLO, CON")
    
    # Volumetric Features
    spkts: int = Field(..., description="Source to destination packet count")
    dpkts: int = Field(..., description="Destination to source packet count")
    sbytes: int = Field(..., description="Source to destination transaction bytes")
    dbytes: int = Field(..., description="Destination to source transaction bytes")
    
    # TTL and others
    sttl: int = Field(..., description="Source to destination time to live value")
    dttl: int = Field(..., description="Destination to source time to live value")
    sload: float = Field(..., description="Source bits per second")
    dload: float = Field(..., description="Destination bits per second")
    sloss: int = Field(..., description="Source packets retransmitted or dropped")
    dloss: int = Field(..., description="Destination packets retransmitted or dropped")
    
    # Time features
    sintpkt: float = Field(..., description="Source interpacket arrival time (mSec)")
    dintpkt: float = Field(..., description="Destination interpacket arrival time (mSec)")
    sjit: float = Field(..., description="Source jitter (mSec)")
    djit: float = Field(..., description="Destination jitter (mSec)")
    swin: int = Field(..., description="Source TCP window advertisement value")
    stcpb: int = Field(..., description="Source TCP base sequence number")
    dtcpb: int = Field(..., description="Destination TCP base sequence number")
    dwin: int = Field(..., description="Destination TCP window advertisement value")
    
    # Advanced / Calculated Features (CT_*)
    ct_srv_src: int = Field(..., description="No. of connections that contain the same service (14) and source address (1) in 100 connections according to the last time (26).")
    ct_state_ttl: int = Field(..., description="No. of for each state (6) according to specific range of values for source/destination time to live (10) (11).")
    ct_dst_ltm: int = Field(..., description="No. of connections of the same destination address (3) in 100 connections according to the last time (26).")
    ct_src_dport_ltm: int = Field(..., description="No of connections of the same source address (1) and the destination port (4) in 100 connections according to the last time (26).")
    ct_dst_sport_ltm: int = Field(..., description="No of connections of the same destination address (3) and the source port (2) in 100 connections according to the last time (26).")
    ct_dst_src_ltm: int = Field(..., description="No of connections of the same source (1) and the destination (3) address in in 100 connections according to the last time (26).")
    
    # Boolean flags
    is_ftp_login: int = Field(0, description="If the ftp session is accessed by user and password then 1 else 0")
    ct_ftp_cmd: int = Field(0, description="No of flows that has a command in ftp session")
    ct_flw_http_mthd: int = Field(0, description="No. of flows that has methods such as Get and Post in http service.")
    ct_src_ltm: int = Field(..., description="No. of connections of the same source address (1) in 100 connections according to the last time (26).")
    ct_srv_dst: int = Field(..., description="No. of connections that contain the same service (14) and destination address (3) in 100 connections according to the last time (26).")
    
    # TCP RTT
    tcprtt: float = Field(0.0, description="TCP connection setup round-trip time, the sum of 'synack' and 'ackdat'.")
    synack: float = Field(0.0, description="TCP connection setup time, the time between the SYN and the SYN_ACK packets.")
    ackdat: float = Field(0.0, description="TCP connection setup time, the time between the SYN_ACK and the ACK packets.")

class PredictionOutput(BaseModel):
    is_attack: bool
    attack_category: str
    confidence: float
    processing_time_ms: float
