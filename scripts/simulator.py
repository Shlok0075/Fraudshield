"""FraudShield transaction simulator with six demo scenarios."""
import argparse, random, time
from datetime import datetime
import requests

SCENARIOS = {
    "normal": lambda: (round(random.uniform(10, 180), 2), "known-device", "known-location"),
    "suspicious": lambda: (round(random.uniform(200, 900), 2), "known-device", "unusual-location"),
    "high-value": lambda: (round(random.uniform(5000, 15000), 2), "known-device", "known-location"),
    "rapid": lambda: (round(random.uniform(20, 400), 2), "known-device", "known-location"),
    "new-device": lambda: (round(random.uniform(50, 800), 2), f"new-{random.randint(1000,9999)}", "known-location"),
    "unusual-location": lambda: (round(random.uniform(80, 1200), 2), "known-device", "geo-anomaly"),
}
def base_features(amount):
    return {"Time": float(datetime.utcnow().hour * 3600 + datetime.utcnow().minute * 60),
            "Amount": amount, **{f"V{i}": random.gauss(0, 1) for i in range(1, 29)}}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--api',default='http://localhost:8000')
    ap.add_argument('--token',required=True)
    ap.add_argument('--scenario',choices=[*SCENARIOS,'all'],default='all')
    ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--delay',type=float,default=.5)
    args=ap.parse_args()
    scenarios=list(SCENARIOS) if args.scenario=='all' else [args.scenario]
    headers={'Authorization':f'Bearer {args.token}'}
    for scenario in scenarios:
        for _ in range(args.count):
            amount, _, _ = SCENARIOS[scenario]()
            features=base_features(amount)
            features['V4'] += {'normal':0,'suspicious':1.5,'high-value':2.5,'rapid':1.0,'new-device':1.3,'unusual-location':1.7}[scenario]
            r=requests.post(f'{args.api}/transactions/predict',json={'features':features},headers=headers,timeout=15)
            print(scenario, r.status_code, r.json().get('prediction',{}))
            time.sleep(args.delay if scenario!='rapid' else .05)
if __name__=='__main__':
    main()
