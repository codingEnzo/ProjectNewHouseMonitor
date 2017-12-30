# coding = utf-8
import sys
import json
import uuid
import random
import copy
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsHF import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


def nscaler(a):
    b = ""
    for i in a:
        if i == "0":
            b += "0"
            continue
        if i == "1":
            b += "2"
            continue
        if i == "2":
            b += "5"
            continue
        if i == "3":
            b += "8"
            continue
        if i == "4":
            b += "6"
            continue
        if i == "5":
            b += "1"
            continue
        if i == "6":
            b += "3"
            continue
        if i == "7":
            b += "4"
            continue
        if i == "8":
            b += "9"
            continue
        if i == "9":
            b += "7"
            continue
    return b


def recode(a, b):
    n = nscaler(a)
    c = SetObjNum(len(a))
    d = SetObjNum(len(a))
    n = int(n) + int(d)
    b = nscaler(str(b))
    return str(c) + "-" + str(n) + "-" + str(d) + "-" + str(b)


def SetObjNum(n):
    a = ""
    for i in range(n):
        a += str(random.randint(0, 10))
    return a


def s(a):
    n = nscaler(a)
    return n


def get_project_url(proID, pageKey):
    proID, pageKey = str(proID), str(pageKey)
    pro_href_base = "http://real.hffd.gov.cn/item/"
    pro_href_code = recode(proID, pageKey)
    return pro_href_base + pro_href_code


def get_house_info_url(houseID):
    houseID = str(houseID)
    house_info_base = "http://real.hffd.gov.cn/details/getrsa/"
    house_info_code = s(houseID)
    return house_info_base + house_info_code


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
        if response.meta.get('PageType') not in ('ProjectBase', ):
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectBase':
            page_key = sel.xpath('//input[@id="iptstamp"]/@value').extract_first() or ''
            project_list = sel.xpath('//span[@class="nav1"]/a[@id]')
            for p in project_list:
                pinfo = ProjectInfoItem()
                pinfo['ProjectName'] = p.xpath('./@title').extract_first() or ''
                pro_id = pinfo['ProjectID'] = p.xpath('./@id').extract_first() or ''
                pinfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                        pinfo['ProjectName'] + pinfo['ProjectID'])
                result.append(Request(url=get_project_url(pro_id, page_key), dont_filter=True,
                                        meta={'PageType': 'ProjectInfo', 'item': copy.deepcopy(pinfo)}))
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
        if response.meta.get('PageType') not in ('ProjectInfo', ):
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectInfo':
            pinfo = response.meta.get('item')
            if pinfo:
                pinfo['ProjectDevelopCompany'] = (sel.xpath('//strong[text()="开发公司："]/parent::dd[1]/text()').extract_first() or '').strip()
                pinfo['ProjectManageCompany'] = (sel.xpath('//strong[text()="物业管理单位："]/parent::dd[1]/text()').extract_first() or '').strip()
                pinfo['ProjectBuildingArea'] = (sel.xpath('//strong[text()="占地面积："]/parent::dd[1]/text()').extract_first() or '').strip()
                pinfo['ProjectMainStructure'] = (sel.xpath('//strong[text()="主力套型："]/parent::dd[1]/text()').extract_first() or '').strip()
                pinfo['ProjectGreenRatio'] = (sel.xpath('//strong[text()="绿 化 率："]/parent::dd[1]/text()').extract_first() or '').strip()
                pinfo['ProjectPlotRatio'] = (sel.xpath('//strong[text()="容 积 率："]/parent::dd[1]/text()').extract_first() or '').strip()
                pinfo['ProjectTranslateTimes'] = (sel.xpath('//strong[text()="累计换手次数："]/parent::dd[1]/text()').extract_first() or '').strip()
                pinfo['ProjectTranslateRatio'] = (sel.xpath('//strong[text()="累计换手率："]/parent::dd[1]/text()').extract_first() or '').strip()
                pinfo['ProjectDistrict'] = (sel.xpath('//strong[text()="所属区域："]/parent::dd[1]/text()').extract_first() or '').strip()
                pinfo['ProjectAddress'] = (sel.xpath('//strong[text()="项目地址："]/parent::dd[1]/text()').extract_first() or '').strip()
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
        if not(200 <= response.status < 300):  # common case
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
            building_list = sel.xpath('//div[@title="详细信息点击进入"]/a')
            for b in building_list:
                b_info = BuildingInfoItem()
                b_info['ProjectName'] = response.meta.get('item').get('ProjectName')
                b_info['ProjectID'] = response.meta.get('item').get('ProjectID')
                b_info['ProjectUUID'] = response.meta.get('item').get('ProjectUUID')
                b_info['BuildingName'] = (b.xpath('./ul/li[1]/text()').extract_first() or '').replace('栋号：', '')
                b_info['BuildingRegName'] = (b.xpath('./ul/li[2]/text()').extract_first() or '').replace('许可证号：', '')
                b_info['BuildingFloorAbove'] = (b.xpath('./ul/li[3]/text()').extract_first() or '').replace('地上楼层：', '')
                b_info['BuildingFloorBelow'] = (b.xpath('./ul/li[4]/text()').extract_first() or '').replace('地下楼层：', '')
                b_info['BuildingHouseNum'] = (b.xpath('./ul/li[1]/span/text()').extract_first() or '').replace('住宅：', '')
                b_info['BuildingBusiness'] = (b.xpath('./ul/li[2]/span/text()').extract_first() or '').replace('商业：', '')
                b_info['BuildingOfficeNum'] = (b.xpath('./ul/li[3]/span/text()').extract_first() or '').replace('办公：', '')
                b_info['BuildingOtherNum'] = (b.xpath('./ul/li[4]/span/text()').extract_first() or '').replace('其它：', '')
                b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                str(b_info['ProjectUUID']) + b_info['BuildingName'] + b_info['BuildingRegName'])
                b_info['BuildingURL'] = building_url = urlparse.urljoin(response.url, b.xpath('./@href').extract_first())
                result.append(Request(url=building_url, dont_filter=True,
                                        meta={'PageType': 'BuildingInfo', 'item': copy.deepcopy(b_info)}))
        elif response.meta.get('PageType') == 'BuildingInfo':
            b_info = copy.deepcopy(response.meta.get('item'))
            if b_info:
                b_info['BuildingAreaCode'] = sel.xpath('//p[text()="土地使用权证："]/span/text()').extract_first() or ''
                b_info['BuildingPlanCode'] = sel.xpath('//p[text()="规划许可证："]/span/text()').extract_first() or ''
                b_info['BuildingStructure'] = sel.xpath('//p[text()="建筑结构："]/span/text()').extract_first() or ''
                b_info['BuildingUsage'] = sel.xpath('//p[text()="用途："]/span/text()').extract_first() or ''
                b_info['BuildingDesignCompany'] = sel.xpath('//p[text()="设计单位："]/span/text()').extract_first() or ''
                b_info['BuildingPreSellArea'] = sel.xpath('//p[text()="预售许可面积："]/span/text()').extract_first() or ''
                b_info['BuildingOnlineSellArea'] = sel.xpath('//p[text()="网上销售总面积："]/span/text()').extract_first() or ''
                b_info['BuildingOpenDate'] = sel.xpath('//p[text()="开盘日期："]/span/text()').extract_first() or ''
                b_info['BuildingCompleteDate'] = sel.xpath('//p[text()="竣工日期："]/span/text()').extract_first() or ''
                b_info['BuildingDeliverDate'] = sel.xpath('//p[text()="交付日期："]/span/text()').extract_first() or ''
                b_info['BuildingAgent'] = sel.xpath('//p[text()="代理销售企业："]/span/text()').extract_first() or ''
                b_info['BuildingSellPhone'] = sel.xpath('//p[text()="销售电话："]/span/text()').extract_first() or ''
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
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseInfo', 'HouseInfoTmp', 'HouseInfoDetail'):
            if result:
                return result
            return []
        print('HouseInfoHandleMiddleware')

        if response.meta.get('PageType') == 'HouseInfo':
            sel = Selector(response)
            if (not response.meta.get('ProjectName')) or (not response.meta.get('BuildingName'))\
            or (not response.meta.get('ProjectUUID')) or (not response.meta.get('BuildingUUID')):
                if result:
                    return result
                return []
            house_floor_list = sel.xpath('//tr[td[@class="cursor"]]')
            for floor_tr in house_floor_list:
                floor_num = (floor_tr.xpath('.//td[contains(text(), "层")]/text()').extract_first() or '').strip().replace('层：', '')
                houseinfodetail_list = sel.xpath('./td[@class="cursor"]')
                for house in houseinfodetail_list:
                    hinfo = HouseInfoItem()
                    hinfo['ProjectName'] = response.meta.get('ProjectName')
                    hinfo['BuildingName'] = response.meta.get('BuildingName')
                    hinfo['ProjectUUID'] = response.meta.get('ProjectUUID')
                    hinfo['BuildingUUID'] = response.meta.get('BuildingUUID')
                    hinfo['HouseID'] = (house.xpath('./@onclick').extract_first() or '').replace("s('", '').replace("')", '')
                    hinfo['HouseFloor'] = floor_num
                    houseinfo_tmp_url = get_house_info_url(hinfo['HouseID'])
                    result.append(Request(url=houseinfo_tmp_url, dont_filter=True,
                                            meta={'PageType': 'HouseInfoTmp', 'item': copy.deepcopy(hinfo)}))

        elif response.meta.get('PageType') == 'HouseInfoTmp':
            houseinfodetail_url = 'http://real.hffd.gov.cn/details/house/' + json.loads(response.body_as_unicode())['id']
            result.append(Request(url=houseinfodetail_url, dont_filter=True,
                                    meta={'PageType': 'HouseInfoDetail', 'item': copy.deepcopy(response.meta.get('item'))}))
        elif response.meta.get('PageType') == 'HouseInfoDetail':
            house_info_dict = json.loads(response.body_as_unicode())
            hinfo = response.meta.get('item')
            if hinfo:
                hinfo['HouseName'] = house_info_dict.get('data').get('strTitle')
                hinfo['HouseStructure'] = house_info_dict.get('data').get('lbStructure')
                hinfo['HouseType'] = house_info_dict.get('data').get('lbHouseType')
                hinfo['HouseShareArea'] = house_info_dict.get('data').get('lbJoinArea')
                hinfo['HouseNum'] = house_info_dict.get('data').get('lbPartNO')
                hinfo['HouseBuildingArea'] = house_info_dict.get('data').get('lbBuildArea')
                hinfo['HouseAddress'] = house_info_dict.get('data').get('lbLocation')
                hinfo['HouseSaleState'] = house_info_dict.get('data').get('lbSellFlag')
                hinfo['HousePreSellPrice'] = house_info_dict.get('data').get('iPrice')
                hinfo['HouseUsage'] = house_info_dict.get('data').get('lbHouseUsefulness')
                hinfo['HouseInnerArea'] = house_info_dict.get('data').get('lbInsideArea')
                hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                        str(hinfo['ProjectUUID']) + str(hinfo['BuildingUUID']) + hinfo['HouseName'])
                result.append(hinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
