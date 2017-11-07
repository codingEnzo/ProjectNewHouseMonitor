# coding = utf-8
import sys
import uuid
import copy
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsDGFC import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


class ProjectBaseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    headers = {'Host': 'dgfc.dg.gov.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://www.bjjs.gov.cn',
                'Upgrade-Insecure-Requests': 1,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'}

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
            req_dict = {'__VIEWSTATE': '',
                        '__EVENTVALIDATION': '',
                        'townName': '',
                        'usage': '',
                        'projectName': '',
                        'projectSite': '',
                        'developer': '',
                        'area1': '',
                        'area2': '',
                        'resultCount': '',
                        'pageIndex': ''}
            base_sel = Selector(response)
            req_dict['__VIEWSTATE'] = base_sel.xpath('//input[@id="__VIEWSTATE"]/@value').\
                                        extract_first() or ""
            req_dict['__EVENTVALIDATION'] = base_sel.xpath('//input[@id="__EVENTVALIDATION"]/@value').\
                                                extract_first() or ""
            req_dict['resultCount'] = base_sel.xpath('//input[@id="resultCount"]/@value').\
                                                extract_first() or "60"
            req_dict['pageIndex'] = base_sel.xpath('//input[@id="pageIndex"]/@value').\
                                                extract_first() or "0"
            for town_info in base_sel.xpath('//select[@id="townName"]/option'):
                pb = ProjectBaseItem()
                pb['ProjectDistrict'] = (town_info.xpath('./text()').extract_first() or '').replace('东莞市', '')
                req_dict['townName'] = town_info.xpath('./@value').extract_first() or ''
                req_body = urlparse.urlencode(req_dict)
                result.append(Request(url=response.url, body=req_body, method='POST',
                                headers=self.headers, meta={'PageType': 'ProjectBase', 'item': pb}))
        elif response.request.method == 'POST':
            print('current area', Selector(response).xpath('//select[@selected="selected"/text()').extract_first())
            project_list = Selector(response).xpath('//tr[@class!="tHead"]')
            for p in project_list:
                p_name = p.xpath('./td[1]/a/text()').extract_first()
                p_href = urlparse.urljoin(response.url, p.xpath('./td[1]/a/@href').extract_first())
                p_address = p.xpath('./td[2]/a/text()').extract_first() or ''
                p_salenum = p.xpath('./td[3]/a/text()').extract_first() or '0'
                pb = copy.deepcopy(response.meta.get('item') or ProjectBaseItem())
                pb['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + p_href)
                pb['ProjectName'] = p_name
                pb['ProjectURL'] = p_href
                pb['ProjectAddress'] = p_address
                pb['ProjectSaleSum'] = p_salenum
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

    headers = {'Host': 'dgfc.dg.gov.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://www.bjjs.gov.cn',
                'Upgrade-Insecure-Requests': 1,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'}

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
            iframe_src = urlparse.urljoin(response.url,
                                Selector(response).xpath('//div[@id="content_3"]/div/iframe/@src').extract_first() or '')
            req = Request(url=iframe_src, meta={'PageType': 'ProjectDetailInfo', 'CurURL': response.url}, method='GET', dont_filter=True)
            result.append(req)
        elif response.meta.get('PageType') == 'ProjectDetailInfo':
            info_sel = Selector(response)
            pinfo = ProjectInfoItem()
            pinfo['ProjectName'] = info_sel.xpath('//span[@id="Projectname1"]/text()').extract_first() or ''
            pinfo['ProjectAddress'] = info_sel.xpath('//span[@id="Address"]/text()').extract_first() or ''
            pinfo['ProjectUsage'] = info_sel.xpath('//span[@id="yongtu"]/text()').extract_first() or ''
            pinfo['ProjectArea'] = info_sel.xpath('//span[@id="Totalarea"]/text()').extract_first() or ''
            pinfo['ProjectHouseNum'] = info_sel.xpath('//span[@id="TotalRoom"]/text()').extract_first() or ''
            pinfo['ProjectCompany'] = info_sel.xpath('//span[@id="Companyname"]/text()').extract_first() or ''
            pinfo['ProjectCorporation'] = info_sel.xpath('//span[@id="MBR2"]/text()').extract_first() or ''
            pinfo['ProjectRegName'] = info_sel.xpath('//span[@id="YsZheng"]/text()').extract_first() or ''
            pinfo['ProjectAreaPlanLicenseCode'] = info_sel.xpath('//span[@id="JiansheZheng"]/text()').extract_first() or ''
            pinfo['ProjectPlanLicenseCode'] = info_sel.xpath('//span[@id="JiansheZheng2"]/text()').extract_first() or ''
            pinfo['ProjectConstructionLicenseCode'] = info_sel.xpath('//span[@id="JiansheZheng3"]/text()').extract_first() or ''
            pinfo['ProjectConstructionCompany'] = info_sel.xpath('//span[@id="Shigong"]/text()').extract_first() or ''
            pinfo['ProjectAuthenticFlag'] = info_sel.xpath('//span[@id="lm"]/text()').extract_first() or ''
            pinfo['ProjectSaleArea'] = info_sel.xpath('//span[@id="KeArea"]/text()').extract_first() or '0.0'
            pinfo['ProjectSaleNum'] = info_sel.xpath('//span[@id="KeRoom"]/text()').extract_first() or '0'
            pinfo['ProjectSaledArea'] = info_sel.xpath('//span[@id="YiArea"]/text()').extract_first() or '0.0'
            pinfo['ProjectSaledNum'] = info_sel.xpath('//span[@id="YiRoom"]/text()').extract_first() or '0'
            pinfo['ProjectUnavailableArea'] = info_sel.xpath('//span[@id="NoArea"]/text()').extract_first() or '0.0'
            pinfo['ProjectUnavailableNum'] = info_sel.xpath('//span[@id="NoRoom"]/text()').extract_first() or '0'
            pinfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, pinfo['ProjectName'] + response.meta.get('CurURL') or '')
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

    headers = {'Host': 'dgfc.dg.gov.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://www.bjjs.gov.cn',
                'Upgrade-Insecure-Requests': 1,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'}

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
        print('BuildingListHandleMiddleware')

        building_base_sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectInfo':
            p_name = building_base_sel.xpath('//div[@id="content_1"]/div[3]/text()').extract()[2].strip()
            for building_info in building_base_sel.xpath('//table[@id="houseTable_1"]/tr[@class!="tHead"]'):
                b_info = BuildingInfoItem()
                b_info['ProjectName'] = p_name
                b_info['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + response.url)
                b_info['ProjectRegName'] = building_info.xpath('./td[1]/a/text()').extract_first() or ''
                b_info['BuildingName'] = building_info.xpath('./td[2]/a/text()').extract_first() or ''
                b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + response.url + b_info['ProjectRegName'] + b_info['BuildingName'])
                b_info['BuildingFloorNum'] = building_info.xpath('./td[3]/a/text()').extract_first() or '0'
                b_info['BuildingHouseNum'] = building_info.xpath('./td[4]/a/text()').extract_first() or '0'
                b_info['BuildingUsage'] = building_info.xpath('./td[5]/a/text()').extract_first() or ''
                b_info['BuildingSaleArea'] = building_info.xpath('./td[6]/a/text()').extract_first() or '0.0'
                b_info['BuildingURL'] = urlparse.urljoin(response.url, p.xpath('./td[1]/a/@href').extract_first())
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

    headers = {'Host': 'www.bjjs.gov.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://www.bjjs.gov.cn',
                'Upgrade-Insecure-Requests': 1,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'}

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        def get_house_state(string):
            STATE_TAB = {'unsaleable': '不可售',
                            'saleable': '可售',
                            'sold': '已售',
                            'forSale': '待售'}
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
            floor_list = Selector(response).xpath('//table[@id="roomTable"]/tr[position()>1]')
            for floor_item in floor_list:
                cur_floor = floor_item.xpath('./td[1]/text()').extract_first() or '0'
                house_list = floor_item.xpath('./td[2]/table/tr/td[@class]')
                for house_item in house_list:
                    hinfo = HouseInfoItem()
                    hinfo['ProjectName'] = response.meta.get('ProjectName')
                    hinfo['BuildingName'] = response.meta.get('BuildingName')
                    hinfo['ProjectUUID'] = response.meta.get('ProjectUUID')
                    hinfo['BuildingUUID'] = response.meta.get('BuildingUUID')
                    hinfo['HouseName'] = house_item.xpath('./text()').extract_first() or\
                                            house_item.xpath('./a/text()').extract_first() or ''
                    hinfo['HouseFloor'] = cur_floor
                    hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                    hinfo['BuildingUUID'] + hinfo['HouseName'] + hinfo['HouseFloor'])
                    hinfo['HouseState'] = get_house_state(house_item.xpath('./@class').extract_first())
                    if not house_item.xpath('./a/@href').extract_first():
                        result.append(hinfo)
                    else:
                        houseinfodetail_href = urlparse.urljoin(response.url,
                                                house_item.xpath('./a/@href').extract_first())
                        houseinfodetail_req = Request(url=houseinfodetail_href, method='GET',
                                                        headers=self.headers, meta={'PageType': 'HouseInfoDetail', 'item': hinfo})
                        result.append(houseinfodetail_req)

        if response.meta.get('PageType') == 'HouseInfoDetail':
            hinfo = response.meta.get('item')
            houseinfodetail_sel = Selector(response).xpath('//div[@class="content"]/table')
            hinfo['HouseRecordState'] = (houseinfodetail_sel.xpath('./tr[3]/td[2]/text()').extract_first() or '').strip()
            hinfo['HousePledgeState'] = (houseinfodetail_sel.xpath('./tr[4]/td[2]/text()').extract_first() or '').strip()
            hinfo['HouseAttachState'] = (houseinfodetail_sel.xpath('./tr[5]/td[2]/text()').extract_first() or '').strip()
            hinfo['HouseUsage'] = (houseinfodetail_sel.xpath('./tr[2]/td[2]/text()').extract_first() or '').strip()
            hinfo['HouseBuildingArea'] = (houseinfodetail_sel.xpath('./tr[2]/td[4]/text()').extract_first() or '').replace('平方米', '').strip()
            hinfo['HouseInnerArea'] = (houseinfodetail_sel.xpath('./tr[3]/td[4]/text()').extract_first() or '').replace('平方米', '').strip()
            hinfo['HouseShareArea'] = (houseinfodetail_sel.xpath('./tr[4]/td[4]/text()').extract_first() or '').replace('平方米', '').strip()
            hinfo['HouseUnitPrice'] = (houseinfodetail_sel.xpath('./tr[6]/td[4]/text()').extract_first() or '').replace('元', '').strip()
            hinfo['HousePrice'] = (houseinfodetail_sel.xpath('./tr[5]/td[4]/text()').extract_first() or '').replace('元', '').strip()
            hinfo['HousePriceFlag'] = False
            result.append(hinfo)

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
