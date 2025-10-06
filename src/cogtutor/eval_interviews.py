import argparse, os, csv, statistics

DIMENSIONS = ["knowledge","logic","error_analysis","detail","style"]

def mean_ci(vals, alpha=0.05):
    n=len(vals)
    if n==0: return (float('nan'), float('nan'), float('nan'))
    m = statistics.mean(vals)
    sd = statistics.pstdev(vals) if n==1 else statistics.stdev(vals)
    z=1.96; se = sd / (n**0.5) if n>0 else float('inf')
    return (m, m - z*se, m + z*se)

def read_scores(path):
    rows=[]
    with open(path,'r',encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            rr={k:v for k,v in r.items()}
            for d in DIMENSIONS:
                rr[d]=float(rr[d])
            rows.append(rr)
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=False)
    ap.add_argument('--scores_csv', default=None)  # data/eval/interview_scores.csv
    args = ap.parse_args()
    eval_dir = 'data/eval'
    scores = args.scores_csv or os.path.join(eval_dir,'interview_scores.csv')
    rows = read_scores(scores); by_turn = {}
    for r in rows:
        t = r.get('turn_type','single')
        by_turn.setdefault(t, []).append(r)
    print('turn_type,dimension,N,mean,ci_low,ci_high')
    for t, items in by_turn.items():
        for d in DIMENSIONS:
            vals=[it[d] for it in items]
            m, lo, hi = mean_ci(vals)
            print('%s,%s,%d,%.2f,%.2f,%.2f' % (t,d,len(vals),m,lo,hi))

if __name__ == '__main__':
    main()
