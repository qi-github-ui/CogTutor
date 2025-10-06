import json

# 直接使用文件名
merged_file_path = 'cleaned_merged_high.json'
new_data_file_path = 'high_output_json_files/merged_generate_high.json'

# 设置新文件路径
new_merged_output_path = 'high_proficiency.json'


def load_json_with_error_handling(file_path):
    valid_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                print(f"Error in full JSON structure, attempting to process line by line in {file_path}.")
                data = []
                lines = content.splitlines()
                buffer = ""
                for line_num, line in enumerate(lines, 1):
                    buffer += line
                    try:
                        parsed_item = json.loads(buffer)
                        if isinstance(parsed_item, dict) or isinstance(parsed_item, list):
                            data.append(parsed_item)
                        buffer = ""  # 清空缓冲区以处理下一条数据
                    except json.JSONDecodeError:
                        # 这里表示当前行可能只是部分数据，继续读取下一行
                        continue

            if isinstance(data, list):
                for idx, item in enumerate(data):
                    try:
                        # 尝试解析每一项，检查其有效性
                        json.dumps(item)  # 尝试将项序列化为JSON字符串以检查其有效性
                        valid_data.append(item)
                    except (TypeError, ValueError) as e:
                        print(f"Skipping invalid entry at index {idx} in {file_path}: {e}")
            else:
                print(f"Error: The file {file_path} does not contain a valid list.")
                exit(1)

    except FileNotFoundError:
        print(f'Error: The file {file_path} does not exist.')
        exit(1)
    except json.JSONDecodeError as e:
        print(f'Error: The file {file_path} is not a valid JSON file. {e}')
        exit(1)

    return valid_data


# 加载 merged_low.json 数据并处理错误
merged_data = load_json_with_error_handling(merged_file_path)
print(f'Successfully loaded data from {merged_file_path}')

# 加载新的数据
new_data = load_json_with_error_handling(new_data_file_path)
print(f'Successfully loaded data from {new_data_file_path}')

# 合并数据
merged_data.extend(new_data)
print(f'Successfully merged data from {new_data_file_path}')

# 将更新后的数据保存到一个新的 JSON 文件中
try:
    with open(new_merged_output_path, 'w', encoding='utf-8') as new_merged_file:
        json.dump(merged_data, new_merged_file, indent=4)
    print(f'New data has been successfully saved into {new_merged_output_path}')
except IOError as e:
    print(f'Error: Failed to write to {new_merged_output_path}. {e}')
    exit(1)
