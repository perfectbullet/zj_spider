import re

def clean_filename(filename):
    """
    去除文件名中的非法字符
    """
    # 将非法字符替换为空字符串
    cleaned_filename = re.sub(r'[\\\/:*?"<>|]', '', filename)
    return cleaned_filename
