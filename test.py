import re

# 定义正则表达式
regex1 = r"https?://t\.me/(?:joinchat/)?\+?[a-zA-Z0-9_\-]{15,50}"
regex2 = r"(?<![a-zA-Z0-9_\-])\+[a-zA-Z0-9_\-]{15,17}(?![a-zA-Z0-9_\-])"

# 合并两个正则表达式
combined_regex = rf"({regex1})|({regex2})"

# 定义要测试的文本
text = """
这里是一些示例文本。
V_DataPanBot_iBmlN85DPIoVyaXoRPjUTdDcbEMraHZCBxNdb1EInFQXm9I320R2ohVdRa
"""

# 匹配符合条件的字符串
matches = re.findall(combined_regex, text)

# 提取匹配结果
results = [match[0] if match[0] else match[1] for match in matches]

# 输出匹配结果
print("符合条件的字符串:")
for result in results:
    print(result)
