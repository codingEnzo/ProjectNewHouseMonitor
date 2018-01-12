# coding = utf-8
import json
import logging
import sys
import uuid

import regex
import time

from scrapy import Request
from HouseNew.models import *
from HouseCrawler.Items.ItemsWulumuqi import *

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
logger = logging.getLogger(__name__)

debug = False


class ProjectBaseHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        def get_totla_page(response):
            total_page = 1
            if debug:
                return 1
            try:
                t = response.xpath('//div[@class="pagenuber_info"]/font[last()]/text()').extract_first()
                total_page = int(t.replace('1/', ''))
            except Exception:
                pass
            return total_page

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectBase':
            return result if result else []
        # print('ProjectBaseHandleMiddleware')
        curPage = response.meta.get('curPage')
        if curPage and curPage == 1:
            source_url = 'http://www.anju-365.com/newhouse/property_searchall.htm?searchkeyword=&keyword=&sid=&districtid=&areaid=&dealprice=&propertystate=&propertytype=&ordertype=&priceorder=&openorder=&view720data=&page={curPage}&bbs=&avanumorder=&comnumorder='
            total_page = get_totla_page(response)
            for page in range(1, total_page + 1):
                list_req = Request(url=source_url.format(curPage=page),
                                   headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                   dont_filter=True,
                                   meta={'PageType': 'ProjectBase'})
                result.append(list_req)
        else:
            onclick_arr = response.xpath('//div[contains(@onclick,"toPropertyInfo")]')
            for onclick in onclick_arr:
                try:
                    s = onclick.xpath('div[3]/p/text()').extract_first()
                    t = regex.search(r'\[(?<region>.*)\]', s)
                    RegionName = t.group(1)
                    s = onclick.xpath('@onclick').extract_first()
                    t = regex.search(r'\((?<sid>.+),(?<propertyID>.+)\)', s)
                    sid = t.group(1)
                    propertyID = t.group(2)
                    url = 'http://www.anju-365.com/newhouse/property_{sid}_{propertyID}_info.htm'.format(sid=sid,
                                                                                                         propertyID=propertyID)
                    req = Request(url=url,
                                  headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                  dont_filter=True,
                                  meta={'PageType': 'ProjectInfo',
                                        'sid': sid,
                                        'PropertyID': propertyID,
                                        'RegionName': RegionName})
                    result.append(req)
                except:
                    pass
        return result


# 项目详细信息
class ProjectInfoHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        def remove_html_tag(string):
            try:
                if isinstance(string, list):
                    string = ''.join(string)
                re_h = regex.compile(r'<[^>]+>', regex.S)
                return re_h.sub('', string)
            except:
                return ''

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectInfo':
            return result if result else []
        # print('ProjectInfoHandleMiddleware')
        projectBase = ProjectBaseItem()
        projectBase['DistrictName'] = response.meta.get('RegionName')
        projectBase['PropertyID'] = response.meta.get('PropertyID')
        projectBase['SourceUrl'] = response.url
        projectBase['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, projectBase['SourceUrl'])
        OnSaleState = response.xpath('//span[contains(@class,"colorwht")]/text()').extract_first()

        projectBase['OnSaleState'] = OnSaleState
        projectBase['Selltel'] = response.xpath(
            '//font[text()="售楼电话："]/following-sibling::font/text()').extract_first()
        projectBase['ProjectAllrankvalue'] = response.xpath('//*[@id="allrankvalue1"]/text()').extract_first()
        projectBase['ProjectName'] = response.xpath(
            '//span[@class="buidname colordg"]/text()').extract_first()
        projectBase['ProjectAddress'] = response.xpath(
            '//strong[text()="楼盘地址："]/following-sibling::span[1]/@title').extract_first()
        projectBase['ProjectMainUnitType'] = response.xpath(
            '//strong[text()="主力户型："]/following-sibling::span[1]/text()').extract_first()
        projectBase['ProjectDecoration'] = response.xpath('//strong[text()="装修状况："]/../text()').extract_first()
        projectBase['LandUse'] = response.xpath(
            '//strong[text()="物业类型："]/following-sibling::span[1]/text()').extract_first()
        projectBase['BuildingType'] = response.xpath('//strong[text()="建筑形式："]/../text()').extract_first()
        projectBase['FloorAreaRatio'] = response.xpath('//span[text()="容 积 率："]/../text()').extract_first()
        projectBase['GreeningRate'] = response.xpath('//span[text()="绿 化 率："]/../text()').extract_first()

        projectBase['FloorArea'] = response.xpath('//span[text()="占地面积："]/../text()').extract_first()
        if not projectBase['FloorArea'] or 'java' in projectBase['FloorArea']:
            projectBase['FloorArea'] = ''
        projectBase['CompletionDate'] = response.xpath('//span[text()="竣工时间："]/../text()').extract_first()
        projectBase['TotalBuidlingArea'] = response.xpath('//span[text()="总建筑面积："]/../text()').extract_first()
        projectBase['HousingCount'] = response.xpath('//span[text()="总户数："]/../text()').extract_first()
        projectBase['LatestDeliversHouseDate'] = response.xpath('//span[text()="预计交付时间："]/../text()').extract_first()
        projectBase['ParkingInfo'] = response.xpath('//span[text()="车位信息："]/../text()').extract_first()
        projectBase['ManagementFees'] = response.xpath('//span[text()="物 业 费："]/../text()').extract_first()
        projectBase['ManagementCompany'] = response.xpath('//span[text()="物业公司："]/../text()').extract_first()
        projectBase['PropertyRightsDescription'] = response.xpath('//span[text()="产权年限："]/../text()').extract_first()
        projectBase['Developer'] = response.xpath('//strong[text()="项目公司："]/../text()').extract_first()
        ProjectIntro_text = response.xpath('//div[@class="lpinfodtxt"]').re(r'.*')
        projectBase['ProjectIntro'] = remove_html_tag(ProjectIntro_text)
        result.append(projectBase)

        # 判断是否有预售证信息(导航栏的一房一价)
        presellHref = response.xpath('//*[@id="yfyj_index"]/../@href').extract_first()
        if presellHref:
            presellHref = 'http://www.anju-365.com' + presellHref
            req = Request(url=presellHref,
                          headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                          dont_filter=True,
                          meta={'PageType': 'PresellList', 'ProjectUUID': str(projectBase['ProjectUUID'])})
            result.append(req)
        return result


class PresellListHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') not in ('PresellList', 'PresellListBuliding'):
            return result if result else []
        # print('PresellListHandleMiddleware')
        ProjectUUID = response.meta.get('ProjectUUID')
        sid = response.xpath('//*[@id="sid"]/@value').extract_first()
        propertyid = response.xpath('//*[@id="propertyid"]/@value').extract_first()

        if response.meta.get('PageType') == 'PresellList':
            # 获取预售证列表
            presell_arr = response.xpath('//a[starts-with(@id,"presell_")]')
            for element in presell_arr[1:]:
                presellInfoItem = PresellInfoItem()
                PresellID = element.xpath('@id').extract_first().replace('presell_', '')
                PresellNO = element.xpath('text()').extract_first()
                # 防止出现没有预售证和楼栋的
                # http://www.anju-365.com/newhouse/property_33_990278678_price.htm?isopen=&presellid=989913453&buildingid=&area=&allprice=&housestate=&housetype=&page=
                if not PresellNO:
                    continue
                PresellUUID = uuid.uuid3(uuid.NAMESPACE_DNS,
                                         ProjectUUID + PresellID)
                presellInfoItem['PresellUUID'] = PresellUUID
                presellInfoItem['ProjectUUID'] = ProjectUUID
                presellInfoItem['sid'] = sid
                presellInfoItem['PropertyID'] = propertyid
                presellInfoItem['PresellID'] = PresellID
                presellInfoItem['PresellNO'] = PresellNO

                api_url = 'http://www.anju-365.com/newhouse/NewPropertyHz_createPresellInfo.jspx?sid={sid}&presellid={presellID}&propertyid={propertyid}&_={timestamp}'
                presellInfo_req = Request(
                    url=api_url.format(sid=sid, propertyid=propertyid, presellID=PresellID,
                                       timestamp=round(time.time())),
                    headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                    dont_filter=True,
                    meta={'PageType': 'PresellInfo', 'presellInfoItem': presellInfoItem})
                result.append(presellInfo_req)

                building_req_url = 'http://www.anju-365.com/newhouse/property_{sid}_{propertyid}_price.htm?isopen=&presellid={presellID}&buildingid=&area=&allprice=&housestate=&housetype=&page='
                bulidingList_req = Request(
                    url=building_req_url.format(sid=sid, propertyid=propertyid, presellID=PresellID),
                    headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                    dont_filter=True,
                    meta={'PageType': 'PresellListBuliding',
                          'ProjectUUID': ProjectUUID,
                          'PresellUUID': str(PresellUUID),
                          'PresellID': PresellID
                          })
                result.append(bulidingList_req)
        elif response.meta.get('PageType') == 'PresellListBuliding':
            PresellUUID = response.meta.get('PresellUUID')
            PresellID = response.meta.get('PresellID')
            # 获取预售证下的楼栋
            building_elements = response.xpath('//a[starts-with(@id,"building_")]')
            building_req_url = 'http://www.anju-365.com/newhouse/property_{sid}_{propertyID}_price.htm?isopen=&presellid={presellID}&buildingid={buildingID}&area=&allprice=&housestate=&housetype=&page={page}'
            for element in building_elements[1:]:
                buildingItem = BuildingInfoItem()
                buildingItem['ProjectUUID'] = ProjectUUID
                buildingItem['PresellUUID'] = PresellUUID
                buildingItem['BuildingID'] = element.xpath('@id').extract_first().replace('building_', '')
                buildingURL = building_req_url.format(sid=sid,
                                                      propertyID=propertyid,
                                                      presellID=PresellID,
                                                      buildingID=buildingItem['BuildingID'],
                                                      page='1')
                buildingItem['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                          str(buildingItem['PresellUUID']) + buildingItem['BuildingID'])
                buildingItem['BuildingName'] = element.xpath('text()').extract_first()
                result.append(buildingItem)
                houseList_req = Request(url = buildingURL,
                                        headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                            dont_filter = True,
                                        meta = {'PageType': 'HouseList',
                                                'curPage': '1',
                                                'sid': sid,
                                                'BuildingID': buildingItem['BuildingID'],
                                                'PropertyID': propertyid,
                                                'PresellID': PresellID,
                                                'ProjectUUID': ProjectUUID,
                                                'PresellUUID': PresellUUID,
                                                'BuildingUUID': str(buildingItem['BuildingUUID'])})
                result.append(houseList_req)
        return result


class PresellInfoHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'PresellInfo':
            return result if result else []
        # print('PresellInfoHandleMiddleware')
        presellInfoItem = response.meta.get('presellInfoItem')
        json_info = json.loads(response.body_as_unicode())
        presell = json_info.get('presell')
        if presell:
            presellInfoItem['PresellName'] = presell['presellname']
            presellInfoItem['LssueDate'] = presell['applydate']
            presellInfoItem['LandUse'] = presell['useful']
            presellInfoItem['ApprovalPresalePosition'] = presell['located']
            presellInfoItem['Applycorp'] = presell['applycorp']
            presellInfoItem['LssuingAuthority'] = presell['sendcorp']
            presellInfoItem['Bank'] = presell['bank']
            presellInfoItem['BankAccount'] = presell['bankaccno']
            presellInfoItem['OpeningDate'] = presell['openingdate']
            presellInfoItem['OpeningPrice'] = presell['openingprice']
            presellInfoItem['ApprovalProjectName'] = presell['projname']
        pre = json_info.get('pre')
        if pre:
            presellInfoItem['num'] = pre['num']
            presellInfoItem['justnum'] = pre['justnum']
            presellInfoItem['area'] = pre['area']
            presellInfoItem['justarea'] = pre['justarea']
            presellInfoItem['avanum'] = pre['avanum']
            presellInfoItem['avaarea'] = pre['avaarea']
            presellInfoItem['waitnum'] = pre['waitnum']
            presellInfoItem['waitarea'] = pre['waitarea']
            presellInfoItem['resideavanum'] = pre['resideavanum']
            presellInfoItem['limitnum'] = pre['limitnum']
            presellInfoItem['resideavaarea'] = pre['resideavaarea']
            presellInfoItem['limitarea'] = pre['limitarea']
            presellInfoItem['dealnum'] = pre['dealnum']
            presellInfoItem['notnum'] = pre['notnum']
            presellInfoItem['dealarea'] = pre['dealarea']
            presellInfoItem['notarea'] = pre['notarea']
            presellInfoItem['plannum'] = pre['plannum']
            presellInfoItem['planarea'] = pre['planarea']
        result.append(presellInfoItem)
        return result


class HouseListHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        def get_number(arr):
            if len(arr) == 0:
                return None
            number = {'numberzero': '0', 'numberone': '1', 'numbertwo': '2', 'numberthree': '3', 'numberfour': '4',
                      'numberfive': '5', 'numbersix': '6', 'numberseven': '7', 'numbereight': '8', 'numbernine': '9',
                      'numberdor': '.'}
            try:
                value = ''
                for key in arr:
                    value += number[key]
                return value
            except:
                return None

        def get_houseList_total_page(response):
            total_page = 1;
            try:
                t = regex.search(r'页数 1/(\d+)\t', response.body_as_unicode())
                total_page = int(t.group(1))
            except:
                pass
            return total_page

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'HouseList':
            return result if result else []
        # print('HouseListHandleMiddleware')
        curPage = response.meta.get('curPage')
        sid = response.meta.get('sid')
        PropertyID = response.meta.get('PropertyID')
        PresellID = response.meta.get('PresellID')
        BuildingID = response.meta.get('BuildingID')
        ProjectUUID = response.meta.get('ProjectUUID')
        PresellUUID = response.meta.get('PresellUUID')
        BuildingUUID = response.meta.get('BuildingUUID')

        if curPage:
            totla_page = get_houseList_total_page(response)
            req_url = 'http://www.anju-365.com/newhouse/property_{sid}_{propertyID}_price.htm?isopen=&presellid={presellID}&buildingid={buildingID}&area=&allprice=&housestate=&housetype=&page={page}'
            for page in range(1, totla_page + 1):
                req = Request(url=req_url.format(sid=sid, propertyID=PropertyID, presellID=PresellID,
                                                 buildingID=BuildingID, page=str(page)),
                              headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                              dont_filter=True,
                              meta={
                                  'PageType': 'HouseList',
                                  'sid': sid,
                                  'BuildingID': BuildingID,
                                  'PropertyID': PropertyID,
                                  'PresellID': PresellID,
                                  'ProjectUUID': ProjectUUID,
                                  'PresellUUID': PresellUUID,
                                  'BuildingUUID': BuildingUUID,
                                  'page': str(page)
                              })
                result.append(req)
        else:
            page = response.meta.get('page')
            tr_arr = response.xpath('//*[@id="search"]/following-sibling::div/table/tbody/tr')
            for idnex, tr in enumerate(tr_arr):
                buildingName = tr.xpath('td[1]/text()').extract_first()
                if not buildingName:
                    buildingName = ''
                houseNO = tr.xpath('td[2]/div/text()').extract_first()
                unitName = None
                if buildingName:
                    unitName = buildingName[buildingName.rindex('幢') + 1:]
                else:
                    unitName = ''
                houseBuildingArea_css_arr = tr.xpath('td[3]/div/span/@class').extract()
                houseBuildingArea = get_number(houseBuildingArea_css_arr)
                houseInnerArea_css_arr = tr.xpath('td[4]/div/span/@class').extract()
                houseInnerArea = get_number(houseInnerArea_css_arr)
                roomRate_css_arr = tr.xpath('td[5]/div/span/@class').extract()
                roomRate = get_number(roomRate_css_arr)
                roughPrice_css_arr = tr.xpath('td[6]/div/span/@class').extract()
                roughPrice = get_number(roughPrice_css_arr)
                price_css_arr = tr.xpath('td[8]/div/span/@class').extract()
                price = get_number(price_css_arr)

                # 可售是div/text(),不可售是div/font/text()
                HouseState = tr.xpath('td[9]/div/text()').extract_first()
                if not HouseState:
                    HouseState = tr.xpath('td[9]/div/font/text()').extract_first()
                houseInfoItem = HouseInfoItem()
                houseInfoItem['HouseState'] = HouseState
                houseInfoItem['ProjectUUID'] = ProjectUUID
                houseInfoItem['PresellUUID'] = PresellUUID
                houseInfoItem['BuildingUUID'] = BuildingUUID
                # 可能出现楼栋名和户号一样的,这里采用 当前页码+所在行数+BuildingUUID+户号 生成HouseUUID
                # houseInfoItem['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, page + str(idnex) + BuildingUUID + houseNO)
                houseInfoItem['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                        page + str(idnex) + BuildingUUID + buildingName + houseNO)
                houseInfoItem['BuildingName'] = buildingName  # 栋号
                houseInfoItem['HouseNO'] = houseNO  # 房号
                houseInfoItem['UnitName'] = unitName  # 单元
                if houseBuildingArea:
                    unit = tr.xpath('td[3]/div/text()').extract_first()
                    houseInfoItem['HouseBuildingArea'] = houseBuildingArea + unit
                if houseInnerArea:
                    unit = tr.xpath('td[4]/div/text()').extract_first()
                    houseInfoItem['HouseInnerArea'] = houseInnerArea + unit
                if roomRate:
                    unit = tr.xpath('td[5]/div/text()').extract_first()
                    houseInfoItem['RoomRate'] = roomRate + unit
                if roughPrice:
                    unit = tr.xpath('td[6]/div/text()').extract_first()
                    if '-' not in unit:
                        houseInfoItem['RoughPrice'] = roughPrice + unit  # 申请毛坯单价
                if price:
                    unit = tr.xpath('td[8]/div/text()').extract_first()
                    if '-' not in unit:
                        houseInfoItem['HousePrice'] = price + unit
                result.append(houseInfoItem)
        return result