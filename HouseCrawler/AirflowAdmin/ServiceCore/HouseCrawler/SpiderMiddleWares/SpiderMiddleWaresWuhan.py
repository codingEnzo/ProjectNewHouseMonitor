# coding = utf-8
import sys
import uuid
import urllib
from scrapy import Request
from HouseNew.models import *
from HouseCrawler.Items.ItemsWuhan import *


if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


class ProjectBaseHandleMiddleware(object):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'scxx.fgj.wuhan.gov.cn',
        'Upgrade-Insecure-Requests': '1',
    }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        def get_total_page():  # 获取总页数
            search_result = response.xpath(
                '//select[@name="pagemenu"]/option[last()]/text()').extract_first() or '0'
            return int(search_result)

        result = list(result)
        if not(200 <= response.status < 300):  # 判断状态码
            if result:
                return result
            return []

        if response.meta.get('PageType') not in ('ProjectBase', 'ProjectList'):  # 获取一个类型,,标识
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectBase':
            page_count = get_total_page()
            for i in range(1, page_count + 1):
                page_url = "http://scxx.fgj.wuhan.gov.cn/xmqk.asp?page=%d&domain=&blname=&bladdr=&prname=" % i
                result.append(Request(url=page_url, method='GET', headers=self.headers, meta={
                    'PageType': 'ProjectList'}))  # 爬取每一页内容,ProjectBase作为标识
        elif response.meta.get('PageType') == 'ProjectList':
            pro_list = response.xpath('//tr[@bgcolor="#FFFFFF"]')  # td的父级
            for tr in pro_list:
                pb = ProjectBaseItem()
                href = tr.xpath('td[1]/a/@href').extract_first()
                base_code = href.split('=')[1]
                uu = urllib.parse.quote(base_code.encode(
                    'gbk', 'replace'))  # gb2312 转gbk
                sphref = href.split('=')[0] + '=' + uu
                http = urlparse.urljoin(response.url, sphref)
                pb['ProjectUUID'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, http))
                pb['ProjectUrl'] = http
                pb['ProjectName'] = tr.xpath(
                    'td[1]/a/span/text()').extract_first() or ''
                pb['Allnumber'] = tr.xpath(
                    'td[2]/text()').extract_first().strip()
                pb['Home_have_sale'] = tr.xpath(
                    'td[3]/text()').extract_first().strip()
                pb['Home_sale'] = tr.xpath(
                    'td[4]/text()').extract_first().strip()
                pb['NoHome_have_sale'] = tr.xpath(
                    'td[5]/text()').extract_first().strip()
                pb['NoHome_sale'] = tr.xpath(
                    'td[6]/text()').extract_first().strip()
                result.append(pb)

        return result


class ProjectInfoHandleMiddleware(object):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'scxx.fgj.wuhan.gov.cn',
        'Upgrade-Insecure-Requests': 1,
    }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)  #

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfo'):  # 判断类型是否吻合  (给定一个标识)
            if result:
                return result
            return []
        # newres = Selector(text=response.body_as_unicode())
        print('ProjectInfoHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfo':
            href = response.xpath('//tr/td[1]/p/font/a/@href').extract_first()
            if href:
                info_code = href.split('=')[1]
                uu = urllib.parse.quote(info_code.encode('gbk', 'replace'))
                sphref = href.split('=')[0] + '=' + uu
                part_http = "http://scxx.fgj.wuhan.gov.cn/" + sphref
                result.append(url=part_http,
                              meta={'PageType': 'BuildingInfo',
                                    'pjuuid': response.meta.get('pjuuid') or '',
                                    'pjname': response.meta.get('pjname') or ''})
            item = ProjectInfoItem()
            item['ProjectName'] = response.meta.get('pjname') or ''
            item['location'] = (response.xpath(
                '//table[2]/tbody/tr[2]/td[2]/text()').extract_first() or '').strip()
            item['start_work_time'] = (response.xpath(
                '//table[2]/tbody/tr[3]/td[2]/text()').extract_first() or '').strip()
            item['completed_time'] = (response.xpath(
                '//table[2]/tbody/tr[3]/td[4]/text()').extract_first() or '').strip()
            item['land_area'] = (response.xpath(
                '//table[2]/tbody/tr[4]/td[3]/text()').extract_first() or '').strip()
            item['land_year'] = (response.xpath(
                '//table[2]/tbody/tr[4]/td[5]/text()').extract_first() or '').strip()
            item['land_purpose'] = (response.xpath(
                '//table[2]/tbody/tr[5]/td[2]/text()').extract_first() or '').strip()
            item['Land_grade'] = (response.xpath(
                '//table[2]/tbody/tr[5]/td[4]/text()').extract_first() or '').strip()
            item['building_area'] = (response.xpath(
                '//table[2]/tbody/tr[6]/td[2]/text()').extract_first() or '').strip()
            item['Volume_rate'] = (response.xpath(
                '//table[2]/tbody/tr[6]/td[4]/text()').extract_first() or '').strip()
            item['home_Tnumber'] = (response.xpath(
                '//table[2]/tbody/tr[7]/td[2]/text()').extract_first() or '').strip()
            item['home_Dnumber'] = (response.xpath(
                '//table[2]/tbody/tr[7]/td[4]/text()').extract_first() or '').strip()
            item['market_time'] = (response.xpath(
                '//table[2]/tbody/tr[8]/td[2]/text()').extract_first() or '').strip()
            item['His_rights'] = (response.xpath(
                '//table[2]/tbody/tr[8]/td[4]/text()').extract_first() or '').strip()
            item['PermitNumberOfConstructionLandPlanning'] = (response.xpath(
                '//table[2]/tbody/tr[9]/td[4]/text()').extract_first() or '').strip()
            item['CertificateOfUseOfStateOwnedLand'] = (response.xpath(
                '//table[2]/tbody/tr[9]/td[6]/text()').extract_first() or '').strip()
            item['ConstructionProjectPlanningPermitNumber'] = (response.xpath(
                '//table[2]/tbody/tr[10]/td[4]/text()').extract_first() or '').strip()
            item['ConstructionPermitNumber'] = (response.xpath(
                '//table[2]/tbody/tr[10]/td[2]/text()').extract_first() or '').strip()
            item['LicenseNumberOfCommercialHousingPresale'] = (response.xpath(
                '//table[2]/tbody/tr[11]/td[2]/text()').extract_first() or '').strip()
            item['DevelopEnterpriseQualificationNumber'] = (response.xpath(
                '//table[2]/tbody/tr[11]/td[4]/text()').extract_first() or '').strip()
            item['DevelopmentEnterprise'] = (response.xpath(
                '//table[2]/tbody/tr[12]/td[2]/text()').extract_first() or '').strip()
            item['Phone1'] = (response.xpath(
                '//table[2]/tbody/tr[13]/td[2]/text()').extract_first() or '').strip()
            item['AgencyCompany'] = (response.xpath(
                '//table[2]/tbody/tr[14]/td[2]/text()').extract_first() or '').strip()
            item['Phone2'] = (response.xpath(
                '//table[2]/tbody/tr[15]/td[2]/text()').extract_first() or '').strip()
            item['ProjectFilingAuthority'] = (response.xpath(
                '//table[2]/tbody/tr[16]/td[2]/text()').extract_first() or '').strip()
            item['InfoUrl'] = response.url
            item['ProjectUUID'] = response.meta.get('pjuuid') or ''
            result.append(item)

        return result


class BuildingListHandleMiddleware(object):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'scxx.fgj.wuhan.gov.cn',
        'Upgrade-Insecure-Requests': '1',
    }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') != 'BuildingInfo':
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        if response.meta.get('PageType') == 'BuildingInfo':
            tr_list = response.xpath('//tr[@bgcolor="#FFFFFF"]')

            for tr in tr_list:
                BuilItem = BuildingInfoItem()
                href = tr.xpath('td[1]/a/@href').extract_first()
                code0 = href.split('=')[0]
                code1 = href.split('=')[1]
                code2 = href.split('=')[2]
                uu1 = urllib.parse.quote(code1.encode(
                    'gbk', 'replace'))  # gb2312  转gbk
                np = uu1.split('%26')
                uu2 = urllib.parse.quote(code2.encode(
                    'gbk', 'replace'))  # gb2312  转gbk
                sphref = code0 + '=' + np[0] + \
                    '&' + np[1] + "=" + uu2  # 拼接href
                houses_url = "http://scxx.fgj.wuhan.gov.cn/" + sphref
                BuilItem['ProjectName'] = response.meta.get('pjname') or ''
                BuilItem['BuildingName'] = tr.xpath(
                    'td[1]/a/span/text()').extract_first(default='').strip()
                BuilItem['BuildingURL'] = houses_url
                BuilItem['Building_structure'] = tr.xpath(
                    'td[2]/text()').extract_first(default='').strip()
                BuilItem['Layer_number'] = tr.xpath(
                    'td[3]/text()').extract_first(default='').strip()
                BuilItem['Set_number'] = tr.xpath(
                    'td[4]/text()').extract_first(default='').strip()
                BuilItem['ProjectUUID'] = response.meta.get('pjuuid') or ''
                BuilItem['BuildingUUID'] = str(uuid.uuid3(
                    uuid.NAMESPACE_DNS, str(houses_url) + BuilItem['BuildingName']))
                result.append(BuilItem)
        return result


class HouseInfoHandleMiddleware(object):

    headers_next = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': '202.103.39.36',
        'Upgrade-Insecure-Requests': '1',
    }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        def get_house_state(string):  # 户状态
            STATE_TAB = {
                '#CCFFFF': '未销售',
                '#FF0000': '已网上销售',
                '#FFFF00': '已抵押',
                '#CC0099': '已查封',
                '#000000': '限制出售',
                '#FFFFFF': '状态不明',
            }
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
        if response.meta.get('PageType') not in ('HouseInfo', 'HouseInfoDetail'):
            if result:
                return result
            return []
        print('HouseInfoHandleMiddleware')

        if response.meta.get('PageType') == 'HouseInfo':
            tr_list = response.xpath(
                "//tr[2]/td/table[3]//tr/td/table//tr[@bgcolor and td[@bgcolor]]")
            for tr in tr_list:
                builnum = tr.xpath('td[1]/text()').extract_first()
                unit = tr.xpath('td[2]/text()').extract_first()
                floornum = tr.xpath('td[3]/text()').extract_first()
                tds = tr.xpath('td[@bgcolor]')
                for td in tds:
                    hinfo = HouseInfoItem()
                    roomurl = td.xpath(
                        './a/@href | ./font/a/@href').extract_first(default='')
                    roomnum = td.xpath(
                        './a/text() | ./font/a/text()').extract_first(default='')
                    hinfo['Unit'] = unit
                    hinfo['FloorNum'] = floornum
                    hinfo['BuildingNum'] = builnum

                    hinfo['HouseName'] = roomnum
                    hinfo['HouseUrl'] = response.url
                    hinfo['HouseSubUrl'] = roomurl

                    hinfo['ProjectName'] = response.meta.get('pjname', '')
                    hinfo['BuildingName'] = response.meta.get('BuilName', '')
                    hinfo['ProjectUUID'] = response.meta.get('pjuuid', '')
                    hinfo['BuildingUUID'] = response.meta.get('builuuid', '')
                    hinfo['HouseUUID'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(
                        hinfo['ProjectName']) + str(builnum) + str(unit) + str(floornum) + str(roomnum) + str(roomurl)))
                    hinfo['State'] = get_house_state(
                        td.xpath('@bgcolor').extract_first(default=''))
                    result.append(Request(url=roomurl, method='GET', headers=self.headers_next,
                                          meta={'PageType': 'HouseInfoDetail', 'item': hinfo}))
        if response.meta.get('PageType') == 'HouseInfoDetail':
            hinfo = response.meta.get('item')
            if hinfo:
                hinfo['House_located'] = response.xpath(
                    '//tr[1]/td[2]/text()').extract_first(default='').strip()
                hinfo['Pre_sale_license_number'] = response.xpath(
                    '//tr[2]/td[2]/text()').extract_first(default='').strip()
                hinfo['Predicted_area'] = response.xpath(
                    '//tr[3]/td[2]/text()').extract_first(default='').strip()
                hinfo['Measured_area'] = response.xpath(
                    '//tr[4]/td[2]/text()').extract_first(default='').strip()
                hinfo['Record_unit_price'] = urlparse.urljoin(response.url, response.xpath(
                    '//tr[5]/td[2]/img/@src').extract_first(default='').strip())
                result.append(hinfo)
        return result


class SignInfoHandleMiddleware(object):

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
        if response.meta.get('PageType') not in ('SignInfoBase', 'SignInfo'):
            if result:
                return result
            return []
        print('SignInfoHandleMiddleware')

        if response.meta.get('PageType') == 'SignInfoBase':
            sign_url = urlparse.urljoin(response.url, response.xpath(
                '//tr[2]/td/table[1]//tr/td[1]/a/@href').extract_first(default=''))
            result.append(Request(url=sign_url, meta={'PageType': 'SignInfo'}))
        elif response.meta.get('PageType') == "SignInfo":
            SignItem = SignInfoItem()
            SignItem['SellInfo'] = {}
            s_info_list = response.xpath(
                '//div[@id="artibody"]/table/tbody/tr[position()>2]')[:-2]
            for s_info in s_info_list:
                s_dict = {s_info.xpath('./td[1]/text()').extract_first(default='').strip(): {
                    'HousingSoldNum': s_info.xpath('./td[2]/text()').extract_first(default='').strip(),
                    'HousingSoldArea': s_info.xpath('./td[3]/text()').extract_first(default='').strip(),
                    'OfficeSoldNum': s_info.xpath('./td[4]/text()').extract_first(default='').strip(),
                    'OfficeSoldArea': s_info.xpath('./td[5]/text()').extract_first(default='').strip(),
                    'BussinessSoldNum': s_info.xpath('./td[6]/text()').extract_first(default='').strip(),
                    'BussinessSoldArea': s_info.xpath('./td[7]/text()').extract_first(default='').strip(),
                    'OtherSoldNum': s_info.xpath('./td[8]/text()').extract_first(default='').strip(),
                    'OtherSoldArea': s_info.xpath('./td[9]/text()').extract_first(default='').strip(),
                    'AllSoldNum': s_info.xpath('./td[10]/text()').extract_first(default='').strip(),
                    'AllSoldArea': s_info.xpath('./td[11]/text()').extract_first(default='').strip()
                }}
                SignItem['SellInfo'].update(s_dict)
            result.append(SignItem)
        return result
