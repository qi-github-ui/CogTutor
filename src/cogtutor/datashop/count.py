import json

# 读取 sim_dataset_medium.json 文件
with open('high_proficiency.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 输出数据条目数量
print(f"数据条目数量: {len(data)}")
