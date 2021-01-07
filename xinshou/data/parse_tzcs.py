from bs4 import BeautifulSoup as bs4


def parse(html):
    res = {
        '身高测量': -1,
        '体重测量': -1,
        '肺活量': -1,
        '50米跑': -1,
        '立定跳远': -1,
        '1000米跑': -1,
        '800米跑': -1,
        '坐体前屈': -1,
        '仰卧起坐': -1,
        '引体向上': -1,
        '左眼视力': -1,
        '右眼视力': -1
    }
    html = bs4(html, 'html.parser')
    tr = html.find_all('tr')
    for i in tr:
        td = i.find_all('td')
        if not td:
            continue
        if td[0].text in res:
            res[td[0].text] = td[1].text
    return res


if __name__ == '__main__':
    with open('test.html') as f:
        d = parse(f)
        print(d)
