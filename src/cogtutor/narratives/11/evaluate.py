import json
import os
from openai import OpenAI

# 加载数据
with open('rubric_transformed.json', 'r', encoding='utf-8') as rubric_file:
    rubric_data = json.load(rubric_file)

# with open('30-2/30-2-high-Qwen-lora.json', 'r', encoding='utf-8') as problems_file:
#     problems_data = json.load(problems_file)

# 归一化函数，用于处理分类名称
def normalize_category_name(category_name):
    return category_name.strip().lower().replace("（", "(").replace("）", ")")

# 匹配评分标准
def get_rubric_for_category(category_name):
    normalized_name = normalize_category_name(category_name)
    for rubric in rubric_data:
        if normalize_category_name(rubric['category']).startswith(normalized_name):
            return rubric['scores']
    return None

# 调用OpenAI API进行评分
def evaluate_response(category, problem, response, rubric_scores):
    prompt = f"根据以下评分标准，给出该回答的评分：\n\n分类：{category}\n\n评分标准：\n"
    for score in rubric_scores:
        prompt += f"- {score['score']}: {score['description']}\n"

    prompt += f"\n问题：{problem}\n回答：{response}\n\n请根据评分标准为该回答打分,不用给出评分理由"

    # 调用OpenAI API
    client = OpenAI(base_url='https://api.pumpkinaigc.online/v1',
                    api_key='sk-TT3RixAQWmVvW3qL5c3166A8A92d428cBfDb483cE3DdE85d')

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是一个评分助手，负责为问题的回答进行评分。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

output_dir = 'Score-High'
os.makedirs(output_dir, exist_ok=True)
# 为所有问题评分
single_dir = 'Single-High'
for filename in sorted(os.listdir(single_dir)):
    if filename.endswith('.json'):
        filepath = os.path.join(single_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as problems_file:
            problems_data = json.load(problems_file)

        # 为所有问题评分
        scored_data = []
        for category_data in problems_data:
            category_name = category_data['code']
            rubric_scores = get_rubric_for_category(category_name)
            if not rubric_scores:
                print(f"未找到分类 {category_name} 的评分标准，跳过。")
                continue

            scored_problems = []
            for problem_data in category_data['problems']:
                problem = problem_data['problem']
                response = problem_data['response']
                try:
                    score = evaluate_response(category_name, problem, response, rubric_scores)
                    scored_problems.append({
                        "problem": problem,
                        "response": response,
                        "score": score
                    })
                except Exception as e:
                    print(f"评分失败：{e}")
                    scored_problems.append({
                        "problem": problem,
                        "response": response,
                        "score": "评分失败"
                    })

            scored_data.append({
                "category": category_name,
                "problems": scored_problems
            })

        # 保存评分结果
        output_filename = f"{filename[:-5]}-Score.json"
        output_file = os.path.join(output_dir, output_filename)
        with open(output_file, 'w', encoding='utf-8') as out_file:
            json.dump(scored_data, out_file, ensure_ascii=False, indent=4)

        print(f"评分完成，结果已保存到 {output_file}")
