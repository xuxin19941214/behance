# -*- coding:utf-8 -*-
import scrapy
from scrapy.http.request import Request
from behance.behance.items import BehanceItem
import re
import json


class BehanceSpider(scrapy.Spider):
    #爬虫名
    name = 'behance'
    #爬取的域名
    allow_domain = 'https://www.behance.net'
    #策展库url
    Li_url = 'https://www.behance.net/galleries'
    #创意工具url
    To_url = 'https://www.behance.net/galleries/adobe'
    #学校和组织url
    Or_url = 'https://www.behance.net/poweredby'
    start_urls = [Li_url, To_url, Or_url]
    set_list = []
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Referer': 'https://www.behance.net/',
        'Cookie': 'bcp=d7cf6132-714c-4484-8a29-8e5969e8a0d0; bgk=31449384; AMCVS_9E1005A551ED61CA0A490D45%40AdobeOrg=1; AMCV_9E1005A551ED61CA0A490D45%40AdobeOrg=-227196251%7CMCMID%7C35850335288003595314395570213350979208%7CMCAID%7CNONE%7CMCOPTOUT-1505487932s%7CNONE%7CMCAAMLH-1506085531%7C7%7CMCAAMB-1506085532%7Chmk_Lq6TPIBMW925SPhw3Q; ilo0=true; s_pers=%20cpn%3D%7C1663247127721%3B%20ppn%3Dbehance.net%253Agallery%7C1663247127722%3B%20s_nr%3D1505480945756-New%7C1537016945756%3B%20s_vs%3D1%7C1505482747673%3B; s_sess=%20s_dmdbase%3D1%3B%20s_dmdbase_custom%3D1%3B%20s_cpc%3D0%3B%20s_ppv%3D%255B%2522www.behance.net%252Fgallery%252F56333259%252FBlack-Taiga%2522%252C6%252C0%252C642%252C681%252C642%252C1366%252C768%252C1%252C%2522P%2522%255D%3B%20s_cc%3Dtrue%3B'
    }
    second_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Referer': 'https://www.behance.net/galleries/2/Graphic-Design?tracking_source=view-all',
        'X-Requested-With': 'XMLHttpRequest',
        'X-BCP': '3c3486cb-767e-4014-be17-2656c626a9b9',
        'X-NewRelic-ID': 'VgUFVldbGwACXFJSBAUF',
        'Cookie': 'bgk=31449384; AMCVS_9E1005A551ED61CA0A490D45%40AdobeOrg=1; AMCV_9E1005A551ED61CA0A490D45%40AdobeOrg=-227196251%7CMCMID%7C35850335288003595314395570213350979208%7CMCAID%7CNONE%7CMCOPTOUT-1505573577s%7CNONE%7CMCAAMLH-1506085531%7C7%7CMCAAMB-1506171177%7Chmk_Lq6TPIBMW925SPhw3Q; bcp=3c3486cb-767e-4014-be17-2656c626a9b9; ilo0=true; s_pers=%20s_nr%3D1505570168238-Repeat%7C1537106168238%3B%20cpn%3Dbehance.net%253Agalleries%7C1663336571104%3B%20ppn%3Dbehance.net%253Agalleries%253A2%253AGraphic-Design%7C1663336571106%3B%20s_vs%3D1%7C1505571971129%3B; s_sess=%20s_dmdbase%3D1%3B%20s_dmdbase_custom%3D1%3B%20s_cpc%3D0%3B%20s_sq%3D%3B%20s_ppv%3D%255B%2522www.behance.net%252Fgallery%252F54843729%252FOsmoz-Gin-Classic-Citrus%2522%252C67%252C0%252C3262%252C1366%252C662%252C1366%252C768%252C1%252C%2522P%2522%255D%3B%20s_cc%3Dtrue%3B'
    }

    #各库的起始url
    def start_requests(self):
        for url in self.start_urls:
            if url == Li_url:
                yield Request(url, headers=self.header)
            elif url == To_url:
                yield Request(url, headers=self.header)
            elif url == Or_url:
                yield Request(url, headers=self.header)


    #策展库
    def Li_parse(self, response):
        #策展库的各分类链接
        Li_link_list = response.xpath(
            '//a[@class="curated-galleries__view-more"]/@href').extract()
        #策展库各分类的名字
        Li_class_name = response.xpath('//h2[@class="rf-curated-galleries-cover__label qa-curated-galleries-cover__label"]/text()').extract()

        for i, Li_img_link in enumerate(Li_link_list):
            # https://www.behance.net/v2/galleries/2/projects?ordinal=48
            # https://www.behance.net/galleries/2/Graphic-Design?tracking_source=view-all
            item = BehanceItem()
            parten = re.compile(r'.*?/galleries/(\d+)/.*')
            num1 = parten.findall(Li_img_link)[0]
            item['Li_classes'] = Li_class_name[i]
            for i in range(30000//48):
                ordinal = 0 + i*48
                #各图片集的链接
                Li_img_link = 'https://www.behance.net/v2/galleries/' + num1 + '/projects?ordinal=' + str(ordinal)
                yield Request(url=Li_img_link, headers=self.second_header, callback=self.Li_jsonData, meta={'meta_1': item})

    # 提取图片集名字和设计者
    def Li_jsonData(self, response):
        meta_1 = response.meta['meta_1']
        data = json.loads(response.body.decode('utf-8'))
        data_list = data['entities']
        for data in data_list:
            item = BehanceItem()
            item['Li_classes'] = meta_1['Li_classes']
            item['Li_name'] = data['name']
            item['Li_designer'] = data['display_name']
            yield Request(url=data['share_url'], headers=self.header, callback=self.Li_bottom_parse, meta={'meta_1': item})

    # 提取图片链接
    def Li_bottom_parse(self, response):
        m = response.meta['meta_1']
        img_urls = response.xpath('//div[contains(@class,"project-module module image project-module-image")]//img/@src').extract()
        #过滤取到的没用图片，filter过滤 map 在原有基础上加 reduce 可迭代对象做合并用的，python内置函数（一种可迭代对象）
        new_img_urls = filter(lambda x: x != 'https://a5.behance.net/ef35637a0f2ac3c0b37914c7d857a18d69849e04/img/site/blank.png', img_urls)
        item = BehanceItem()
        #策展库的类名
        item['Li_classes'] = m['Li_classes']
        #策展库的图片集名
        item['Li_name'] = m['Li_name']
        #策展库图片集的设计者名
        item['Li_designer'] = m['Li_designer']
        #类型转换成list
        #策展库里图片链接
        item['Li_img_list'] = list(new_img_urls)
        #返回数据
        yield item



    #创意工具
    def To_parse(self, response):
        #创意工具的各分类链接
        To_link_list = response.xpath(
            '//a[@class="curated-galleries__view-more"]/@href').extract()
        #创意工具各分类的名字
        To_class_name = response.xpath('//h2[@class="rf-curated-galleries-cover__label qa-curated-galleries-cover__label"]/text()').extract()

        for i, To_img_link in enumerate(To_link_list):
            # https://www.behance.net/v2/galleries/adobe/1/projects?ordinal=48
            # https://www.behance.net/galleries/adobe/1/Photoshop?tracking_source=view-all
            item = BehanceItem()
            parten = re.compile(r'.*?/galleries/adobe/(\d+)/.*')
            num2 = parten.findall(To_img_link)[0]
            item['To_classes'] = To_class_name[i]
            for i in range(30000//48):
                ordinal = 0 + i*48
                To_img_link = 'https://www.behance.net/v2/galleries/adobe/' + num2 + '/projects?ordinal=' + str(ordinal)
                yield Request(url=To_img_link, headers=self.second_header, callback=self.To_jsonData, meta={'meta_2': item})
    #提取图片集名字和设计者
    def To_jsonData(self, response):
        meta_2 = response.meta['meta_2']
        data = json.loads(response.body.decode('utf-8'))
        data_list = data['entities']
        for data in data_list:
            item = BehanceItem()
            item['To_classes'] = meta_2['To_classes']
            item['To_name'] = data['name']
            item['To_designer'] = data['display_name']
            yield Request(url=data['share_url'], headers=self.header, callback=self.To_bottom_parse, meta={'meta_2': item})

    # 提取图片链接
    def To_bottom_parse(self, response):
        l = response.meta['meta_2']
        img_urls = response.xpath('//div[contains(@class,"project-module module image project-module-image")]//img/@src').extract()
        #过滤取到的没用图片，filter过滤 map 在原有基础上加 reduce 可迭代对象做合并用的，python内置函数（一种可迭代对象）
        new_img_urls = filter(lambda x: x != 'https://a5.behance.net/ef35637a0f2ac3c0b37914c7d857a18d69849e04/img/site/blank.png', img_urls)
        item = BehanceItem()
        #创意工具的类名
        item['To_classes'] = l['To_classes']
        #创意工具的图片集名
        item['To_name'] = l['To_name']
        #创意工具图片集的设计者名
        item['To_designer'] = l['To_designer']
        #类型转换成list
        #创意工具里图片链接
        item['To_img_list'] = list(new_img_urls)
        #返回数据
        yield item




    #学校和组织
    def Or_parse(self, response):
        #学校和组织的各分类链接
        Or_link_list = response.xpath(
            '//a[@class="gallery-name"]/@href').extract()
        #学校和组织各分类的名字
        Or_class_name = response.xpath('//a[@class="gallery-name"]/text()').extract()

        for i, Or_img_link in enumerate(Or_link_list):
            # http://portfolios.risd.edu/?page=3
            # http://portfolios.risd.edu/
            item = BehanceItem()
            parten = re.compile(r'.*?/\.([a-zA-Z])\./.*')
            name = parten.findall(Or_img_link)[0]
            item['Or_classes'] = Or_class_name[i]
            #page=56还有图片集，57就没有了
            for i in range():

                img_link = 'http://portfolios.' + name + '.edu/?page=' + 第几页数
                yield Request(url=img_link, headers=self.second_header, callback=self.Or_jsonData, meta={'meta_3': item})

    # 提取图片集名字和设计者
    def Or_jsonData(self, response):
        meta_3 = response.meta['meta_3']
        data = json.loads(response.body.decode('utf-8'))
        data_list = data['id']
        for data in data_list:
            item = BehanceItem()
            item['Or_classes'] = meta_3['Or_classes']
            item['Or_name'] = data['name']
            item['Or_designer'] = data['display_name']
            yield Request(url=data['url'], headers=self.header, callback=self.Or_bottom_parse, meta={'meta_3': item})

    #提取图片链接
    def Or_bottom_parse(self, response):
        q = response.meta['meta_3']
        img_urls = response.xpath('//li[contains(@class,"module image")]//img/@src').extract()
        #过滤取到的没用图片，filter过滤 map 在原有基础上加 reduce 可迭代对象做合并用的，python内置函数（一种可迭代对象）
        new_img_urls = filter(lambda x: x != 'https://a5.behance.net/ef35637a0f2ac3c0b37914c7d857a18d69849e04/img/site/blank.png', img_urls)
        item = BehanceItem()
        #学校和组织的类名
        item['Or_classes'] = q['Or_classes']
        #学校和组织的图片集名
        item['Or_name'] = q['Or_name']
        #学校和组织图片集的设计者名
        item['Or_designer'] = q['Or_designer']
        #类型转换成list
        #学校和组织里图片链接
        item['Or_img_list'] = list(new_img_urls)
        #返回数据
        yield item