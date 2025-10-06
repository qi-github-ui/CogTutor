import argparse, os, pandas as pd

try:
    from . import dataops
except Exception:
    dataops = None
try:
    from . import brd
except Exception:
    brd = None
try:
    from . import tutorshop
except Exception:
    tutorshop = None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=False)
    args = ap.parse_args()

    interim_dir = 'data/interim'
    os.makedirs(interim_dir, exist_ok=True)
    aligned_path = os.path.join(interim_dir, 'aligned_logs.csv')


    if not os.path.exists(aligned_path):
        df = pd.DataFrame([
            {"session_id":"S1","problem_id":"P1","step":1,"input":"3+2=7","gold":"5","correct":0,"hint":"Check addition rule.","ability":"low"},
            {"session_id":"S2","problem_id":"P2","step":1,"input":"1/2 + 1/3","gold":"5/6","correct":1,"hint":"","ability":"high"},
        ])
        df.to_csv(aligned_path, index=False)
    print(f"[prepare_datashop] aligned logs -> {aligned_path}")

if __name__ == '__main__':
    main()
