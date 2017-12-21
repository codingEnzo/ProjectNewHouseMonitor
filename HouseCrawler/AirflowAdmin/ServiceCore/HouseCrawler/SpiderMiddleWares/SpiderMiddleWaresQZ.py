# coding = utf-8
import copy
import json
import re
import sys
import uuid

from HouseCrawler.Items.ItemsQZ import *
from HouseNew.models import *
from scrapy import Request
from scrapy import Selector

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse

HEADERS = {'Host': 'www.qzfdc.gov.cn:2015',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Referer': 'http://www.qzfdc.gov.cn:2015/qzjsj_web2/xygs.do?method=fdcxxfb&title=zslp',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': 1}


def get_project_request(string):
    url_base = 'http://www.qzfdc.gov.cn:2015/qzjsj_web2/xygs.do?method=fdcxxfbDetail2'
    req_dict = {'xygs_title': '',
                'xygs_id': '',
                'xygs_name': ''}
    match = re.search(r"javascript:goTo_after\('(.*)','(.*)','(.*)'\)", str(string))
    if match:
        req_dict['xygs_title'] = match.group(1)
        req_dict['xygs_id'] = match.group(2)
        req_dict['xygs_name'] = match.group(3)
        return json.dumps({'source_url': url_base, 'body': urlparse.urlencode(req_dict, encoding='gbk'),
                           'method': 'POST', 'meta': {'PageType': 'ProjectInfo'}})
    return None


class ProjectBaseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectBase', 'ProjectList'):
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectBase':
            total_page = int(sel.xpath('//tr/td[@class="textDiv"]/span[2]/text()').extract_first() or '0')
            for cur_page in range(1, total_page + 1):
                result.append(Request(url=response.url, body=urlparse.urlencode({'currentPage': cur_page}),
                                      headers=HEADERS, method='POST', meta={'PageType': 'ProjectList'}))
        elif response.meta.get('PageType') == 'ProjectList':
            project_list = sel.xpath('//tr[@class="eg_mainlist"]')
            for p in project_list:
                p_name = (p.xpath('./td[1]/a/text()').extract_first() or '').strip()
                p_req = get_project_request(p.xpath('./td[1]/a/@href').extract_first() or '')
                pb = ProjectBaseItem()
                pb['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name)
                pb['ProjectName'] = p_name
                pb['ProjectURL'] = p_req
                result.append(pb)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class ProjectInfoHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfo',):
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectInfo':
            pinfo = ProjectInfoItem()
            pinfo['ProjectName'] = sel.xpath('//td[img]/text()').extract()[0].strip().replace('项目名称：', '')
            pinfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, pinfo['ProjectName'])
            pinfo['ProjectCompany'] = sel.xpath('//td[img]/text()').extract()[1].strip().replace('开发企业：', '')
            pinfo['ProjectAddress'] = sel.xpath('//td[img]/text()').extract()[4].strip().replace('坐落：', '')
            pinfo['ProjectDistrict'] = sel.xpath('//td[img]/text()').extract()[3].strip().replace('区属：', '')
            pinfo['ProjectArea'] = sel.xpath('//td[img]/text()').extract()[2].strip().replace('总面积：', '').replace('㎡',
                                                                                                                  '')
            pinfo['ProjectPhone'] = sel.xpath('//td[img]/text()').extract()[6].strip().replace('联系电话：', '')
            pinfo['ProjectPhoneConn'] = sel.xpath('//td[img]/text()').extract()[5].strip().replace('联系人：', '')
            result.append(pinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class BuildingListHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfo', 'BuildingInfo'):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectInfo':
            p_name = sel.xpath('//td[img][1]/text()').extract_first().strip().replace('项目名称：', '')
            building_list = sel.xpath('//tr[@title]')
            for b in building_list:
                b_info = BuildingInfoItem()
                b_info['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name)
                b_info['ProjectName'] = p_name
                b_info['BuildingName'] = (b.xpath('./td[1]/a/text()').extract_first() or '').strip()
                b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                    b_info['BuildingName'] + p_name)
                b_info['BuildingNum'] = (b.xpath('./td[2]/text()').extract_first() or '').strip()
                b_info['BuildingArea'] = (b.xpath('./td[3]/text()').extract_first() or '').strip()
                b_info['BuildingDistrict'] = (b.xpath('./td[4]/text()').extract_first() or '').strip()
                b_info['BuildingAddress'] = (b.xpath('./td[5]/text()').extract_first() or '').strip()
                building_info_url = urlparse.urljoin(response.url,
                                                     b.xpath('./td[1]/a/@href').extract_first() or '')
                if building_info_url:
                    result.append(Request(url=building_info_url, method='GET',
                                          meta={'PageType': 'BuildingInfo', 'item': copy.deepcopy(b_info)}))
                else:
                    result.append(b_info)
        elif response.meta.get('PageType') == 'BuildingInfo':
            b_info = response.meta.get('item')
            if b_info:
                b_info['BuildingRegName'] = sel.xpath('//td[img]/text()').extract()[3].strip().replace('许可证号：', '')
                b_info['BuildingBuildDate'] = sel.xpath('//td[img]/text()').extract()[7].strip().replace('开工日期：', '')
                b_info['BuildingCompleteDate'] = sel.xpath('//td[img]/text()').extract()[8].strip().replace('竣工日期：', '')
                b_info['BuildingURL'] = urlparse.urljoin(response.url,
                                                         sel.xpath('//a[text()="查看楼盘"]/@href').extract_first())
                result.append(b_info)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class HouseInfoHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        def get_house_state(string):
            STATE_TAB = {'background-color: #00ff00;': '可以进行认购、签约等操作',
                         'background-image:url(images/2.png);': '预售许可、已办理在建抵押或土地抵押，但取得抵押权人同意可以进行认购、签约操作',
                         'background-color: #FF00FF;': '认购已经完成',
                         'background-color: #FFFF00;': '签约已经完成',
                         'background-color: red;': '登记机关已完成备案登记',
                         'background-color: goldenrod;': '预售许可、已办理在建抵押或土地抵押，但未取得抵押权人同意不能进行认购、签约等操作',
                         'background-color: #cccccc;': '无预售许可、限制、未经许可，禁止销售'}
            state = ''
            for key in STATE_TAB:
                if key == string:
                    state = STATE_TAB[key]
                    break
            return state

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseInfo',):
            if result:
                return result
            return []
        print('HouseInfoHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'HouseInfo':
            if (not response.meta.get('ProjectName')) or (not response.meta.get('BuildingName')) \
                    or (not response.meta.get('ProjectUUID')) or (not response.meta.get('BuildingUUID')):
                if result:
                    return result
                return []
            floor_list = sel.xpath('//table[@cellspacing="0"]/tr[td[@style]]')
            for floor in floor_list:
                cur_floor = floor.xpath('./td[2]/text()').extract_first() or ''
                houseinfodetail_list = floor.xpath('./td[@style]')
                for house in houseinfodetail_list:
                    hinfo = HouseInfoItem()
                    hinfo['ProjectName'] = response.meta.get('ProjectName')
                    hinfo['BuildingName'] = response.meta.get('BuildingName')
                    hinfo['ProjectUUID'] = response.meta.get('ProjectUUID')
                    hinfo['BuildingUUID'] = response.meta.get('BuildingUUID')
                    hinfo['HouseName'] = house.xpath('./text()').extract_first() or ''
                    hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                    hinfo['HouseName'] + str(hinfo['BuildingUUID']))
                    hinfo['HouseFloor'] = cur_floor
                    hinfo['HouseSaleState'] = get_house_state(house.xpath('./@style').extract_first() or '')
                    house_detail = re.search(
                        r"室号/部位：(?P<housenum>.*), 预测建筑面积：(?P<buildingarea>.*), 预测套内面积：(?P<innerarea>.*), 结构：(?P<structure>.*), 用途：(?P<houseusage>.*), 预测公摊面积：(?P<sharearea>.*)",
                        house.xpath('./@title').extract_first() or '')
                    if house_detail:
                        house_dict = house_detail.groupdict() or {}
                        hinfo['HouseNum'] = house_dict.get('housenum') or ''
                        hinfo['HouseBuildingArea'] = house_dict.get('buildingarea') or ''
                        hinfo['HouseInnerArea'] = house_dict.get('innerarea') or ''
                        hinfo['HouseStructure'] = house_dict.get('structure') or ''
                        hinfo['HouseUsage'] = house_dict.get('houseusage') or ''
                        hinfo['HouseShareArea'] = house_dict.get('sharearea') or ''
                    result.append(hinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
