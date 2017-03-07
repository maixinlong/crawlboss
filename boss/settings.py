# -*- coding: utf-8 -*-

# Scrapy settings for boss project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import random

BOT_NAME = 'boss'

SPIDER_MODULES = ['boss.spiders']
NEWSPIDER_MODULE = 'boss.spiders'

#可选的级别有: CRITICAL、 ERROR、WARNING、INFO、DEBUG
LOG_LEVEL = 'ERROR'

ITEM_PIPELINES = {
    'boss.pipelines.BossPipeline':10,
}


#下载延时，即下载两个页面的等待时间
DOWNLOAD_DELAY = 0.5


###自己从不同浏览器中获取cookie在添加到这
def getCookie():
    cookie_list = [
        "Hm_lvt_d86954201130d615136257dde062a503",
        "Hm_lvt_64482d28852c5bf661868b4153de444c"
    ]
    cookie = random.choice(cookie_list)
    return cookie

#设置默认request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'www.baidu.com',
    'RA-Sid':'7739A016-20140918-030243-3adabf-48f828',
    'RA-Ver':'3.0.7',
    'Upgrade-Insecure-Requests':'1',
    'Cookie':'%s' % getCookie()
}