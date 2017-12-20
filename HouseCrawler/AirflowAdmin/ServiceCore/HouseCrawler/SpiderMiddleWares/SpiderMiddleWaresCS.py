# coding = utf-8
import json
import re
import sys
import uuid

from HouseCrawler.Items.ItemsCS import *
from HouseNew.models import *
from scrapy import Request
from scrapy import Selector

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse

headers = {'Host': 'search.csfdc.gov.cn',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': 1,
           'Content-Type': 'application/x-www-form-urlencoded',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8'}


def get_json(strRes):
    strRes = str(strRes).replace("'", '"').replace('\\', ' '). \
        replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    return json.loads(strRes)


def get_url_id(strUrl):
    res_id = '0'
    match_res = re.search(r'(\d+)', str(strUrl).lower())
    if match_res:
        res_id = match_res.group(1)
    return res_id


def get_href(strHref):
    res_href = ''
    match_res = re.search(r"'(.+)','_blank'", str(strHref))
    if match_res:
        res_href = match_res.group(1)
    return res_href


def get_house_req(strHref, ProjectName, ProjectUUID, BuildingName, BuildingUUID):
    house_req = None
    house_header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Host': 'search.csfdc.gov.cn',
                    'Referer': 'http://search.csfdc.gov.cn/index.php/home/index/floorinfo_n/xmbh/201409301985',
                    'X-Requested-With': 'XMLHttpRequest'}
    req_url = 'http://search.csfdc.gov.cn/index.php/home/Index/geths/'
    match_id = re.search(r"javascript:hsjajx('(.+)',.+)", str(strHref))
    if match_id:
        req_dict = {'ywzh': str(match_id.group(1))}
        house_req = Request(url=req_url, body=urlparse.urlencode(req_dict), method='POST',
                                headers=house_header,
                                meta={'PageType': 'HouseInfo',
                                        'ProjectName': ProjectName,
                                        'ProjectUUID': ProjectUUID,
                                        'BuildingName': BuildingName,
                                        'BuildingUUID': BuildingUUID})
    return house_req


def get_total_page(string):
    total_page = 0
    try:
        search_result = re.search(r'<a href="javascript:pager\((\d+)\)">末页</a>',
                                  str(string))
        if search_result:
            total_page = int(search_result.group(1))
    except Exception:
        import traceback
        traceback.print_exc()
    return total_page


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
            base_url = 'http://search.csfdc.gov.cn/index.php/home/Index/sfloor'
            req_dict = {'xmmc': '',
                        'p': 0,
                        '__hash__': ''}
            req_dict['__hash__'] = sel.xpath('//meta[@name="__hash__"]/@content').extract_first()
            total_page = get_total_page(response.body_as_unicode())
            for page in range(1, total_page + 1):
                req_dict['p'] = page
                url = base_url
                body = urlparse.urlencode(req_dict)
                result.append(Request(url=url, body=body, method='POST', dont_filter=True,
                                      headers=headers, meta={'PageType': 'ProjectList'}))
        elif response.meta.get('PageType') == 'ProjectList':
            project_list = sel.xpath('//tr[td[a and not(@colspan)]]')
            for p in project_list:
                p_id = get_url_id(p.xpath('./td[1]/a/@href').extract_first() or '')
                p_name = p.xpath('./td[1]/a/text()').extract_first() or ''
                p_href = urlparse.urljoin(response.url,
                                          p.xpath('./td[1]/a/@href').extract_first() or '')
                p_address = p.xpath('./td[2]/text()').extract_first() or ''
                p_regname = p.xpath('./td[3]/text()').extract_first() or ''
                p_regdate = p.xpath('./td[4]/text()').extract_first() or ''
                pb = ProjectBaseItem()
                pb['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + p_id)
                pb['ProjectRegUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_regname + p_id)
                pb['ProjectName'] = p_name
                pb['ProjectURL'] = p_href
                pb['ProjectAddress'] = p_address
                pb['ProjectRegName'] = p_regname
                pb['ProjectRegDate'] = p_regdate
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
            pinfo['ProjectName'] = sel.xpath('//body/div/div/div[1]/table/tr[1]/th/text()').extract_first() or ''
            pinfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                              pinfo['ProjectName'] + get_url_id(response.url))
            pinfo['ProjectDistrict'] = sel.xpath('//body/div/div/div[1]/table/tr[2]/td[2]/text()').extract_first() or ''
            pinfo['ProjectBaseLicenseCode'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[2]/td[4]/text()').extract_first() or ''
            pinfo['ProjectCompany'] = sel.xpath('//body/div/div/div[1]/table/tr[3]/td[2]/text()').extract_first() or ''
            pinfo['ProjectBuildingNum'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[3]/td[4]/text()').extract_first() or ''
            pinfo['ProjectAddress'] = sel.xpath('//body/div/div/div[1]/table/tr[4]/td[2]/text()').extract_first() or ''
            pinfo['ProjectBasePrice'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[4]/td[4]/text()').extract_first() or ''
            pinfo['ProjectSaleAddress'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[5]/td[2]/text()').extract_first() or ''
            pinfo['ProjectSalePhone'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[5]/td[4]/text()').extract_first() or ''
            pinfo['ProjectHouseNum'] = sel.xpath('//body/div/div/div[1]/table/tr[6]/td[2]/text()').extract_first() or ''
            pinfo['ProjectBusLine'] = sel.xpath('//body/div/div/div[1]/table/tr[6]/td[4]/text()').extract_first() or ''
            pinfo['ProjectTotalArea'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[7]/td[2]/text()').extract_first() or ''
            pinfo['ProjectBuildingArea'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[8]/td[2]/text()').extract_first() or ''
            pinfo['ProjectDesignCompany'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[7]/td[4]/text()').extract_first() or ''
            pinfo['ProjectSaleAgent'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[8]/td[4]/text()').extract_first() or ''
            pinfo['ProjectManageCompany'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[9]/td[4]/text()').extract_first() or ''
            pinfo['ProjectBuildCompany'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[10]/td[4]/text()').extract_first() or ''
            pinfo['ProjectFinishAt'] = sel.xpath(
                '//body/div/div/div[1]/table/tr[11]/td[4]/text()').extract_first() or ''
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
        if response.meta.get('PageType') not in ('ProjectInfo',):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectInfo':
            p_name = sel.xpath('//body/div/div/div[1]/table/tr[1]/th/text()').extract_first() or ''
            p_id = get_url_id(response.url)
            building_list = sel.xpath('//div[@class="hs_table"]/table/tr[not(@class) and td]')
            for b in building_list:
                b_info = BuildingInfoItem()
                b_info['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + p_id)
                b_info['ProjectName'] = p_name
                b_info['BuildingRegName'] = b.xpath('./td[1]/text()').extract_first() or ''
                b_info['BuildingRegDate'] = b.xpath('./td[3]/text()').extract_first() or ''
                b_info['BuildingName'] = b.xpath('./td[2]/text()').extract_first() or ''
                b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                    b_info['BuildingRegName'] + b_info['BuildingName'] + p_id)
                b_info['BuildingAreaLicenceCode'] = b.xpath('./td[5]/text()').extract_first() or ''
                b_info['BuildingEngPlanLicenceCode'] = b.xpath('./td[6]/text()').extract_first() or ''
                b_info['BuildingAreaPlanLicenceCode'] = b.xpath('./td[7]/text()').extract_first() or ''
                b_info['BuildingBuildLicenceCode'] = b.xpath('./td[8]/text()').extract_first() or ''
                b_info['BuildingRegArea'] = b.xpath('./td[4]/text()').extract_first() or ''
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

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfo',):
            if result:
                return result
            return []
        print('HouseInfoHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfo':
            sel = Selector(response)
            building_list = sel.xpath('//div[@class="hs_table"]/table/tr[not(@class) and td]')
            if building_list == []:
                if result:
                    return result
                return []
            for building_info in building_list:
                p_name = sel.xpath('//body/div/div/div[1]/table/tr[1]/th/text()').extract_first() or ''
                b_name = building_info.xpath('./td[2]/text()').extract_first() or ''
                breg_name = building_info.xpath('./td[1]/text()').extract_first() or ''
                p_uuid = uuid.uuid3(uuid.NAMESPACE_DNS,
                                    p_name + get_url_id(response.url))
                b_uuid = uuid.uuid3(uuid.NAMESPACE_DNS,
                                    breg_name + b_name + get_url_id(response.url))
                req = get_house_req(building_info.xpath('./td[@onclick]/@onclick').extract_first(),
                                    p_name, p_uuid, b_name, b_uuid)
                result.append(req)
        elif response.meta.get('PageType') == 'HouseInfo':
            sel = Selector(text=response.body_as_unicode()[1:-1])
            house_list = sel.xpath('//tr[not(th)]')
            for house in house_list:
                hinfo = HouseInfoItem()
                hinfo['ProjectName'] = response.meta.get('ProjectName') or ''
                hinfo['BuildingName'] = response.meta.get('BuildingName') or ''
                hinfo['ProjectUUID'] = response.meta.get('ProjectUUID') or ''
                hinfo['BuildingUUID'] = response.meta.get('BuildingUUID') or ''
                hinfo['HouseName'] = json.loads('{"foo":"%s"}' % house.xpath('./td[1]/text()').extract_first() or '').get('foo')
                hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, hinfo['HouseName'] + str(hinfo['BuildingUUID']))
                hinfo['HouseFloor'] = json.loads('{"foo":"%s"}' % house.xpath('./td[2]/text()').extract_first() or '').get('foo')
                hinfo['HouseBuildingArea'] = json.loads('{"foo":"%s"}' % house.xpath('./td[5]/text()').extract_first() or '').get('foo')
                hinfo['HouseInnerArea'] = json.loads('{"foo":"%s"}' % house.xpath('./td[6]/text()').extract_first() or '').get('foo')
                hinfo['HouseShareArea'] = json.loads('{"foo":"%s"}' % house.xpath('./td[7]/text()').extract_first() or '').get('foo')
                hinfo['HouseType'] = json.loads('{"foo":"%s"}' % house.xpath('./td[4]/text()').extract_first() or '').get('foo')
                hinfo['HouseUsage'] = json.loads('{"foo":"%s"}' % house.xpath('./td[3]/text()').extract_first() or '').get('foo')
                hinfo['HouseSaleState'] = json.loads('{"foo":"%s"}' % house.xpath('./td[9]/text()').extract_first() or '').get('foo')
                hinfo['HouseDType'] = json.loads('{"foo":"%s"}' % house.xpath('./td[5]/text()').extract_first() or '').get('foo')
                result.append(hinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
