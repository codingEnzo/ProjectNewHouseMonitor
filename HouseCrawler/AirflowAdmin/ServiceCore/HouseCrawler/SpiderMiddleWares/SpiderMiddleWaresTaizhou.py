# coding = utf-8
import json
import logging
import sys
import uuid
import regex
import time
from redis import Redis
from scrapy import Request
from HouseNew.models import *
from HouseCrawler.Items.ItemsTaizhou import *

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
logger = logging.getLogger(__name__)

debug = False



def get_number(arr, type):
    if len(arr) == 0:
        return None
    number = {'numbzero': '0', 'numbone': '1', 'numbtwo': '2', 'numbthree': '3', 'numbfour': '4',
              'numbfive': '5', 'numbsix': '6', 'numbseven': '7', 'numbeight': '8', 'numbnine': '9',
              'numbdor': '.'}
    ss_number = {'numbbzero': '0', 'numbbone': '1', 'numbtwo': '2', 'numbbthree': '3', 'numbbfour': '4',
                 'numbbfive': '5', 'numbbsix': '6', 'numbbseven': '7', 'numbbeight': '8', 'numbbnine': '9',
                 'numbbdor': '.'}
    try:
        value = ''
        if type == 'number':
            for key in arr:
                value += number[key]
        elif type == 'ss_number':
            for key in arr:
                value += ss_number[key]
        return value
    except:
        return None


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
                t_arr = t.split('/')
                total_page = int(t_arr[1])
            except:
                import traceback
                traceback.print_exc()
            return total_page

        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectBase':
            return result if result else []
        # print('ProjectBaseHandleMiddleware')
        result = list(result)
        if response.request.method == 'GET':
            total_page = get_totla_page(response)
            for page in range(1, total_page + 1):
                req_dict = {'keytype': '1', 'keyword': '', 'sid': '', 'districtid': '', 'areaid': '', 'dealprice': '',
                            'propertystate': '', 'propertytype': '', 'ordertype': '', 'priceorder': '', 'openorder': '',
                            'page': str(page)}
                project_base_req = Request(url = 'http://tz.tmsf.com/newhouse/property_searchall.htm',
                                           headers = self.settings.get('POST_DEFAULT_REQUEST_HEADERS'),
                                           dont_filter = True,
                                           method = 'POST',
                                           body = urlparse.urlencode(req_dict),
                                           meta = {'PageType': 'ProjectBase'})
                result.append(project_base_req)
        else:
            req_list = []
            div_arr = response.xpath('//div[@class="build_des"]')
            for div in div_arr:
                projectBaseItem = ProjectBaseItem()
                try:
                    s = div.xpath('div[2]/div[2]/p/text()').extract_first()
                    t = regex.search(r'\[(?<region>.*)\]', s)
                    projectBaseItem['DistrictName'] = t.group(1)
                except:
                    projectBaseItem['DistrictName'] = ''
                projectBaseItem['ProjectName'] = div.xpath(
                        'div[2]/h3/a[starts-with(@href,"/newhouse/property_")]/text()').extract_first()
                url = 'http://tz.tmsf.com' + div.xpath(
                        'div[2]/h3/a[starts-with(@href,"/newhouse/property_")]/@href').extract_first()
                t = regex.search(r'property_(?<sid>.+)_(?<propertyID>.+)_info.htm', url)
                projectBaseItem['sid'] = t.group(1)
                projectBaseItem['PropertyID'] = t.group(2)
                projectBaseItem['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, url)
                s = div.xpath('div[1]/div[1]/p[last()]').re(r'.*')
                if s:
                    s = ''.join(s)
                    s = s.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
                    t = regex.search(
                            r'<pclass="ash1">(?<saleCount>\d+)<fontclass="green1">可售</font>\|(?<totalCount>\d+)总套数</p>',
                            s)
                    projectBaseItem['OnsoldAmount'] = t.group(1)
                    projectBaseItem['ApprovalPresaleAmount'] = t.group(2)
                price_css_arr = div.xpath('div[2]/div[6]/p[1]/span/@class').extract()
                if len(price_css_arr) == 0:
                    projectBaseItem['LatelyAveragePrice'] = div.xpath('div[2]/div[6]/p[1]/text()').extract_first()
                else:
                    LatelyAveragePrice = get_number(price_css_arr, 'ss_number')
                    projectBaseItem['LatelyAveragePrice'] = LatelyAveragePrice if LatelyAveragePrice else ''
                price_css_arr = div.xpath(' div[2]/div[6]/p[2]/span/@class').extract()
                CumulativeSoldAveragePrice = get_number(price_css_arr, 'number')
                projectBaseItem[
                    'CumulativeSoldAveragePrice'] = CumulativeSoldAveragePrice if CumulativeSoldAveragePrice else ''
                req = Request(url = url,
                              dont_filter = True,
                              headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                              meta = {'PageType': 'ProjectInfo', 'projectBaseItem': projectBaseItem})
                req_list.append(req)
            result.extend(req_list)
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
        projectBaseItem = response.meta.get('projectBaseItem')
        projectBaseItem['SourceUrl'] = response.url
        try:
            css_arr = response.xpath('//strong[text()="非住宅均价"]/../span[starts-with(@class,"num")]/@class').extract()
            if len(css_arr) > 0:
                AveragePrice = get_number(css_arr, 'ss_number')
                projectBaseItem['AveragePrice'] = AveragePrice if AveragePrice else ''
            else:
                projectBaseItem['AveragePrice'] = response.xpath(
                    '//span[starts-with(text(),"非住宅")]/text()').extract_first().replace('非住宅', '')
        except:
            projectBaseItem['AveragePrice'] = ''

        projectBaseItem['OnSaleState'] = response.xpath('//span[contains(@class,"colorwht")]/text()').extract_first()
        projectBaseItem['Selltel'] = response.xpath(
                '//font[text()="售楼电话："]/following-sibling::font/text()').extract_first()
        projectBaseItem['ProjectAllrankvalue'] = response.xpath('//*[@id="allrankvalue1"]/text()').extract_first()

        projectBaseItem['ProjectAddress'] = response.xpath(
                '//strong[text()="楼盘地址："]/following-sibling::span[1]/@title').extract_first()

        projectBaseItem['ProjectMainUnitType'] = response.xpath(
                '//strong[text()="主力户型："]/following-sibling::span[1]/@title').extract_first()
        projectBaseItem['ProjectDecoration'] = response.xpath('//strong[text()="装修状况："]/../text()').extract_first()
        projectBaseItem['LandUse'] = response.xpath(
                '//strong[text()="物业类型："]/following-sibling::span[1]/text()').extract_first()
        projectBaseItem['BuildingType'] = response.xpath('//strong[text()="建筑形式："]/../text()').extract_first()
        FloorAreaRatio = response.xpath('//span[text()="容 积 率："]/../text()').extract_first()
        projectBaseItem['FloorAreaRatio'] = FloorAreaRatio if FloorAreaRatio else ''
        GreeningRate = response.xpath('//span[text()="绿 化 率："]/../text()').extract_first()
        projectBaseItem['GreeningRate'] = GreeningRate if GreeningRate else ''
        FloorArea = response.xpath('//span[text()="占地面积："]/../text()').extract_first()
        projectBaseItem['FloorArea'] = FloorArea if FloorArea else ''
        if projectBaseItem['FloorArea'] and 'java' in projectBaseItem['FloorArea']:
            projectBaseItem['FloorArea'] = ''
        # projectBaseItem['CompletionDate'] = response.xpath(
        #         '//strong[text()="竣工时间："]/following-sibling::span[1]/text()').extract_first()
        TotalBuidlingArea = response.xpath('//span[text()="总建筑面积："]/../text()').extract_first()
        projectBaseItem['TotalBuidlingArea'] = TotalBuidlingArea if TotalBuidlingArea else ''
        # projectBaseItem['HousingCount'] = response.xpath(
        #         '//strong[text()="总户数："]/following-sibling::span[1]/text()').extract_first()
        LatestDeliversHouseDate = response.xpath(
                '//span[text()="预计交付时间："]/../text()').extract_first()
        projectBaseItem['LatestDeliversHouseDate'] = LatestDeliversHouseDate if LatestDeliversHouseDate else ''
        ParkingInfo = response.xpath('//span[text()="车位信息："]/../text()').extract_first()
        projectBaseItem['ParkingInfo'] = ParkingInfo if ParkingInfo else ''
        ManagementFees = response.xpath('//span[text()="物 业 费："]/../text()').extract_first()
        projectBaseItem['ManagementFees'] = ManagementFees if ManagementFees else ''
        ManagementCompany = response.xpath('//span[text()="物业公司："]/../text()').extract_first()
        projectBaseItem['ManagementCompany'] = ManagementCompany if ManagementCompany else ''
        PropertyRightsDescription = response.xpath(
                '//span[text()="产权年限："]/../text()').extract_first()
        projectBaseItem['PropertyRightsDescription'] = PropertyRightsDescription if PropertyRightsDescription else ''

        projectBaseItem['Developer'] = response.xpath('//strong[text()="项目公司："]/../text()').extract_first()
        ProjectIntro_text = response.xpath('//div[@class="lpinfodtxt"]').re(r'.*')
        projectBaseItem['ProjectIntro'] = remove_html_tag(ProjectIntro_text)

        result.append(projectBaseItem)

        # 判断下有没有一房一价的链接
        pre_href = response.xpath('//*[@id="buildnavbar"]/a[contains(@href,"_price.htm")]/@href').extract_first()
        if pre_href:
            pre_href = 'http://tz.tmsf.com' + pre_href
            req = Request(url = pre_href,
                          headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                          dont_filter = True,
                          meta = {'PageType': 'PreselList',
                                  'sid': projectBaseItem['sid'],
                                  'ProjectUUID': str(projectBaseItem['ProjectUUID']),
                                  'PropertyID': projectBaseItem['PropertyID'],
                                  'ProjectName':projectBaseItem['ProjectName']})
            result.append(req)
        return result


class PreselListHandleMiddleware(object):
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
        if response.meta.get('PageType') != 'PreselList':
            return result if result else []
        # print('PreselListHandleMiddleware')
        sid = response.meta.get('sid')
        PropertyID = response.meta.get('PropertyID')
        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')

        presell_arr = response.xpath('//a[starts-with(@id,"presell_")]')

        # 获取预售证列表
        for element in presell_arr[1:]:
            presellInfoItem = PresellInfoItem()
            presellInfoItem['ProjectUUID'] = ProjectUUID
            presellInfoItem['ProjectName'] = ProjectName
            presellInfoItem['sid'] = sid
            presellInfoItem['PresellID'] = element.xpath('@id').extract_first().replace('presell_', '')
            presellInfoItem['PresalePermitNumber'] = element.xpath('text()').extract_first()
            presellInfoItem['PresellUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                        ProjectUUID + presellInfoItem['PresellID'])

            url = 'http://tz.tmsf.com/newhouse/NewPropertyHz_createPresellInfo.jspx?sid={sid}&presellid={presellID}&propertyid={propertyID}&_={timestamp}'
            req = Request(
                    url = url.format(sid = sid, propertyID = PropertyID, presellID = presellInfoItem['PresellID'],
                                     timestamp = round(time.time())),
                    dont_filter = True,
                    headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                    meta = {'PageType': 'PresellInfo', 'presellInfoItem': presellInfoItem})
            result.append(req)

            # 发起请求获取预售证下的楼栋
            buildingList_url = 'http://tz.tmsf.com/newhouse/property_{sid}_{propertyID}_price.htm?isopen=1&presellid={presellID}&buildingid=&area=&allprice=&housestate=&housetype=&page=1'
            buildingList_req = Request(
                url = buildingList_url.format(sid = sid, propertyID = PropertyID, presellID = presellInfoItem['PresellID']),
                headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                meta = {'PageType': 'BuildingList',
                        'PropertyID': PropertyID,
                        'ProjectName': ProjectName,
                        'PresalePermitNumber': presellInfoItem['PresalePermitNumber'],
                        'sid': sid,
                        'PresellID': presellInfoItem['PresellID'],
                        'ProjectUUID': ProjectUUID,
                        'PresellUUID': str(presellInfoItem['PresellUUID'])})
            result.append(buildingList_req)

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
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'PresellInfo':
            return result if result else []
        # print('PresellInfoHandleMiddleware')
        result = list(result)
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
            openingprice = presell['openingprice']
            presellInfoItem['OpeningPrice'] = str(openingprice) if openingprice else ''
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


class BuildingListHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'BuildingList':
            return result if result else []
        # print('BuildingListHandleMiddleware')
        result = list(result)
        sid = response.meta.get('sid')
        ProjectUUID = response.meta.get('ProjectUUID')
        PresellUUID = response.meta.get('PresellUUID')
        PropertyID = response.meta.get('PropertyID')
        ProjectName = response.meta.get('ProjectName')
        PresellID = response.meta.get('PresellID')
        PresalePermitNumber = response.meta.get('PresalePermitNumber')

        building_elements = response.xpath('//a[starts-with(@id,"building_")]')
        building_req_url = 'http://tz.tmsf.com/newhouse/property_{sid}_{propertyID}_price.htm?isopen=&presellid={presellID}&buildingid={buildingID}&area=&allprice=&housestate=&housetype='
        req_list = []
        for element in building_elements[1:]:
            buildingItem = BuildingInfoItem()
            buildingItem['ProjectUUID'] = ProjectUUID
            buildingItem['PresellUUID'] = PresellUUID
            buildingItem['ProjectName'] = ProjectName
            buildingItem['PresalePermitNumber'] = PresalePermitNumber
            buildingItem['BuildingID'] = element.xpath('@id').extract_first().replace('building_', '')
            buildingItem['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                      str(buildingItem['PresellUUID']) + buildingItem['BuildingID'])
            buildingItem['BuildingName'] = element.xpath('text()').extract_first()
            result.append(buildingItem)

            buildingURL = building_req_url.format(sid = sid,
                                                  propertyID = PropertyID,
                                                  presellID = PresellID,
                                                  buildingID = buildingItem['BuildingID']) + '&page={curPage}'
            houseList_req = Request(url = buildingURL.format(curPage = '1'),
                                    headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                    dont_filter = True,
                                    meta = {'PageType': 'HouseList',
                                            'curPage': '1',
                                            'buildingURL': buildingURL,
                                            'ProjectUUID': buildingItem['ProjectUUID'],
                                            'PresellUUID': buildingItem['PresellUUID'],
                                            'BuildingUUID': str(buildingItem['BuildingUUID']),
                                            'ProjectName':ProjectName,
                                            'PresalePermitNumber':PresalePermitNumber,})
            req_list.append(houseList_req)
        result.extend(req_list)
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
        def get_houseList_total_page(response):
            total_page = 1;
            try:
                t = regex.search(r'页数 1/(\d+)\t', response.body_as_unicode())
                total_page = int(t.group(1))
            except:
                import traceback
                traceback.print_exc()
            return total_page

        def get_houseList_number(classTextArr):
            number = {'numberzero': '0', 'numberone': '1', 'numbertwo': '2', 'numberthree': '3', 'numberfour': '4',
                      'numberfive': '5', 'numbersix': '6', 'numberseven': '7', 'numbereight': '8', 'numbernine': '9',
                      'numberdor': '.'}
            value = ''
            for key in classTextArr:
                value += number[key]
            try:
                return value
            except:
                return None

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'HouseList':
            return result if result else []
        # print('HouseListHandleMiddleware')
        curPage = response.meta.get('curPage')
        ProjectUUID = response.meta.get('ProjectUUID')
        PresellUUID = response.meta.get('PresellUUID')
        BuildingUUID = response.meta.get('BuildingUUID')
        ProjectName = response.meta.get('ProjectName')
        PresalePermitNumber = response.meta.get('PresalePermitNumber')

        if curPage:
            buildingURL = response.meta.get('buildingURL')
            totla_page = get_houseList_total_page(response)
            for page in range(1, totla_page + 1):
                req = Request(url = buildingURL.format(curPage = str(page)),
                              headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                              dont_filter = True,
                              meta = {'PageType': 'HouseList',
                                      'ProjectUUID': ProjectUUID,
                                      'PresellUUID': PresellUUID,
                                      'BuildingUUID': BuildingUUID})
                result.append(req)
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
            houseBuildingArea = get_houseList_number(houseBuildingArea_css_arr)
            houseInnerArea_css_arr = tr.xpath('td[4]/a/div/span/@class').extract()
            houseInnerArea = get_houseList_number(houseInnerArea_css_arr)
            roomRate_css_arr = tr.xpath('td[5]/a/div/span/@class').extract()
            roomRate = get_houseList_number(roomRate_css_arr)
            roughPrice_css_arr = tr.xpath('td[6]/a/div/span/@class').extract()
            roughPrice = get_houseList_number(roughPrice_css_arr)

            houseInfoItem = HouseInfoItem()
            houseInfoItem['ProjectUUID'] = ProjectUUID
            houseInfoItem['PresellUUID'] = PresellUUID
            houseInfoItem['BuildingUUID'] = BuildingUUID
            houseInfoItem['ProjectName'] = ProjectName
            houseInfoItem['PresalePermitNumber'] = PresalePermitNumber
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
            houseInfo_req = Request(url = 'http://tz.tmsf.com' + href,
                                    dont_filter = True,
                                    headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                    meta = {'PageType': 'HouseInfo',
                                            'houseInfoItem': houseInfoItem})
            result.append(houseInfo_req)
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
            try:
                value = ''
                for key in classTextArr:
                    if ssnumberOrNumber == 'ssnumber':
                        value += ssnumber[key]
                    else:
                        value += number[key]
                return value
            except:
                return None

        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'HouseInfo':
            return result if result else []
        # print('HouseInfoHandleMiddleware')
        result = list(result)
        houseInfoItem = response.meta.get('houseInfoItem')
        houseInfoItem['SourceUrl'] = response.url
        houseInfoItem['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                str(houseInfoItem['BuildingUUID']) + houseInfoItem['SourceUrl'])
        # 判断页面模板
        m = response.xpath('//li[@id="siteother"]').extract()
        if len(m) == 0:

            TotalPrice_css_arr = response.xpath('//strong[text()="总　　价："]/../span/@class').extract()
            if len(TotalPrice_css_arr) == 0:
                houseInfoItem['TotalPrice'] = response.xpath('//strong[text()="总　　价："]/../text()').extract_first()
            else:
                TotalPrice = get_ssnumber(TotalPrice_css_arr, 'ssnumber')
                if TotalPrice:
                    unitName = response.xpath('//strong[text()="总　　价："]/../text()').extract_first()
                    houseInfoItem['TotalPrice'] = TotalPrice + unitName if TotalPrice else ''
            houseInfoItem['HouseState'] = response.xpath('//strong[text()="当前状态："]/../text()').extract_first()
            houseInfoItem['HouseType'] = response.xpath('//strong[text()="户　　型："]/../text()').extract_first()
            try:
                floor_text = response.xpath('//strong[text()="所在层数："]/../text()') \
                    .extract_first().replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
                houseInfoItem['FloorCount'] = floor_text[:floor_text.index('（')]
                houseInfoItem['BuildingFloor'] = floor_text[floor_text.index('（') + 1:-1]
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
            houseInfoItem['Toward'] = response.xpath('//strong[text()="朝　　向："]/../text()').extract_first()
            houseInfoItem['DeclarationTime'] = response.xpath('//strong[text()="申报时间："]/../text()').extract_first()
        else:
            houseInfoItem['HouseState'] = response.xpath(
                    '//strong[text()="当前状态"]/../following-sibling::td[1]/text()').extract_first()
            houseInfoItem['HouseType'] = response.xpath(
                    '//strong[text()="户 型"]/../following-sibling::td[1]/text()').extract_first()
            try:
                floor_text = response.xpath(
                        '//strong[text()="所在层数"]/../following-sibling::td[1]/text()') \
                    .extract_first().extract_first().replace(' ', '').replace('\r', '').replace('\n', '').replace('\t',
                                                                                                                  '')
                houseInfoItem['FloorCount'] = floor_text[:floor_text.index('（')]
                houseInfoItem['BuildingFloor'] = floor_text[floor_text.index('（') + 1:-1]
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
            houseInfoItem['Toward'] = response.xpath(
                    '//strong[text()="朝 向"]/../following-sibling::td[1]/text()').extract_first()
            houseInfoItem['DeclarationTime'] = response.xpath(
                    '//strong[text()="申报时间"]/../following-sibling::td[1]/text()').extract_first()
        result.append(houseInfoItem)

        return result
