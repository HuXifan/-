# encoding: utf-8
import re
import requests


def parse_page(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
    }
    response = requests.get(url, headers)
    text = response.text  # 爬取页面
    # .不能匹配反斜杠\n
    titles = re.findall(r'<div class="cont">.*?<b>(.*?)</b>', text, re.DOTALL)
    # 使用非贪婪模式 .*?   匹配的是（）里面的字符
    # print(titles)
    dynasties = re.findall(
        r'<p class="source">.*?<a.*?>(.*?)</a>',
        text,
        re.DOTALL)
    # print(dynasties)
    """
    <p class="source"><a href="/shiwen/default.aspx?cstr=%e5%94%90%e4%bb%a3" target="_blank">唐代</a><span>：</span><a href="https://so.gushiwen.org/search.aspx?value=%e6%9d%8e%e7%99%bd" target="_blank">李白</a></p>
    """
    # 作者在第二个a标签中 给两个a
    authors = re.findall(
        r'<p class="source">.*?<a.*?>.*?<a.*?>(.*?)</a>',
        text,
        re.DOTALL)  # re.DOTALL 匹配\n
    # print(authors)
    contents = []
    contents_tag = re.findall(
        r'<div class="contson".*?>(.*?)</div>',
        text,
        re.DOTALL)
    for content in contents_tag:
        # print(content)  去除标签
        x = re.sub(r'<.*?>', "", content)
        # print(x.strip()) .strip去除空格
        contents.append(x.strip())  # 放进列表 好看

    poems = []  # 定义列表
    for value in zip(titles, dynasties, authors, contents):
        title, dynasty, author, content = value  # 解包
        # 装进字典
        poem = {
            "标题": title,
            "朝代": dynasty,
            "作者": author,
            "内容": content
        }
        poems.append(poem)
    for poem in poems:
        print(poem)  # 打印
        print("__" * 30)


def main():
    # url = "https://www.gushiwen.org/default_2.aspx"
    for u in range(1, 10):  # 爬取1到10页的内容
        # url = "https://www.gushiwen.org/default_%s.aspx" % u
        url = "https://www.gushiwen.org/default.aspx?page=%s" % u
        parse_page(url)


if __name__ == '__main__':
    main()
