# coding = utf-8
import re
import sys
import uuid
import json
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsHY import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse

headers = {'Host': '183.63.60.194:8808',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate',
           'Referer': 'http://183.63.60.194:8808',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': 1
           }


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
        if response.meta.get('PageType') not in ('ProjectBase'):
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        if response.meta.get('PageType') == "ProjectBase":
            project_list = json.loads(response.body_as_unicode()).get('Data')
            for p in project_list:
                pb = ProjectBaseItem()
                pb['SubProjectName'] = p.get('YSXMMC', '')
                pb['SubProjectID'] = p.get('YSXMID', '')
                pb['ProjectName'] = p.get('KFXMMC', '')
                pb['ProjectUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, pb['ProjectName'])
                pb['ProjectDistrict'] = p.get('QXMC', '')
                pb['ProjectOpenDate'] = p.get('KPSJ', '')
                pb['ProjectRegDate'] = p.get('FZSJ', '')
                pb['ProjectRegName'] = p.get('XKZH', '')
                pb['ProjectRegUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, pb['ProjectRegName'])
                pb['ProjectCompany'] = p.get('KFQYMC', '')
                pb['ProjectCompanyUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, pb['ProjectCompany'])
                pb['ProjectURL'] = "http://183.63.60.194:8808/public/web/ysxm?ysxmid=%s" % pb['SubProjectID']
                pb['SubProjectProjectUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, pb['ProjectName'] + pb['SubProjectName'])
                if pb['SubProjectID'] != '':
                    result.append(pb)
                company_url = "http://183.63.60.194:8808/public/web/KfxmList?kfsid=%s" % p.get(
                    'KFQYBM', '')
                result.append(Request(url=company_url,
                                      headers=headers, meta={'PageType': 'CompanyPage'}))
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
        if response.meta.get('PageType') not in ('ProjectInfo', 'ProjectInfoUse'):
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfo':
            pinfo = ProjectInfoItem()
            pinfo['ProjectPlanBuildingArea'] = (response.xpath(
                '//td[text()="预售房屋建筑面积：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or '').replace('平方米', '').strip()
            pinfo['ProjectLandLicense'] = (response.xpath(
                '//td[text()="土地使用证号：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectUsage'] = (response.xpath(
                '//td[text()="土地用途：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            result.append(Request(url=urlparse.urljoin(response.url, response.xpath('//td[@id="PresellName"]/a/@href').extract_first(default='')),
                                  headers=headers, meta={'PageType': 'ProjectInfoUse', 'item': pinfo}))
        elif response.meta.get('PageType') == 'ProjectInfoUse':
            pinfo = response.meta.get('item')
            if pinfo:
                pinfo['ProjectName'] = (response.xpath(
                    '//td[text()="项目名称："]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pinfo['ProjectUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, pinfo['ProjectName'])
                pinfo['ProjectCompany'] = (response.xpath(
                    '//td[text()="开发商："]/following-sibling::td[1]/a/text()').extract_first() or '').strip()
                pinfo['CompanyUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, pinfo['ProjectCompany'])
                pinfo['ProjectAddress'] = (response.xpath(
                    '//td[text()="项目座落："]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pinfo['ProjectBuildingNum'] = str(
                    len(response.xpath('//table[@id="selltable1"]/tr')))
                pinfo['ProjectDistrict'] = (response.xpath(
                    '//td[text()="所在地区："]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pinfo['ProjectBuildingArea'] = (response.xpath(
                    '//td[text()="总建筑面积："]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pinfo['ProjectSaleInfo'] = {
                    '总套数': response.xpath(
                        '//td[text()="总套数："]/following-sibling::td[1]/text()').extract_first() or '',
                    '总面积': response.xpath(
                        '//td[text()="总面积："]/following-sibling::td[1]/text()').extract_first() or '',
                    '住宅套数': response.xpath(
                        '//td[text()="住宅套数："]/following-sibling::td[1]/text()').extract_first() or '',
                    '住宅面积': response.xpath(
                        '//td[text()="住宅面积："]/following-sibling::td[1]/text()').extract_first() or '',
                    '非住宅套数': response.xpath(
                        '//td[text()="非住宅套数："]/following-sibling::td[1]/text()').extract_first() or '',
                    '非住宅面积': response.xpath(
                        '//td[text()="非住宅面积："]/following-sibling::td[1]/text()').extract_first() or '',
                    '已售住宅套数': response.xpath(
                        '//td[text()="已售住宅套数："]/following-sibling::td[1]/text()').extract_first() or '',
                    '已售住宅面积': response.xpath(
                        '//td[text()="已售住宅面积："]/following-sibling::td[1]/text()').extract_first() or '',
                    '剩余住宅套数': response.xpath(
                        '//td[text()="剩余住宅套数："]/following-sibling::td[1]/text()').extract_first() or '',
                    '剩余住宅面积': response.xpath(
                        '//td[text()="剩余住宅面积："]/following-sibling::td[1]/text()').extract_first() or '',
                    '住宅均价': response.xpath(
                        '//td[text()="住宅均价："]/following-sibling::td[1]/text()').extract_first() or '',
                    '非住宅均价': response.xpath(
                        '//td[text()="非住宅均价："]/following-sibling::td[1]/text()').extract_first() or '',
                    '已售非住宅套数': response.xpath(
                        '//td[text()="已售非住宅套数："]/following-sibling::td[1]/text()').extract_first() or '',
                    '合同撤销次数': response.xpath(
                        '//td[text()="合同撤销次数："]/following-sibling::td[1]/text()').extract_first() or ''}
                result.append(pinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class CompanyInfoHandleMiddleware(object):
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
        if response.meta.get('PageType') not in ('CompanyPage',):
            if result:
                return result
            return []
        print('CompanyInfoHandleMiddleware')

        if response.meta.get('PageType') == 'CompanyPage':
            cinfo = CompanyInfoItem()
            cinfo['CompanyName'] = response.xpath(
                '//td[text()="开发商名称：\xa0\xa0\xa0"]/following-sibling::td[1]/a/text()').extract_first() or ''
            cinfo['CompanyUUID'] = uuid.uuid3(
                uuid.NAMESPACE_DNS, cinfo['CompanyName'])
            cinfo['CompanyAddress'] = response.xpath(
                '//td[text()="企业地址：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyRegName'] = response.xpath(
                '//td[text()="营业执照号：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyDeveloperRegName'] = response.xpath(
                '//td[text()="开发商登记号：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyRegDate'] = response.xpath(
                '//td[text()="登记日期：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyLevelLicense'] = response.xpath(
                '//td[text()="开发商资质证书号：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyRegCapital'] = response.xpath(
                '//td[text()="注册资金（万元）：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyLevel'] = response.xpath(
                '//td[text()="开发商资质等级：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyType'] = response.xpath(
                '//td[text()="企业性质：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyConnect'] = response.xpath(
                '//td[text()="联系人：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyPhone'] = response.xpath(
                '//td[text()="联系电话：\xa0\xa0\xa0"]/following-sibling::td[1]/text()').extract_first() or ''
            result.append(cinfo)
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
        if response.meta.get('PageType') not in ('ProjectInfo'):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfo':
            b_sell_list = response.xpath(
                '//table[@id="table33"]/tr[position()>1]')
            for b in b_sell_list:
                binfo = BuildingInfoItem()
                binfo['ProjectName'] = response.xpath(
                    '//td[@id="PresellName"]/a/text()').extract_first() or ''
                binfo['ProjectUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, binfo['ProjectName'])
                binfo['BuildingName'] = (b.xpath('./td[1]/text()').extract_first() or '') + (
                    b.xpath('./td[3]/text()').extract_first() or '')
                binfo['BuildingAddress'] = b.xpath(
                    './td[2]/text()').extract_first() or ''
                binfo['BuildingFloorNum'] = b.xpath(
                    './td[4]/text()').extract_first() or ''
                binfo['BuildingURL'] = urlparse.urljoin(
                    response.url, b.xpath('./td[5]/a/@href').extract_first() or '')
                binfo['BuildingUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, binfo['BuildingName'])
                result.append(binfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class PreSellInfoHandleMiddleware(object):
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

        def get_presell_num1(string):
            house_num = '0'
            match_num = re.search(r'(\d+)套', string)
            if match_num:
                house_num = match_num.group(1)
            return house_num

        def get_presell_num2(string):
            area_num = '0'
            house_num = '0'
            match_num = re.search(r'([\d\.]+).*平方米 +(\d+).*套', string)
            if match_num:
                area_num = match_num.group(1)
                house_num = match_num.group(2)
            return (area_num, house_num)

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfo', 'PreSellInfo'):
            if result:
                return result
            return []
        print('PreSellInfoHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfo':
            preinfo = PreSellInfoItem()
            preinfo['PreRegName'] = response.xpath(
                '//td[@id="bookid"]/a/text()').extract_first() or ''
            preinfo['PreRegUUID'] = uuid.uuid3(
                uuid.NAMESPACE_DNS, preinfo['PreRegName'])
            preinfo['PreHouseArea'] = (response.xpath(
                '//td[@id="PresellArea"]/text()').extract_first() or '').replace('平方米', '').strip()
            preinfo['PreHouseNum'] = get_presell_num1(response.xpath(
                '//td[@id="djrqtd"]/text()').extract_first() or '')
            preinfo['PreLandLicense'] = response.xpath(
                '//td[@id="landinfo"]/text()').extract_first() or ''
            preinfo['PreLandUsage'] = response.xpath(
                '//td[@id="zczjtd"]/text()').extract_first() or ''
            preinfo['PreLimitDate'] = response.xpath(
                '//td[@id="FZDatebegin"]/text()').extract_first() or ''
            preinfo['PreDistrict'] = response.xpath(
                '//td[@id="FQ"]/text()').extract_first() or ''
            preinfo['PreOpenDate'] = response.xpath(
                '//td[@id="kpdate"]/text()').extract_first() or ''
            preinfo['PreBankList'] = []
            bank_list = response.xpath(
                '//table[@id="banktable"]/tr[@bgcolor="#f5f5f5"]')
            for bank in bank_list:
                preinfo['PreBankList'].append({'BankName': bank.xpath('./td[1]/text()').extract_first() or '',
                                               'BankAcount': bank.xpath('./td[2]/text()').extract_first() or '',
                                               'BankPhone': bank.xpath('./td[3]/text()').extract_first() or ''})
            preinfo_url = urlparse.urljoin(response.url, response.xpath(
                '//td[@id="bookid"]/a/@href').extract_first() or '')
            result.append(Request(url=preinfo_url, headers=headers, meta={
                          'PageType': 'PreSellInfo', 'item': preinfo}))
        elif response.meta.get('PageType') == 'PreSellInfo':
            preinfo = response.meta.get('item')
            if preinfo:
                preinfo['PreInfoDetail'] = {'House': {
                    'Area': get_presell_num2(response.xpath('//font[@id="zhuzhai"]/text()').extract_first() or '')[0],
                    'Num': get_presell_num2(response.xpath('//font[@id="zhuzhai"]/text()').extract_first() or '')[1]
                },
                    'Buisiness': {
                    'Area': get_presell_num2(response.xpath('//font[@id="businesshouse"]/text()').extract_first() or '')[0],
                    'Num': get_presell_num2(response.xpath('//font[@id="businesshouse"]/text()').extract_first() or '')[1]
                },
                    'Office': {
                    'Area': get_presell_num2(response.xpath('//font[@id="Officestatistics"]/text()').extract_first() or '')[0],
                    'Num': get_presell_num2(response.xpath('//font[@id="Officestatistics"]/text()').extract_first() or '')[1]
                },
                    'Other': {
                    'Area': get_presell_num2(response.xpath('//font[@id="others"]/text()').extract_first() or '')[0],
                    'Num': get_presell_num2(response.xpath('//font[@id="others"]/text()').extract_first() or '')[1]
                }}
                result.append(preinfo)
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

        def get_house_list_str(string):
            list_str = ''
            match_list = re.search(r"var _table_html_ = '(.+)'", string)
            if match_list:
                list_str = match_list.group(1)
            return list_str

        def get_house_state(string):
            STATE_TAB = {'red': '不可售（因超建、查封、物业用房、回迁安置等原因）',
                         'black': '可售',
                         '#00CC00': '已售',
                         'blue': '已被开发企业抵押给金融机构，暂不可售'}
            state = ''
            for key in STATE_TAB:
                if key in string:
                    state = STATE_TAB[key]
                    break
            return state

        result = list(result)
        print(response.status, response.url, response.meta.get('PageType'))
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
            floor_list = Selector(text=get_house_list_str(
                response.body_as_unicode())).xpath('//tr[@bgcolor="#FFFFFF"]')
            for floor in floor_list:
                cur_floor = floor.xpath('./td[1]/text()').extract_first() or ''
                house_list = floor.xpath('./td[2]/table/tr/td')
                for house in house_list:
                    hinfo = HouseInfoItem()
                    hinfo['ProjectName'] = response.meta.get(
                        'ProjectName') or ''
                    hinfo['BuildingName'] = response.meta.get(
                        'BuildingName') or ''
                    hinfo['ProjectUUID'] = response.meta.get(
                        'ProjectUUID') or ''
                    hinfo['BuildingUUID'] = response.meta.get(
                        'BuildingUUID') or ''
                    hinfo['HouseName'] = house.xpath(
                        './a/font/text()').extract_first() or ''
                    hinfo['HouseSaleState'] = house.xpath(
                        './table/tr/td/a/font/text()').extract_first() or ''
                    hinfo['HouseFloor'] = cur_floor
                    hinfo_url = urlparse.urljoin(response.url, house.xpath(
                        './table/tr/td/a/@href').extract_first() or '')
                    hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, hinfo[
                                                    'HouseName'] + hinfo_url)
                    result.append(Request(url=hinfo_url, method='GET',
                                          headers=headers, meta={'PageType': 'HouseInfoDetail', 'item': hinfo}))
        elif response.meta.get('PageType') == 'HouseInfoDetail':
            hinfo = response.meta.get('item')
            if hinfo:
                hinfo['HouseInnerArea'] = (response.xpath(
                    '//td[@id="HouseArea"]/text()').extract_first() or '').replace('m', '').strip()
                hinfo['HouseBuildingArea'] = (response.xpath(
                    '//td[@id="SumBuildArea1"]/text()').extract_first() or '').replace('m', '').strip()
                hinfo['HouseUsage'] = (response.xpath(
                    '//td[@id="HouseUse"]/text()').extract_first() or '').strip()
                hinfo['HouseRegUnitPrice'] = (response.xpath(
                    '//td[@id="sbdj"]/text()').extract_first() or '').replace('元/m', '').replace(',', '').strip()
                hinfo['HouseRegTotalPrice'] = (response.xpath(
                    '//td[@id="sbzj"]/text()').extract_first() or '').replace('元', '').replace(',', '').strip()
                hinfo['HouseDealUnitPrice'] = (response.xpath(
                    '//td[@id="Housedj"]/text()').extract_first() or '').replace('元/m', '').replace(',', '').strip()
                hinfo['HouseDealTotalPrice'] = (response.xpath(
                    '//td[@id="HouseWorth"]/text()').extract_first() or '').replace('元', '').replace(',', '').strip()
                hinfo['HouseOrientation'] = (response.xpath(
                    '//td[@id="CHX"]/text()').extract_first() or '').strip()
                hinfo['HouseVisaDate'] = (response.xpath(
                    '//td[@id="VisaDate"]/text()').extract_first() or '').strip()
                hinfo['HouseManageCompany'] = (response.xpath(
                    '//td[@id="ManagerCom"]/text()').extract_first() or '').strip()
                hinfo['HouseManagePrice'] = (response.xpath(
                    '//td[@id="ManagerCharge"]/text()').extract_first() or '').replace('元/月*m', '').strip()
                result.append(hinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
