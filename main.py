import bs4
import re
import time
from functs.rent_inf import RentInf
from functs import cal_distance, rent_inf,headless
import datetime
from selenium.webdriver.common.by import By
from multiprocessing import Pool
#webdriverwait
import threading
import traceback
def open_index(b,page_source):
    # soup = bs4.BeautifulSoup(open('yeeyi.html'), 'lxml')
    soup = bs4.BeautifulSoup(page_source, 'lxml')
    indexs=soup.find('div',class_='qtc')
    indexs = indexs.find_all('li')
    for index in indexs:
        tmp_rent = RentInf()
        index_a = index.find('a')
        db = rent_inf.getDB()
        cur=db.cursor()
        cur.execute('select count(title) from mytable where title = ?', [index_a.getText()])
        counts = cur.fetchall()
        if (int(counts[0][0]) >= 1):
            # print('重复了', index_a.getText())
            continue
        cur.close()
        db.close()
        #find house_type
        house_type_room=index.find('div',class_='lroom').getText()
        tmp_rent.rent_type= house_type_room.split('|')[0].replace(' ','')
        room_type=house_type_room.split('|')[1]
        tmp_rent.bedroom = room_type[1]
        tmp_rent.bathroom = room_type[5]
        tmp_rent.url=index_a['href']
        tmp_rent.title=index_a.getText()
        open_content_page(b, tmp_rent)
def open_content_page( b,tmp_rent):
    # soup = bs4.BeautifulSoup(open('singleInf.html'), 'lxml')
    st=time.time()
    b.get(tmp_rent.url)
    cal_distance.smart_wait(b, By.ID, 'nav')
    page_source = b.page_source
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
    except Exception as e:
        print(traceback.print_exc())
        print('时间出错')
    if soup.find('table',id='mytable') is None:
        soup = soup.find('table', class_='carcontent')
        tds=''
        try :
            tds = soup.find_all('td')
        except Exception as e:
            print('zz table')
            print(traceback.print_exc())
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
    if '公寓' in tmp_rent.house_type:
        tmp_rent.distance = cal_distance.get_distance('Australia rmit', tmp_rent.address + ',Melbourne')
        try:
            tmp_rent.insert_into_table()
        except Exception as e:
            print(traceback.print_exc())
            print('SQL wrong')
    e = time.time()
    print(tmp_rent.title,',total use',round(e-st,2),'s')
def addData(sstr, tmp_rent):
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
        tmp_rent.house_type = sstr.split(':')[1]
    if ("地址" in sstr):
        tmp_rent.address = sstr.split(':')[1]
def getdate(beforeOfDay):
    # 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date
def mmain(start_page,id):
        b = headless.getBrowser()
        for i in range(start_page, start_page+1):
            url = "http://www.yeeyi.com/forum/index.php?app=forum&act=display&fid=142&rhousetype1=1&listtype=txt&rents1=6&renttype1=1&page=" + str(
                i)
            b.get(url)
            page_source = b.page_source
            if 'cloudflare' in page_source:
                s = time.time()
                cal_distance.smart_wait(b, By.ID, 'nav')
                e = time.time()
                print('browser id:'+str(id)+',open index page used', round(e - s, 2), 's')
            page_source = b.page_source
            open_index(b, page_source)
            print(str(id + 1) , '页爬取完毕')

if __name__ == '__main__':
    p = Pool(8)
    for i in range(8):
        p.apply_async(mmain,args=(i,i,))
    p.close()
    p.join()









