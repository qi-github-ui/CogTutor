import os
import re
import json
from openai import OpenAI

# 设置文件夹路径
problem_folder = 'problem'
formatted_data_folder = 'formatted_student_data_files'
output_folder = 'output'

# 获取文件夹中所有的txt文件
problem_files = [f for f in os.listdir(problem_folder) if f.endswith('.txt')]

# 遍历所有problem文件夹中的txt文件
for problem_file in problem_files:
    # 生成路径
    problem_file_path = os.path.join(problem_folder, problem_file)

    # 从文件名中提取任务标识符
    task_identifier = problem_file[:-4]  # 去掉 '.txt' 后缀，保留完整文件名

    # 寻找对应的json文件
    action_file_name = f'formatted_student_data_{task_identifier}.json'
    action_file = os.path.join(formatted_data_folder, action_file_name)

    # 设置输出文件路径
    output_file_path = os.path.join(output_folder, f'background_output-{task_identifier}.json')

    # 确保json文件存在
    if not os.path.exists(action_file):
        print(f"对应的JSON文件 {action_file} 不存在，跳过该任务。")
        continue

    # 打印处理的文件名
    print(f"Processing txt file: {problem_file}")
    print(f"Corresponding JSON file: {action_file_name}")

    # 读取题目文本文件
    with open(problem_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # 使用更灵活的正则表达式提取 task 部分
        match = re.search(r"题目任务[:：]\s*(.*?)\s*题目描述[:：]", content, re.S)
        if match:
            task = match.group(1).strip()
        else:
            print(f"未能正确提取任务，跳过该文件：{problem_file}")
            continue

        # 固定 problem_description 内容
        problem_description = "给定一个标有十分位和百分位的数轴。数轴从0到0.1，其中每个大刻度代表一个十分位，每个小刻度代表一个百分位。"

    # 打印提取的 task
    print(f"Task: {task}")
    print(f"Problem Description: {problem_description}")

    # 读取 JSON 文件
    with open(action_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    output_data = []

    for record in data:
        stu_id = record.get('学生id (对应的Anon Student Id)')
        stu_ability = record.get('学生水平Tier')

        # 获取 "操作信息" 和 "操作记录"
        operation_info = record.get('操作信息')
        operation_steps = record.get('操作记录')

        # 合并两个字段
        act_information = f"Operation Info: {operation_info}; Operation Steps: {operation_steps}"

        # 构建 prompt
        prompt = (
            f"Based on the provided student's answer data, generate a detailed background description including the following sections:\n"
            f"(1). First, describe the student's skill level (including their performance in math and any challenges or strengths observed during the answering process).\n"
            f"(2). Secondly,describe the task (explain the task the student needs to complete, along with the task details).\n"
            f"(3). Finally,set the scene to introduce the teacher-student dialogue (describe the current practice session the student is engaged in).\n"
            f"\n"
            f"Below are the original problem data, the student's operation data, and the task determination:\n"
            f"- **Problem Original Data**: {task},{problem_description} including the problem background, task details.\n"
            f"- **Operation Data**: {act_information}, detailing each of the student's steps, including their selected values, inputs, and outcomes.\n"
            f"- **Student Level**: {stu_ability}, Student Skill Level"

            f"\n"
            f"Example:\n"
            f"Stu_00 is a low-level middle school student who struggles with understanding mathematical concepts, especially locating values on a number line. He typically needs multiple attempts to find the correct answer and often makes mistakes while adjusting inputs. He lacks precision in recognizing scale markers, causing him to frequently miss the correct answer range. Today, his task is to accurately find the position of 0.2 on a number line. The number line ranges from 0 to 1, divided into tenths and hundredths. Stu_00 needs teacher guidance to understand how to correctly locate 0.2 through multiple interactions.\n"
            f"Based on this information,generate a teacher-student dialogue background description in one integrated paragraph.Description should not involve specific student operational data."
        )

        # 调用 OpenAI 接口
        client = OpenAI(base_url='https://api.pumpkinaigc.online/v1',
                        api_key='sk-ZAzPh87XnJN0u0eTD051D1277523446bA32136C873690392')

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # 提取并保存结果
        background_description = response.choices[0].message.content

        output_data.append({
            'student_id': stu_id,
            'tier': stu_ability,
            'background_description': background_description
        })

    # 保存输出数据到新的 JSON 文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)

    print(f"Data has been successfully saved to {output_file_path}.")
