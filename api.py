from fastapi import FastAPI
from pydantic import BaseModel
from fraud_detector import FraudDetector

class SimpleCreditScorer:
    def __init__(self):
        self.weights = {
            'recharge_freq': 0.4,
            'sim_age_days': 0.3,
            'avg_recharge': 0.2,
            'defaults': -0.5
        }
    
    def score(self, subscriber):
        freq_score = min(subscriber['recharge_freq'] / 30, 1)
        age_score = min(subscriber['sim_age_days'] / 730, 1)
        recharge_score = min(subscriber['avg_recharge'] / 5000, 1)
        default_penalty = 0 if subscriber['defaults'] == 0 else 0.8
        
        raw = (
            freq_score * self.weights['recharge_freq'] +
            age_score * self.weights['sim_age_days'] +
            recharge_score * self.weights['avg_recharge'] -
            default_penalty * abs(self.weights['defaults'])
        )
        
        score = max(0, min(100, raw * 100))
        
        if score > 80:
            max_loan = 5000
        elif score > 60:
            max_loan = 3000
        else:
            max_loan = 1500
            
        return {'credit_score': round(score, 1), 'max_loan': max_loan}

app = FastAPI()
credit_model = SimpleCreditScorer()
fraud_detector = FraudDetector()

class LoanRequest(BaseModel):
    msisdn: str
    requested_amount: int
    recharge_freq: int
    sim_age_days: int
    avg_recharge: int
    defaults: int

@app.post("/request_loan")
async def request_loan(req: LoanRequest):
    subscriber = {
        'recharge_freq': req.recharge_freq,
        'sim_age_days': req.sim_age_days,
        'avg_recharge': req.avg_recharge,
        'defaults': req.defaults
    }
    
    is_fraud, reason = fraud_detector.check(req.msisdn, req.requested_amount, subscriber)
    if is_fraud:
        return {"status": "rejected", "reason": reason}
    
    result = credit_model.score(subscriber)
    
    if req.requested_amount <= result['max_loan']:
        return {"status": "approved", "loan_amount": req.requested_amount, "credit_score": result['credit_score']}
    else:
        return {"status": "rejected", "reason": f"Request exceeds limit of ₦{result['max_loan']}"}

@app.get("/health")
def health():
    return {"status": "ok"}