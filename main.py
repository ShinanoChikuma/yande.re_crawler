import requests
import re
import os


def download_image(image_url, save_path):
    image_filename = image_url.split("/")[-1]
    save_file_path = os.path.join(save_path, image_filename)
    response = requests.get(image_url)
    with open(save_file_path, "wb") as img_file:
        img_file.write(response.content)
    print(f"已下载并保存图片：{save_file_path}")


# 第一页的基本网址
base_url = "https://yande.re/post?page={}&tags={}"

# 输入需要搜索的tags和起始的page_number
tags_input = input("请输入需要搜索的tags：")
page_number = int(input("请输入起始的page_number："))

# 图片保存路径
save_path = r"C:\Users\naras\Downloads"  # 改成你期望的下载地址

while True:
    try:
        # 生成当前页的网址
        url_1 = base_url.format(page_number, tags_input)

        response = requests.get(url_1)
        source_code = response.text

        pattern = r"https://yande\.re/post/show/\d+"
        matches = re.findall(pattern, source_code)

        if not matches:
            print("未找到以指定开头的链接")
            break

        for url_2 in matches:
            response = requests.get(url_2)
            source_code = response.text

            start_text = "https://files.yande.re/image/"
            end_text2 = "\""

            start_index = source_code.find(start_text)
            if start_index != -1:
                end_index = source_code.find(end_text2, start_index + len(start_text))
                if end_index != -1:
                    image_url = source_code[start_index:end_index]
                    print("找到链接:", image_url)
                    download_image(image_url, save_path)
                else:
                    print("未找到以指定开头的链接")
            else:
                print("未找到以指定开头的链接")

        # 移动到下一页
        page_number += 1

    except Exception as e:
        print(f"出现错误：{e}")
        print(f"当前的page_number值为：{page_number}")
        break
