# -*- coding: utf-8 -*-
import json
import urllib2
import sys
import time
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding('utf8')
#url = 'http://tianqi.2345.com/air-59287.htm'
#f = open('C:\Users\Administrator\Desktop\douban\guangdong.html', 'w')
#f.write(html)

province_map = {
    u'安徽': u'58321',
    u'澳门': u'45011',
    u'北京': u'54511',
    u'重庆': u'57516',
    u'福建': u'58847',
    u'甘肃': u'52889',
    u'广东': u'59287',
    u'广西': u'59431',
    u'贵州': u'57816',
    u'海南': u'59758',
    u'河北': u'53698',
    u'河南': u'57083',
    u'黑龙江': u'50953',
    u'湖北': u'57494',
    u'湖南': u'57687',
    u'吉林': u'54161',
    u'江苏': u'58238',
    u'江西': u'58606',
    u'辽宁': u'54342',
    u'内蒙古': u'53463',
    u'宁夏': u'53614',
    u'青海': u'52866',
    u'山东': u'54823',
    u'山西': u'53772',
    u'陕西': u'57036',
    u'上海': u'58362',
    u'四川': u'56294',
    u'台湾': u'59554',
    u'天津': u'54527',
    u'西藏': u'55591',
    u'香港': u'45007',
    u'新疆': u'51463',
    u'云南': u'56778',
    u'浙江': u'58457',
}


def task():
    with open('/home/heng/data/pm.json', 'a+') as f:
        for k, v in province_map.items():
            province_name = k
            city_code = v
            city_url = 'http://tianqi.2345.com/air-%s.htm' % city_code
            resp = urllib2.urlopen(city_url)
            html = resp.read()
            doc = pq(html)
            result = {}
            city_name = doc('.city_title.clearfix .btitle')('h1').text()
            if city_name:
                result[u'cityName'] = city_name.replace(u'空气质量pm2.5', '').strip()
            publish_time = doc('.fleft.state-C .filter .publish').text()
            publish_time = publish_time.replace(u'中国环境保护部', '').replace(u'发布', '').strip()
            info = doc('.fleft.state-C dl.pm25 ul.clearfix')('li').items()
            result[u'provinceName'] = province_name
            result[u'publishTime'] = publish_time
            for i in info:
                name = i('.name').text()
                value_unit = i('.value')('i').text().strip()
                value = i('.value').remove('i').text().replace(u'暂无', '').strip()
                if name == u'PM2.5':
                    if value:
                        result[u'pm25'] = {u'value': value, u'unit': value_unit}
                elif name == u'PM10':
                    if value:
                        result[u'pm10'] = {u'value': value, u'unit': value_unit}
                elif name == u'二氧化硫':
                    if value:
                        result[u'so2'] = {u'value': value, u'unit': value_unit}
                elif name == u'二氧化氮':
                    if value:
                        result[u'no2'] = {u'value': value, u'unit': value_unit}
                elif name == u'一氧化碳':
                    if value:
                        result[u'co'] = {u'value': value, u'unit': value_unit}
                elif name == u'臭氧':
                    if value:
                        result[u'o3'] = {u'value': value, u'unit': value_unit}
            if result:
                f.write('%s\n' % json.dumps(result, ensure_ascii=False, encoding='utf-8'))


def timer(n):
    while True:
        print time.strftime('%Y-%m-%d %X', time.localtime())
        task()
        time.sleep(n)

if __name__ == '__main__':
    #timer(3600)
    task()