import xml.etree.ElementTree as ET
import json
import os


def extract_data_from_xml(file_path, target_ids, output_directory):
    # 解析 XML 文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 存放所有目标 ID 数据的列表
    actions_data = []

    # 遍历所有 ID
    for target_id in target_ids:
        # 初始化结果字典
        action_data = {
            "id": target_id,
            "action": None,
            "feedback": {},
            "hints": [],
            "path": []
        }

        # 设置一个标志，确认是否找到了目标 ID 的信息
        found = False

        # 遍历 XML 中的所有 'edge' 元素寻找与 target_id 相关的动作
        for edge in root.findall(".//edge"):
            message = edge.find(".//message")
            if message is not None:
                selection = message.find(".//Selection/value")
                if selection is not None and selection.text == target_id:
                    found = True
                    action = message.find(".//Action/value")
                    input_value = message.find(".//Input/value")

                    action_data["action"] = action.text if action is not None else "No action specified"
                    action_data["feedback"][
                        "successMessage"] = input_value.text if input_value is not None else "No input found"

                    # 抽取提示信息
                    for hint in edge.findall(".//hintMessage"):
                        action_data["hints"].append(hint.text if hint is not None else "No hint provided")

                    # 假设路径信息与 edge 相关联
                    source_id = edge.get("sourceID")
                    dest_id = edge.get("destID")
                    action_data["path"].append({"from": source_id, "to": dest_id})

        # 只有当找到相关信息时，才将此 ID 的数据添加到总列表中
        if found:
            actions_data.append(action_data)


    json_file_path = os.path.join(output_directory, os.path.splitext(os.path.basename(file_path))[0] + '.json')
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(actions_data, json_file, indent=4, ensure_ascii=False)

    return json_file_path


# 调用函数
file_path = 'S_6.06HTML_json/3-sydney.txt'  # 指定文件路径
target_ids = ['r3c1', 'r2c3', 'r2c4', 'r3c4', 'r3c3']  # 指定需要查找的多个 ID
json_file_path = extract_data_from_xml(file_path, target_ids, "test")
print(f"Data saved to JSON file: {json_file_path}")
