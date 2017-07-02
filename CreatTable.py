import pymysql
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

if __name__ =="__main__":
    ip_address = ['beijing', 'guangdong', 'shandong', 'zhejiang', 'jiangsu', 'shanghai', 'liaoning', 'sichuan', 'henan',
                  'hubei', 'fujian', 'hunan', 'hebei', 'chongqing', 'shanxi', 'jiangxi', 'shan_xi', 'anhui',
                  'heilongjiang', 'guangxi', 'jilin', 'yunnan', 'tianjin', 'neimenggu', 'xinjiang', 'gansu', 'guizhou',
                  'hainan', 'ningxia', 'qinghai', 'xizang', 'xianggang']
    ip_aa = ['北京市', '广州省', '山东省', '浙江省', '江苏省', '上海市', '辽宁省', '四川省', '河南省', '湖北省', '福建省', '湖南省', '河北省', '重庆市', '山西省',
             '江西省', '陕西省', '安徽省', '黑龙江省', '广西壮族自治区', '吉林省', '云南省', '天津市', '内蒙古自治区', '新疆维吾尔自治区', '甘肃省', '贵州省', '海南省',
             '宁夏回族自治区', '青海省', '西藏自治区', '香港特别行政区']
    ip_dict = dict(zip(ip_aa, ip_address))
    print(ip_dict)
    for ip_add in ip_address:
        creat_table(ip_add)
    creat_table('c_ip')
    creat_table("all_ip")
    print(ip_dict.get("北京市"))
