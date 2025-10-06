import argparse, os, pandas as pd, json
try:
    from . import tutorshop
except Exception:
    tutorshop = None

def _map_kc(expr: str):

    if '/' in str(expr): return ['fraction','addition']
    if '+' in str(expr): return ['addition']
    return ['arithmetic']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=False)
    args = ap.parse_args()

    interim_dir = 'data/interim'
    os.makedirs(interim_dir, exist_ok=True)
    aligned_path = os.path.join(interim_dir, 'aligned_logs.csv')

    df = pd.read_csv(aligned_path)

    df['kcs'] = df['input'].apply(_map_kc)

    domain_path = os.path.join(interim_dir, 'domain_model.json')
    json.dump({'kcs': sorted({k for row in df['kcs'] for k in row})}, open(domain_path,'w'))

    df.to_csv(aligned_path, index=False)
    print(f"[build_domain_model] domain -> {domain_path}; updated logs -> {aligned_path}")

if __name__ == '__main__':
    main()
