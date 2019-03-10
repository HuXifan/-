# encoding: utf-8
from lxml import etree
import requests

# 腾讯招聘首页地址 设为常量
BASE_DOMAIN = "https://hr.tencent.com/"

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Cookie":"_ga=GA1.2.991593201.1544011481; pgv_pvi=8387815424; PHPSESSID=mc171td4ufvjd01873l5igef51; pgv_si=s4377520128",
    "Host": "hr.tencent.com",
    "Upgrade-Insecure-Requests": "1"
}


# 获取详情页
def get_detail_urls(url):
    # url = "https://hr.tencent.com/position.php?keywords=python&tid=0&start=0#a"
    response = requests.get(url, headers=HEADERS)
    text = response.text
    html = etree.HTML(text)

    # 获取详情页href属性
    links = html.xpath("//tr[@class='even' or @class='odd']//a/@href")
    links = map(lambda url: BASE_DOMAIN + url, links)
    # for detail_url in detail_urls:
    #     print(BASE_DOMAIN + detail_url)
    return links


def parse_detail_page(url):
    position = {}
    response = requests.get(url, headers=HEADERS)
    html = etree.HTML(response.text)

    # 获取详情页信息
    title = html.xpath("//td[@id='sharetitle']/text()")[0]
    tds = html.xpath("//tr[@class='c bottomline']/td")
    # 地址tr标签下 第一个td标签 取地址则选列表第二个元素[1]
    address = tds[0].xpath(".//text()")[1]
    # 类别是tr标签下 第二个td标签中 取类别字段也是列表第二个元素[1]
    category = tds[1].xpath(".//text()")[1]
    nums = tds[2].xpath(".//text()")[1]
    # 职责和要求在相同的两个tr标签下 用more_infos取全部内容
    more_infos = html.xpath("//ul[@class='squareli']")
    # 职责是返回more_infos列表的第一个元素[0]
    duty = more_infos[0].xpath(".//text()")
    # [1]第二个元素
    require = more_infos[1].xpath(".//text()")
    # 装进position
    position['标题'] = title
    position['地址'] = address
    position['类别'] = category
    position['招聘人数'] = nums
    position['工作职责'] = duty
    position['工作要求'] = require

    return position


def spider():
    # 分页网址
    base_url = "https://hr.tencent.com/position.php?keywords=python&tid=0&start={}"
    # base_url = "https://hr.tencent.com/position.php?keywords=python&tid=0&lid=2175&start={}"地址在上海的网址

    positions = []
    for x in range(0, 3):
        # 控制页数
        x *= 10
        url = base_url.format(x)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:
            # 第二个for用来遍历一页中所有的职位详情
            position = parse_detail_page(detail_url)
            positions.append(position)
            print(position)


if __name__ == '__main__':
    spider()


"""
爬取腾讯招聘网站关键字为'python',的职位信息。
共爬取3页（0、10、20）。
获取到工作名称、工作地点、招聘人数、工作职责和要求等
相比于电影天堂代码要更为简洁
"""