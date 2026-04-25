from datetime import datetime, timedelta
from collections import defaultdict

class FraudDetector:
    def __init__(self):
        self.request_history = defaultdict(list)
    
    def check(self, msisdn, requested_amount, subscriber_data):
        now = datetime.now()
        
        if subscriber_data['sim_age_days'] < 30:
            return True, f"SIM too new ({subscriber_data['sim_age_days']} days)"
        
        if requested_amount > subscriber_data['avg_recharge'] * 3:
            return True, f"Request ₦{requested_amount} > 3x avg recharge"
        
        self.request_history[msisdn] = [t for t in self.request_history[msisdn] if t > now - timedelta(hours=1)]
        
        if len(self.request_history[msisdn]) >= 3:
            return True, "Rate limit exceeded"
        
        self.request_history[msisdn].append(now)
        return False, "Approved"

if __name__ == "__main__":
    d = FraudDetector()
    test = {'sim_age_days': 15, 'avg_recharge': 500}
    print(d.check("08012345678", 2000, test))