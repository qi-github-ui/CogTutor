import argparse, os, pandas as pd, json
try:
    from . import narratives
except Exception:
    narratives = None

def to_llama_factory_record(row):
    ability = row.get('ability','medium')
    instr = f"You are a student with ability level: {ability}. Solve the problem and narrate your thinking."
    problem = row.get('input','')
    narrative = "I read the problem carefully, recall related knowledge, and check my steps. If I see a mistake, I fix it."
    return {
        "instruction": instr,
        "input": str(problem),
        "output": narrative,
        "meta": {"ability": ability, "kcs": row.get('kcs',[]), "source":"real"}
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=False)
    args = ap.parse_args()

    interim_dir = 'data/interim'
    processed_dir = 'data/processed'
    os.makedirs(processed_dir, exist_ok=True)

    df = pd.read_csv(os.path.join(interim_dir,'aligned_logs.csv'))

    # 切分 train/val/test
    n = len(df)
    a, b = max(1,int(0.7*n)), max(2,int(0.85*n))
    train, val, test = df.iloc[:a], df.iloc[a:b], df.iloc[b:]

    for split, d in [("train",train),("val",val),("test",test)]:
        out_path = os.path.join(processed_dir, f"cogtutor_{split}.jsonl")
        with open(out_path,'w',encoding='utf-8') as f:
            for _,row in d.iterrows():
                rec = to_llama_factory_record(row.to_dict())
                f.write(json.dumps(rec, ensure_ascii=False)+"\n")
        print(f"[make_cogtutor_corpus] {split} -> {out_path}")

if __name__ == '__main__':
    main()
