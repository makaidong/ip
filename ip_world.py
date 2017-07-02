import requests
from bs4 import BeautifulSoup
import threading
import json
import time
import random
import pymysql
import queue
from urllib.request import urlopen
# 导入方法模块
def creat_table(table_name):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 db='test',
                                 port=3306,
                                 charset='utf8')
    try:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS %s"%table_name)
        sql="CREATE TABLE "+table_name+ " (`ip` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`country` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`region` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`ips` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`area` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`county` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL)"
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()

def mysql(table,a,b,c,d,e,f):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 db='test',
                                 port=3306,
                                 charset='utf8')
    #数据库的配置
    try:
        with connection.cursor() as cursor:
            # sql="inser into news(id,title,url) values(\"%d\",\"%s\",\"%s\")"
            sql="insert into "+  table+" (ip,country,region,ips,area,county) values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(a,b,c,d,e,f))
            connection.commit()
    finally:
        connection.close()
def c_mysql(a):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 db='test',
                                 port=3306,
                                 charset='utf8')#数据库配置文件
    try:
        with connection.cursor() as cursor:

            sql="insert into "+"c_ip"+" (ip) values(%s)"
            cursor.execute(sql,a)
            connection.commit()
    finally:
        connection.close()
def all_mysql(a):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 db='test',
                                 port=3306,
                                 charset='utf8') #数据库配置文件
    try:
        with connection.cursor() as cursor:

            sql="insert into "+"all_ip"+" (ip) values(%s)"
            cursor.execute(sql,(a))
            connection.commit()
    finally:
        connection.close()
def get_ip_field(html):
    html=requests.get(html).text
    ip_field1=[]
    ip_field2=[]
    all_ip = []
    ip_html=BeautifulSoup(html)
    ip_bq1=ip_html.findAll("span",{"class":"v_l"})
    ip_bq2=ip_html.findAll("span",{"class":"v_r"})
    for ip_text1 in ip_bq1:
        ip_field1.append(ip_text1.get_text())
    for ip_text2 in ip_bq2:
        ip_field2.append(ip_text2.get_text())
    print(len(ip_field1))
    for m in range(len(ip_field1)):
        ip1=ip_field1[m].split('.')
        ip2=ip_field2[m].split('.')
        for ip_2 in range(int(ip1[1]),int(ip2[1])+1):
            for ip_3 in range(int(ip1[2]),int(ip2[2])+1):
                one_ip= ip1[0]+'.'+str(ip_2)+'.'+str(ip_3)+'.'+'0'
                all_ip.append(one_ip)
    return all_ip

def main(inargs):
    work_queue = queue.Queue()  # queue类中实现了锁
    for i in range(200):  # 设置了200个子进程
        worker = Worker(work_queue, i)  # 工作线程、工作队列、线程编号
        worker.daemon = True  # 守护进程
        worker.start()  # 启动线程开始
    for ip in inargs:
        work_queue.put(ip)  # 加入到队列中开始各个线程
    work_queue.join()  # 队列同步

class Worker(threading.Thread):

    def __init__(self, work_queue, number):
        super().__init__()
        self.work_queue = work_queue
        self.number = number

    def process(self, ip):
        # 自定义的线程处理函数，用于run()中.
        global urlRoot
        urlRoot = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s'
        content = False
        retry = 100
        i=0;
        while retry != 0:

            try:
                content = urlopen(urlRoot % ip, timeout=0.5).read().decode('utf8')
                retry = 0
            except Exception as  e:
                retry -= 1
                print(e)
                continue
            if content:
                content = json.loads(content)
                if content['code'] != 0:
                    retry -= 1
                    i = i +1;
                    if i == 20:
                        print(i)
                        c_mysql(ip)
                        break
                    print(retry)
                    print(content)
                    continue
                else:
                    print(content)
                    content = content['data']
                    try:
                        ip_dict = {'海南省': 'hainan', '北京市': 'beijing', '黑龙江省': 'heilongjiang', '广东省': 'guangdong', '上海市': 'shanghai', '湖北省': 'hubei', '香港特别行政区': 'xianggang', '内蒙古自治区': 'neimenggu', '宁夏回族自治区': 'ningxia', '山西省': 'shanxi', '江西省': 'jiangxi', '四川省': 'sichuan', '新疆维吾尔自治区': 'xinjiang', '西藏自治区': 'xizang', '贵州省': 'guizhou', '山东省': 'shandong', '陕西省': 'shan_xi', '吉林省': 'jilin', '湖南省': 'hunan', '河南省': 'henan', '江苏省': 'jiangsu', '天津市': 'tianjin', '安徽省': 'anhui', '浙江省': 'zhejiang', '云南省': 'yunnan', '福建省': 'fujian', '辽宁省': 'liaoning', '青海省': 'qinghai', '重庆市': 'chongqing', '河北省': 'hebei', '广西壮族自治区': 'guangxi', '甘肃省': 'gansu'}
                        table = ip_dict.get(content.get("region"))
                        mysql(table,content.get("ip"), content.get("country"),
                          content.get("region"),
                          content.get("isp"), content.get("city"),content.get("county"))
                        all_mysql(ip)

                    except Exception as e:
                        print(e)
                        c_mysql(ip)
                        print("数据未导入")
            return content

    def run(self):
        # 重载threading类中的run()
        while True:
            try:
                ip = self.work_queue.get()  # 从队列取出任务
                self.process(ip)
            finally:
                self.work_queue.task_done()  # 通知queue前一个task已经完成


if __name__ == "__main__":

    all_url=['http://ips.chacuo.net/view/s_BJ','http://ips.chacuo.net/view/s_GD', 'http://ips.chacuo.net/view/s_SD',
     'http://ips.chacuo.net/view/s_ZJ', 'http://ips.chacuo.net/view/s_JS', 'http://ips.chacuo.net/view/s_SH',
     'http://ips.chacuo.net/view/s_LN', 'http://ips.chacuo.net/view/s_SC', 'http://ips.chacuo.net/view/s_HA',
     'http://ips.chacuo.net/view/s_HB', 'http://ips.chacuo.net/view/s_FJ', 'http://ips.chacuo.net/view/s_HN',
     'http://ips.chacuo.net/view/s_HE', 'http://ips.chacuo.net/view/s_CQ', 'http://ips.chacuo.net/view/s_SX',
     'http://ips.chacuo.net/view/s_JX', 'http://ips.chacuo.net/view/s_SN', 'http://ips.chacuo.net/view/s_AH',
     'http://ips.chacuo.net/view/s_HL', 'http://ips.chacuo.net/view/s_GX', 'http://ips.chacuo.net/view/s_JL',
     'http://ips.chacuo.net/view/s_YN', 'http://ips.chacuo.net/view/s_TJ', 'http://ips.chacuo.net/view/s_NM',
     'http://ips.chacuo.net/view/s_XJ', 'http://ips.chacuo.net/view/s_GS', 'http://ips.chacuo.net/view/s_GZ',
     'http://ips.chacuo.net/view/s_HI', 'http://ips.chacuo.net/view/s_NX', 'http://ips.chacuo.net/view/s_QH',
     'http://ips.chacuo.net/view/s_XZ', 'http://ips.chacuo.net/view/s_HK']
    for url in all_url:
        all_ip =get_ip_field(url)
        main(all_ip)

