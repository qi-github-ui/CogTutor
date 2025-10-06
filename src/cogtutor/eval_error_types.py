import argparse, os, json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

ERROR_ORDER = ["NC","CU","PC","SD","SO"]

def load_jsonl(path):
    with open(path,'r',encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line: continue
            yield json.loads(line)

def dist(records):
    c = Counter([r.get('error_type','') for r in records if r.get('error_type')])
    total = sum(c.values()) or 1
    return [c.get(k,0)/total for k in ERROR_ORDER]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=False)
    ap.add_argument('--preds', default=None)    # 模型预测(ability,error_type)
    ap.add_argument('--student', default=None)  # 学生基线(ability,error_type)
    args = ap.parse_args()
    eval_dir = 'data/eval'
    preds_path = args.preds or os.path.join(eval_dir,'preds_model.jsonl')
    student_path = args.student or os.path.join(eval_dir,'student_baseline.jsonl')

    preds = defaultdict(list)
    for r in load_jsonl(preds_path):   preds[r.get('ability','unknown')].append(r)
    students = defaultdict(list)
    for r in load_jsonl(student_path): students[r.get('ability','unknown')].append(r)

    abilities = [a for a in ["low","medium","high"] if a in preds or a in students]
    os.makedirs('docs/figures', exist_ok=True)
    for a in abilities:
        m = dist(preds[a]); s = dist(students[a])
        xs = list(range(len(ERROR_ORDER))); width = 0.35
        plt.figure()
        plt.bar([x - width/2 for x in xs], s, width=width, label='Students')
        plt.bar([x + width/2 for x in xs], m, width=width, label='Model')
        plt.xticks(xs, ERROR_ORDER)
        plt.title(f'Error-Type Distribution (ability={a})')
        plt.xlabel('Error Type'); plt.ylabel('Proportion')
        plt.legend()
        out = f'docs/figures/error_types_{a}.png'
        plt.savefig(out, bbox_inches='tight', dpi=160); plt.close()
        print(f'[eval_error_types] saved {out}')

if __name__ == '__main__':
    main()
