import re
import json

# 读取并尝试修复 JSON 文件
with open('merged_low.json', 'r', encoding='utf-8') as file:
    content = file.read()

# 尝试查找常见的 JSON 格式问题并修复
# 例如，查找缺少的逗号：在两组 }{ 之间加上逗号
content_fixed = re.sub(r'}\s*{', r'}, {', content)

# 保存修复后的内容到新文件
with open('merged_low_fixed.json', 'w', encoding='utf-8') as file:
    file.write(content_fixed)

# 再次尝试解析修复后的文件
try:
    new_data = json.loads(content_fixed)
    print("Successfully loaded fixed JSON data.")
except json.JSONDecodeError as e:
    print(f"Error: The file is still not a valid JSON file after attempting to fix it. {e}")
