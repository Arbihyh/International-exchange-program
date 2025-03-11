import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 目标URL
url = "https://oice.ustb.edu.cn/xsgjjl/hwjl_/xmsq/gjdq/index.htm"

# 发送请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)
response.encoding = "utf-8"

# 解析HTML
soup = BeautifulSoup(response.text, "lxml")

# 定位列表容器（根据实际网页结构调整选择器）
list_container = soup.find("table")  # 修改为实际的容器class或id

# 提取所有列表项
quotes = []
if list_container:
    for item in list_container.find_all("tr"):  # 根据实际列表项标签调整
        link = item.find("a",class_="hover")
        tds = item.find_all("td")
        if len(tds) > 0:  # 确保至少有一个<td>
            # 提取第一个<td>中的信息
            first_td = tds[0].text.strip() if tds[0] else "无标题"
            
            # 提取第二个<td>中的信息（如果有）
            second_td = tds[1].text.strip() if len(tds) > 1 else "无第二个td"
            
            # 提取第三个<td>中的信息（如果有）
            third_td = tds[2].text.strip() if len(tds) > 2 else "无第三个td"
        
            title = first_td +" "+second_td + " "+third_td
      
        
        
        if link:
            # 处理相对路径
            absolute_url = urljoin(url, link.get("href"))
            
            # 提取其他信息（根据实际需求添加）
            
            # date_tag = item.find("span", class_="date")  # 示例日期标签
            # date = date_tag.text.strip() if date_tag else "无日期"
            
            quotes.append({
                "title": title,
                "url": absolute_url,
                # "date": date
            })





# 生成HTML内容
html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>项目列表 - 共 {len(quotes)} 条</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: "Roboto" sans-serif;
            line-height: 1.8;
            padding: 2rem;
            background-color: #f8f9fa;
            color:495057
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 3rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            
            color: #2c3e50;
            margin-bottom: 2rem;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.5rem;
            text-align: center;
        }}
        .list-item {{
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            background: #ffffff;
            border-radius: 8px;
            transition: transform 0.3s, box-shadow 0.3s;
            border: 1px solid #e9ecef
        }}
        .list-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            border-color: #3498db;
        }}
        .item-title {{
            font-size: 1.2rem;
            color: #0366d6;
            margin-bottom: 0.75rem;
            font-weight: 500;
        }}
        .item-meta {{
            font-size: 0.95rem;
            color: #6c757d;
            margin-top: 0.5rem;
        }}
        a {{
            text-decoration: none;
            color: inherit;
        }}
        .empty-tip {{
            color: #6c757d;
            text-align: center;
            padding: 2rem;
            font-size: 1.1rem;
        }}
         .icon {{
            margin-right: 0.5rem;
            color: #3498db;
        }}
        .footer {{
            text-align: center;
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #6c757d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>北京科技大学国际合作项目列表（共 {len(quotes)} 项）</h1>
        {''.join(
            f'<div class="list-item">'
            f'<a href={item["url"]} target="_blank">'
            f'<div class="item-title">{item["title"]}</div>'
            
            f'</a ></div>'
            for item in quotes
        ) 
        if quotes else '<div class="empty-tip">暂无数据</div>'}
    </div>
</body>
</html>
"""         #添加发布日期项
            #f'<div class="item-meta">发布日期：{item["date"]}</div>'

# 保存文件
# with open("project_list.html", "w", encoding="utf-8") as f:
#     f.write(html_content)

import os

# 确保目标文件夹存在，如果不存在则创建
output_folder = r"E:\HTML文件"
os.makedirs(output_folder, exist_ok=True)

# 指定文件路径
file_path = os.path.join(output_folder, "index.html")

# 写入文件
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print("数据已保存至 project_list.html")



