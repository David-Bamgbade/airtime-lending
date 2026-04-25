import pickle

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
        elif score > 40:
            max_loan = 1500
        elif score > 20:
            max_loan = 500
        else:
            max_loan = 0
            
        return {'credit_score': round(score, 1), 'max_loan': max_loan, 'risk_level': 'Low' if score > 70 else 'Medium' if score > 40 else 'High'}

if __name__ == "__main__":
    model = SimpleCreditScorer()
    with open('credit_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("✅ Model saved")
    test_sub = {'recharge_freq': 25, 'sim_age_days': 500, 'avg_recharge': 3000, 'defaults': 0}
    print(model.score(test_sub))