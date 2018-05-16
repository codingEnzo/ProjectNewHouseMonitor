# coding = utf-8
import json
import logging
import time
import urllib.parse as urlparse
import uuid

import regex
from HouseCrawler.Items.ItemsHZ import *
from scrapy import Request

logger = logging.getLogger(__name__)

debug = False


# r = Redis(host='10.30.2.11', port=6379)


class IndexInfoHandleMiddleware(object):
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
            if result:
                return result
            return []
        if response.meta.get('PageType') != 'IndexInfo':
            if result:
                return result
            return []
        IndexInfo_tr_arr = response.xpath('//*[@id="myCont4"]/div[2]/div/div[1]/div[2]/table/tr')
        for tr in IndexInfo_tr_arr:
            indexInfo = IndexInfoItem()
            indexInfo['Region'] = tr.xpath('td[1]/text()').extract_first()
            indexInfo['RegionUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, 'IndexInfo' + indexInfo['Region'])
            indexInfo['SignCount'] = tr.xpath('td[2]/text()').extract_first()
            indexInfo['SaleArea'] = tr.xpath('td[3]/text()').extract_first()
            result.append(indexInfo)
        IndexHouseInfo_tr_arr = response.xpath('//*[@id="myCont4"]/div[1]/div[2]/table/tr')
        for tr in IndexHouseInfo_tr_arr:
            indexHouseInfo = IndexHouseInfoItem()
            indexHouseInfo['Region'] = tr.xpath('td[1]/text()').extract_first()
            indexHouseInfo['RegionUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, 'IndexHouseInfo' + indexHouseInfo['Region'])
            indexHouseInfo['SignCount'] = tr.xpath('td[2]/text()').extract_first()
            indexHouseInfo['BookCount'] = tr.xpath('td[3]/text()').extract_first()
            indexHouseInfo['SaleCount'] = tr.xpath('td[4]/text()').extract_first()
            result.append(indexHouseInfo)
        return result


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
            if result:
                return result
            return []
        if response.meta.get('PageType') != 'ProjectBase':
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')
        curPage = response.meta.get('curPage')
        if curPage and curPage == 1:
            total_page = get_totla_page(response)
            url = 'http://www.tmsf.com/newhouse/property_searchall.htm?searchkeyword=&keyword=&sid=&districtid=&areaid=&dealprice=&propertystate=&propertytype=&ordertype=&priceorder=&openorder=&view720data=&page={curPage}&bbs=&avanumorder=&comnumorder='
            req_list = []
            for page in range(1, total_page + 1):
                project_base = {
                    'source_url': url.format(curPage=page),
                    'meta': {'PageType': 'ProjectBase'}}
                # project_base_json = json.dumps(project_base, sort_keys=True)
                # r.sadd(self.settings.get('REDIS_KEY'), project_base_json)
                req_list.append(
                    Request(url=project_base.get('source_url'), meta=project_base.get('meta'), dont_filter=True))
            result.extend(req_list)
        else:
            req_list = []
            onclick_arr = response.xpath('//div[contains(@onclick,"toPropertyInfo")]')
            for onclick in onclick_arr:
                try:
                    DistrictName = ''
                    try:
                        s = onclick.xpath('../div[3]/p/text()').extract_first()
                        t = regex.search(r'\[(?<region>.*)\]', s)
                        DistrictName = t.group(1)
                    except:
                        DistrictName = ''
                    s = onclick.xpath('@onclick').extract_first()
                    t = regex.search(r'\((?<sid>.+),(?<propertyID>.+)\)', s)
                    sid = t.group(1)
                    propertyID = t.group(2)

                    ProjectName = onclick.xpath('./a/text()').extract_first(default='').strip()

                    url = 'http://www.tmsf.com/newhouse/property_{sid}_{propertyID}_info.htm'.format(sid=sid,
                                                                                                     propertyID=propertyID)
                    req = Request(url=url,
                                  headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                  dont_filter=True,
                                  meta={'PageType': 'TemplateInfo', 'sid': sid, 'PropertyID': propertyID,
                                        'DistrictName': DistrictName, 'ProjectName': ProjectName})
                    req_list.append(req)
                except:
                    import traceback
                    traceback.print_exc()
            result.extend(req_list)
        return result


class TemplateInfoHandleMiddleware(object):
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
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('TemplateInfo', 'MonitProjectInfo'):
            if result:
                return result
            return []
        print('TemplateInfoHandleMiddleware')
        projectBase = ProjectBaseItem()
        projectBase['PropertyID'] = response.meta.get('PropertyID')
        projectBase['sid'] = response.meta.get('sid')
        projectBase['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, projectBase['PropertyID'] + response.url)
        projectBase['DistrictName'] = response.meta.get('DistrictName')
        projectBase['RegionName'] = response.meta.get('DistrictName')
        projectBase['ProjectName'] = response.meta.get('ProjectName')
        projectBase['SourceUrl'] = response.url
        # 判断页面模板，富阳区的页面模板为分站
        m = response.xpath('//li[@id="siteother"]').extract()
        if len(m) > 0:  # 分站模板
            projectBase['ManagementCompany'] = ''
            projectBase['ProjectAddress'] = response.xpath('//span[text()="物业地址："]/../text()').extract_first('')
            projectBase['Developer'] = response.xpath('//span[text()="项目公司："]/../text()').extract_first('')
            stateDict = {'b1': '打折', 'b2': '在售', 'b3': '尾盘', 'b4': '售完', 'b5': '待售'}
            css = response.xpath('//*[@id="head"]/ul/li[2]/@class').extract_first()
            projectBase['OnSaleState'] = stateDict[css]
            result.append(projectBase)

            yfyj_index = response.xpath('//*[@id="price"]/@href').extract_first()
            presell_page_req = Request(url='http://www.tmsf.com' + yfyj_index,
                                       headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                       dont_filter=True,
                                       meta={
                                           'PageType': 'PresellList',
                                           'sid': projectBase['sid'],
                                           'ProjectName': projectBase['ProjectName'],
                                           'PropertyID': projectBase['PropertyID'],
                                           'ProjectUUID': str(projectBase['ProjectUUID'])
                                       })
            result.append(presell_page_req)
        else:
            # 主站模板的信息在basicinfo.htm
            property_basicinfo_url = 'http://www.tmsf.com/newhouse/property_{sid}_{propertyID}_basicinfo.htm'
            property_basicinfo_req = Request(
                url=property_basicinfo_url.format(sid=projectBase['sid'],
                                                  propertyID=projectBase['PropertyID']),
                headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                dont_filter=True,
                meta={'PageType': 'ProjectInfo', 'projectBase': projectBase})
            result.append(property_basicinfo_req)

            # 判断有没有预售证的页面,例如"竞得"状态下是没有预售证信息的
            yfyj_index = response.xpath('//*[@id="yfyj_index"]/../@href').extract_first()
            if yfyj_index:
                presell_page_req = Request(url='http://www.tmsf.com' + yfyj_index,
                                           headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                           dont_filter=True,
                                           meta={
                                               'PageType': 'PresellList',
                                               'sid': projectBase['sid'],
                                               'ProjectName': projectBase['ProjectName'],
                                               'PropertyID': projectBase['PropertyID'],
                                               'ProjectUUID': str(projectBase['ProjectUUID'])
                                           })
                result.append(presell_page_req)
        return result


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
                re_h = regex.compile(r'<[^>]+>', regex.S)
                return re_h.sub('', string)
            except:
                return ''

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') != 'ProjectInfo':
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')
        projectBase = response.meta.get('projectBase')
        OnSaleState = response.xpath('//span[contains(@class,"colorwht")]/text()').extract_first()

        projectBase['OnSaleState'] = OnSaleState
        projectBase['Selltel'] = response.xpath(
            '//font[text()="售楼电话："]/following-sibling::font/text()').extract_first()
        projectBase['ProjectAllrankvalue'] = response.xpath('//*[@id="allrankvalue1"]/text()').extract_first()
        projectBase['ProjectName'] = response.xpath(
            '//span[@class="buidname colordg"]/text()').extract_first()
        projectBase['ProjectAddress'] = response.xpath(
            '//strong[text()="楼盘地址："]/following-sibling::span[1]/@title').extract_first()
        projectBase['ProjectSellAddress'] = response.xpath(
            '//strong[text()="售楼地址："]/following-sibling::span[1]/text()').extract_first()
        projectBase['ProjectMainUnitType'] = response.xpath(
            '//strong[text()="主力户型："]/following-sibling::span[1]/text()').extract_first()
        projectBase['ProjectDecoration'] = response.xpath(
            '//strong[text()="装修状况："]/following-sibling::span[1]/text()').extract_first()
        projectBase['LandUse'] = response.xpath(
            '//strong[text()="物业类型："]/following-sibling::span[1]/text()').extract_first()
        projectBase['BuildingType'] = response.xpath(
            '//strong[text()="建筑形式："]/following-sibling::span[1]/text()').extract_first()
        projectBase['FloorAreaRatio'] = response.xpath(
            '//strong[text()="容积率："]/following-sibling::span[1]/text()').extract_first()
        projectBase['GreeningRate'] = response.xpath(
            '//strong[text()="绿化率："]/following-sibling::span[1]/text()').extract_first()

        projectBase['FloorArea'] = response.xpath(
            '//strong[text()="占地面积："]/following-sibling::span[1]/text()').extract_first()
        try:
            if 'java' in projectBase['FloorArea']:
                projectBase['FloorArea'] = ''
        except:
            pass
        projectBase['CompletionDate'] = response.xpath(
            '//strong[text()="竣工时间："]/following-sibling::span[1]/text()').extract_first()
        projectBase['TotalBuidlingArea'] = response.xpath(
            '//strong[text()="总建筑面积："]/following-sibling::span[1]/text()').extract_first()
        projectBase['HousingCount'] = response.xpath(
            '//strong[text()="总户数："]/following-sibling::span[1]/text()').extract_first()
        projectBase['LatestDeliversHouseDate'] = response.xpath(
            '//strong[text()="预计交付时间："]/following-sibling::span[1]/text()').extract_first()
        projectBase['ParkingInfo'] = response.xpath(
            '//strong[text()="车位信息："]/following-sibling::span[1]/text()').extract_first()
        projectBase['ManagementFees'] = response.xpath(
            '//strong[text()="物业费："]/following-sibling::span[1]/text()').extract_first()
        projectBase['ManagementCompany'] = response.xpath(
            '//strong[text()="物业公司："]/following-sibling::span[1]/text()').extract_first()
        projectBase['PropertyRightsDescription'] = response.xpath(
            '//strong[text()="产权年限："]/following-sibling::span[1]/text()').extract_first()
        projectBase['Developer'] = response.xpath(
            '//strong[text()="项目公司："]/following-sibling::span[1]/text()').extract_first()
        traffic_text = response.xpath('//div[text()="交通情况"]/following-sibling::div[1]/p/text()').extract()
        projectBase['TrafficSituation'] = remove_html_tag(traffic_text)
        ProjectSupporting_text = response.xpath('//div[text()="项目配套"]/following-sibling::div[1]/p/text()').extract()
        projectBase['ProjectSupporting'] = remove_html_tag(ProjectSupporting_text)
        ProjectIntro_text = response.xpath(
            '//div[text()="项目简介"]/following-sibling::div[1]/p/text()').extract_first()
        projectBase['ProjectIntro'] = remove_html_tag(ProjectIntro_text)
        PromotionName = response.xpath('//li[text()="推广名"]/following-sibling::li[1]/text()').extract_first()
        projectBase['PromotionName'] = PromotionName if PromotionName else ''
        result.append(projectBase)
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
        if response.meta.get('PageType') != 'PresellList':
            return result if result else []
        print('PresellListHandleMiddleware')
        sid = response.meta.get('sid')
        PropertyID = response.meta.get('PropertyID')
        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')

        presell_arr = response.xpath('//a[starts-with(@id,"presell_")]')
        # 获取预售证列表
        for element in presell_arr[1:]:
            PresellID = element.xpath('@id').extract_first().replace('presell_', '')
            PresellNO = element.xpath('text()').extract_first()

            PresellUUID = uuid.uuid3(uuid.NAMESPACE_DNS, ProjectUUID + PresellID)
            presellItem = PresellInfoItem()
            presellItem['PropertyID'] = PropertyID
            presellItem['ProjectUUID'] = ProjectUUID
            presellItem['ProjectName'] = ProjectName
            presellItem['PresellID'] = PresellID
            presellItem['PresellNO'] = PresellNO
            presellItem['PresellUUID'] = PresellUUID
            presellItem['sid'] = sid

            url = 'http://www.tmsf.com/newhouse/NewPropertyHz_createPresellInfo.jspx?sid={sid}&presellid={PresellID}&propertyid={propertyID}&_={timestamp}'
            api_req = Request(url=url.format(sid=presellItem['sid'], PresellID=presellItem['PresellID'],
                                             propertyID=presellItem['PropertyID'], timestamp=round(time.time())),
                              headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                              dont_filter=True,
                              meta={'PageType': 'PresellAPI', 'presellItem': presellItem})
            result.append(api_req)
        return result


class PresellAPIHandleMiddleware(object):
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
            if result:
                return result
            return []
        if response.meta.get('PageType') != 'PresellAPI':
            if result:
                return result
            return []
        print('PresellAPIHandleMiddleware')
        presellItem = response.meta.get('presellItem')

        jsonObj = json.loads(response.body_as_unicode())
        pre = jsonObj.get('pre')
        presell = jsonObj.get('presell')
        if presell:
            presellItem['PresellName'] = presell['presellname']
            presellItem['LssueDate'] = presell['applydate']
            presellItem['Applycorp'] = presell['applycorp']
            presellItem['LssuingAuthority'] = presell['sendcorp']
            presellItem['Bank'] = presell['bank']
            presellItem['BankAccount'] = presell['bankaccno']
            presellItem['OpeningDate'] = presell['openingdate']
            presellItem['ApprovalProjectName'] = presell['projname']
        if pre:
            presellItem['num'] = pre['num']
            presellItem['justnum'] = pre['justnum']
            presellItem['area'] = pre['area']
            presellItem['justarea'] = pre['justarea']
            presellItem['avanum'] = pre['avanum']
            presellItem['avaarea'] = pre['avaarea']
            presellItem['waitnum'] = pre['waitnum']
            presellItem['waitarea'] = pre['waitarea']
            presellItem['resideavanum'] = pre['resideavanum']
            presellItem['limitnum'] = pre['limitnum']
            presellItem['resideavaarea'] = pre['resideavaarea']
            presellItem['limitarea'] = pre['limitarea']
            presellItem['dealnum'] = pre['dealnum']
            presellItem['notnum'] = pre['notnum']
            presellItem['dealarea'] = pre['dealarea']
            presellItem['notarea'] = pre['notarea']
            presellItem['plannum'] = pre['plannum']
            presellItem['planarea'] = pre['planarea']
        result.append(presellItem)
        return result


class BuildingListHandleMiddleware(object):
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
            if result:
                return result
            return []
        if response.meta.get('PageType') != 'BuildingList':
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        sid = response.meta.get('sid')
        PropertyID = response.meta.get('PropertyID')
        PresellID = response.meta.get('PresellID')
        ProjectUUID = response.meta.get('ProjectUUID')
        PresellUUID = response.meta.get('PresellUUID')
        ProjectName = response.meta.get('ProjectName')
        PresellName = response.meta.get('PresellName')
        building_elements = response.xpath('//a[starts-with(@id,"building_")]')

        # 判断页面模板，富阳区的页面模板为分站
        m = response.xpath('//li[@id="siteother"]').extract()
        for element in building_elements[1:]:
            buildingItem = BuildingInfoItem()
            buildingItem['ProjectUUID'] = ProjectUUID
            buildingItem['PresellUUID'] = PresellUUID
            buildingItem['ProjectName'] = ProjectName
            buildingItem['PresellName'] = PresellName
            buildingItem['BuildingID'] = element.xpath('@id').extract_first().replace('building_', '')
            buildingItem['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                      str(buildingItem['PresellUUID']) + buildingItem['BuildingID'])
            buildingItem['BuildingName'] = element.xpath('text()').extract_first()
            result.append(buildingItem)

            if len(m) > 0:  # 分站
                url = 'http://www.tmsf.com/newhouse/property_pricesearch.htm'
                houseList_page = {
                    'source_url': url,
                    'method': 'POST',
                    'body': {
                        'sid': sid, 'propertyid': PropertyID, 'tid': '', 'presellid': PresellID,
                        'buildingid': buildingItem['BuildingID'],
                        'area': '', 'allprice': '', 'housestate': '', 'housetype': '', 'page': '1',
                    },
                    'meta': {'PageType': 'TemplateHouseList', 'sid': sid, 'PropertyID': PropertyID,
                             'PresellID': PresellID,
                             'BuildingID': buildingItem['BuildingID'],
                             'BuildingUUID': str(buildingItem['BuildingUUID']),
                             'ProjectUUID': ProjectUUID, 'PresellUUID': PresellUUID,
                             'curPage': 1}}
                # houseList_page_json = json.dumps(houseList_page, sort_keys=True)
                # r.sadd(self.settings.get('REDIS_KEY'), houseList_page_json)
                result.append(Request(houseList_page.get('source_url'), method=houseList_page.get('method'),
                                      body=urlparse.urlencode(houseList_page.get('body')),
                                      meta=houseList_page.get('meta')))

            else:
                building_req_url = 'http://www.tmsf.com/newhouse/property_{sid}_{propertyID}_price.htm?isopen=&presellid={presellID}&buildingid={buildingID}&area=&allprice=&housestate=&housetype=&page={page}'
                buildingListURL = building_req_url.format(sid=sid,
                                                          propertyID=PropertyID,
                                                          presellID=PresellID,
                                                          buildingID=buildingItem['BuildingID'],
                                                          page=1)
                houseList_req = Request(url=buildingListURL,
                                        meta={'PageType': 'HouseList',
                                              'curPage': 1,
                                              'sid': sid,
                                              'BuildingID': buildingItem['BuildingID'],
                                              'BuildingName': buildingItem['BuildingName'],
                                              'PropertyID': PropertyID,
                                              'PresellID': PresellID,
                                              'ProjectUUID': buildingItem['ProjectUUID'],
                                              'ProjectName': buildingItem['ProjectName'],
                                              'PresellUUID': buildingItem['PresellUUID'],
                                              'PresellName': buildingItem['PresellName'],
                                              'BuildingUUID': buildingItem['BuildingUUID']})
                result.append(houseList_req)
        return result


class TemplateHouseListHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        def get_total_page(response):
            total_page_count = 1
            try:
                t = response.xpath('//*[@id="yf_four"]/div/div[1]/text()').extract_first()
                t = t.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
                res = regex.search(r'页数1/(?<page>.+)总', t)
                total_page_count = int(res.group(1))
            except:
                pass
            return total_page_count

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

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') != 'TemplateHouseList':
            if result:
                return result
            return []
        print('TemplateHouseListHandleMiddleware')
        sid = response.meta.get('sid')
        PropertyID = response.meta.get('PropertyID')
        PresellID = response.meta.get('PresellID')
        BuildingID = response.meta.get('BuildingID')
        ProjectUUID = response.meta.get('ProjectUUID')
        PresellUUID = response.meta.get('PresellUUID')
        BuildingUUID = response.meta.get('BuildingUUID')
        curPage = response.meta.get('curPage')
        if curPage and curPage == 1:
            total_page = get_total_page(response)
            url = 'http://www.tmsf.com/newhouse/property_pricesearch.htm'
            req_list = []
            for page in range(1, total_page + 1):
                houseList_page = {
                    'source_url': url, 'method': 'POST',
                    'body': {
                        'sid': sid, 'propertyid': PropertyID, 'tid': 'price', 'presellid': PresellID,
                        'buildingid': BuildingID,
                        'area': '', 'allprice': '', 'housestate': '', 'housetype': '', 'page': str(page),
                    },
                    'meta': {'PageType': 'TemplateHouseList', 'PropertyID': PropertyID, 'PresellID': PresellID,
                             'ProjectUUID': ProjectUUID, 'PresellUUID': PresellUUID, 'BuildingUUID': BuildingUUID}}
                # houseList_page_json = json.dumps(houseList_page, sort_keys=True)
                # r.sadd(self.settings.get('REDIS_KEY'), houseList_page_json)
                req_list.append(Request(url, body=urlparse.urlencode(houseList_page.get('body')),
                                        method=houseList_page.get('method'), meta=houseList_page.get('meta')))
            result.extend(req_list)
        else:
            tr_arr = response.xpath('//td[contains(text(),"幢号")]/../following-sibling::tr')
            for tr in tr_arr:
                houseBuildingArea_css_arr = tr.xpath('td[4]/a/div/span/@class').extract()
                houseBuildingArea = get_number(houseBuildingArea_css_arr)
                houseInnerArea_css_arr = tr.xpath('td[5]/a/div/span/@class').extract()
                houseInnerArea = get_number(houseInnerArea_css_arr)
                roomRate_css_arr = tr.xpath('td[6]/a/div/span/@class').extract()
                roomRate = get_number(roomRate_css_arr)
                roughPrice_css_arr = tr.xpath('td[7]/a/div/span/@class').extract()
                roughPrice = get_number(roughPrice_css_arr)
                price_css_arr = tr.xpath('td[9]/a/div/span/@class').extract()
                price = get_number(price_css_arr)

                houseInfoItem = HouseInfoItem()
                houseInfoItem['ProjectUUID'] = ProjectUUID
                houseInfoItem['PresellUUID'] = PresellUUID
                houseInfoItem['BuildingUUID'] = BuildingUUID

                if houseBuildingArea:
                    unit = tr.xpath('td[4]/a/div/text()').extract_first()
                    houseInfoItem['HouseBuildingArea'] = houseBuildingArea + unit
                if houseInnerArea:
                    unit = tr.xpath('td[5]/a/div/text()').extract_first()
                    houseInfoItem['HouseInnerArea'] = houseInnerArea + unit
                if roomRate:
                    unit = tr.xpath('td[6]/a/div/text()').extract_first()
                    houseInfoItem['RoomRate'] = roomRate + unit
                if roughPrice:
                    unit = tr.xpath('td[7]/a/div/text()').extract_first()
                    houseInfoItem['RoughPrice'] = roughPrice + unit  # 申请毛坯单价
                if price:
                    unit = tr.xpath('td[9]/a/div/text()').extract_first()
                    houseInfoItem['HousePrice'] = price + unit
                try:
                    unitName = tr.xpath('td[2]/a/div/text()').extract_first()
                    houseInfoItem['UnitName'] = '' if unitName.startwith('-') else unitName
                except:
                    houseInfoItem['UnitName'] = ''
                houseInfoItem['BuildingName'] = tr.xpath('td[1]/a/text()').extract_first()
                href = tr.xpath('td[3]/a/@href').extract_first()
                houseInfoItem['HouseNO'] = tr.xpath('td[3]/a/div/text()').extract_first()
                req = Request(url='http://www.tmsf.com' + href,
                              headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                              dont_filter=True,
                              meta={'PageType': 'TemplateHouseInfo', 'houseInfoItem': houseInfoItem})
                result.append(req)
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
                import traceback
                traceback.print_exc()
                return None

        def get_houseList_total_page(response):
            total_page = 1
            try:
                t = regex.search(r'页数 1/(\d+)\t', response.body_as_unicode())
                total_page = int(t.group(1))
            except:
                pass
            return total_page

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') != 'HouseList':
            if result:
                return result
            return []
        print('HouseListHandleMiddleware')
        req_list = []
        curPage = response.meta.get('curPage')
        sid = response.meta.get('sid')
        PropertyID = response.meta.get('PropertyID')
        PresellID = response.meta.get('PresellID')
        BuildingID = response.meta.get('BuildingID')
        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')
        PresellName = response.meta.get('PresellName')
        BuildingName = response.meta.get('BuildingName')
        PresellUUID = response.meta.get('PresellUUID')
        BuildingUUID = response.meta.get('BuildingUUID')
        if curPage and curPage == 1:
            totla_page = get_houseList_total_page(response)
            req_url = 'http://www.tmsf.com/newhouse/property_{sid}_{propertyID}_price.htm?isopen=&presellid={presellID}&buildingid={buildingID}&area=&allprice=&housestate=&housetype=&page={page}'
            for page in range(1, totla_page + 1):
                # req = Request(url = req_url.format(sid = sid, propertyID = PropertyID, presellID = PresellID,
                #                                    buildingID = BuildingID, page = str(page)),
                #               headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                #               dont_filter = True,
                #               meta = {'PageType': 'HouseList',
                #                       'PropertyID': PropertyID,
                #                       'PresellID': PresellID,
                #                       'BuildingID': BuildingID,
                #                       'ProjectUUID': ProjectUUID,
                #                       'PresellUUID': PresellUUID,
                #                       'BuildingUUID': BuildingUUID})
                # req_list.append(req)
                houseList_base = {
                    'source_url': req_url.format(sid=sid, propertyID=PropertyID, presellID=PresellID,
                                                 buildingID=BuildingID, page=str(page)),
                    'meta': {
                        'PageType': 'HouseList',
                        'PropertyID': PropertyID,
                        'PresellID': PresellID,
                        'BuildingID': BuildingID,
                        'ProjectUUID': str(ProjectUUID),
                        'BuildingName': BuildingName,
                        'ProjectName': ProjectName,
                        'PresellName': PresellName,
                        'PresellUUID': str(PresellUUID),
                        'BuildingUUID': str(BuildingUUID),
                    }
                }
                # houseList_base_json = json.dumps(houseList_base, sort_keys=True)
                # r.sadd(self.settings.get('REDIS_KEY'), houseList_base_json)
                result.append(Request(houseList_base.get('source_url'), meta=houseList_base.get('meta')))

        tr_arr = response.xpath('//*[@id="search"]/following-sibling::div/table/tbody/tr')
        for tr in tr_arr:

            buildingName = tr.xpath('td[1]/a/text()').extract_first()
            houseNO = tr.xpath('td[2]/a/div/text()').extract_first()
            href = tr.xpath('td[2]/a/@href').extract_first()
            unitName = tr.xpath('td[1]/a/text()').extract_first()
            if unitName:
                unitName = unitName[unitName.rindex('幢') + 1:]
            else:
                unitName = ''
            houseBuildingArea_css_arr = tr.xpath('td[3]/a/div/span/@class').extract()
            houseBuildingArea = get_number(houseBuildingArea_css_arr)
            houseInnerArea_css_arr = tr.xpath('td[4]/a/div/span/@class').extract()
            houseInnerArea = get_number(houseInnerArea_css_arr)
            roomRate_css_arr = tr.xpath('td[5]/a/div/span/@class').extract()
            roomRate = get_number(roomRate_css_arr)
            roughPrice_css_arr = tr.xpath('td[6]/a/div/span/@class').extract()
            roughPrice = get_number(roughPrice_css_arr)
            price_css_arr = tr.xpath('td[8]/a/div/span/@class').extract()
            price = get_number(price_css_arr)

            houseInfoItem = HouseInfoItem()
            houseInfoItem['ProjectUUID'] = ProjectUUID
            houseInfoItem['ProjectName'] = ProjectName
            houseInfoItem['PresellUUID'] = PresellUUID
            houseInfoItem['PresellName'] = PresellName
            houseInfoItem['BuildingUUID'] = BuildingUUID
            houseInfoItem['BuildingName'] = BuildingName

            houseInfoItem['BuildingName'] = buildingName  # 栋号
            houseInfoItem['HouseNO'] = houseNO  # 房号
            houseInfoItem['UnitName'] = unitName  # 单元
            if houseBuildingArea:
                unit = tr.xpath('td[3]/a/div/text()').extract_first()
                houseInfoItem['HouseBuildingArea'] = houseBuildingArea + unit
            if houseInnerArea:
                unit = tr.xpath('td[4]/a/div/text()').extract_first()
                houseInfoItem['HouseInnerArea'] = houseInnerArea + unit
            if roomRate:
                unit = tr.xpath('td[5]/a/div/text()').extract_first()
                houseInfoItem['RoomRate'] = roomRate + unit
            if roughPrice:
                unit = tr.xpath('td[6]/a/div/text()').extract_first()
                houseInfoItem['RoughPrice'] = roughPrice + unit  # 申请毛坯单价
            if price:
                unit = tr.xpath('td[8]/a/div/text()').extract_first()
                houseInfoItem['HousePrice'] = price + unit
            houseInfo_req = Request(url='http://www.tmsf.com' + href,
                                    headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                    dont_filter=True,
                                    meta={'PageType': 'HouseInfo',
                                          'houseInfoItem': houseInfoItem})
            req_list.append(houseInfo_req)
        result.extend(req_list)
        return result


class HouseInfoHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        def get_ssnumber(classTextArr, ssnumberOrNumber):
            ssnumber = {'ssnumberzero': '0', 'ssnumberone': '1', 'ssnumbertwo': '2', 'ssnumberthree': '3',
                        'ssnumberfour': '4', 'ssnumberfive': '5', 'ssnumbersix': '6', 'ssnumberseven': '7',
                        'ssnumbereight': '8', 'ssnumbernine': '9', 'ssnumberdor': '.'}
            number = {'numberzero': '0', 'numberone': '1', 'numbertwo': '2', 'numberthree': '3', 'numberfour': '4',
                      'numberfive': '5', 'numbersix': '6', 'numberseven': '7', 'numbereight': '8', 'numbernine': '9',
                      'numberdor': '.'}
            price = ''
            for key in classTextArr:
                if ssnumberOrNumber == 'ssnumber':
                    price += ssnumber[key]
                else:
                    price += number[key]
            try:
                return price
            except:
                return None

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseInfo', 'TemplateHouseInfo'):
            if result:
                return result
            return []
        print('HouseInfoHandleMiddleware')
        houseInfoItem = response.meta.get('houseInfoItem')
        houseInfoItem['HouseURL'] = response.url
        houseInfoItem['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                str(houseInfoItem['BuildingUUID']) + houseInfoItem['HouseURL'])
        # 判断页面模板
        m = response.xpath('//li[@id="siteother"]').extract()
        if len(m) == 0:
            houseInfoItem['HouseState'] = response.xpath('//strong[text()="当前状态："]/../text()').extract_first()
            houseInfoItem['HouseType'] = response.xpath('//strong[text()="户　　型："]/../text()').extract_first()
            try:
                floor_text = response.xpath('//strong[text()="所在层数："]/../text()').extract_first()
                houseInfoItem['HouseFloor'] = floor_text[:floor_text.index('（')]
                houseInfoItem['BuildingFloor'] = floor_text[floor_text.index('（') + 1:-1].replace('）', '')
            except:
                pass
            houseInfoItem['HouseLocated'] = response.xpath('//strong[text()="房屋坐落："]/../text()').extract_first()
            houseInfoItem['HouseStructure'] = response.xpath('//strong[text()="房屋结构："]/../text()').extract_first()
            houseInfoItem['HouseUsage'] = response.xpath('//strong[text()="房屋用途："]/../text()').extract_first()

            houseManagementFees_text = response.xpath('//strong[contains(text(),"费：")]/../text()').extract_first()
            if houseManagementFees_text:
                houseInfoItem['HouseManagementFees'] = houseManagementFees_text
            elif len(response.xpath('//strong[contains(text(),"费：")]/../span/@class').extract()) > 0:
                HouseManagementFees = get_ssnumber(
                    response.xpath('//strong[contains(text(),"费：")]/../span/@class').extract(), 'number')
                houseInfoItem['HouseManagementFees'] = HouseManagementFees
            houseInfoItem['HouseOrientation'] = response.xpath('//strong[text()="朝　　向："]/../text()').extract_first()
            houseInfoItem['DeclarationTime'] = response.xpath('//strong[text()="申报时间："]/../text()').extract_first()
        else:
            houseInfoItem['HouseState'] = response.xpath(
                '//strong[text()="当前状态"]/../following-sibling::td[1]/text()').extract_first()
            houseInfoItem['HouseType'] = response.xpath(
                '//strong[text()="户 型"]/../following-sibling::td[1]/text()').extract_first()
            try:
                floor_text = response.xpath(
                    '//strong[text()="所在层数"]/../following-sibling::td[1]/text()').extract_first()
                houseInfoItem['HouseFloor'] = floor_text[:floor_text.index('（')]
                houseInfoItem['BuildingFloor'] = floor_text[floor_text.index('（') + 1:floor_text.rindex('）')]
            except:
                pass
            houseInfoItem['HouseLocated'] = response.xpath(
                '//strong[text()="房屋坐落"]/../following-sibling::td[1]/text()').extract_first()
            houseInfoItem['HouseStructure'] = response.xpath(
                '//strong[text()="房屋结构"]/../following-sibling::td[1]/text()').extract_first()
            houseInfoItem['HouseUsage'] = response.xpath(
                '//strong[text()="房屋用途"]/../following-sibling::td[1]/text()').extract_first()
            houseInfoItem['HouseManagementFees'] = response.xpath(
                '//strong[text()="物 业 费"]/../following-sibling::td[1]/text()').extract_first()
            houseInfoItem['HouseOrientation'] = response.xpath(
                '//strong[text()="朝 向"]/../following-sibling::td[1]/text()').extract_first()
            houseInfoItem['DeclarationTime'] = response.xpath(
                '//strong[text()="申报时间"]/../following-sibling::td[1]/text()').extract_first()
        result.append(houseInfoItem)

        return result
