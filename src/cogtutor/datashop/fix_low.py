import json


def fix_nested_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.read().strip().split('\n},\n{')

        # Fixing first and last lines
        if lines[0].startswith('{'):
            lines[0] = lines[0][1:]
        if lines[-1].endswith('}'):
            lines[-1] = lines[-1][:-1]

        data = []

        for line in lines:
            try:
                # Parse the outer JSON object
                outer_json = json.loads('{' + line + '}')

                if 'dialogue' in outer_json:
                    # Parse the nested JSON inside the 'dialogue' field
                    try:
                        outer_json['dialogue'] = json.loads(outer_json['dialogue'])
                    except json.JSONDecodeError as e:
                        print(f"JSONDecodeError in 'dialogue' field: {e}")

                data.append(outer_json)
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError in line: {e}")

    # Save the cleaned data to a new file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"修复后的 JSON 文件已保存到 '{output_file}'")


# 调用修复函数
fix_nested_json('high.json', 'fixed_high.json')
