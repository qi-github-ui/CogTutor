import os

# 设置要处理的目录路径
directory = 'high_output_json_files'

# 遍历目录下的所有文件
for filename in os.listdir(directory):
    # 检查文件是否为JSON文件，并且文件名中包含"response"
    if filename.endswith('.json') and 'sponse' in filename:
        # 构造新文件名，将 "response" 移除
        new_filename = filename.replace('sponse', '')

        # 获取完整的文件路径
        old_file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(directory, new_filename)

        # 重命名文件
        os.rename(old_file_path, new_file_path)
        print(f'Renamed: {filename} -> {new_filename}')

print('All files have been processed.')
