import pandas as pd

# 读取CSV文件
file_path = 'D:\code_dc\sim_stu\converd_data/580/580final.csv'  # 替换为你的文件路径
data = pd.read_csv(file_path, encoding='GB2312')  # 使用适当的编码读取

# 筛选 'Level (ProblemSet)' 等于 6.06 且 'Selection' 不是 'done'
filtered_data = data[(data['Level (ProblemSet)'] == 6.07) & (data['Selection'] != 'done')]

# 按 'Problem Name' 分组并获取不重复的 'Selection' 值
problem_selections = filtered_data.groupby('Problem Name')['Selection'].unique()

# 将结果排序并按需求格式化文件名
sorted_problems = sorted(problem_selections.index)
problem_files = {f"{i+1}-{problem}.txt": list(values) for i, (problem, values) in enumerate(problem_selections.items())}

# 输出结果
print(problem_files)
