import pandas as pd
import json

# 加载 Excel 文件
file_path = 'Qwen2.xlsx'
excel_data = pd.ExcelFile(file_path)

# 选择工作表
sheet_name = 'Sheet1'
data = pd.read_excel(file_path, sheet_name=sheet_name)

# 将 DataFrame 转换为 JSON 格式
json_data = data.to_dict(orient='records')

# 保存 JSON 数据到文件，保证输出格式整洁
output_path = 'Qwen2_output.json'
with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)

print(f"JSON 数据已保存到 {output_path}")
