# coding = utf-8
import re
import sys
import uuid
import copy
import datetime
from scrapy import Request
from HouseNew.models import *
from HouseCrawler.Items.ItemsZQ import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


headers = {'Host': '61.146.213.163',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': 1,
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Referer': 'http://61.146.213.163:8011/',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cookie': 'ASP.NET_SessionId=ib5doi554mnu3g550vvattmf;'}


class ProjectIndexHandleMiddleware(object):
    """docstring for ProjectIndexHandleMiddleware"""

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not(200 <= response.status < 303):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectBaseUse',):
            if result:
                return result
            return []
        print('ProjectIndexHandleMiddleware')

        index_info = IndexInfoItem()
        index_info['District'] = response.xpath(
            '//span[@id="townentry"]/a[@style="font-weight:bold"]/text()').extract_first(default='').strip()
        index_info['Date'] = str(datetime.datetime.now().date())
        index_info['HouseSaleInfo'] = {'成交套数（套）': response.xpath('//table[@id="indextable1"]/tr[2]/td[2]/text()').extract_first('0').replace('--', '0').strip(),
                                       '成交面积（m2）': response.xpath('//table[@id="indextable1"]/tr[3]/td[2]/text()').extract_first('0.0').replace('--', '0.0').strip(),
                                       '成交均价（元/m2）': response.xpath('//table[@id="indextable1"]/tr[4]/td[2]/text()').extract_first('0.0').replace('--', '0.0').strip(),
                                       '成交总额（元）': response.xpath('//table[@id="indextable1"]/tr[5]/td[2]/text()').extract_first('0').replace('--', '0').strip()}
        index_info['OfficeSaleInfo'] = {'成交套数（套）': response.xpath('//table[@id="indextable1"]/tr[2]/td[3]/text()').extract_first('0').replace('--', '0').strip(),
                                        '成交面积（m2）': response.xpath('//table[@id="indextable1"]/tr[3]/td[3]/text()').extract_first('0.0').replace('--', '0.0').strip(),
                                        '成交均价（元/m2）': response.xpath('//table[@id="indextable1"]/tr[4]/td[3]/text()').extract_first('0.0').replace('--', '0.0').strip(),
                                        '成交总额（元）': response.xpath('//table[@id="indextable1"]/tr[5]/td[3]/text()').extract_first('0').replace('--', '0').strip()}
        index_info['BussinessSaleInfo'] = {'成交套数（套）': response.xpath('//table[@id="indextable1"]/tr[2]/td[4]/text()').extract_first('0').replace('--', '0').strip(),
                                           '成交面积（m2）': response.xpath('//table[@id="indextable1"]/tr[3]/td[4]/text()').extract_first('0.0').replace('--', '0.0').strip(),
                                           '成交均价（元/m2）': response.xpath('//table[@id="indextable1"]/tr[4]/td[4]/text()').extract_first('0.0').replace('--', '0.0').strip(),
                                           '成交总额（元）': response.xpath('//table[@id="indextable1"]/tr[5]/td[4]/text()').extract_first('0').replace('--', '0').strip()}
        index_info['OtherSaleInfo'] = {'成交套数（套）': response.xpath('//table[@id="indextable1"]/tr[2]/td[5]/text()').extract_first('0').replace('--', '0').strip(),
                                       '成交面积（m2）': response.xpath('//table[@id="indextable1"]/tr[3]/td[5]/text()').extract_first('0.0').replace('--', '0.0').strip(),
                                       '成交均价（元/m2）': response.xpath('//table[@id="indextable1"]/tr[4]/td[5]/text()').extract_first('0.0').replace('--', '0.0').strip(),
                                       '成交总额（元）': response.xpath('//table[@id="indextable1"]/tr[5]/td[5]/text()').extract_first('0').replace('--', '0').strip()}
        index_info['AllSaleInfo'] = {'成交套数（套）': response.xpath('//table[@id="indextable1"]/tr[2]/td[6]/text()').extract_first('0').replace('--', '0').strip(),
                                     '成交面积（m2）': response.xpath('//table[@id="indextable1"]/tr[3]/td[6]/text()').extract_first('0.0').replace('--', '0.0').strip(),
                                     '成交均价（元/m2）': response.xpath('//table[@id="indextable1"]/tr[4]/td[6]/text()').extract_first('0.0').replace('--', '0.0').strip(),
                                     '成交总额（元）': response.xpath('//table[@id="indextable1"]/tr[5]/td[6]/text()').extract_first('0').replace('--', '0').strip()}
        result.append(index_info)
        return result


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
        if not(200 <= response.status < 303):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectBase', 'ProjectBaseUse', 'ProjectPage', 'ProjectList'):
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware', response.meta.get('PageType'))

        if response.meta.get('PageType') == "ProjectBase":
            result.append(Request(url=response.url,
                                  headers=headers, meta={'PageType': 'ProjectBaseUse'}))
        elif response.meta.get('PageType') == "ProjectBaseUse":
            p_page_base_url = response.xpath(
                '//div[@id="frame"]/iframe/@src').extract_first()
            if p_page_base_url:
                result.append(Request(url=urlparse.urljoin(response.url, p_page_base_url),
                                      headers=headers, meta={'PageType': 'ProjectPage'}))
        elif response.meta.get('PageType') == "ProjectPage":
            page_list = [urlparse.urljoin(response.url, path) for path in response.xpath(
                '//td[@id="pagetd"]/a[not (@title)]/@href').extract()]
            page_list.append(response.url)
            for page_url in page_list:
                result.append(Request(url=page_url,
                                      headers=headers, meta={'PageType': 'ProjectList'}))
            page_10_next_path = response.xpath(
                '//td[@id="pagetd"]/a[@title="下十页"]/@href').extract_first()
            if page_10_next_path:
                page_10_next_url = urlparse.urljoin(
                    response.url, page_10_next_path)
                result.append(Request(url=page_10_next_url,
                                      headers=headers, meta={'PageType': 'ProjectPage'}))
        elif response.meta.get('PageType') == "ProjectList":
            project_list = response.xpath(
                '//table[@id="listtable"]/tr[not (@id)]')
            for p in project_list:
                pb = ProjectBaseItem()
                pb['ProjectName'] = p.xpath(
                    './td[1]/a/text()').extract_first() or ''
                pb['ProjectAddress'] = p.xpath(
                    './td[2]/text()').extract_first() or ''
                pb['ProjectDistrict'] = p.xpath(
                    './td[3]/text()').extract_first() or ''
                pb['ProjectURL'] = (urlparse.urljoin(
                    response.url, p.xpath('./td[1]/a/@href').extract_first() or '')).replace(' ', '').strip()
                pb['ProjectUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, pb['ProjectName'] + pb['ProjectURL'])
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
        if not(200 <= response.status < 303):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfo', 'ProjectInfoUse'):
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfo':
            meta = copy.deepcopy(response.meta)
            meta['PageType'] = 'ProjectInfoUse'
            result.append(Request(url=response.url,
                                  headers=headers, meta=meta))
        elif response.meta.get('PageType') == 'ProjectInfoUse':
            pinfo = ProjectInfoItem()
            pinfo['ProjectName'] = response.meta.get('ProjectName', '')
            pinfo['ProjectUUID'] = response.meta.get('ProjectUUID', '')
            pinfo['ProjectCompany'] = response.xpath(
                '//td[text()="开发商名称："]/following-sibling::td[1]/a/text()').extract_first() or ''
            pinfo['CompanyUUID'] = uuid.uuid3(
                uuid.NAMESPACE_DNS, pinfo['ProjectCompany'])
            pinfo['ProjectAddress'] = response.xpath(
                '//td[text()="项目座落："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectBuildingNum'] = response.xpath(
                '//td[text()="栋数："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectDistrict'] = response.xpath(
                '//td[text()="所在地区："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectEngPlanLicense'] = (response.xpath(
                '//td[text()="建设工程规划许可证号："]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectPlanBuildingArea'] = (response.xpath(
                '//td[text()="规划建筑面积："]/following-sibling::td[1]/text()').extract_first() or '').replace('m', '').strip()
            pinfo['ProjectLandLicense'] = response.xpath(
                '//td[text()="土地证号："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectLandArea'] = (response.xpath(
                '//td[text()="土地使用权面积："]/following-sibling::td[1]/text()').extract_first() or '').replace('m', '').strip()
            pinfo['ProjectLandYearLimit'] = response.xpath(
                '//td[text()="土地使用期限："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectUsage'] = response.xpath(
                '//td[text()="地类(用途)："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectEngBuildingLicense'] = response.xpath(
                '//td[text()="建筑工程施工许可证号："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectBuildingArea'] = response.xpath(
                '//td[text()="施工面积："]/following-sibling::td[1]/text()').extract_first() or ''
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
        if not(200 <= response.status < 303):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfoUse',):
            if result:
                return result
            return []
        print('CompanyInfoHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfoUse':
            cinfo = CompanyInfoItem()
            cinfo['CompanyName'] = response.xpath(
                '//td[text()="开发商名称："]/following-sibling::td[1]/a/text()').extract_first() or ''
            cinfo['CompanyUUID'] = uuid.uuid3(
                uuid.NAMESPACE_DNS, cinfo['CompanyName'])
            cinfo['CompanyAddress'] = response.xpath(
                '//td[text()="企业地址："]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyRegName'] = response.xpath(
                '//td[text()="营业执照注册号："]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyDeveloperRegName'] = response.xpath(
                '//td[text()="开发商登记号："]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyRegDate'] = response.xpath(
                '//td[text()="登记日期："]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyLevelLicense'] = response.xpath(
                '//td[text()="开发商资质证书号："]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyRegCapital'] = response.xpath(
                '//td[text()="注册资金（万元）："]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyLevel'] = response.xpath(
                '//td[text()="开发商资质等级："]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyType'] = response.xpath(
                '//td[text()="企业性质："]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyConnect'] = response.xpath(
                '//td[text()="联系人："]/following-sibling::td[1]/text()').extract_first() or ''
            cinfo['CompanyPhone'] = response.xpath(
                '//td[text()="联系电话："]/following-sibling::td[1]/text()').extract_first() or ''
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
        if not(200 <= response.status < 303):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfoUse', 'BuildingPreSell'):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfoUse':
            b_sell_list = response.xpath(
                '//table[@id="selltable1" or @id="selltable2"]/tr[position()>1]')
            b_presell_list = response.xpath(
                '//table[contains(@id, "preselltable")]/tr[position()>1]')
            for b in b_sell_list:
                binfo = BuildingInfoItem()
                binfo['ProjectName'] = response.meta.get('ProjectName', '')
                binfo['ProjectUUID'] = response.meta.get('ProjectUUID', '')
                binfo['BuildingName'] = b.xpath(
                    './td[2]/text()').extract_first() or ''
                binfo['BuildingRegName'] = b.xpath(
                    './td[1]/text()').extract_first() or b.xpath('./td[1]/a/@title').extract_first() or ""
                binfo['BuildingRegUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, binfo['BuildingRegName']) if binfo['BuildingRegName'] != "" else binfo['BuildingRegName']
                binfo['BuildingURL'] = (urlparse.urljoin(
                    response.url, b.xpath('./td[4]/a/@href').extract_first() or '')).replace(' ', '').strip()
                binfo['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, binfo[
                                                   'BuildingName'] + binfo['BuildingURL'])
                result.append(binfo)
            for b in b_presell_list:
                binfo = BuildingInfoItem()
                binfo['ProjectName'] = response.xpath(
                    '//td[text()="项目名称："]/following-sibling::td[1]/text()').extract_first() or ''
                binfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, binfo[
                                                  'ProjectName'] + response.url)
                presell_url = urlparse.urljoin(response.url, b.xpath(
                    './td[4]/a/@href').extract_first() or '')
                result.append(Request(url=presell_url, headers=headers, meta={
                              'PageType': 'BuildingPreSell', 'item': binfo}))
        elif response.meta.get('PageType') == 'BuildingPreSell':
            b_sell_list = response.xpath('//table[@id="donglist"]/tr')
            binfo = response.meta.get('item')
            if binfo:
                for b in b_sell_list:
                    binfo['BuildingName'] = (b.xpath('./td[2]/text()').extract_first() or '') + (
                        b.xpath('./td[3]/text()').extract_first() or '')
                    binfo['BuildingRegName'] = response.xpath(
                        '//td[@id="bookid"]/a/text()').extract_first() or ''
                    binfo['BuildingRegUUID'] = uuid.uuid3(
                        uuid.NAMESPACE_DNS, binfo['BuildingRegName']) if binfo['BuildingRegName'] != "" else binfo['BuildingRegName']
                    binfo['BuildingURL'] = urlparse.urljoin(
                        response.url, b.xpath('./td[5]/a/@href').extract_first() or '')
                    binfo['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, binfo[
                                                       'BuildingName'] + binfo['BuildingURL'])
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
        if not(200 <= response.status < 303):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('BuildingPreSell', 'PreSellInfo'):
            if result:
                return result
            return []
        print('PreSellInfoHandleMiddleware')

        if response.meta.get('PageType') == 'BuildingPreSell':
            preinfo = PreSellInfoItem()
            preinfo['PreRegName'] = response.xpath(
                '//td[@id="bookid"]/a/text()').extract_first() or ''
            if preinfo['PreRegName'] != "":
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
                print(preinfo_url)
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
        if not(200 <= response.status < 303):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseInfo', 'HouseInfoUse', 'HouseInfoDetail'):
            if result:
                return result
            return []
        print('HouseInfoHandleMiddleware')

        if response.meta.get('PageType') == 'HouseInfo':
            meta = copy.deepcopy(response.meta)
            meta['PageType'] = 'HouseInfoUse'
            result.append(Request(url=response.url,
                                  headers=headers, meta=meta))
        if response.meta.get('PageType') == 'HouseInfoUse':
            if (not response.meta.get('ProjectName')) or (not response.meta.get('BuildingName'))\
                    or (not response.meta.get('ProjectUUID')) or (not response.meta.get('BuildingUUID')):
                if result:
                    return result
                return []
            floor_list = response.xpath('//div[@id="houseshow"]/table/tr')
            for floor in floor_list:
                cur_floor = floor.xpath('./td[1]/text()').extract_first() or ''
                house_list = floor.xpath('./td[2]/table/tr/td')
                print(len(house_list))
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
                    hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, hinfo['ProjectName'] + hinfo['BuildingName'] + hinfo[
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
