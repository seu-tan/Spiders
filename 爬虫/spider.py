import requests ##导入requests
from bs4 import BeautifulSoup ##导入bs4中的BeautifulSoup
import os
import time
import sqlite3

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
http = 'http://www.'
polyvore = '.polyvore.com/?filter=sets'
all_url = 'http://www.polyvore.com/'

path = "/storage/songxuemeng/lizekun/polyvore/polyvore8/"

f1 = open(path + 'user.txt', 'a+', encoding='utf-8')
f2 = open(path + 'outfit.txt', 'a+', encoding='utf-8')
f3 = open(path + 'item.txt', 'a+', encoding='utf-8')
f4 = open(path + 'item_outfit.txt', 'a+', encoding='utf-8')
f5 = open(path+'user_link.txt', 'a+', encoding='utf-8')
f6 = open(path+'top_outfit.txt', 'a+', encoding='utf-8')
f7 = open(path + 'bottom_outfit.txt', 'a+', encoding='utf-8')
f8 = open(path + 'shoes_outfit.txt', 'a+', encoding='utf-8')
f9 = open(path + 'top.txt', 'a+', encoding='utf-8')
f10 = open(path + 'bottom.txt', 'a+', encoding='utf-8')
f11 = open(path + 'shoes.txt', 'a+', encoding='utf-8')


idb = sqlite3.connect(path + "item.db")
odb = sqlite3.connect(path + "outfit.db")
udb = sqlite3.connect(path + "user.db")
tdb = sqlite3.connect(path + "top.db")
bdb = sqlite3.connect(path + "bottom.db")
sdb = sqlite3.connect(path + "shoes.db")
iodb = sqlite3.connect(path + "item_outfit.db")
todb = sqlite3.connect(path + "top_outfit.db")
bodb = sqlite3.connect(path + "bottom_outfit.db")
sodb = sqlite3.connect(path + "shoes_outfit.db")
uldb = sqlite3.connect(path + "user_link.db")
icu = idb.cursor()
ocu = odb.cursor()
ucu = udb.cursor()
tcu = tdb.cursor()
bcu = bdb.cursor()
scu = sdb.cursor()
iocu = iodb.cursor()
tocu = todb.cursor()
bocu = bodb.cursor()
socu = sodb.cursor()
ulcu = uldb.cursor()

#循环开始
uid = 135
while uid < 248:
    f = open(path + "/html/"+str(uid)+".txt",'r',encoding='utf-8')
    start_html = f.read()

    Soup = BeautifulSoup(start_html, 'lxml')
    info = Soup.find('div', class_="user_info")
    country = info.find('div', class_='meta').get_text()
    create = info.find('div',class_='display_name').find('span').get_text()
    ins = ""
    try:
        ins_soup = info.find('div', class_='user_links clearfix').find_all('a')
        for ins_a in ins_soup:
            ins = ins + ins_a['href'] + " "
    except:
        ins = ""

    more = Soup.find('ul', class_="activity_summary").find_all('li')
    summary = ''
    for x in more:
        summary = summary + x.get_text()

    uc = ucu.execute("select count(*) from user").fetchone()
    ucu.execute("insert into user values('" + str(uid) + "','" + create.replace("'", '') + "','" + country.replace("'", '') + "','" + ins.replace( "'", '') + "','" + summary.replace("'", '') + "')")
    udb.commit()
    f5.write(str(uid)+" "+ins)
    ulcu.execute("insert into user_link values('" + str(uid) + "','" + ins + "')")
    uldb.commit()


    grid = Soup.find_all('ul',class_="layout_grid grid_6 mod_inline_save clearfix ")
    for g in grid:
        all_div = g.find_all('div',class_="grid_item hover_container type_set span2w span2h")
        for li in all_div:
            t = li.find('div', class_='title')
            c = li.find('div', class_='createdby')
            l = li.find('span', class_='fav_count')
            at = t.find("a")
            ac = c.find('a')

            title = at.get_text() #取出a标签的文本
            link = at['href'][3:]
            like = l.get_text()

            oid_sql = ocu.execute("select oid from outfit where oname='" + title.replace("'", '') + "'").fetchone()
            if oid_sql is not None:
                oid = str(oid_sql).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
            else:
                oc = ocu.execute("select count(*) from outfit").fetchone()
                oid = str(oc).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
                f2.write(str(oid) + " " + title + " " + str(uid) + " " + like + "\n")
                ocu.execute("insert into outfit values('"+str(oid)+"','"+title.replace("'",'')+"','"+str(uid)+"','"+like.replace("'",'')+"')")
                odb.commit()

            link = all_url + link
            html = requests.get(link, headers=headers)
            html_Soup = BeautifulSoup(html.text, 'lxml')
            item = html_Soup.find('ul',class_='layout_grid grid_5 mod_inline_save clearfix ').find_all('div',class_="grid_item hover_container type_thing span1w span1h")
            for i in item:
                a = i.find('div',class_='main').find('a')
                href = a['href']
                page_url = link + href
                img_html = requests.get(page_url, headers=headers)
                img_Soup = BeautifulSoup(img_html.text, 'html.parser')
                img_url = a.find('img')['src']
                try:
                    kind = img_Soup.find('div', id='body').find('div',class_='page thing').find('div',class_='clearfix').find('div',id='right').find_all('span',itemprop='title')
                    kind_des = ''

                    for k in kind:
                        kind_des = kind_des + '>'+ k.get_text()

                    text_url = img_Soup.find('div', id='body').find('div',class_='page thing').find('div',class_='clearfix').find('div',id='right').find('h1')
                    name = text_url['title']
                    img = requests.get(img_url, headers=headers)

                    iid_sql = icu.execute("select iid from item where iname='" + name.replace("'",'') + "'").fetchone()
                    if iid_sql is not None:
                        iid = str(iid_sql).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
                    else:
                        ic = icu.execute("select count(*) from item").fetchone()
                        iid = str(ic).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
                        f3.write(str(iid) + " " + name + " " + kind_des + " " + "\n")
                        icu.execute("insert into item values('" + str(iid) + "','" + name.replace("'",'') + "','" + kind_des.replace("'",'') +"')")
                        idb.commit()
                        if kind_des.__contains__('Tops') or kind_des.__contains__('Outerwear'):
                            f9.write(str(iid) + " " + name + " " + kind_des + " " + "\n")
                            tcu.execute("insert into top values('" + str(iid) + "','" + name.replace("'",
                                                                                                      '') + "','" + kind_des.replace(
                                "'", '') + "')")
                            tdb.commit()
                            os.chdir(path + "top")  ##切换到上面创建的文件夹
                            f = open(str(iid) + '.jpg', 'ab')
                            f.write(img.content)
                            f.close()
                        if kind_des.__contains__('Skirts') or kind_des.__contains__('Jeans') or kind_des.__contains__( 'Pants') or kind_des.__contains__('Shorts'):
                            f10.write(str(iid) + " " + name + " " + kind_des + " " + "\n")
                            bcu.execute("insert into bottom values('" + str(iid) + "','" + name.replace("'",
                                                                                                      '') + "','" + kind_des.replace(
                                "'", '') + "')")
                            bdb.commit()
                            os.chdir(path + "bottom")  ##切换到上面创建的文件夹
                            f = open(str(iid) + '.jpg', 'ab')
                            f.write(img.content)
                            f.close()
                        if kind_des.__contains__('Shoes') or kind_des.__contains__('Boots'):
                            f11.write(str(iid) + " " + name + " " + kind_des + " " + "\n")
                            scu.execute("insert into shoes values('" + str(iid) + "','" + name.replace("'",
                                                                                                      '') + "','" + kind_des.replace(
                                "'", '') + "')")
                            sdb.commit()
                            os.chdir(path + "shoes")  ##切换到上面创建的文件夹
                            f = open(str(iid) + '.jpg', 'ab')
                            f.write(img.content)
                            f.close()

                    ioid_sql = iocu.execute("select oid from item_outfit where iid='" + str(iid).replace("'", '') + "'").fetchone()
                    if ioid_sql is None:
                        f4.write(str(oid)+" "+str(iid)+"\n")
                        iocu.execute("insert into item_outfit values('" + str(oid) + "','" + str(iid) + "')")
                        iodb.commit()
                        if kind_des.__contains__('Tops') or kind_des.__contains__(
                                'Outerwear'):
                            f6.write(str(oid) + " " + str(iid) + "\n")
                            tocu.execute("insert into top_outfit values('" + str(oid) + "','" + str(iid) + "')")
                            todb.commit()
                        if kind_des.__contains__('Skirts') or kind_des.__contains__(
                                'Jeans') or kind_des.__contains__('Pants') or kind_des.__contains__('Shorts'):
                            f7.write(str(oid) + " " + str(iid) + "\n")
                            bocu.execute("insert into bottom_outfit values('" + str(oid) + "','" + str(iid) + "')")
                            bodb.commit()
                        if kind_des.__contains__('Shoes') or kind_des.__contains__('Boots'):
                            f8.write(str(oid) + " " + str(iid) + "\n")
                            socu.execute("insert into shoes_outfit values('" + str(oid) + "','" + str(iid) + "')")
                            sodb.commit()
                    else:
                        ioid_sql_all = iocu.execute("select oid from item_outfit where iid='" + str(iid).replace("'", '') + "'").fetchall()
                        inoid = 0
                        for oid_sql_all in ioid_sql_all:
                            oid_all = str(oid_sql_all).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
                            if oid_all == oid:
                                inoid = 1
                        if inoid == 0:
                            f4.write(str(oid) + " " + str(iid) + "\n")
                            iocu.execute("insert into item_outfit values('" + str(oid) + "','" + str(iid) + "')")
                            iodb.commit()
                            if kind_des.__contains__('Tops') or kind_des.__contains__(
                                    'Outwear'):
                                f6.write(str(oid) + " " + str(iid) + "\n")
                                tocu.execute("insert into top_outfit values('" + str(oid) + "','" + str(iid) + "')")
                                todb.commit()
                            if kind_des.__contains__('Skirts') or kind_des.__contains__(
                                    'Jeans') or kind_des.__contains__('Pants') or kind_des.__contains__('Shorts'):
                                f7.write(str(oid) + " " + str(iid) + "\n")
                                bocu.execute("insert into bottom_outfit values('" + str(oid) + "','" + str(iid) + "')")
                                bodb.commit()
                            if kind_des.__contains__('Shoes') or kind_des.__contains__('Boots'):
                                f8.write(str(oid) + " " + str(iid) + "\n")
                                socu.execute("insert into shoes_outfit values('" + str(oid) + "','" + str(iid) + "')")
                                sodb.commit()

                except:
                    print(uid)

    uid = uid + 1
    print(uid)



idb.close()
odb.close()
udb.close()
tdb.close()
bdb.close()
sdb.close()
iodb.close()
todb.close()
bodb.close()
sodb.close()
uldb.close()

f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
f7.close()
f8.close()
f9.close()
f10.close()
f11.close()
