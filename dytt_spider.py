# encoding: utf-8

from lxml import etree
import requests

BASE_DOMAIN = "https://www.dytt8.net"

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }


# 获取详情页
def get_detail_urls(url):
    # url = "https://www.dytt8.net/html/gndy/dyzz/list_23_3.html" 注释掉 不要写死
    response = requests.get(url, headers=HEADERS)
    # requests 默认使用自己猜测的编码方式解码，抓取下来的网页进行解码，然后存到text中，在电影天堂的网页中，因为编码方式request猜错了，所以就会产生乱码，故不能使用text,需要使用其他编码方式，此处查看源代码，找到META标签，charset属性 电影天堂是‘gb2312' gbk编码的一种
    # print(response.encoding)encoding 打印网页采用的编码方式
    # text = response.content.decode('gbk')
    text = response.text  # 后续代码出现gbk不能识别的字符 这里只能使用text 不适用content
    html = etree.HTML(text)

    # 获取电影详情页 获href属性值
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urls = map(lambda url: BASE_DOMAIN + url, detail_urls)
    return detail_urls

    # for detail_url in detail_urls:
    #     print(BASE_DOMAIN + detail_url)


def parse_detail_page(url):
    movie = {}
    response = requests.get(url, headers=HEADERS)
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    # for x in title:
    #     print(etree.tostring(x, encoding='utf-8').decode('utf-8'))
    # print(title)
    movie['title'] = title

    zoomE = html.xpath("//div[@id='Zoom']")[0]
    imgs = zoomE.xpath(".//img/@src")
    cover =imgs[0]
    screenshot = imgs[1]

    movie['cover'] = cover
    movie['screen'] = screenshot

    def parse_info(info, rule):
        return info.replace(rule, "").strip()
        # strip删除字符串前后的空格

    infos = zoomE.xpath(".//text()")
    for index, info in enumerate(infos):
        # print(info)
        # print(index)
        # print("=" * 20)
        if info.startswith("◎年　　代"):
            info = parse_info(info, "◎年　　代")
            movie['year'] = info

        elif info.startswith("◎产　　地"):
            info = parse_info(info, "◎产　　地")
            movie['nation'] = info

        elif info.startswith("◎类　　别"):
            info = parse_info(info, "◎类　　别")
            movie['category'] = info

        elif info.startswith("◎语　　言"):
            info = parse_info(info, "◎语　　言")
            movie['language'] = info

        elif info.startswith("◎豆瓣评分"):
            info = parse_info(info, "◎豆瓣评分")
            movie['douban_score'] = info

        elif info.startswith("◎片　　长"):
            info = parse_info(info, "◎片　　长")
            movie['duration'] = info

        elif info.startswith("◎导　　演"):
            info = parse_info(info, "◎导　　演")
            movie['director'] = info

        elif info.startswith("◎主　　演"):
            info = parse_info(info, "◎主　　演")
            actors = [info]
            # 上面的info是第一个元素（演员）下面for循环获取不到的
            for x in range(index+1, len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor.strip())
            movie['actors'] = actors

        elif info.startswith("◎标　　签"):
            info = parse_info(info, "◎标　　签")
            movie['target'] = info

        elif info.startswith("◎简　　介"):
            info = parse_info(info, "◎简　　介")
            for x in range(index+1, len(infos)):
                profile = infos[x].strip()
                if profile.startswith("◎获"):
                    break

                # .strip() 删除前后空白字符
                movie['profile'] = profile

    download_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    movie['download_url'] = download_url
    return movie


def spider():
    base_url = "https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"
    movies = []
    for x in range(1, 8):
        # 第一个for控制页数1-7
        url = base_url.format(x)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:
            # 第二个for 用来遍历一页中所有的电影详情
            movie = parse_detail_page(detail_url)
            movies.append(movie)
            print(movie)


if __name__ == '__main__':
    spider()
