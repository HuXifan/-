# encoding: utf-8
import re
import requests


def parse_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }
    response = requests.get(url, headers)
    text = response.text
    # 在 class="content"的div标签下 匹配span标签里的内容
    contents = re.findall(r'<div\sclass="content">.*?<span>(.*?)</span>', text, re.DOTALL)
    # duanzi = []
    for content in contents:
        # sub 去除标签例如换行/br
        x = re.sub(r'<.*?>', "", content)
        # duanzi.append(x.strip())
        print(x.strip())
        print("====" * 20)


if __name__ == '__main__':
    url = 'https://www.qiushibaike.com/text/page/1/'
    # 爬1-4页
    for x in range(1, 5):
        url = 'https://www.qiushibaike.com/text/page/%s/' % x
        parse_url(url)


