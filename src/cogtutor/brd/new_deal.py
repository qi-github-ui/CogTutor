#批量抽取brd文件的相关id信息
import os
import shutil
import xml.etree.ElementTree as ET
import json
from final_deal import *

def copy_and_rename_files(source_directory, dest_directory):
    # 确保目标目录存在
    os.makedirs(dest_directory, exist_ok=True)

    for filename in os.listdir(source_directory):
        if filename.endswith(".brd"):
            new_filename = filename[:-4] + ".txt"
            shutil.copyfile(os.path.join(source_directory, filename), os.path.join(dest_directory, new_filename))
            print(f"Copied and renamed {filename} to {new_filename}")


def new_extract_data_from_xml(file_path, target_ids, output_directory):
    tree = ET.parse(file_path)
    root = tree.getroot()
    actions_data = []

    for target_id in target_ids:
        action_data = {
            "id": target_id,
            "action": None,
            "feedback": {},
            "hints": [],
            "path": []
        }

        for edge in root.findall(".//edge"):
            message = edge.find(".//message")
            if message:
                selection = message.find(".//Selection/value")
                if selection and selection.text == target_id:
                    action = message.find(".//Action/value")
                    input_value = message.find(".//Input/value")

                    action_data["action"] = action.text if action else "No action specified"
                    action_data["feedback"]["successMessage"] = input_value.text if input_value else "No input found"

                    for hint in edge.findall(".//hintMessage"):
                        action_data["hints"].append(hint.text if hint else "No hint provided")

                    source_id = edge.get("sourceID")
                    dest_id = edge.get("destID")
                    action_data["path"].append({"from": source_id, "to": dest_id})

        if action_data["action"]:
            actions_data.append(action_data)

    json_file_path = os.path.join(output_directory, os.path.splitext(os.path.basename(file_path))[0] + '.json')
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(actions_data, json_file, indent=4, ensure_ascii=False)

    return json_file_path


# 文件夹路径和输出文件夹
source_directory = 'S_6.06HTML'
output_directory = 'S_6.06HTML_json'
copy_and_rename_files(source_directory, output_directory)

# 6.06 ID 列表应由您提供，这里假设是每个文件对应的 ID 列表
id_mapping = {
    '4-allison.txt': ['r1c3', 'r1c4', 'r2c1', 'r2c2', 'r2c4', 'r3c1', 'r3c2', 'r3c3'],
'5-charlie.txt': ['r1c1', 'r1c2', 'r1c3', 'r1c4', 'r2c2', 'r2c3', 'r2c4', 'r3c2', 'r3c3', 'r3c4'],
'6-jordan.txt': ['r1c1', 'r1c2', 'r1c3', 'r1c4', 'r2c1', 'r2c3', 'r2c4', 'r3c1', 'r3c4', 'r3c2'],
'9-lauren.txt': ['r1c1', 'r1c2', 'r1c3', 'r1c4', 'r2c1', 'r3c1', 'r2c2', 'r2c4', 'r3c2', 'r3c4'],
'7-martin.txt': ['r2c1', 'r1c1', 'r1c2', 'r1c3', 'r1c4', 'r2c3', 'r2c4', 'r3c1', 'r3c2', 'r3c4'],
'2-molly.txt': ['r3c4'],
'8-paul.txt': ['r1c1', 'r1c2', 'r1c4', 'r1c3', 'r2c4', 'r2c1', 'r2c2', 'r3c3', 'r3c4', 'r3c1'],
'3-sydney.txt': ['r3c1', 'r2c3', 'r2c4', 'r3c4', 'r3c3']
}

# 遍历文件并提取数据
for filename, ids in id_mapping.items():
    file_path = os.path.join(output_directory, filename)
    if os.path.exists(file_path):
        json_file_path = extract_data_from_xml(file_path, ids, output_directory)
        # print(f"Data saved to JSON file: {json_file_path}")
