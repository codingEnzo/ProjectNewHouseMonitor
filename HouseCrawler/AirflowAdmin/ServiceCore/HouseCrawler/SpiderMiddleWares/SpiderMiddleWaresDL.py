# coding = utf-8
import re
import sys
import uuid
import copy
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsDL import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.5',
           'Connection': 'keep-alive',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Host': 'old.gtfwj.dl.gov.cn',
           'Upgrade-Insecure-Requests': '1'}


def get_mxid(string):
    res_id = '0'
    match_res = re.search(r"xmid: '(.+)'", str(string))
    if match_res:
        res_id = match_res.group(1)
    return res_id


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
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') != 'ProjectBase':
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        if response.request.method == 'GET':
            req_dict = {'kfs.kfsmc': '',
                        'pageNo': '1',
                        'pageSize': '99999',
                        'xmmc': '',
                        'xzqh': ''
                        }
            req_body = urlparse.urlencode(req_dict)
            result.append(Request(url=response.url, body=req_body, method='POST',
                                  headers=headers, meta={'PageType': 'ProjectBase'}))
        elif response.request.method == 'POST':
            project_list = Selector(response).xpath(
                '//tr[@class="info"]')[:-1]
            for p in project_list:
                p_district = (
                    p.xpath('./td[1]/text()').extract_first() or '')
                p_name = (
                    p.xpath('./td[2]/a/text()').extract_first() or '')
                p_href = urlparse.urljoin(response.url,
                                          p.xpath('./td[2]/a/@href').extract_first())
                p_address = (
                    p.xpath('./td[3]/text()').extract_first() or '')
                p_company = (
                    p.xpath('./td[4]/text()').extract_first() or '')
                pb = copy.deepcopy(response.meta.get(
                    'item') or ProjectBaseItem())
                pb['ProjectUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, p_name + p_href)
                pb['ProjectName'] = p_name
                pb['ProjectDistrict'] = p_district
                pb['ProjectURL'] = p_href
                pb['ProjectAddress'] = p_address
                pb['ProjectCorporation'] = p_company
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
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfo', 'ProjectDetailInfo'):
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfo':
            info_sel = Selector(response)
            pinfo = ProjectInfoItem()
            pinfo['ProjectName'] = info_sel.xpath(
                '//td[b[text()="项目名称："]]/following-sibling::td[1]/text()').extract_first().strip()
            pinfo['ProjectAddress'] = info_sel.xpath(
                '//td[b[text()="项目地址："]]/following-sibling::td[1]/text()').extract_first().strip()
            pinfo['ProjectCompany'] = info_sel.xpath(
                '//td[b[text()="开发单位："]]/following-sibling::td[1]/text()').extract_first().strip()
            pinfo['ProjectRegName'] = info_sel.xpath(
                '//td[b[text()="预售许可证："]]/following-sibling::td[1]/text()').extract_first().strip()
            pinfo['ProjectAreaPlanLicenseCode'] = info_sel.xpath(
                '//td[b[text()="国有土地使用证："]]/following-sibling::td[1]/text()').extract_first().strip()
            pinfo['ProjectPlanLicenseCode'] = info_sel.xpath(
                '//td[b[text()="工程规划许可证："]]/following-sibling::td[1]/text()').extract_first().strip()
            pinfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, pinfo[
                                              'ProjectName'] + response.url)
            sale_sum = {}
            sale_tds = info_sel.xpath(
                '//table[@class="table table-bordered FCtable mar-bo"]/tr/td[@class="info"]')
            for td in sale_tds:
                key = td.xpath(
                    './b/text()').extract_first(default='').replace('：', '').strip()
                if key:
                    sale_sum[key] = td.xpath(
                        './following-sibling::td[1]/text()').extract_first(default='')
            pinfo['ProjectSaleSum'] = sale_sum or {{'Null': True}}
            result.append(pinfo)

            req_dict = {'xmid': get_mxid(response.body_as_unicode()),
                        'pageNo': '1',
                        'pageSize': '999'}
            req_body = urlparse.urlencode(req_dict)
            result.append(Request(url='http://old.gtfwj.dl.gov.cn/bd/tgxm/LAjax', body=req_body, method='POST',
                                  headers=headers, meta={'PageType': 'BuildingInfo', 'ProjectName': pinfo['ProjectName'], 'ProjectUUID': pinfo['ProjectUUID']}))
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
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('BuildingInfo'):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        building_base_sel = Selector(response)
        if response.meta.get('PageType') == 'BuildingInfo':
            p_name = response.meta.get('ProjectName', '')
            p_uuid = response.meta.get('ProjectUUID', '')
            for building_info in building_base_sel.xpath('//table[@class="table table-bordered FCtable mar-bo"]/tr[not(@class) and td[a]]')[1:-2]:
                b_info = BuildingInfoItem()
                b_info['ProjectName'] = p_name
                b_info['ProjectUUID'] = p_uuid
                b_info['BuildingName'] = building_info.xpath(
                    './td[1]/a/text()').extract_first() or ''
                b_info['BuildingRegName'] = building_info.xpath(
                    './td[2]/text()').extract_first() or ''
                b_info['BuildingHouseNum'] = (building_info.xpath(
                    './td[4]/text()').extract_first() or '').replace('套', '').strip()
                b_info['BuildingAddress'] = building_info.xpath(
                    './td[3]/text()').extract_first() or ''
                b_info['BuildingArea'] = (building_info.xpath(
                    './td[5]/text()').extract_first() or '').replace('平方米', '').strip()
                b_info['BuildingURL'] = urlparse.urljoin(
                    'http://old.gtfwj.dl.gov.cn', building_info.xpath('./td[1]/a/@href').extract_first())
                b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                    str(p_name) + str(p_uuid) + str(b_info['BuildingURL']) + str(b_info['BuildingRegName']) + str(b_info['BuildingName']))
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
            STATE_TAB = {'color: red': '不可售（因超建、查封、物业用房、回迁安置等原因）',
                         'color: black': '可售',
                         'color: #00CC00': '已售',
                         'color: blue': '已被开发企业抵押给金融机构，暂不可售'}
            state = ''
            for key in STATE_TAB:
                if key in string:
                    state = STATE_TAB[key]
                    break
            return state

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseInfo', 'HouseInfoDetail'):
            if result:
                return result
            return []
        print('HouseInfoHandleMiddleware')

        if response.meta.get('PageType') == 'HouseInfo':
            if (not response.meta.get('ProjectName')) or (not response.meta.get('BuildingName'))\
                    or (not response.meta.get('ProjectUUID')) or (not response.meta.get('BuildingUUID')):
                if result:
                    return result
                return []
            houseinfodetail_tr = Selector(response).xpath(
                '//table[@class="table table-bordered FCtable"]/tr')
            for tr in houseinfodetail_tr:
                cur_floor = tr.xpath(
                    './td[1]/text()').extract_first(default='').replace('第[', '').replace(']层', '').strip()
                for house in tr.xpath('./td[@style]'):
                    hinfo = HouseInfoItem()
                    hinfo['ProjectName'] = response.meta.get('ProjectName')
                    hinfo['BuildingName'] = response.meta.get('BuildingName')
                    hinfo['ProjectUUID'] = response.meta.get('ProjectUUID')
                    hinfo['BuildingUUID'] = response.meta.get('BuildingUUID')
                    hinfo['HouseName'] = house.xpath(
                        './text()').extract_first(default='')
                    hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, hinfo[
                                                    'HouseName'] + hinfo['BuildingUUID'] + hinfo['ProjectUUID'])
                    hinfo['HouseFloor'] = cur_floor
                    hinfo['HouseSaleState'] = get_house_state(
                        house.xpath('./@style').extract_first())
                    hinfo['HouseInfoStr'] = house.xpath(
                        './@title').extract_first() or ''
                    result.append(hinfo)

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
