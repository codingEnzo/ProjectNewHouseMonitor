# coding = utf-8
import json
import logging
import sys
import traceback
import uuid

import regex
from HouseCrawler.Items.ItemsQingDao import *
from scrapy import Request

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
        def get_totla_page(string):
            total_page = 1
            if debug or not string:
                return 1
            try:
                t = regex.search(r'共(?<page>\d+)页', string)
                total_page = int(t.group(1))
            except Exception:
                traceback.print_exc()
            return total_page

        def get_projectID(string):
            projectID = None
            try:
                t = regex.search(r'javascript:detailProjectInfo\("(?<page>.+)"\)', string)
                if t:
                    projectID = t.group(1)
            except:
                pass
            return projectID

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectBase':
            return result if result else []
        # print('ProjectBaseHandleMiddleware')
        curPage = response.meta.get('curPage')
        if curPage and curPage == 1:
            total_page = get_totla_page(response.xpath('//a[contains(@onclick,"GoToPage")]/../text()').extract_first())
            url = 'https://www.qdfd.com.cn/qdweb/realweb/fh/FhProjectQuery.jsp?page={curPage}&rows=20&okey=&order='
            for page in range(1, total_page + 1):
                project_base_req = Request(url = url.format(curPage = page),
                                           headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                           dont_filter = True,
                                           meta = {'PageType': 'ProjectBase'})
                result.append(project_base_req)
        else:
            tr_arr = response.xpath('//a[contains(@href,"javascript:detailProjectInfo")]/../..')
            for tr in tr_arr:
                projectState = tr.xpath('td[1]/text()').extract_first()
                href = tr.xpath(
                        'td[2]/a[contains(@href,"javascript:detailProjectInfo")]/../../td[2]/a/@href').extract_first()
                ProjectID = get_projectID(href)
                if ProjectID:
                    url = 'https://www.qdfd.com.cn/qdweb/realweb/fh/FhProjectInfo.jsp'
                    projectInfo_req = Request(url = url,
                                              method = 'POST',
                                              body = urlparse.urlencode({'projectID': ProjectID}),
                                              headers = self.settings.get('POST_DEFAULT_REQUEST_HEADERS'),
                                              dont_filter = True,
                                              meta = {
                                                  'PageType': 'ProjectInfo',
                                                  'ProjectID': ProjectID,
                                                  'ProjectState': projectState
                                              })
                    result.append(projectInfo_req)
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
        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectInfo':
            return result if result else []
        # print('ProjectInfoHandleMiddleware')
        if response.request.method == 'POST':
            projectInfo = ProjectBaseItem()
            ProjectID = response.meta.get('ProjectID')
            projectInfo['ProjectState'] = response.meta.get('ProjectState')
            projectInfo['ProjectID'] = ProjectID
            projectInfo['ProjectName'] = response.xpath('//td[@class = "bszn_title"]/text()').extract_first()
            ProjectUUID = uuid.uuid3(uuid.NAMESPACE_DNS, ProjectID + projectInfo['ProjectName'])
            projectInfo['ProjectUUID'] = ProjectUUID
            projectInfo['DistrictName'] = response.xpath(
                    '//span[contains(text(),"所在区县：")]/following-sibling::span[1]/text()').extract_first()
            projectInfo['ProjectAddress'] = response.xpath(
                    '//span[contains(text(),"项目地址：")]/following-sibling::span[1]/text()').extract_first()
            projectInfo['Developer'] = response.xpath(
                    '//a[contains(@href,"FhCompanyInfo.jsp?compID")]/text()').extract_first()
            projectInfo['HousingAmount'] = response.xpath(
                    '//td[text()="住宅套数"]/following-sibling::td[1]/text()').extract_first()
            projectInfo['HousingArea'] = response.xpath(
                '//td[text()="住宅面积"]/following-sibling::td[1]/text()').extract_first()
            projectInfo['TotalAmount'] = response.xpath(
                '//td[text()="总套数"]/following-sibling::td[1]/text()').extract_first()
            projectInfo['TotalArea'] = response.xpath(
                '//td[text()="总面积"]/following-sibling::td[1]/text()').extract_first()
            projectInfo['HousingOnsoldAmount'] = response.xpath(
                    '//td[contains(text(),"可售住宅套数")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['HousingOnsoldArea'] = response.xpath(
                    '//td[contains(text(),"可售住宅面积")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['TotalOnsoldAmount'] = response.xpath(
                    '//td[contains(text(),"可售总套数")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['TotalOnsoldArea'] = response.xpath(
                    '//td[contains(text(),"可售总面积")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['BookingHousingAmount'] = response.xpath(
                    '//td[contains(text(),"预定住宅套数")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['BookingHousingArea'] = response.xpath(
                    '//td[contains(text(),"预定住宅面积")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['TotalBookingAmount'] = response.xpath(
                    '//td[contains(text(),"预定总套数")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['TotalBookingArea'] = response.xpath(
                    '//td[contains(text(),"预定总面积")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['HousingSoldAmount'] = response.xpath(
                    '//td[contains(text(),"已售住宅套数")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['HousingSoldArea'] = response.xpath(
                    '//td[contains(text(),"已售住宅面积")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['TotalSoldAmount'] = response.xpath(
                    '//td[contains(text(),"已售总套数")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['TotalSoldArea'] = response.xpath(
                    '//td[contains(text(),"已售总面积")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['RegisterHousingAmount'] = response.xpath(
                    '//td[contains(text(),"已登记住宅套数")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['RegisterHousingArea'] = response.xpath(
                    '//td[contains(text(),"已登记住宅面积")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['TotalRegisterAmount'] = response.xpath(
                    '//td[contains(text(),"已登记总套数")]/following-sibling::td[1]/text()').extract_first()
            projectInfo['TotalRegisterArea'] = response.xpath(
                    '//td[contains(text(),"已登记总面积")]/following-sibling::td[1]/text()').extract_first()
            result.append(projectInfo)

            # 预售证
            tr_arr = response.xpath('//th[text()="编号"]/../following-sibling::tr')
            for tr in tr_arr:
                presellInfo = PresellInfoItem()
                presellInfo['ProjectUUID'] = ProjectUUID
                presellInfo['ProjectName'] = projectInfo['ProjectName']
                presellInfo['PresalePermitNumber'] = tr.xpath('td[1]/text()').extract_first()
                presellInfo['PresalePermitName'] = tr.xpath('td[2]/a/text()').extract_first()
                href = tr.xpath('td[2]/a/@href').extract_first()
                presellID = None
                if href:
                    t = regex.match(r'javascript:getBuilingList\("(?<presellID>.+)",', href)
                    presellID = t.group(1)
                presellInfo['PresellID'] = presellID
                presellInfo['PresellUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                        presellID + presellInfo['PresalePermitNumber'] +
                                                        presellInfo['PresalePermitName'])
                presellInfo['EarliestOpeningDate'] = tr.xpath('td[3]/text()').extract_first()
                presellInfo['SellAddress'] = tr.xpath('td[4]/text()').extract_first()
                presellInfo['SellTel'] = tr.xpath('td[5]/text()').extract_first()
                presellInfo['TotalAmount'] = tr.xpath('td[6]/text()').extract_first()
                presellInfo['TotalArea'] = tr.xpath('td[7]/text()').extract_first()
                presellInfo['OnsoldAmount'] = tr.xpath('td[8]/text()').extract_first()
                presellInfo['OnsoldArea'] = tr.xpath('td[9]/text()').extract_first()
                presellInfo['SoldAmount'] = tr.xpath('td[10]/text()').extract_first()
                presellInfo['SoldArea'] = tr.xpath('td[11]/text()').extract_first()
                result.append(presellInfo)
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
            return result if result else []
        if response.meta.get('PageType') != 'BuildingListInfo':
            return result if result else []
        # print('BuildingListHandleMiddleware')
        ProjectUUID = response.meta.get('ProjectUUID')
        PresellUUID = response.meta.get('PresellUUID')
        ProjectName = response.meta.get('ProjectName')
        PresalePermitName = response.meta.get('PresalePermitName')

        tr_arr = response.xpath('//th[text()="楼栋名称"]/../following-sibling::tr')
        for tr in tr_arr:
            buildingInfo = BuildingInfoItem()
            buildingInfo['ProjectUUID'] = ProjectUUID
            buildingInfo['PresellUUID'] = PresellUUID
            buildingInfo['ProjectName'] = ProjectName
            buildingInfo['PresalePermitName'] = PresalePermitName
            href = tr.xpath('td[1]/a/@href').extract_first()
            if href:
                t = regex.search(
                        r'javascript:showHouseStatus\("(?<buildingID>.+)","(?<startID>.+)","(?<projectID>.+)"\)',
                        href)
                buildingInfo['BuildingID'] = t.group(1)
                buildingInfo[
                    'BuildingURL'] = 'https://www.qdfd.com.cn/qdweb/realweb/fh/FhHouseStatus.jsp?buildingID={BuildingID}&startID={startID}&projectID={projectID}'.format(
                        BuildingID = buildingInfo['BuildingID'], startID = t.group(2), projectID = t.group(3))
                buildingInfo['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, buildingInfo['BuildingURL'])
                buildingInfo['BuildingName'] = tr.xpath('td[1]/a/text()').extract_first()
                buildingInfo['BuildingReferencePrice'] = tr.xpath('td[2]/text()').extract_first()
                buildingInfo['BuildingFloatingRange'] = tr.xpath('td[3]/text()').extract_first()
                buildingInfo['OnsoldAmount'] = tr.xpath('td[4]/text()').extract_first()
                buildingInfo['BookingAmount'] = tr.xpath('td[5]/text()').extract_first()
                buildingInfo['TotalAmount'] = tr.xpath('td[6]/text()').extract_first()
                result.append(buildingInfo)
        return result


class HouseListInfoHandleMiddleware(object):
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
        if response.meta.get('PageType') != 'HouseListInfo':
            return result if result else []
        # print('HouseListInfoHandleMiddleware')
        ProjectUUID = response.meta.get('ProjectUUID')
        PresellUUID = response.meta.get('PresellUUID')
        BuildingUUID = response.meta.get('BuildingUUID')
        ProjectName = response.meta.get('ProjectName')
        PresalePermitName = response.meta.get('PresalePermitName')
        BuildingName = response.meta.get('BuildingName')
        colors = {'#FFFF00': '已签约', '#FF0000': '已登记', '#00C200': '可售', '#FF00FF': '已付定金', '#FFFFFF': '未纳入网上销售'}
        tr_arr = response.xpath('//td[text()="实际层"]/../following-sibling::tr')
        for tr in tr_arr:
            td_arr = tr.xpath('td')
            floor = td_arr[0].xpath('text()').extract_first()
            for colNum, td in enumerate(td_arr[1:]):
                houseInfo = HouseInfoItem()
                houseInfo['ProjectUUID'] = ProjectUUID
                houseInfo['PresellUUID'] = PresellUUID
                houseInfo['BuildingUUID'] = BuildingUUID
                houseInfo['ProjectName'] = ProjectName
                houseInfo['PresalePermitName'] = PresalePermitName
                houseInfo['BuildingName'] = BuildingName

                bgcolor = td.xpath('@bgcolor').extract_first()
                try:
                    state = colors[bgcolor]
                    state_arr = td.xpath('font/text()').extract()
                    if len(state_arr) > 0:
                        state = state + ',' + ','.join(state_arr)
                    houseInfo['HouseState'] = state
                except:
                    houseInfo['HouseState'] = ''
                houseInfo['ActualFloor'] = floor
                HouseName = None
                houseID = None
                a_arr = td.xpath('a')
                if len(a_arr) > 0:
                    HouseName = a_arr[0].xpath('text()').extract_first()
                    href_text = a_arr[0].xpath('@href').extract_first()
                    try:
                        t = regex.search(r'javascript:houseDetail\(\'(?<houseID>.+)\'\)', href_text)
                        houseID = t.group(1)
                    except:
                        pass
                else:
                    HouseName = td.xpath('text()').extract_first()
                houseInfo['HouseName'] = HouseName.strip().replace(' ', '')
                # HouseUUID = BuildingUUID +HouseName+楼层+在销控表的所在列数
                houseInfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                    BuildingUUID + houseInfo['HouseName'] +
                                                    houseInfo['ActualFloor'] +
                                                    str(colNum))
                if houseID:  # 如果有id,则代表有url
                    houseInfo['HouseID'] = houseID
                    houseInfo[
                        'SourceUrl'] = 'https://www.qdfd.com.cn/qdweb/realweb/fh/FhHouseDetail.jsp?houseID={houseID}'.format(
                            houseID = houseID)
                    req = Request(url = houseInfo['SourceUrl'],
                                  headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                  dont_filter = True,
                                  meta = {'PageType': 'HouseInfo', 'houseInfo': houseInfo})
                    result.append(req)
                else:
                    result.append(houseInfo)
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
        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'HouseInfo':
            return result if result else []
        # print('HouseInfoHandleMiddleware')
        houseInfo = response.meta.get('houseInfo')
        FloorName_text = response.xpath(
                '//td[contains(text(),"名义层/实际层")]/following-sibling::td[1]/text()').extract_first()
        try:
            t = FloorName_text.replace(' ', '').strip().split('/')
            houseInfo['FloorName'] = t[-1]
        except:
            houseInfo['FloorName'] = ''

        houseInfo['HouseUseType'] = response.xpath(
                '//td[contains(text(),"房屋类型")]/following-sibling::td[1]/text()').extract_first()
        houseInfo['HouseUnitShape'] = response.xpath(
                '//td[contains(text(),"房型")]/following-sibling::td[1]/text()').extract_first()
        houseInfo['ForecastBuildingArea'] = response.xpath(
                '//td[contains(text(),"预测建筑面积")]/following-sibling::td[1]/text()').extract_first()
        houseInfo['MeasuredBuildingArea'] = response.xpath(
                '//td[contains(text(),"实测建筑面积")]/following-sibling::td[1]/text()').extract_first()
        houseInfo['ForecastInsideOfBuildingArea'] = response.xpath(
                '//td[contains(text(),"预测套内面积 ")]/following-sibling::td[1]/text()').extract_first()
        houseInfo['MeasuredInsideOfBuildingArea'] = response.xpath(
                '//td[contains(text(),"实测套内面积")]/following-sibling::td[1]/text()').extract_first()
        houseInfo['ForecastPublicArea'] = response.xpath(
                '//td[contains(text(),"预测分摊面积")]/following-sibling::td[1]/text()').extract_first()
        houseInfo['MeasuredSharedPublicArea'] = response.xpath(
                '//td[contains(text(),"实测分摊面积")]/following-sibling::td[1]/text()').extract_first()
        houseInfo['ForecastUndergroundArea'] = response.xpath(
                '//td[contains(text(),"预测地下面积")]/following-sibling::td[1]/text()').extract_first()
        houseInfo['MeasuredUndergroundArea'] = response.xpath(
                '//td[contains(text(),"实测地下面积")]/following-sibling::td[1]/text()').extract_first()
        price = response.xpath('//td[contains(text(),"参考价格")]/following-sibling::td[1]/text()').extract_first()
        if price:
            houseInfo['HouseReferencePrice'] = price
        result.append(houseInfo)
        return result
