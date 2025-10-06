# Simulating Student Learning Behaviors with LLM-based Role-Playing Agents: A Data-Driven and Cognitively Inspired Framework

*(LLaMA-Factory Edition — 数据与评测，仅用于复现；训练/微调请在 LLaMA-Factory 中完成)*

> 复现论文：**“Simulating Student Learning Behaviors with LLM-based Role-Playing Agents: A Data-Driven and Cognitively Inspired Framework“
> 本仓库负责**数据准备与评测**；**模型训练/微调在 [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) 外部进行**。

---

* **📦 重要说明**：**`CogTutor_dataset` 是本论文对应的数据集**（与本文方法配套的发布版数据）。如果你仅需要数据，请使用 `CogTutor_dataset`。

---

## 目录结构

```
.
├── src/cogtutor/
│   ├── __init__.py
│   ├── prepare_datashop.py        # 数据清洗/对齐 → data/interim/aligned_logs.csv
│   ├── build_domain_model.py      # KC/领域模型 → data/interim/domain_model.json
│   ├── make_cogtutor_corpus.py    # 生成 LLaMA-Factory JSONL（train/val/test）
│   ├── eval_accuracy.py           # 分能力准确率 
│   ├── eval_error_types.py        # 错误类型分布分组柱状图（含学生基线）
│   └── eval_interviews.py         # 访谈式评测聚合
│   ├── dataops/                   # 原始数据处理脚本
│   ├── brd/                       # BRD 选择/抽取
│   ├── narratives/                # 叙事生成/过滤
│   └── tutorshop/                 # TutorShop 解析
├── configs/
│   └── data_paths.yaml
├── scripts/
│   ├── prepare_data.sh
│   └── eval_all.sh
├── data/
├── dataset/             
├── docs/
│   └── figures/                   # 评测图（自动生成）
└── README.md
```
## 安装

* Python ≥ 3.10
* 数据与评测依赖：

```bash
pip install -U pandas numpy scikit-learn matplotlib
```

> 训练/微调依赖由 **LLaMA-Factory** 环境负责，不在本仓库安装。

---

## 快速开始

```bash
# 1) 数据清洗/对齐
python -m src.cogtutor.prepare_datashop --config configs/data_paths.yaml

# 2) 领域模型 / KC 映射
python -m src.cogtutor.build_domain_model --config configs/data_paths.yaml

# 3) 生成 LLaMA-Factory 数据集 (JSONL)
python -m src.cogtutor.make_cogtutor_corpus --config configs/data_paths.yaml

# —— 训练/微调在 LLaMA-Factory 中完成 ——

# 4) 评测（需先准备模型预测/评分文件）
python -m src.cogtutor.eval_accuracy --config configs/data_paths.yaml
python -m src.cogtutor.eval_error_types --config configs/data_paths.yaml
python -m src.cogtutor.eval_interviews --config configs/data_paths.yaml
```

> 也可使用脚本：
> `bash scripts/prepare_data.sh` 与 `bash scripts/eval_all.sh`。

---

## 数据准备（Data Preparation）

1. **PSLC DataShop（Fractions Lab 2012）**：导出**步骤级日志**（CSV/TSV），放入 `data/raw/datashop/`。
2. **TutorShop**：导出**题目文本、KC、反馈/得分规则**等，放入 `data/raw/tutorshop/`。
3. 执行：

```bash
python -m src.cogtutor.prepare_datashop --config configs/data_paths.yaml
python -m src.cogtutor.build_domain_model --config configs/data_paths.yaml
```

生成：

* `data/interim/aligned_logs.csv`（对齐后的交互记录）
* `data/interim/domain_model.json`（KC/依赖等摘要）

> **注意**：不分发 DataShop/TutorShop 原始数据；请按其条款合法获取与使用。

---

## 导出 LLaMA-Factory 数据集

```bash
python -m src.cogtutor.make_cogtutor_corpus --config configs/data_paths.yaml
```

输出到 `data/processed/`：

* `cogtutor_train.jsonl`
* `cogtutor_val.jsonl`
* `cogtutor_test.jsonl`


> **合成叙事**：在 `src/cogtutor/narratives/` 中实现你的**生成与过滤**流程；如需外部 API，请通过环境变量配置密钥。

---

## 在 LLaMA-Factory 中训练/微调（外部）

---

## 评测（Evaluation）

### 1) 答题准确率（分能力层级）

输入预测（示例 `data/eval/preds_model.jsonl`），**每行**：

```json
{ "ability": "low", "gold": "5/6", "pred": "5/6" }
```

执行：

```bash
python -m src.cogtutor.eval_accuracy --config configs/data_paths.yaml
```


### 2) 错误类型分布（分组柱状图 + 学生基线）

错误类型：`NC`（数值计算）, `CU`（概念理解）, `PC`（题意理解）, `SD`（策略/推导）, `SO`（表述/其他）。
需要：

* 模型：`data/eval/preds_model.jsonl`（含 `ability`, `error_type`）
* 学生：`data/eval/student_baseline.jsonl`（同字段）
  执行：

```bash
python -m src.cogtutor.eval_error_types --config configs/data_paths.yaml
```

在 `docs/figures/` 生成**Students vs Model** 的**分组柱状图**（按能力层级）。

### 3) 访谈式评测（人类/LLM 评分聚合）

输入 `data/eval/interview_scores.csv`：

```csv
item_id,rater_id,turn_type,knowledge,logic,error_analysis,detail,style
q001,expertA,single,4,5,4,4,5
q002,expertB,multi,3,4,3,4,4
```

执行：

```bash
python -m src.cogtutor.eval_interviews --config configs/data_paths.yaml
```

---

## 数据集（CogTutor_dataset）

* **`CogTutor_dataset` 是本论文对应的数据集**，与本文方法配套：包含清洗后的交互记录、KC 映射摘要与指令式训练样本（或其获取/生成脚本）。
* 如果你**只需要数据集**而不运行全流程，请直接使用 **`CogTutor_dataset`**。
---
