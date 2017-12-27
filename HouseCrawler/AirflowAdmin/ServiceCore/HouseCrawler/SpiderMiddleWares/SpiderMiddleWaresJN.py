# coding = utf-8
import sys
import json
import uuid
import re
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsJN import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


class ProjectBaseHandleMiddleware(object):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'www.jnfdc.gov.cn',
               'Upgrade-Insecure-Requests': '1',
               }

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
        # 判断类型是否吻合  (给定一个标识)
        if response.meta.get('PageType') not in ('ProjectBase', 'ProjectList'):
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectBase':
            page_count = sel.xpath(
                '//*[@id="allpage"]/@value').extract_first() or '0'
            for i in range(1, int(page_count) + 1):
                page_url = "http://www.jnfdc.gov.cn/onsaling/index_%s.shtml" % i
                Page_houst = Request(url=page_url, method='GET', headers=self.headers, meta={
                                     'PageType': 'ProjectList'})
                result.append(Page_houst)
        elif response.meta.get('PageType') == 'ProjectList':
            pro_list = sel.xpath('//table[@class="project_table"]/tr[td[a]]')
            for p in pro_list:
                pb = ProjectBaseItem()
                pb['ProjectName'] = p.xpath(
                    './td[2]/a/text()').extract_first() or ''
                pb['ProjectURL'] = urlparse.urljoin(
                    response.url, p.xpath('./td[2]/a/@href').extract_first() or '')
                pb['ProjectUUID'] = str(uuid.uuid3(uuid.NAMESPACE_DNS,
                                                   pb['ProjectName'] + pb['ProjectURL'].split('?')[1]))
                pb['ProjectAddress'] = p.xpath(
                    './td[3]/text()').extract_first() or ''
                pb['ProjectCompany'] = p.xpath(
                    './td[4]/text()').extract_first() or ''
                pb['ProjectSaleNum'] = p.xpath(
                    './td[5]/text()').extract_first() or ''
                result.append(pb)
        return result


class ProjectInfoHandleMiddleware(object):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': 'www.jnfdc.gov.cn',
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

        if response.meta.get('PageType') != 'ProjectInfo':  # 判断类型是否吻合  (给定一个标识)
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')

        pinfo = ProjectInfoItem()
        pinfo['ProjectName'] = (response.xpath(
            '//td[text()="项目名称"]/following-sibling::td[1]/text()').extract_first() or '').strip()
        pinfo['ProjectAddress'] = (response.xpath(
            '//td[text()="项目地址"]/following-sibling::td[1]/text()').extract_first() or '').strip()
        pinfo['ProjectCompany'] = (response.xpath(
            '//td[text()="企业名称"]/following-sibling::td[1]/text()').extract_first() or '').strip()
        pinfo['ProjectDistrict'] = (response.xpath(
            '//td[text()="所在区县"]/following-sibling::td[1]/text()').extract_first() or '').strip()
        pinfo['ProjectScale'] = (response.xpath(
            '//td[text()="项目规模"]/following-sibling::td[1]/text()').extract_first() or '').strip()
        pinfo['ProjectBuildingNum'] = (response.xpath(
            '//td[text()="总 栋 数"]/following-sibling::td[1]/text()').extract_first() or '').strip()
        pinfo['ProjectSaleAddress'] = (response.xpath(
            '//td[text()="售楼地址"]/following-sibling::td[1]/text()').extract_first() or '').strip()
        pinfo['ProjectSalePhone'] = (response.xpath(
            '//td[text()="售楼电话"]/following-sibling::td[1]/text()').extract_first() or '').strip()
        pinfo['ProjectManageCompany'] = (response.xpath(
            '//td[text()="物业公司"]/following-sibling::td[1]/text()').extract_first() or '').strip()
        pinfo['ProjectUUID'] = str(uuid.uuid3(
            uuid.NAMESPACE_DNS, pinfo['ProjectName'] + response.url.split('?')[1]))
        result.append(pinfo)
        return result


class BuildingListHandleMiddleware(object):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Cookie': 'clientlanguage=zh_CN; JSESSIONID=46EC98AF5CC8248C6576C81228461633',
               'Host': 'www.jnfdc.gov.cn',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
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
        # 判断类型是否吻合  (给定一个标识)
        if response.meta.get('PageType') not in ('ProjectInfo', 'BuildingList', 'BuildingInfo'):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfo':
            total_page = response.xpath(
                '//input[@id="allpage"]/@value').extract_first() or '0'
            page_url = 'http://www.jnfdc.gov.cn/onsaling/show_%s.shtml?'
            for i in range(1, int(total_page) + 1):
                url = (page_url % i) + (response.url).split('?')[1]
                result.append(Request(url=url, method='GET', headers=self.headers,
                                      meta={'PageType': 'BuildingList'}))
        elif response.meta.get('PageType') == 'BuildingList':
            b_list = response.xpath(
                '//table[@class="project_table"]/tr[td[a]]')
            for b in b_list:
                binfo = BuildingInfoItem()
                binfo['ProjectName'] = (response.xpath(
                    '//td[text()="项目名称"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['ProjectUUID'] = str(uuid.uuid3(
                    uuid.NAMESPACE_DNS, binfo['ProjectName'] + response.url.split('?')[1]))
                binfo['BuildingName'] = (b.xpath(
                    './td[2]/@title').extract_first() or '').strip()
                binfo['BuildingRegName'] = (b.xpath(
                    './td[3]/@title').extract_first() or '').strip()
                binfo['BuildingUUID'] = str(uuid.uuid3(
                    uuid.NAMESPACE_DNS, binfo['ProjectName'] + binfo['BuildingName'] + binfo['BuildingRegName']))
                binfo['BuildingSaleNum'] = (b.xpath(
                    './td[4]/text()').extract_first() or '').strip()
                binfo['BuildingSaleArea'] = (b.xpath(
                    './td[5]/text()').extract_first() or '').strip()
                binfo['BuildingAvailabeNum'] = (b.xpath(
                    './td[6]/text()').extract_first() or '').strip()
                binfo['BuildingAvailabeArea'] = (b.xpath(
                    './td[7]/text()').extract_first() or '').strip()
                binfo['BuildingSoldNum'] = (b.xpath(
                    './td[8]/text()').extract_first() or '').strip()
                binfo['BuildingSoldArea'] = (b.xpath(
                    './td[9]/text()').extract_first() or '').strip()
                binfo_url = urlparse.urljoin(
                    response.url, b.xpath('./td[2]/a/@href').extract_first() or '')
                result.append(Request(url=binfo_url, method='GET', headers=self.headers,
                                      meta={'PageType': 'BuildingInfo', 'item': binfo}))
        elif response.meta.get('PageType') == 'BuildingInfo':
            binfo = response.meta.get('item')
            if binfo:
                binfo['BuildingNameAlias'] = (response.xpath(
                    '//td[text()="楼盘名称"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['BuildingDevCompany'] = (response.xpath(
                    '//td[text()="开发单位"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['BuildingDevCredential'] = (response.xpath(
                    '//td[text()="开发企业资质"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['BuildingArea'] = (response.xpath(
                    '//td[text()="建筑面积(万m²)"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['BuildingDistrict'] = (response.xpath(
                    '//td[text()="所在区县"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['BuildingDecoration'] = (response.xpath(
                    '//td[text()="装修标准"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['BuildingUsage'] = (response.xpath(
                    '//td[text()="规划用途"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['BuildingIsMortgage'] = (response.xpath(
                    '//td[text()="有无抵押"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['BuildingAreaCode'] = (response.xpath(
                    '//td[text()="国有土地使用证"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['BuildingEngPlanCode'] = (response.xpath(
                    '//td[text()="建设工程规划许可证"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['BuildingEngCode'] = (response.xpath(
                    '//td[text()="建设工程施工许可证"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                binfo['BuildingURL'] = 'http://www.jnfdc.gov.cn/onsaling/viewhouse.shtml?fmid=' + \
                    response.url.split('=')[1]
                building_sale_list = response.xpath(
                    '//table[@class="flow_message_table"]/tr[not (@style)]')
                building_sale_dict = {}
                for tr in building_sale_list:
                    building_sale_dict[tr.xpath('./td[1]/text()').extract_first() or ''] = {
                        '批准销售套数': tr.xpath('./td[2]/text()').extract_first() or '',
                        '批准销售面积': tr.xpath('./td[3]/text()').extract_first() or '',
                        '已售套数': tr.xpath('./td[4]/text()').extract_first() or '',
                        '已售面积': tr.xpath('./td[5]/text()').extract_first() or '',
                        '可售套数': tr.xpath('./td[6]/text()').extract_first() or '',
                        '可售面积': tr.xpath('./td[7]/text()').extract_first() or ''
                    }
                binfo['BuildingSaleDict'] = building_sale_dict
                result.append(binfo)
        return result


class HouseInfoHandleMiddleware(object):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'www.jnfdc.gov.cn',
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
                '15701': '可售',
                '15702': '已预订',
                '15709': '已预订',
                '15703': '已备案',
                '15704': '已签约',
                '15705': '可租赁',
                '15707': '不可租售',
                '15710': '查封',
                '15711': '冻结',
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
        if response.meta.get('PageType') not in ('HouseInfo', 'HouseList', 'HouseDetail'):
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
            house_list_url = urlparse.urljoin(response.url, re.search(
                r'urls= "(/r/house/.+xml)"', response.body_as_unicode()).group(1))
            meta = response.meta
            meta['PageType'] = 'HouseList'
            result.append(Request(url=house_list_url, method='GET', headers=self.headers,
                                  meta=meta))
        if response.meta.get('PageType') == 'HouseList':
            house_list = response.xpath('//house[id[text()!="null"]]')
            for h in house_list:
                hinfo = HouseInfoItem()
                hinfo['ProjectName'] = response.meta.get('ProjectName') or ''
                hinfo['ProjectUUID'] = response.meta.get('ProjectUUID') or ''
                hinfo['BuildingName'] = response.meta.get('BuildingName') or ''
                hinfo['BuildingUUID'] = response.meta.get('BuildingUUID') or ''
                hinfo['HouseName'] = h.xpath(
                    './title/text()').extract_first() or ''
                hinfo['HouseID'] = h.xpath('./id/text()').extract_first() or ''
                hinfo['HouseUUID'] = str(uuid.uuid3(
                    uuid.NAMESPACE_DNS, hinfo['HouseID']))
                hinfo['HouseSaleState'] = get_house_state(
                    h.xpath('./roomState/text()').extract_first() or '')
                room_url = "http://www.jnfdc.gov.cn/onsaling/viewDiv.shtml?fid=%s" % hinfo[
                    'HouseID']
                houseinfodetail_req = Request(url=room_url, method='GET', headers=self.headers,
                                              meta={'PageType': 'HouseDetail', 'item': hinfo})
                result.append(houseinfodetail_req)

        if response.meta.get('PageType') == 'HouseDetail':
            hinfo = response.meta.get('item')
            if hinfo:
                dict_data = json.loads(response.body_as_unicode())
                hinfo['HouseArea'] = dict_data.get('housearea') or ''
                hinfo['HouseUnitArea'] = dict_data.get('unitarea') or ''
                hinfo['HouseApportioArea'] = dict_data.get(
                    'apportioarea') or ''
                hinfo['HouseUsage'] = dict_data.get('usedtypeno') or ''
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
        if response.meta.get('PageType') != 'SignInfo':
            if result:
                return result
            return []
        print('SignInfoHandleMiddleware')
        signitem = SignInfoItem()
        sale_list = response.xpath(
            '//body/div[5]/div[1]/div[2]/div[3]/div[2]/div/table/tr[not(th)]')
        sale_dict = {}
        for tr in sale_list:
            sale_dict[tr.xpath('./td[2]/text()').extract_first() or ''] = {
                '可售套数': tr.xpath('./td[3]/text()').extract_first() or '',
                '住宅可售套数': tr.xpath('./td[4]/text()').extract_first() or '',
                '今日签约套数': tr.xpath('./td[5]/text()').extract_first() or '',
                '今日签约面积': tr.xpath('./td[6]/text()').extract_first() or ''
            }
        signitem['SaleDict'] = sale_dict
        result.append(signitem)
        return result
