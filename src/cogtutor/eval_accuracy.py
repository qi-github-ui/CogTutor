import argparse, os, json, random
from collections import defaultdict

def load_jsonl(path):
    with open(path,'r',encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line: continue
            yield json.loads(line)

def bootstrap_ci(accs, reps=2000, alpha=0.05):
    n=len(accs)
    if n==0: return (float('nan'), float('nan'), float('nan'))
    boots=[]
    for _ in range(reps):
        sample=[accs[random.randrange(n)] for __ in range(n)]
        boots.append(sum(sample)/len(sample))
    boots.sort()
    lo = boots[int((alpha/2)*reps)]
    hi = boots[int((1-alpha/2)*reps)-1]
    mean = sum(accs)/len(accs)
    return mean, lo, hi

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=False)
    ap.add_argument('--preds', default=None)  # data/eval/preds_model.jsonl
    args = ap.parse_args()
    eval_dir = 'data/eval'
    preds_path = args.preds or os.path.join(eval_dir, 'preds_model.jsonl')

    # 每行: { "ability": "...", "gold": "...", "pred": "..." }
    by_ability=defaultdict(list)
    for ex in load_jsonl(preds_path):
        gold=str(ex.get('gold','')).strip()
        pred=str(ex.get('pred','')).strip()
        ability=ex.get('ability','unknown')
        acc = 1.0 if (gold!='' and gold==pred) else 0.0
        by_ability[ability].append(acc)

    print('Ability\tN\tMeanAcc\tCI_low\tCI_high')
    for ability in sorted(by_ability.keys()):
        mean, lo, hi = bootstrap_ci(by_ability[ability])
        print(f'{ability}\t{len(by_ability[ability])}\t{mean:.3f}\t{lo:.3f}\t{hi:.3f}')

if __name__ == '__main__':
    main()
