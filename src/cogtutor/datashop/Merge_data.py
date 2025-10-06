import os
import json

# 设置要处理的目录路径
directory = 'high_output_json_files'  # 替换为你的目录路径
output_file_path = os.path.join(directory, 'merged_generate_high.json')

# 用于存储所有处理后的数据
all_data = []

# 遍历目录下的所有文件
for filename in os.listdir(directory):
    if filename.endswith('.json') and filename != 'low_example_data.json':  # 排除示例文件
        file_path = os.path.join(directory, filename)

        # 检查文件是否为空
        if os.path.getsize(file_path) == 0:
            print(f"Skipping empty file: {filename}")
            continue

        # 读取 JSON 文件内容
        with open(file_path, 'r') as file:
            try:
                file_content = file.read()
                data = json.loads(file_content)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON in file {filename}: {e}")
                continue

        # 获取并解析 dialogue 字符串中的 JSON 对象
        if "dialogue" in data and isinstance(data["dialogue"], str):
            try:
                raw_json_str = data["dialogue"].strip("```json").strip()
                parsed_data = json.loads(raw_json_str)
            except json.JSONDecodeError as e:
                print(f"Error parsing dialogue JSON in file {filename}: {e}")
                continue
        else:
            parsed_data = data

        # 处理为期望的格式
        formatted_data = {
            "dialogue": {
                "dialogue": parsed_data["dialogue"]  # 使用解析后的 dialogue 数据
            }
        }

        # 添加到合并数据中
        all_data.append(formatted_data)

# 将合并后的数据存放到一个新的 JSON 文件中
with open(output_file_path, 'w') as output_file:
    json.dump(all_data, output_file, indent=4)

print(f'All files have been processed and merged into {output_file_path}')
