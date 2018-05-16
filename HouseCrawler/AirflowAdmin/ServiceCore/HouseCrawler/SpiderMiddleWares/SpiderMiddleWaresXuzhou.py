# coding = utf-8
import re
import json
import logging
import sys
import traceback
import uuid
import datetime

from scrapy import Request
from HouseCrawler.Items.ItemsXuzhou import *

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

        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectBase':
            return result if result else []
        # print(ProjectBaseHandleMiddleware')
        result = list(result)

        resp = json.loads(response.body_as_unicode())
        obj_list = resp.get('obj')
        if isinstance(obj_list, list):
            for obj in obj_list:
                try:
                    projectItem = ProjectInfoItem()
                    projectItem['ProjectID'] = obj.get('id')
                    projectItem['ProjectUUID'] = uuid.uuid3(
                        uuid.NAMESPACE_DNS, projectItem['ProjectID'])
                    projectItem['ProjectName'] = obj.get('xmmc')
                    projectItem['PromotionName'] = obj.get('tgmc')
                    if obj.get('lx'):
                        projectItem['HouseUseType'] = ''.join(
                            re.split('\s+', str(obj.get('lx'))))
                    projectItem['AveragePrice'] = obj['nxsjg']
                    projectItem['ProjectAddress'] = obj.get('xmdz')
                    zt = obj.get('zt')
                    zt_map = {'01': '未售', '02': '在售', '03': '售罄'}
                    projectItem['OnSaleState'] = zt_map.get(zt, zt)
                    projectItem['DistrictName'] = obj.get('xzqh')
                    # 项目详情
                    projectInfo_req = Request(
                        url='http://www.xzhouse.com.cn/platform/actionController.do?doQuery&code=item_Info&id={id}'.format(
                            id=projectItem['ProjectID']),
                        meta={
                            'PageType': 'ProjectInfo',
                            'projectItem': projectItem
                        })
                    result.append(projectInfo_req)
                except Exception:
                    traceback.print_exc()
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
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') not in ('ProjectInfo', 'ProjectAllcount'):
            return result if result else []
        # print(ProjectInfoHandleMiddleware')
        result = list(result)
        projectItem = response.meta.get('projectItem')
        resp = json.loads(response.body_as_unicode())
        if response.meta.get('PageType') == 'ProjectInfo':
            if resp.get('success'):
                try:
                    info = resp.get('obj').get('item_Info')[0]
                    projectItem['Developer'] = info['CorpName']
                    projectItem['SaleAddress'] = info['xsdz']
                    projectItem['TotalBuidlingArea'] = info['jzmj']
                    projectItem['PropertyRightsDescription'] = info['tdnx']
                    projectItem['FloorAreaRatio'] = info['rjl']
                    projectItem['GreeningRate'] = info['lhl']
                    projectItem['ManagementFees'] = info['wyf']
                    projectItem['ProjectPoint'] = info['zb']
                    kpsj = info.get('kpsj')
                    if kpsj:
                        t = kpsj / 1000
                        projectItem['EarliestOpeningDate'] = str(
                            datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d'))
                except Exception:
                    traceback.print_exc()
                allcount_req = Request(
                    url='http://www.xzhouse.com.cn/platform/actionController.do?doQuery&code=item_allcount&itemid={id}'.format(
                        id=projectItem['ProjectID']),
                    meta={'PageType': 'ProjectAllcount',
                          'projectItem': projectItem
                          })
                result.append(allcount_req)
        elif response.meta.get('PageType') == 'ProjectAllcount':
            if resp.get('success'):
                try:
                    allcount = resp.get('obj').get('item_allcount')[0]
                    projectItem['UnsoldArea'] = allcount['ksmj']
                    projectItem['UnsoldAmount'] = allcount['ksts']
                    projectItem['ApprovalPresaleAmount'] = allcount['rwts']
                    projectItem['SoldArea'] = allcount['xsmj']
                    projectItem['SoldAmount'] = allcount['xsts']
                    projectItem['ApprovalPresaleArea'] = allcount['zrwmj']
                except Exception:
                    traceback.print_exc()
                result.append(projectItem)
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
        if response.meta.get('PageType') not in ('PresellInfo', 'NowsellInfo', 'BuildingList'):
            return result if result else []
        print('PresellInfoHandleMiddleware')
        print(response.meta.get('PageType'))
        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectID = response.meta.get('ProjectID')
        ProjectName = response.meta.get('ProjectName')
        resp = json.loads(response.body_as_unicode())
        if resp.get('success'):
            if response.meta.get('PageType') in('PresellInfo', 'NowsellInfo'):
                try:
                    if response.meta.get('PageType') == 'PresellInfo':
                        xsqk_list = resp.get('obj').get('item_xsqk')
                        sell_type = 'Presell'
                    else:
                        xsqk_list = resp.get('obj').get('item_xsxx')
                        sell_type = 'Nowsell'
                    for index, xsqk in enumerate(xsqk_list):
                        if xsqk.get('SaleScope') is None:
                            continue
                        presellInfoItem = PresellInfoItem()
                        presellInfoItem['SellType'] = sell_type

                        presellInfoItem['ProjectUUID'] = ProjectUUID
                        presellInfoItem['ProjectID'] = ProjectID
                        presellInfoItem['ProjectName'] = ProjectName
                        presellInfoItem['PresellID'] = xsqk['SaleItemID']
                        if sell_type == 'Presell':
                            presellInfoItem['PresellUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                                        ProjectUUID + presellInfoItem['PresellID'])
                        else:
                            presellInfoItem['PresellUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                                        ProjectUUID + presellInfoItem['PresellID'] +
                                                                        sell_type + 'index:' + str(index))

                        presellInfoItem['DistrictName'] = xsqk['District']
                        presellInfoItem['RegionName'] = xsqk['Zone']
                        presellInfoItem['Developer'] = xsqk['CorpName']
                        presellInfoItem['ConstructionPermitNumber'] = xsqk[
                            'ConstructCertNo']
                        presellInfoItem['ProjectApproval'] = xsqk['ItAcPaper']
                        presellInfoItem['CertificateOfUseOfStateOwnedLand'] = xsqk[
                            'CertifyPlanLand']
                        presellInfoItem['LandUse'] = xsqk['LandUse']
                        presellInfoItem['LandCertificate'] = xsqk['CertNo']
                        presellInfoItem['FloorArea'] = xsqk['LandArea']
                        presellInfoItem['PlanUse'] = xsqk['PlanUse']
                        presellInfoItem['PresalePermitNumber'] = xsqk[
                            'CertificateNO']
                        presellInfoItem['PresaleArea'] = xsqk['TotalArea']
                        presellInfoItem['SaleScope'] = xsqk['SaleScope']
                        presellInfoItem['MonitBank'] = xsqk['ControlBank']
                        presellInfoItem['MonitAccount'] = xsqk['SP_JGJGZH']
                        presellInfoItem['SaleAddress'] = xsqk['SaleLocation']
                        presellInfoItem['SalePhone'] = xsqk['SalePhone']
                        presellInfoItem[
                            'ApprovalPresaleAmount'] = xsqk['rwzts']
                        presellInfoItem['SoldAmount'] = xsqk['cjts']
                        presellInfoItem['UnsoldAmount'] = xsqk['kxsts']
                        presellInfoItem['TotalArea'] = xsqk['TotalArea']
                        presellInfoItem['LssueDate'] = xsqk['CertificateTime']
                        result.append(presellInfoItem)
                except:
                    traceback.print_exc()
            elif response.meta.get('PageType') == 'BuildingList':
                PresalePermitNumber = response.meta.get('PresalePermitNumber')
                PresellUUID = response.meta.get('PresellUUID')

                try:
                    lpxx_list = resp.get('obj').get('item_lpxx')
                    for lpxx in lpxx_list:
                        buildingItem = BuildingInfoItem()
                        buildingItem['ProjectUUID'] = ProjectUUID
                        buildingItem['ProjectID'] = ProjectID
                        buildingItem['ProjectName'] = ProjectName
                        buildingItem[
                            'PresalePermitNumber'] = PresalePermitNumber
                        buildingItem['PresellUUID'] = PresellUUID
                        buildingItem['BuildingName'] = lpxx['BuildingName']
                        buildingItem['BuildingID'] = lpxx['BuildingInfo_ID']
                        buildingItem['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                                  PresellUUID + buildingItem['BuildingID'])
                        buildingItem['ApprovalPresaleAmount'] = lpxx['rwzts']
                        buildingItem['SoldAmount'] = lpxx['cjts']
                        buildingItem['UnsoldAmount'] = lpxx['kxsts']
                        buildingItem['ApprovalPresaleArea'] = lpxx['zmj']
                        buildingItem['SoldArea'] = lpxx['cjmj']
                        buildingItem['UnsoldArea'] = lpxx['kxsmj']
                        result.append(buildingItem)
                except:
                    traceback.print_exc()
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
        if response.meta.get('PageType') != 'HouseList':
            return result if result else []
        result = list(result)

        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectID = response.meta.get('ProjectID')
        ProjectName = response.meta.get('ProjectName')
        PresellUUID = response.meta.get('PresellUUID')
        PresalePermitNumber = response.meta.get('PresalePermitNumber')
        BuildingUUID = response.meta.get('BuildingUUID')
        BuildingName = response.meta.get('BuildingName')
        resp = json.loads(response.body_as_unicode())
        if resp.get('success'):
            try:
                houseinfo_list = resp.get('obj').get('item_houseinfo')
                for index, houseinfo in enumerate(houseinfo_list):
                    houseItem = HouseInfoItem()
                    houseItem['ProjectUUID'] = ProjectUUID
                    houseItem['ProjectID'] = ProjectID
                    houseItem['ProjectName'] = ProjectName
                    houseItem['PresellUUID'] = PresellUUID
                    houseItem['PresalePermitNumber'] = PresalePermitNumber
                    houseItem['BuildingUUID'] = BuildingUUID
                    houseItem['BuildingName'] = BuildingName
                    houseItem['HouseID'] = houseinfo['HouseID']
                    houseItem['DataIndex'] = str(index)
                    houseItem['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, BuildingUUID + houseItem[
                                                        'HouseID'] + 'index:{0}'.format(houseItem['DataIndex']))
                    houseItem['UnitName'] = houseinfo['UnitNo']
                    houseItem['HouseName'] = houseinfo['HouseNo']
                    houseItem['HouseMapID'] = houseinfo['HouseMapID']
                    houseItem['HouseState'] = houseinfo['HouseState']
                    houseItem['HouseUseType'] = houseinfo['SaleHouseUse']
                    houseItem['ContractRecordNumber'] = houseinfo['CRecordNo']
                    houseItem['BuildingStructure'] = houseinfo['HouseStruct']
                    houseItem['MeasuredBuildingArea'] = houseinfo['BuArea']
                    houseItem['MeasuredInsideOfBuildingArea'] = houseinfo[
                        'InnerArea']
                    houseItem['MeasuredSharedPublicArea'] = houseinfo[
                        'ShareArea']
                    result.append(houseItem)
            except Exception:
                traceback.print_exc()
        return result
