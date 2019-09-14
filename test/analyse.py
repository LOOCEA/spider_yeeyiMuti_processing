import bs4
import time
from functs.rent_inf import RentInf
import re
from functs import cal_distance, headless, rent_inf
import datetime

#webdriverwait
import traceback
import cfscrape
from fake_useragent import UserAgent as UA
def open_index(s,page_source):
    # soup = bs4.BeautifulSoup(open('yeeyi.html'), 'lxml')
    soup = bs4.BeautifulSoup(page_source, 'lxml')
    indexs = soup.find_all('div', class_='ptxt')
    for index in indexs:
        junk_wb = index.find('span', class_='pin')
        if (junk_wb is None):
            index_a = index.find('a')
            db = rent_inf.getDB()
            cur=db.cursor()
            cur.execute('select count(title) from mytable where title = %s', index_a.getText())
            counts = cur.fetchall()
            if (int(counts[0][0]) >= 1):
                # print('重复了', index_a.getText())
                continue
            cur.close()
            db.close()
            print('we are going to ' + index_a['href'] + " " + index_a.getText())
            #find house_type
            house_types=index.find_all('span')
            for i in house_types:
                if '户型' in i.getText():
                    house_type=i.getText().split('：')[1]
                    break
            tmp_rent=RentInf()
            tmp_rent.bedroom=house_type[0]
            tmp_rent.bathroom=house_type[2]
            tmp_rent.url=index_a['href']
            tmp_rent.title=index_a.getText()
            page_source2=s.get(index_a['href']).text
            open_content_page(page_source2, tmp_rent)
def open_content_page( page_source,tmp_rent):
    # soup = bs4.BeautifulSoup(open('singleInf.html'), 'lxml')
    st=time.time()
    soup = bs4.BeautifulSoup(page_source, 'lxml')
    try:

        day=soup.find_all('em')[7].getText()
        if "天" in  day:
            day= re.sub("\D", "", day)
            tmp_rent.time = getdate(int(day))
        elif "小时" in day:
            tmp_rent.time = getdate(0)
        elif "分钟" in day:
            tmp_rent.time = getdate(0)
        elif '秒' in day:
            tmp_rent.time = getdate(0)
        else:
            tmp_rent.time=soup.find_all('em')[7].getText().split(' ')[1]
        print(tmp_rent.time)
    except Exception as e:
        print(traceback.print_exc())
        print('时间出错')
    if soup.find('table',id='mytable') is None:
        soup = soup.find('table', class_='carcontent')
        tds = soup.find_all('td')
        ind = 0
        sstr=''
        for td in tds:
            if ind % 2 == 0:
                sstr=td.getText()
                #print(td.getText(), end='')
            else:
                #print(td.getText())
                sstr+=td.getText()
                addData(sstr, tmp_rent)
            ind += 1
    else:
        soup = soup.find('table', id='mytable')
        trs = soup.find_all('tr')
        sstr=''
        for tr in trs:
            try:
                sstr=tr.th.getText()+tr.td.getText()
            except Exception as e:
                print(traceback.print_exc())
                print('zz table')
            addData(sstr, tmp_rent)
    if 'ouse' not in tmp_rent.house_type and '小区' not in tmp_rent.house_type:
        tmp_rent.distance = cal_distance.get_distance('Australia rmit', tmp_rent.address + ',Melbourne')
        print('distance:',)
        # tmp_rent.insert_into_table()
    e = time.time()
    print('total use',round(e-st,2),'s')
    print('__________________')
def addData(sstr, tmp_rent):
    print(sstr)
    if("所在城市" in sstr):
        tmp_rent.city=sstr.split(':')[1]
    if ("性别" in sstr):
        sstr=sstr.split(':')[1]
        if'不' in sstr:
            tmp_rent.gender_requirement= 'No requirement'
        elif '男' in sstr:
            tmp_rent.gender_requirement= 'M'
        elif '女' in sstr:
            tmp_rent.gender_requirement = 'F'
    if ("租金" in sstr):
        sstr = sstr.split(':')[1]
        tmp_rent.rent_price= re.sub("\D", "", sstr)
    if ("有效期" in sstr):
        sstr = sstr.split(':')[1]
        if("一" in sstr):
            tmp_rent.time_limit=1
        if ("二" in sstr):
            tmp_rent.time_limit = 2
        if ("三" in sstr):
            tmp_rent.time_limit = 3
        if ("四" in sstr):
            tmp_rent.time_limit = 4
    if ("类型" in sstr):
        if 'house' in sstr:
            return False
        tmp_rent.house_type = sstr.split(':')[1]
    if ("地址" in sstr):
        tmp_rent.address = sstr.split(':')[1]
    if("方式" in sstr):
        tmp_rent.rent_type = sstr.split(':')[1]
def getdate(beforeOfDay):
    # 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date
headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept - Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
            'Connection': 'Keep-Alive',
            'User-Agent': UA().random  # 获取随机的useragent
        }

# ua = UserAgent()
# posC = "C:\Download\small App\WebDriver\chromedriver.exe"
# s = Session(webdriver_path=posC,
#             browser='chrome',
#             default_timeout=15,
#             webdriver_options={'arguments': ['headless','--no-sandbox','--disable-gpu']})
# # 'arguments': ['headless','--no-sandbox','--disable-gpu']
# # response=s.get('http://www.yeeyi.com/bbs/forum.php?mod=viewthread&tid=4523663',headers={'User-Agent':ua.chrome}).text
# pages=10
# url = "http://www.yeeyi.com/bbs/forum.php?mod=viewthread&tid=4521587"
# print(1)
# s.driver.get(url)
# print(1)
# time.sleep(5)
# s.transfer_driver_cookies_to_session()
# page_source =s.driver.page_source
# tmp=RentInf()
# open_content_page(page_source,tmp)



# b= headless.getBrowser()
# pages=5
# for i in range(1,pages):
#     url = "http://www.yeeyi.com/forum/index.php?app=forum&act=display&fid=142&rcity1=1&rhousetype1=1&rents1=4&page="+str(i)
#     b.get(url)
#     time.sleep(5)
#     open_index(b)
#     print('翻页了！')
# print('前',pages,'页抓取完毕')




