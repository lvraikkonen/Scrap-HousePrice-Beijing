# -*- coding: utf-8 -*-

import sys
import random
import re
import urllib2
import json
from bs4 import BeautifulSoup
from bs4.element import Tag
import codecs

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}

#指定系统默认编码
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


HOUSE_DIR = './houses.txt'


def get_url(url,page):
    content=urllib2.urlopen(url+'/pg%s'%page).read()
    typeEncode = sys.getfilesystemencoding()
    html = content.decode("utf-8").encode(typeEncode)
    doc = BeautifulSoup(html,"html.parser")
    table = doc.find('ul',{'class':'listContent'})
    # table=BeautifulSoup(html,'lxml').find('ul',{'class':'listContent'})#.find_all('ul',{'class':'listContent'})
    result=[]
    for li in table:
        item={}
        item['url']=li.find('a').get('href')# a house detail info
        item['title']=li.find('div',{'class':'title'}).get_text()
        # print item['title'].decode('utf-8')
        result.append(item)
    return result

def get_infor(item):
    # item contains detail url for one house
    print 'Fetching detail data from ' + item['url']
    content = urllib2.urlopen(item['url']).read()
    typeEncode = sys.getfilesystemencoding()
    html = content.decode("utf-8").encode(typeEncode)
    soup = BeautifulSoup(html,"html.parser")
    hlst = soup.findAll('div', class_='overview')
    one_page_house = []
    for h in hlst:
        print '...',
        print "名字：" + item['title'].decode('utf-8')
        item['totalPrice'] = h.find('div',class_='price ').find('span').string
        print "总价：" + item['totalPrice'].decode('utf-8')
        item['unitPrice'] = h.find('div',class_='price ').find('div',class_='unitPrice').find('span',class_='unitPriceValue').next_element
        print "单价：" + item['unitPrice'].decode('utf-8')
        item['shoufu'] = h.find('div',class_='price ').find('div',class_='tax').find('span').string
        print "首付：" + item['shoufu'].decode('utf-8')
        item['houseType'] = h.find('div',class_='houseInfo').find('div',class_='room').find('div',class_='mainInfo').string
        print "户型：" + item['houseType'].decode('utf-8')
        item['houseSubType'] = h.find('div',class_='houseInfo').find('div',class_='room').find('div',class_='subInfo').string
        item['area'] = h.find('div',class_='houseInfo').find('div',class_='area').find('div',class_='mainInfo').string
        item['buildType'] = h.find('div',class_='houseInfo').find('div',class_='area').find('div',class_='subInfo').string
        item['chaoxiang'] = h.find('div',class_='houseInfo').find('div',class_='type').find('div',class_='mainInfo').string
        item['zhuangxiu'] = h.find('div',class_='houseInfo').find('div',class_='type').find('div',class_='subInfo').string

        item['communityName'] = h.find('div',class_='aroundInfo').find('div',class_='communityName').find('a',class_='info').string

        item['houseRecordNum'] = h.find('div',class_='aroundInfo').find('div',class_='houseRecord').find('span',class_='info').next_element

        # region = h.find('span',class_='region').string
        # zone = h.find('span',class_='zone').string
        # meters = h.find('span',class_='meters').string[0:-2]
        # direction = h.find('span',class_='meters').next_sibling.string
        # direction = (direction if direction != None else '')
        # con = h.find('div',class_='con').a.string
        # floor = h.find('div',class_='con').contents[2][0:3]
        # year = h.find('div',class_='con').contents[4][0:4]
        # school = h.find('span',class_='fang05-ex')
        # school = ('1' if school != None else '0')
        # subway = h.find('span',class_='fang-subway-ex')
        # subway = ('1' if subway != None else '0')
        # taxfree = h.find('span',class_='taxfree-ex')
        # taxfree = (taxfree.string if taxfree != None else '')
        # num = h.find('span',class_='num').string
        # price = h.find('div',class_='price-pre').string[0:-5]
        # house.append(''.join(area.split()))
        # house.append(''.join(region.split()))
        # house.append(''.join(zone.split()))
        # house.append(''.join(meters.split()))
        # house.append(''.join(direction.split()))
        # house.append(''.join(con.split()))
        # house.append(''.join(floor.split()))
        # house.append(''.join(year.split()))
        # house.append(school)
        # house.append(subway)
        # house.append(''.join(taxfree.split()))
        # house.append(''.join(num.split()))
        # house.append(''.join(price.split()))
        # one_page_house.append(house)
    print 'done'
    return item

def test():
    url='http://bj.lianjia.com/ershoufang/pg1'#input('Input url:')
    if '/pg' in url:
        url=re.sub('/pg\d+','',url)
    # print url
    page=1
    pre=[]
    houses = []
    f=codecs.open('result.txt','wb','utf-8')
    while True:
        try:
            result=get_url(url,page)
        except:
            print('failed')
            break
        if pre==result:
            break
        pre=result
        for item in result:
            try:
                house=get_infor(item)
            except:
                failed=codecs.open('failed.txt','wb','utf-8')
                failed.write(str(item)+'\n')
                failed.close()
                continue
            f.write(str(house)+'\n')
            houses.append(house)
        print(page,'ok')
        page+=1
        if page==101:
            break
        # Writing JSON data
        with codecs.open('data.json', 'w','utf-8') as f:
            f.write(unicode(json.dump(houses,ensure_ascii=False)))
        with codecs.open("json_file.json", "w") as json_file:
            json.dump(houses, json_file)
    f.close()


def get_one_page_house(url):
    print 'Fetching detail data from ' + url
    r = requests.get(url)
    r.encoding = 'utf-8'
    html = r.text
    soup = BeautifulSoup(html)
    hlst = soup.findAll('div', class_='info-panel')
    one_page_house = []
    for h in hlst:
        print '...',
        house = []
        area =  h.parent['data-id'][0:4]
        region = h.find('span',class_='region').string
        zone = h.find('span',class_='zone').string
        meters = h.find('span',class_='meters').string[0:-2]
        direction = h.find('span',class_='meters').next_sibling.string
        direction = (direction if direction != None else '')
        con = h.find('div',class_='con').a.string
        floor = h.find('div',class_='con').contents[2][0:3]
        year = h.find('div',class_='con').contents[4][0:4]
        school = h.find('span',class_='fang05-ex')
        school = ('1' if school != None else '0')
        subway = h.find('span',class_='fang-subway-ex')
        subway = ('1' if subway != None else '0')
        taxfree = h.find('span',class_='taxfree-ex')
        taxfree = (taxfree.string if taxfree != None else '')
        num = h.find('span',class_='num').string
        price = h.find('div',class_='price-pre').string[0:-5]
        house.append(''.join(area.split()))
        house.append(''.join(region.split()))
        house.append(''.join(zone.split()))
        house.append(''.join(meters.split()))
        house.append(''.join(direction.split()))
        house.append(''.join(con.split()))
        house.append(''.join(floor.split()))
        house.append(''.join(year.split()))
        house.append(school)
        house.append(subway)
        house.append(''.join(taxfree.split()))
        house.append(''.join(num.split()))
        house.append(''.join(price.split()))
        one_page_house.append(house)
    print 'done'
    return one_page_house


def write_to_txt(s):
    # 带加号为可读写
    print 'Write to file...',
    hl = codecs.open(HOUSE_DIR, 'a')
    hl.write(s)
    hl.close()
    print 'done',


# if __name__ == '__main__':
#     url_pre = 'http://bj.lianjia.com/ershoufang/pg'
#     if len(sys.argv) == 3:
#         page_num = int(sys.argv[1])
#         total_page_num = int(sys.argv[2])
#     else:
#         print "Please input how many pages to get and the total number of pages"
#         sys.exit(0)
#     # 随机的从总页码中抽取一定数量的页
#     page_basket = random.sample(xrange(1, total_page_num), page_num)
#     i = 0  #对抓取的页数计数
#     for p in page_basket:
#         url = url_pre + str(p)
#         write_to_txt('\n'.join([','.join(h) for h in get_one_page_house(url)]) + '\n')
#         i = i + 1
#         print '+' + str(i)

test()