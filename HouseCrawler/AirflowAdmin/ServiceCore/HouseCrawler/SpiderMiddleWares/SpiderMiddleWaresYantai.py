# coding = utf-8
import logging
import sys
import uuid

import time
from HouseCrawler.Items.ItemsYantai import *
from HouseNew.models import *
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
        def get_totla_page(response):
            total_page = 1
            if debug:
                return 1
            try:
                t = response.xpath('//*[@id="PageNavigator1_LblPageCount"]/text()').extract_first()
                total_page = int(t)
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
                req_dict = {
                    'PageNavigator1$txtNewPageIndex': str(page),
                    'txtPrjName': '',
                    'txtYsxkz': '',
                    'txtKfsName': '',
                    'txtPrjAdress': '',
                    '__EVENTARGUMENT': '',
                    '__EVENTTARGET': 'PageNavigator1$LnkBtnGoto',
                    '__EVENTVALIDATION': response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first(),
                    '__VIEWSTATE': response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first(),
                }
                req = Request(url = 'http://www.ytfcjy.com/public/project/ProjectList.aspx',
                              headers = self.settings.get('POST_DEFAULT_REQUEST_HEADERS'),
                              body = urlparse.urlencode(req_dict),
                              method = 'POST',
                              dont_filter = True,
                              meta = {'PageType': 'ProjectBase'})
                result.append(req)
        else:
            tr_arr = response.xpath('//tr[@class="TR_BG_list"]')
            for tr in tr_arr:
                projectBaseItem = ProjectBaseItem()
                href = 'http://www.ytfcjy.com/public/project/' + tr.xpath('td[2]/a/@href').extract_first()
                projectBaseItem['SourceUrl'] = href
                projectBaseItem['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, href)
                projectBaseItem['ProjectName'] = tr.xpath('td[2]/a/u/text()').extract_first()
                projectBaseItem['Developer'] = tr.xpath('td[3]/text()').extract_first()
                projectBaseItem['ProjectAddress'] = tr.xpath('td[4]/text()').extract_first()
                projectBaseItem['PresalePermitNumber'] = tr.xpath('td[5]/text()').extract_first()
                projectBaseItem['SoldAmount'] = tr.xpath('td[6]/text()').extract_first()
                projectBaseItem['UnsoldAmount'] = tr.xpath('td[7]/text()').extract_first()
                result.append(projectBaseItem)

                projectInfo_req = Request(url = projectBaseItem['SourceUrl'],
                        headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                        dont_filter = True,
                        meta = {'PageType': 'ProjectInfo'})
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
        def get_dict(string):
            if string is None:
                return None
            try:
                d = {}
                arr = string.split(';;')
                for a in arr:
                    infos = a.split(',,')
                    d[infos[1]] = infos[0]
                return d
            except:
                return None

        def get_infos(string):
            d = get_dict(string)
            try:
                values = []
                for key, value in d.items():
                    values.append(key)
                return ','.join(values)
            except:
                return ''

        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectInfo':
            return result if result else []

        result = list(result)
        # print('ProjectInfoHandleMiddleware')
        projectInfoItem = ProjectInfoItem()
        projectInfoItem['SourceUrl'] = response.url
        projectInfoItem['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, response.url)
        projectInfoItem['ProjectNO'] = response.xpath('//*[@id="PROJECT_XMBH"]/text()').extract_first()
        projectInfoItem['ProjectName'] = response.xpath('//*[@id="PROJECT_XMMC_1"]/text()').extract_first()
        projectInfoItem['Developer'] = response.xpath('//*[@id="PROJECT_KFQY_NAME"]/text()').extract_first()
        projectInfoItem['ProjectAddress'] = response.xpath('//*[@id="PROJECT_XMDZ"]/text()').extract_first()
        projectInfoItem['DistrictName'] = response.xpath('//*[@id="PROJECT_SZQY"]/text()').extract_first()
        projectInfoItem['FloorAreaRatio'] = response.xpath('//*[@id="PROJECT_RJL"]/text()').extract_first()
        projectInfoItem['TotalBuidlingArea'] = response.xpath('//*[@id="PROJECT_GHZJZMJ"]/text()').extract_first()
        projectInfoItem['PlanningAcceptanceDate'] = response.xpath('//*[@id="PROJECT_GHYSRQ"]/text()').extract_first()
        projectInfoItem['ComprehensiveAcceptanceDate'] = response.xpath(
                '//*[@id="PROJECT_ZHYSRQ"]/text()').extract_first()
        projectInfoItem['PlanInvest'] = response.xpath('//*[@id="PROJECT_JHZTZ"]/text()').extract_first()
        projectInfoItem['PresalePermitNumber'] = response.xpath('//*[@id="YSXKZH"]/text()').extract_first()
        projectInfoItem['SoldAmount'] = response.xpath('//*[@id="YSZTS"]/text()').extract_first()
        projectInfoItem['UnsoldAmount'] = response.xpath('//*[@id="WSZTS"]/text()').extract_first()
        projectInfoItem['SoldArea'] = response.xpath('//*[@id="YSZMJ"]/text()').extract_first()
        projectInfoItem['UnsoldArea'] = response.xpath('//*[@id="WSZMJ"]/text()').extract_first()
        projectInfoItem['CheckOutAmount'] = response.xpath('//*[@id="TFCS"]/text()').extract_first()
        projectInfoItem['CheckOutRatio'] = response.xpath('//*[@id="TFL"]/text()').extract_first()
        projectInfoItem['SellAddress'] = response.xpath('//*[@id="PROJECT_SLCDH"]/text()').extract_first()
        projectInfoItem['Selltel'] = response.xpath('//*[@id="PROJECT_SLDH"]/text()').extract_first()
        projectInfoItem['DesignUnit'] = response.xpath('//*[@id="PROJECT_SJDW"]/text()').extract_first()
        projectInfoItem['ConstructionUnit'] = response.xpath('//*[@id="PROJECT_SGDW"]/text()').extract_first()
        projectInfoItem['SupervisionUnit'] = response.xpath('//*[@id="PROJECT_JLDW"]/text()').extract_first()
        projectInfoItem['ManagementCompany'] = response.xpath('//*[@id="PROJECT_WYGLGS"]/text()').extract_first()
        projectInfoItem['ProjectSupporting'] = response.xpath('//*[@id="PROJECT_XMPT"]/text()').extract_first()
        projectInfoItem['AroundSupporting'] = response.xpath('//*[@id="PROJECT_ZBPT"]/text()').extract_first()
        projectInfoItem['ProjectIntro'] = response.xpath('//*[@id="PROJECT_XMJL"]/text()').extract_first()

        projectInfoItem['TodayHousingSoldAmount'] = response.xpath('//*[@id="ZZ_JRYSTS"]/text()').extract_first()
        projectInfoItem['TodayHousingSoldArea'] = response.xpath('//*[@id="ZZ_JRYSMJ"]/text()').extract_first()
        projectInfoItem['HousingSoldAmount'] = response.xpath('//*[@id="ZZ_LJYSTS"]/text()').extract_first()
        projectInfoItem['HousingSoldArea'] = response.xpath('//*[@id="ZZ_LJYSMJ"]/text()').extract_first()
        projectInfoItem['HousingUnsoldAmount'] = response.xpath('//*[@id="ZZ_WSTS"]/text()').extract_first()
        projectInfoItem['HousingUnsoldArea'] = response.xpath('//*[@id="ZZ_WSMJ"]/text()').extract_first()

        projectInfoItem['TodayShopSoldAmount'] = response.xpath('//*[@id="SY_JRYSTS"]/text()').extract_first()
        projectInfoItem['TodayShopSoldArea'] = response.xpath('//*[@id="SY_JRYSMJ"]/text()').extract_first()
        projectInfoItem['ShopSoldAmount'] = response.xpath('//*[@id="SY_LJYSTS"]/text()').extract_first()
        projectInfoItem['ShopSoldArea'] = response.xpath('//*[@id="SY_LJYSMJ"]/text()').extract_first()
        projectInfoItem['ShopUnsoldAmount'] = response.xpath('//*[@id="SY_WSTS"]/text()').extract_first()
        projectInfoItem['ShopUnsoldArea'] = response.xpath('//*[@id="SY_WSMJ"]/text()').extract_first()

        projectInfoItem['TodayOfficeSoldAmount'] = response.xpath('//*[@id="BG_JRYSTS"]/text()').extract_first()
        projectInfoItem['TodayOfficeSoldArea'] = response.xpath('//*[@id="BG_JRYSMJ"]/text()').extract_first()
        projectInfoItem['OfficeSoldAmount'] = response.xpath('//*[@id="BG_LJYSTS"]/text()').extract_first()
        projectInfoItem['OfficeSoldArea'] = response.xpath('//*[@id="BG_LJYSMJ"]/text()').extract_first()
        projectInfoItem['OfficeUnsoldAmount'] = response.xpath('//*[@id="BG_WSTS"]/text()').extract_first()
        projectInfoItem['OfficeUnsoldArea'] = response.xpath('//*[@id="BG_WSMJ"]/text()').extract_first()

        projectInfoItem['TodayOtherSoldAmount'] = response.xpath('//*[@id="QT_JRYSTS"]/text()').extract_first()
        projectInfoItem['TodayOtherSoldArea'] = response.xpath('//*[@id="QT_JRYSMJ"]/text()').extract_first()
        projectInfoItem['OtherSoldAmount'] = response.xpath('//*[@id="QT_LJYSTS"]/text()').extract_first()
        projectInfoItem['OtherSoldArea'] = response.xpath('//*[@id="QT_LJYSMJ"]/text()').extract_first()
        projectInfoItem['OtherUnsoldAmount'] = response.xpath('//*[@id="QT_WSTS"]/text()').extract_first()
        projectInfoItem['OtherUnsoldArea'] = response.xpath('//*[@id="QT_WSMJ"]/text()').extract_first()

        # 土地证
        tdzInfo = response.xpath('//*[@id="tdzInfo"]/@value').extract_first()
        projectInfoItem['CertificateOfUseOfStateOwnedLand'] = get_infos(tdzInfo)
        # 施工许可证
        sgxkzInfo = response.xpath('//*[@id="sgxkzInfo"]/@value').extract_first()
        projectInfoItem['ConstructionPermitNumber'] = get_infos(sgxkzInfo)
        # 用地规划许可证
        jsydghxkzInfo = response.xpath('//*[@id="ghxkzInfo"]/@value').extract_first()
        projectInfoItem['LandUsePermit'] = get_infos(jsydghxkzInfo)
        # 工程规划许可证
        ghxkzInfo = response.xpath('//*[@id="ghxkzInfo"]/@value').extract_first()
        projectInfoItem['BuildingPermit'] = get_infos(ghxkzInfo)

        result.append(projectInfoItem)

        # 预售证信息
        presellInfo = response.xpath('//*[@id="presellInfo"]/@value').extract_first()
        presellInfo_dict = get_dict(presellInfo)
        if presellInfo_dict:
            for key, value in presellInfo_dict.items():
                if value:
                    url = 'http://www.ytfcjy.com/public/project/presellCertInfo.aspx?code={code}'.format(code = value)
                    presell_info_req = Request(url = url,
                                               headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                               dont_filter = True,
                                               meta = {
                                                   'PageType': 'PresellInfo',
                                                   'ProjectUUID': str(projectInfoItem['ProjectUUID']),
                                                   'ProjectName': projectInfoItem['ProjectName'],
                                               })
                    result.append(presell_info_req)
        # 楼栋信息
        buildingInfo = response.xpath('//*[@id="buildInfo"]/@value').extract_first()
        buildingInfo_dict = get_dict(buildingInfo)
        if buildingInfo_dict:
            for key, value in buildingInfo_dict.items():
                if value:
                    # 销控表的列表访问链接
                    url = 'http://www.ytfcjy.com/public/project/RoomList.aspx?code={code}&rsr=1001&rse=0&jzmj=&tnmj='.format(
                            code = value)
                    buildingInfoItem = BuildingInfoItem()
                    buildingInfoItem['SourceUrl'] = url
                    buildingInfoItem['ProjectUUID'] = projectInfoItem['ProjectUUID']
                    buildingInfoItem['ProjectName'] = projectInfoItem['ProjectName']
                    buildingInfoItem['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, url)
                    buildingInfoItem['BuildingName'] = key[:key.index('(')]
                    buildingInfoItem['BuildingID'] = value
                    result.append(buildingInfoItem)

                    body = '%3C?xml%20version=%221.0%22%20encoding=%22utf-8%22%20standalone=%22yes%22?%3E%0A%3Cparam%20funname=%22SouthDigital.Wsba.CBuildTableEx.GetBuildHTMLEx%22%3E%0A%3Citem%3E{BuildingID}%3C/item%3E%0A%3Citem%3E1%3C/item%3E%0A%3Citem%3E1%3C/item%3E%0A%3Citem%3E80%3C/item%3E%0A%3Citem%3E720%3C/item%3E%0A%3Citem%3Eg_oBuildTable%3C/item%3E%0A%3Citem%3E%201=1%3C/item%3E%0A%3C/param%3E%0A'
                    building_info_req = Request(
                        url='http://www.ytfcjy.com/Common/Agents/ExeFunCommon.aspx?&req={time}'.format(
                            time=round(time.time() * 1000)),
                        headers={
                            'Host': 'www.ytfcjy.com',
                            'Connection': 'keep-alive',
                            'Origin': 'http:/www.ytfcjy.com',
                            'Content-Type': 'text/plain;charset=UTF-8',
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'zh-CN,zh;q=0.9',
                        },
                        dont_filter=True,
                        method='POST',
                        body=body.format(BuildingID=value),
                        meta={
                            'PageType': 'HouseList',
                            'ProjectUUID': str(projectInfoItem['ProjectUUID']),
                            'ProjectName': projectInfoItem['ProjectName'],
                            'BuildingName': buildingInfoItem['BuildingName'],
                            'BuildingUUID': str(buildingInfoItem['BuildingUUID']),
                        })
                    result.append(building_info_req)
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
        result = list(result)
        # print('PresellInfoHandleMiddleware')

        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')

        presellInfoItem = PresellInfoItem()
        presellInfoItem['SourceUrl'] = response.url
        presellInfoItem['PresellUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, response.url)
        presellInfoItem['ProjectUUID'] = ProjectUUID
        presellInfoItem['ProjectName'] = ProjectName
        presellInfoItem['PresalePermitNumber'] = response.xpath('//*[@id="YSXKZ_XKZH"]/text()').extract_first()
        presellInfoItem['LssueDate'] = response.xpath('//*[@id="YSXKZ_FZRQ"]/text()').extract_first()
        presellInfoItem['ValidityDateStartDate'] = response.xpath('//*[@id="YSXKZ_YXQX1"]/text()').extract_first()
        presellInfoItem['ValidityDateClosingDate'] = response.xpath('//*[@id="YSXKZ_YXQX2"]/text()').extract_first()
        presellInfoItem['PresaleBuildingName'] = response.xpath('//*[@id="YSZMC"]/text()').extract_first()
        presellInfoItem['LssuingAuthority'] = response.xpath('//*[@id="YSXKZ_FZJG"]/text()').extract_first()
        presellInfoItem['Bank'] = response.xpath('//*[@id="YSXKZ_YSZJKHYH"]/text()').extract_first()
        presellInfoItem['BankAccount'] = response.xpath('//*[@id="YSXKZ_YSZJZH"]/text()').extract_first()
        presellInfoItem['ApprovalPresaleHouseAmount'] = response.xpath('//*[@id="YSXKZ_ZZYSTS"]/text()').extract_first()
        presellInfoItem['ApprovalPresaleHouseArea'] = response.xpath('//*[@id="YSXKZ_ZZYSMJ"]/text()').extract_first()
        presellInfoItem['ApprovalPresaleShopAmount'] = response.xpath('//*[@id="YSXKZ_SYYSTS"]/text()').extract_first()
        presellInfoItem['ApprovalPresaleShopArea'] = response.xpath('//*[@id="YSXKZ_SYYSMJ"]/text()').extract_first()
        presellInfoItem['ApprovalPresaleOfficeAmount'] = response.xpath(
                '//*[@id="YSXKZ_BGYSTS"]/text()').extract_first()
        presellInfoItem['ApprovalPresaleOfficeArea'] = response.xpath('//*[@id="YSXKZ_BGYSMJ"]/text()').extract_first()
        presellInfoItem['ApprovalPresaleOtherAmount'] = response.xpath('//*[@id="YSXKZ_QTYSTS"]/text()').extract_first()
        presellInfoItem['ApprovalPresaleOtherArea'] = response.xpath('//*[@id="YSXKZ_QTYSMJ"]/text()').extract_first()

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
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'HouseList':
            return result if result else []
        result = list(result)
        # print('HouseListHandleMiddleware')
        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')
        BuildingUUID = response.meta.get('BuildingUUID')
        BuildingName = response.meta.get('BuildingName')
        tr_arr = response.xpath('//tr[@class="TR_BG_list"]')
        for tr in tr_arr:
            href = 'http://www.ytfcjy.com/public/project/' + tr.xpath('td[1]/a/@href').extract_first()
            HouseState = tr.xpath('td[6]/text()').extract_first()
            house_info_req = Request(url = href, dont_filter = True,
                                     headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                     meta = {
                                         'PageType': 'HouseInfo',
                                         'ProjectUUID': ProjectUUID,
                                         'ProjectName': ProjectName,
                                         'BuildingName': BuildingName,
                                         'BuildingUUID': BuildingUUID,
                                         'HouseState': HouseState,
                                     })
            result.append(house_info_req)
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
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'HouseInfo':
            return result if result else []
        result = list(result)
        # print('HouseInfoHandleMiddleware')

        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')
        BuildingUUID = response.meta.get('BuildingUUID')
        BuildingName = response.meta.get('BuildingName')
        HouseState = response.meta.get('HouseState')

        houseInfoItem = HouseInfoItem()
        houseInfoItem['SourceUrl'] = response.url
        houseInfoItem['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, response.url)
        houseInfoItem['ProjectUUID'] = ProjectUUID
        houseInfoItem['ProjectName'] = ProjectName
        houseInfoItem['BuildingUUID'] = BuildingUUID
        houseInfoItem['BuildingName'] = BuildingName
        houseInfoItem['HouseState'] = HouseState

        houseInfoItem['HouseNumber'] = response.xpath('//*[@id="ROOM_ROOMNO"]/text()').extract_first()
        houseInfoItem['UnitName'] = response.xpath('//*[@id="ROOM_UNITNAME"]/text()').extract_first()
        houseInfoItem['UnitShape'] = response.xpath('//*[@id="ROOM_FWHX"]/text()').extract_first()
        houseInfoItem['Dwelling'] = response.xpath('//*[@id="ROOM_FWLX"]/text()').extract_first()
        houseInfoItem['NatureOfPropertyRight'] = response.xpath('//*[@id="ROOM_FWXZ"]/text()').extract_first()
        houseInfoItem['HouseUseType'] = response.xpath('//*[@id="ROOM_GHYT"]/text()').extract_first()
        houseInfoItem['OwnershipStatus'] = response.xpath('//*[@id="ROOM_QSZT"]/text()').extract_first()
        houseInfoItem['BalconyType'] = response.xpath('//*[@id="ROOM_YTLX"]/text()').extract_first()
        houseInfoItem['ForecastBuildingArea'] = response.xpath('//*[@id="ROOM_YCJZMJ"]/text()').extract_first()
        houseInfoItem['ForecastInsideOfBuildingArea'] = response.xpath('//*[@id="ROOM_YCTNMJ"]/text()').extract_first()
        houseInfoItem['ForecastPublicArea'] = response.xpath('//*[@id="ROOM_YCFTMJ"]/text()').extract_first()
        houseInfoItem['MeasuredBuildingArea'] = response.xpath('//*[@id="ROOM_SCJZMJ"]/text()').extract_first()
        houseInfoItem['MeasuredInsideOfBuildingArea'] = response.xpath('//*[@id="ROOM_SCTNMJ"]/text()').extract_first()
        houseInfoItem['MeasuredSharedPublicArea'] = response.xpath('//*[@id="ROOM_SCFTMJ"]/text()').extract_first()
        houseInfoItem['Decoration'] = response.xpath('//*[@id="ROOM_ZSBZ"]/text()').extract_first()
        houseInfoItem['EquipmentStandard'] = response.xpath('//*[@id="ROOM_SBBZ"]/text()').extract_first()
        houseInfoItem['HouseMatching'] = response.xpath('//*[@id="ROOM_HSPT"]/text()').extract_first()
        houseInfoItem['IsMortgage'] = response.xpath('//*[@id="SFDY"]/text()').extract_first()
        houseInfoItem['IsAttachment'] = response.xpath('//*[@id="SFCF"]/text()').extract_first()
        houseInfoItem['IsSold'] = response.xpath('//*[@id="XSZT"]/text()').extract_first()
        houseInfoItem['Price'] = response.xpath('//*[@id="ROOM_PRICE"]/text()').extract_first()
        result.append(houseInfoItem)

        return result