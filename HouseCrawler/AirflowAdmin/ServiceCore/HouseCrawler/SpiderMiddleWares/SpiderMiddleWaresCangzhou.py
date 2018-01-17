#!/usr/python3
# -*- coding: utf-8 -*-
import sys
import uuid
import re
import random
import copy

import logging
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsCangzhou import *


if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
'''
    Created on 2017-12-11 10:58:11.
'''
contextflag = True


def check_data_num(string):
    fix_result = 0
    if string:
        fix_result = string.strip()
        fix_data = {'\r': '',
                    '幢': '',
                    '一房一价：元': '',
                    '\n': '',
                    '套': '',
                    '\\': '',
                    '\t': '',
                    '㎡': '',
                    ' ': '',
                    '/': '',
                    '个': '',
                    "%": '',
                    'm': '',
                    'M': '',
                    '²': '',
                    '元': '',
                    ',': '',
                    }

        for r in fix_data:
            fix_result = fix_result.strip().replace(r, fix_data[r])
        resultnum = re.search(r'(\d+)', fix_result)
        if resultnum:
            fix_result = int(resultnum.group(1))
        else:
            fix_result = 0
    return fix_result


def check_data_str(string):
    fix_result = ''
    if string:
        fix_result = string.strip()
        fix_data = {'\r': '',
                    '\n': '',
                    '\t': '',
                    ' ': ''
                    }
        for r in fix_data:
            fix_result = fix_result.strip().replace(r, fix_data[r])
    return fix_result

class SpiderMiddlerProject(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.mainurl = 'http://www.hbczfdc.com:4993/'
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.hbczfdc.com:4993",
            'Cache-Control': "max-age=0",
            'Content-Type':'application/x-www-form-urlencoded',
            'Refer':'http://www.hbczfdc.com:4993/index.aspx'
        }

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
        if response.meta.get('PageType') == 'ProjectBase':
            logging.debug('ProjectBase')

            EVENTARGUMENT = Selector(response).xpath('//*[@id="__EVENTARGUMENT"]/@value').extract_first()
            VIEWSTATE = Selector(response).xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
            EVENTVALIDATION = Selector(response).xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first()

            pagenumstr = Selector(response).xpath('//*[@id="PageNavigator1_LblPageCount"]/text()').extract_first()
            if pagenumstr:
                logging.debug(pagenumstr)
                pagenum = int(pagenumstr)
            else:
                pagenum = 74

            lastpagenum = int(response.meta.get('pagenum'))

            ProjectTables = Selector(response).xpath('//*[@id="wrapper"]/div[3]/div[1]/div[2]/table/tr')
            if ProjectTables:
                for ProjectTable in ProjectTables[1:]:
                    ProjectCode = check_data_str(ProjectTable.xpath('./td[1]/text()').extract_first())
                    logging.debug('ProjectCode' + ProjectCode)

                    ProjectName = check_data_str(ProjectTable.xpath('./td[2]/a/u/text()').extract_first())
                    logging.debug('ProjectName' + ProjectName)

                    ProjectUrl = check_data_str(ProjectTable.xpath('./td[2]/a/@href').extract_first())
                    logging.debug('ProjectUrl' + ProjectUrl)

                    PresaleNo = check_data_str(ProjectTable.xpath('./td[3]/text()').extract_first())
                    logging.debug('PresaleNo' + PresaleNo)

                    DeveloperName = check_data_str(ProjectTable.xpath('./td[4]/text()').extract_first())
                    logging.debug('DeveloperName' + DeveloperName)

                    BUildingNumber = check_data_str(ProjectTable.xpath('./td[5]/text()').extract_first())
                    logging.debug('BUildingNumber' + BUildingNumber)

                    ProjectAddress = check_data_str(ProjectTable.xpath('./td[6]/text()').extract_first())
                    logging.debug('ProjectAddress' + ProjectAddress)

                    if ProjectUrl:
                        ProjectDetailUrl = ProjectUrl.replace('../', self.mainurl)
                        headers = self.headers
                        headers['Refer'] = response.url
                        result.append(Request(url=ProjectDetailUrl,
                                              headers=headers,
                                              method='GET',
                                              meta={
                                                  'PageType': 'ProjectInfo',
                                                  'ProjectName': ProjectName,
                                                  'PresaleNo': PresaleNo,
                                                  'DeveloperName': DeveloperName,
                                                  'BUildingNumber': BUildingNumber,
                                                  'ProjectAddress': ProjectAddress}))
            if lastpagenum < pagenum:
                req_dict = {
                    '__EVENTTARGET': 'PageNavigator1$LnkBtnNext',
                    '__EVENTARGUMENT': EVENTARGUMENT,
                    '__VIEWSTATE': VIEWSTATE,
                    '__EVENTVALIDATION': EVENTVALIDATION,
                    'txtXMMC': '',
                    'txtXMDZ': '',
                    'txtKFQY': '',
                    'txtXkzh': '',
                    'txtCheckCode': '',
                    'PageNavigator1$txtNewPageIndex': lastpagenum + 1
                }
                req_body = urlparse.urlencode(req_dict)
                result.append(Request(
                    url=response.url,
                    body=req_body,
                    headers=self.headers,
                    method='POST',
                    meta={
                    'PageType': 'ProjectBase',
                    'pagenum': lastpagenum + 1
                    }))
        if response.meta.get('PageType') == 'ProjectInfo':
            logging.debug('ProjectInfo')
            Projectbaseitem = ProjectBaseItem()
            ProjectName = response.meta.get('ProjectName')
            PresaleNo = response.meta.get('PresaleNo')
            DeveloperName = response.meta.get('DeveloperName')
            BUildingNumber = response.meta.get('BUildingNumber')
            ProjectAddress = response.meta.get('ProjectAddress')
            Projectbaseitem['ProjectName'] = ProjectName
            Projectbaseitem['PresaleNo'] = PresaleNo
            Projectbaseitem['DeveloperName'] = DeveloperName
            Projectbaseitem['BUildingNumber'] = BUildingNumber
            Projectbaseitem['ProjectAddress'] = ProjectAddress
            Projectbaseitem['ProjectUrl'] = response.url

            BuildingAres = check_data_str(
                Selector(response).xpath('//*[@id="Project_GHZJZMJ"]/text()').extract_first())
            Projectbaseitem['BuildingAres'] = BuildingAres
            logging.debug('BuildingAres' + BuildingAres)

            DistrictName = check_data_str(
                Selector(response).xpath('//*[@id="Project_AREA_NAME"]/text()').extract_first())
            Projectbaseitem['DistrictName'] = DistrictName
            logging.debug('DistrictName' + DistrictName)

            QualificationNumber = check_data_str(
                Selector(response).xpath('//*[@id="lblZZZS"]/text()').extract_first())
            Projectbaseitem['QualificationNumber'] = QualificationNumber
            logging.debug('QualificationNumber' + QualificationNumber)

            QualificationLevel = check_data_str(
                Selector(response).xpath('//*[@id="lblZZDJ"]/text()').extract_first())
            Projectbaseitem['QualificationLevel'] = QualificationLevel
            logging.debug('QualificationLevel' + QualificationLevel)

            soldAmount = check_data_num(Selector(response).xpath('//*[@id="lblYSZTS"]/text()').extract_first())
            Projectbaseitem['soldAmount'] = soldAmount

            UnsoldAmount = check_data_num(Selector(response).xpath('//*[@id="lblWSZTS"]/text()').extract_first())
            Projectbaseitem['UnsoldAmount'] = UnsoldAmount

            soldAreas = check_data_str(Selector(response).xpath('//*[@id="lblYSZMJ"]/text()').extract_first())
            Projectbaseitem['soldAreas'] = soldAreas
            logging.debug('soldAreas' + soldAreas)

            UnsoldAreas = check_data_str(Selector(response).xpath('//*[@id="lblWSZMJ"]/text()').extract_first())
            Projectbaseitem['UnsoldAreas'] = UnsoldAreas
            logging.debug('UnsoldAreas' + UnsoldAreas)

            soldAddress = check_data_str(
                Selector(response).xpath('//*[@id="Project_SLCDH"]/text()').extract_first())
            Projectbaseitem['soldAddress'] = soldAddress
            logging.debug('soldAddress' + soldAddress)

            soldPhonNumber = check_data_str(
                Selector(response).xpath('//*[@id="Project_SLDH"]/text()').extract_first())
            Projectbaseitem['soldPhonNumber'] = soldPhonNumber
            logging.debug('soldPhonNumber' + soldPhonNumber)

            CurrentMonthHouseSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblZZYSTS"]/text()').extract_first())
            Projectbaseitem['CurrentMonthHouseSoldNumber'] = CurrentMonthHouseSoldNumber

            CurrentMonthHouseSoldAreas = check_data_str(
                Selector(response).xpath('//*[@id="lblZZYSMJ"]/text()').extract_first())
            Projectbaseitem['CurrentMonthHouseSoldAreas'] = CurrentMonthHouseSoldAreas

            CurrentMonthBusinessSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblSYYSTS"]/text()').extract_first())
            Projectbaseitem['CurrentMonthBusinessSoldNumber'] = CurrentMonthBusinessSoldNumber

            CurrentMonthBusinessSoldAres = check_data_str(
                Selector(response).xpath('//*[@id="lblSYYSMJ"]/text()').extract_first())
            Projectbaseitem['CurrentMonthBusinessSoldAres'] = CurrentMonthBusinessSoldAres
            logging.debug('CurrentMonthBusinessSoldAres' + CurrentMonthBusinessSoldAres)

            CurrentMonthOtherSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblQTYSTS"]/text()').extract_first())
            Projectbaseitem['CurrentMonthOtherSoldNumber'] = CurrentMonthOtherSoldNumber

            CurrentMonthOtherSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblQTYSMJ"]/text()').extract_first())
            Projectbaseitem['CurrentMonthOtherSoldNumber'] = CurrentMonthOtherSoldNumber

            TotalHouseSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblZZYSZTS"]/text()').extract_first())
            Projectbaseitem['TotalHouseSoldNumber'] = TotalHouseSoldNumber

            TotalHouseSoldAreas = check_data_str(
                Selector(response).xpath('//*[@id="lblZZYSZMJ"]/text()').extract_first())
            Projectbaseitem['TotalHouseSoldAreas'] = TotalHouseSoldAreas
            logging.debug('TotalHouseSoldAreas' + TotalHouseSoldAreas)

            TotalBusinessSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblSYYSZTS"]/text()').extract_first())
            Projectbaseitem['TotalBusinessSoldNumber'] = TotalBusinessSoldNumber

            TotalBusinessSoldAres = check_data_str(
                Selector(response).xpath('//*[@id="lblSYYSZMJ"]/text()').extract_first())
            Projectbaseitem['TotalBusinessSoldAres'] = TotalBusinessSoldAres
            logging.debug('TotalBusinessSoldAres' + TotalBusinessSoldAres)

            TotalOtherSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblQTYSZTS"]/text()').extract_first())
            Projectbaseitem['TotalOtherSoldNumber'] = TotalOtherSoldNumber

            TotalOtherSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblQTYSZMJ"]/text()').extract_first())
            Projectbaseitem['TotalOtherSoldNumber'] = TotalOtherSoldNumber

            HouseUnSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblZZWSTS"]/text()').extract_first())
            Projectbaseitem['HouseUnSoldNumber'] = HouseUnSoldNumber

            HouseUnSoldAreas = check_data_str(
                Selector(response).xpath('//*[@id="lblZZWSMJ"]/text()').extract_first())
            Projectbaseitem['HouseUnSoldAreas'] = HouseUnSoldAreas

            BusinessUnSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblSYWSTS"]/text()').extract_first())
            Projectbaseitem['BusinessUnSoldNumber'] = BusinessUnSoldNumber

            BusinessUnSoldAres = check_data_str(
                Selector(response).xpath('//*[@id="lblSYWSMJ"]/text()').extract_first())
            Projectbaseitem['BusinessUnSoldAres'] = BusinessUnSoldAres
            logging.debug('BusinessUnSoldAres' + BusinessUnSoldAres)

            OtherUnSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblQTWSTS"]/text()').extract_first())
            Projectbaseitem['OtherUnSoldNumber'] = OtherUnSoldNumber

            OtherUnSoldNumber = check_data_num(
                Selector(response).xpath('//*[@id="lblQTWSMJ"]/text()').extract_first())
            Projectbaseitem['OtherUnSoldNumber'] = OtherUnSoldNumber

            ProjectCode = check_data_str(Selector(response).xpath('//*[@id="hdProjectCode"]/@value').extract_first())
            Projectbaseitem['ProjectCode'] = ProjectCode
            logging.debug('ProjectCode' + ProjectCode)

            presellInfoCode = check_data_str(
                Selector(response).xpath('//*[@id="presellInfo"]/@value').extract_first())
            Projectbaseitem['presellInfoCode'] = presellInfoCode
            logging.debug('presellInfoCode' + presellInfoCode)

            buildInfoCode = check_data_str(Selector(response).xpath('//*[@id="buildInfo"]/@value').extract_first())
            Projectbaseitem['buildInfoCode'] = buildInfoCode
            logging.debug('buildInfoCode' + buildInfoCode)

            tdzInfoCode = check_data_str(Selector(response).xpath('//*[@id="tdzInfo"]/@value').extract_first())
            Projectbaseitem['tdzInfoCode'] = tdzInfoCode
            logging.debug('tdzInfoCode' + tdzInfoCode)

            sgxkzInfoCode = check_data_str(Selector(response).xpath('//*[@id="sgxkzInfo"]/@value').extract_first())
            Projectbaseitem['sgxkzInfoCode'] = sgxkzInfoCode
            logging.debug('sgxkzInfoCode' + sgxkzInfoCode)

            ghxkzInfo = check_data_str(Selector(response).xpath('//*[@id="ghxkzInfo"]/@value').extract_first())
            Projectbaseitem['ghxkzInfo'] = ghxkzInfo
            logging.debug('ghxkzInfo' + ghxkzInfo)

            jsydghxkzInfoCode = check_data_str(Selector(response).xpath('//*[@id="jsydghxkzInfo"]/@value').extract_first())
            Projectbaseitem['jsydghxkzInfoCode'] = jsydghxkzInfoCode
            logging.debug('jsydghxkzInfoCode' + jsydghxkzInfoCode)
            Projectbaseitem['SourceUrl'] = response.url

            Projectbaseitem['ProjectNo'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                      ProjectName +
                                                      PresaleNo).hex

            result.append(Projectbaseitem)

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class SpiderMiddlerPresale(object):
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
        if response.meta.get('PageType') == 'PresaleBase':
            logging.debug('PresaleBase')
            Presalebaseitem = PresaleBaseItem()
            ProjectNo = response.meta.get('ProjectNo')
            ProjectName = response.meta.get('ProjectName')

            Presalebaseitem['ProjectNo'] = ProjectNo
            Presalebaseitem['ProjectName'] = ProjectName
            Presalebaseitem['SourceUrl'] = response.url

            PresalePermitNumber = check_data_str(
                Selector(response).xpath('//*[@id="YSXKZ_XKZH"]/text()').extract_first())
            Presalebaseitem['PresalePermitNumber'] = PresalePermitNumber
            logging.debug('PresalePermitNumber' + PresalePermitNumber)

            LssueDate = check_data_str(Selector(response).xpath('//*[@id="YSXKZ_FZRQ"]/text()').extract_first())
            Presalebaseitem['LssueDate'] = LssueDate
            logging.debug('LssueDate' + LssueDate)

            ValidityDateStartDate = check_data_str(
                Selector(response).xpath('//*[@id="YSXKZ_YXQX1"]/text()').extract_first())
            Presalebaseitem['ValidityDateStartDate'] = ValidityDateStartDate
            logging.debug('ValidityDateStartDate' + ValidityDateStartDate)

            ValidityDateClosingDate = check_data_str(
                Selector(response).xpath('//*[@id="YSXKZ_YXQX2"]/text()').extract_first())
            Presalebaseitem['ValidityDateClosingDate'] = ValidityDateClosingDate
            logging.debug('ValidityDateClosingDate' + ValidityDateClosingDate)

            PresalePermitBuildingName = check_data_str(
                Selector(response).xpath('//*[@id="YSZMC"]/text()').extract_first())
            Presalebaseitem['PresalePermitBuildingName'] = PresalePermitBuildingName
            logging.debug('PresalePermitBuildingName' + PresalePermitBuildingName)

            LssuingAuthority = check_data_str(Selector(response).xpath('//*[@id="YSXKZ_FZJG"]/text()').extract_first())
            Presalebaseitem['LssuingAuthority'] = LssuingAuthority
            logging.debug('LssuingAuthority' + LssuingAuthority)

            PresaleCapitalOpenAccountBank = check_data_str(
                Selector(response).xpath('//*[@id="YSXKZ_YSZJKHYH"]/text()').extract_first())
            Presalebaseitem['PresaleCapitalOpenAccountBank'] = PresaleCapitalOpenAccountBank
            logging.debug('PresaleCapitalOpenAccountBank' + PresaleCapitalOpenAccountBank)

            PresaleCapitalManageAccount = check_data_str(
                Selector(response).xpath('//*[@id="YSXKZ_YSZJZH"]/text()').extract_first())
            Presalebaseitem['PresaleCapitalManageAccount'] = PresaleCapitalManageAccount
            logging.debug('PresaleCapitalManageAccount' + PresaleCapitalManageAccount)

            HouseApprovalPresaleAmount = check_data_num(
                Selector(response).xpath('//*[@id="YSXKZ_HZTS_PTZZ"]/text()').extract_first())
            Presalebaseitem['HouseApprovalPresaleAmount'] = HouseApprovalPresaleAmount

            HouseApprovalPresaleArea = check_data_str(
                Selector(response).xpath('//*[@id="YSXKZ_HZMJ_PTZZ"]/text()').extract_first())
            Presalebaseitem['HouseApprovalPresaleArea'] = HouseApprovalPresaleArea

            BussinessApprovalPresaleAmount = check_data_num(
                Selector(response).xpath('//*[@id="YSXKZ_HZTS_SM"]/text()').extract_first())
            Presalebaseitem['BussinessApprovalPresaleAmount'] = BussinessApprovalPresaleAmount

            BussinessApprovalPresaleArea = check_data_str(
                Selector(response).xpath('//*[@id="YSXKZ_HZMJ_SM"]/text()').extract_first())
            Presalebaseitem['BussinessApprovalPresaleArea'] = BussinessApprovalPresaleArea

            OtherApprovalPresaleAmount = check_data_num(
                Selector(response).xpath('//*[@id="YSXKZ_HZTS_QT"]/text()').extract_first())
            Presalebaseitem['OtherApprovalPresaleAmount'] = OtherApprovalPresaleAmount

            OtherApprovalPresaleArea = check_data_str(
                Selector(response).xpath('//*[@id="YSXKZ_HZMJ_QT"]/text()').extract_first())
            Presalebaseitem['OtherApprovalPresaleArea'] = OtherApprovalPresaleArea

            Presalebaseitem['PresaleNo'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                      PresalePermitNumber +
                                                      LssueDate).hex

            if PresalePermitNumber:
                result.append(Presalebaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return

class SpiderMiddlerPlanning(object):
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
        if response.meta.get('PageType') == 'PlanningBase':
            logging.debug('PlanningBase')
            Planningbaseitem = PlanningBaseItem()
            ProjectNo = response.meta.get('ProjectNo')
            ProjectName = response.meta.get('ProjectName')

            Planningbaseitem['ProjectNo'] = ProjectNo
            Planningbaseitem['ProjectName'] = ProjectName
            Planningbaseitem['SourceUrl'] = response.url

            LssuingAuthority = check_data_str(
                Selector(response).xpath('//*[@id="JSGCGHXKZ_FZDW"]/text()').extract_first())
            Planningbaseitem['LssuingAuthority'] = LssuingAuthority
            logging.debug('LssuingAuthority' + LssuingAuthority)

            PlanningPermitNumber = check_data_str(
                Selector(response).xpath('//*[@id="JSGCGHXKZ_ZH"]/text()').extract_first())
            Planningbaseitem['PlanningPermitNumber'] = PlanningPermitNumber
            logging.debug('PlanningPermitNumber' + PlanningPermitNumber)

            LssueDate = check_data_str(Selector(response).xpath('//*[@id="JSGCGHXKZ_FZRQ"]/text()').extract_first())
            Planningbaseitem['LssueDate'] = LssueDate
            logging.debug('LssueDate' + LssueDate)

            ProjectName = check_data_str(Selector(response).xpath('//*[@id="JSGCGHXKZ_GCMC"]/text()').extract_first())
            Planningbaseitem['ProjectName'] = ProjectName
            logging.debug('ProjectName' + ProjectName)

            BuildAddress = check_data_str(Selector(response).xpath('//*[@id="JSGCGHXKZ_JSDZ"]/text()').extract_first())
            Planningbaseitem['BuildAddress'] = BuildAddress
            logging.debug('BuildAddress' + BuildAddress)

            BuildOrganization = check_data_str(
                Selector(response).xpath('//*[@id="JSGCGHXKZ_JSDW"]/text()').extract_first())
            Planningbaseitem['BuildOrganization'] = BuildOrganization
            logging.debug('BuildOrganization' + BuildOrganization)

            BuildArea = check_data_str(Selector(response).xpath('//*[@id="JSGCGHXKZ_JSGM"]/text()').extract_first())
            Planningbaseitem['BuildArea'] = BuildArea
            logging.debug('BuildArea' + BuildArea)

            Remark = check_data_str(Selector(response).xpath('//*[@id="JSGCGHXKZ_BZ"]/text()').extract_first())
            Planningbaseitem['Remark'] = Remark
            logging.debug('Remark' + Remark)

            Planningbaseitem['PlanningNo'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                        PlanningPermitNumber +
                                                        LssueDate).hex
            if PlanningPermitNumber:
                result.append(Planningbaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return



class SpiderMiddlerLand(object):
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
        if response.meta.get('PageType') == 'LandBase':
            logging.debug('LandBase')
            Landbaseitem = LandBaseItem()
            ProjectNo = response.meta.get('ProjectNo')
            ProjectName = response.meta.get('ProjectName')
            Landbaseitem['ProjectNo'] = ProjectNo
            Landbaseitem['ProjectName'] = ProjectName
            Landbaseitem['SourceUrl'] = response.url

            LandCertificateNumber = check_data_str(
                Selector(response).xpath('//*[@id="TDSYQZ_ZH"]/text()').extract_first())
            Landbaseitem['LandCertificateNumber'] = LandCertificateNumber
            logging.debug('LandCertificateNumber' + LandCertificateNumber)

            LandNumber = check_data_str(Selector(response).xpath('//*[@id="TDSYQZ_DH"]/text()').extract_first())
            Landbaseitem['LandNumber'] = LandNumber
            logging.debug('LandNumber' + LandNumber)

            PictureNumber = check_data_str(Selector(response).xpath('//*[@id="TDSYQZ_TH"]/text()').extract_first())
            Landbaseitem['PictureNumber'] = PictureNumber
            logging.debug('PictureNumber' + PictureNumber)

            LandUseType = check_data_str(Selector(response).xpath('//*[@id="YSXKZ_QSXZ"]/text()').extract_first())
            Landbaseitem['LandUseType'] = LandUseType
            logging.debug('LandUseType' + LandUseType)

            LandUser = check_data_str(Selector(response).xpath('//*[@id="TDSYQZ_SQZ"]/text()').extract_first())
            Landbaseitem['LandUser'] = LandUser
            logging.debug('LandUser' + LandUser)

            LandAddress = check_data_str(Selector(response).xpath('//*[@id="TDSYQZ_TDZL"]/text()').extract_first())
            Landbaseitem['LandAddress'] = LandAddress
            logging.debug('LandAddress' + LandAddress)

            LssueDate = check_data_str(Selector(response).xpath('//*[@id="TDSYQZ_FZRQ"]/text()').extract_first())
            Landbaseitem['LssueDate'] = LssueDate
            logging.debug('LssueDate' + LssueDate)

            EndDate = check_data_str(Selector(response).xpath('//*[@id="TDSYQZ_ZZRQ"]/text()').extract_first())
            Landbaseitem['EndDate'] = EndDate
            logging.debug('EndDate' + EndDate)

            RightAreaOfUse = check_data_str(Selector(response).xpath('//*[@id="TDSYQZ_ZDMJ"]/text()').extract_first())
            Landbaseitem['RightAreaOfUse'] = RightAreaOfUse
            logging.debug('RightAreaOfUse' + RightAreaOfUse)

            AcquireWay = check_data_str(Selector(response).xpath('//*[@id="TDSYQZ_QDFS"]/text()').extract_first())
            Landbaseitem['AcquireWay'] = AcquireWay
            logging.debug('AcquireWay' + AcquireWay)

            Landbaseitem['LandNo'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                LandNumber +
                                                LssueDate).hex

            if LandNumber:
                result.append(Landbaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return



class SpiderMiddlerHouse(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.hbczfdc.com:4993",
            'User-Agent':random.choice(self.settings.get('USER_AGENTS')),
            'Cache-Control': "max-age=0",
            'Content-Type':'application/x-www-form-urlencoded',
            'Refer':'http://www.hbczfdc.com:4993/index.aspx'}

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        def get_re_date(restring,datestring):
            result_date = ''
            re_dates = re.findall(restring,datestring)
            if re_dates:
                if len(re_dates) > 1:
                    for re_d in re_dates:
                        result_date = result_date + '|' + re_d
                elif len(re_dates) == 1:
                    result_date = re_dates[0]
            return result_date
        def get_house_sts(string):
            houseStsClass = {
                '#00FF00':'待销售',
                '#FF00FF':'已预定',
                '#FFFF00': '已签约',
                '#FF0000': '已备案',
                '#CCCCCC': '限制销售',
                '#87CEFF': '已过户',

            }
            houseSts = ''
            if string in houseStsClass.keys():
                houseSts = houseStsClass[string]
            return houseSts


        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'HouseBase':
            logging.debug('HouseBase')
            ProjectNo = response.meta.get('ProjectNo')
            ProjectName = response.meta.get('ProjectName')
            BuildName = response.meta.get('BuildName')
            ProjectCode = response.meta.get('ProjectCode')
            BuildCode = response.meta.get('BuildCode')


            RoomDatas = re.findall(r'nowrap(.*?)</td>', check_data_str(response.body_as_unicode()))
            for RoomData in RoomDatas:
                Housebaseitem = HouseBaseItem()

                Housebaseitem['ProjectNo'] = ProjectNo
                Housebaseitem['ProjectName'] = ProjectName
                Housebaseitem['BuildName'] = BuildName
                Housebaseitem['ProjectCode'] = ProjectCode
                Housebaseitem['BuildCode'] = BuildCode
                HouseNum = check_data_str(get_re_date(r"房号：(.*?)建筑", RoomData))
                logging.debug('HouseNum' + HouseNum)
                Housebaseitem['HouseNum'] = HouseNum

                HouseDetailUrlCode = check_data_str(get_re_date(r"clickRoom\('(.*?)'\)", RoomData))
                HouseDetailUrl = 'http://www.hbczfdc.com:4993/HPMS/RoomInfo.aspx?code=%s&PCODE=%s' \
                                 % (HouseDetailUrlCode, ProjectCode)
                logging.debug('HouseDetailUrl' + HouseDetailUrl)
                Housebaseitem['HouseDetailUrl'] = HouseDetailUrl

                UnitNum = check_data_str(get_re_date(r"单元：(.*?)规划用途", RoomData))
                logging.debug('UnitNum' + UnitNum)
                Housebaseitem['UnitNum'] = UnitNum

                HouseType = check_data_str(get_re_date(r"规划用途：(.*?)'>", RoomData))
                logging.debug('HouseType' + HouseType)
                Housebaseitem['HouseType'] = HouseType

                TotalAreas = check_data_str(get_re_date(r"建筑面积：(.*?)单元", RoomData))
                logging.debug('TotalAreas' + TotalAreas)
                Housebaseitem['TotalAreas'] = TotalAreas

                SellSchedule = check_data_str(get_re_date(r"alt='(.*?)'", RoomData))
                logging.debug('SellSchedule' + SellSchedule)
                Housebaseitem['SellSchedule'] = SellSchedule

                HouseStsColor = check_data_str(get_re_date(r"color:(.*?);", RoomData))
                HouseSts = get_house_sts(HouseStsColor)
                logging.debug('HouseSts' + HouseSts)
                Housebaseitem['HouseSts'] = HouseSts

                Housebaseitem['HouseNo'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                      HouseNum +
                                                      UnitNum +
                                                      ProjectName +
                                                      BuildName).hex

                if HouseDetailUrl:
                    InfoUrl = HouseDetailUrl
                    headers = self.headers
                    headers['Refer'] = response.url
                    result.append(Request(url=InfoUrl,
                                          headers=headers,
                                          method='GET',
                                          meta={
                                              'PageType': 'HouseInfo',
                                              'item': Housebaseitem
                                          }))

        if response.meta.get('PageType') == 'ListHouseBase':
            logging.debug('ListHouseBase')

            ProjectName = response.meta.get('ProjectName')

            BuildName = response.meta.get('BuildName')

            houseTables = Selector(response).xpath('//*[@id="divRoomList"]/table/tr')
            if houseTables:
                for houseTable in houseTables[1:]:
                    Housebaseitem = HouseBaseItem()

                    Housebaseitem['ProjectName'] = ProjectName
                    Housebaseitem['BuildName'] = BuildName

                    HouseNum = check_data_str(houseTable.xpath('./td[1]/a/u/text()').extract_first())
                    logging.debug('HouseNum' + HouseNum)
                    Housebaseitem['HouseNum'] = HouseNum

                    HouseDetailUrl = check_data_str(houseTable.xpath('./td[1]/a/@href').extract_first())
                    logging.debug('HouseDetailUrl' + HouseDetailUrl)
                    Housebaseitem['HouseDetailUrl'] = HouseDetailUrl

                    UnitNum = check_data_str(houseTable.xpath('./td[2]/text()').extract_first())
                    logging.debug('UnitNum' + UnitNum)
                    Housebaseitem['UnitNum'] = UnitNum

                    HouseType = check_data_str(houseTable.xpath('./td[3]/text()').extract_first())
                    logging.debug('HouseType' + HouseType)
                    Housebaseitem['HouseType'] = HouseType

                    TotalAreas = check_data_str(houseTable.xpath('./td[4]/text()').extract_first())
                    logging.debug('TotalAreas' + TotalAreas)
                    Housebaseitem['TotalAreas'] = TotalAreas

                    InsideOfBuildingArea = check_data_str(houseTable.xpath('./td[5]/text()').extract_first())
                    logging.debug('InsideOfBuildingArea' + InsideOfBuildingArea)
                    Housebaseitem['InsideOfBuildingArea'] = InsideOfBuildingArea

                    HouseSts = check_data_str(houseTable.xpath('./td[6]/text()').extract_first())
                    logging.debug('HouseSts' + HouseSts)
                    Housebaseitem['HouseSts'] = HouseSts

                    Housebaseitem['HouseNo'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                          HouseNum +
                                                          UnitNum +
                                                          ProjectName +
                                                          BuildName).hex

                    if HouseDetailUrl:
                        InfoUrl = 'http://www.hbczfdc.com:4993/HPMS/' + HouseDetailUrl
                        headers = self.headers
                        headers['Refer'] = response.url
                        result.append(Request(url=InfoUrl,
                                              headers=headers,
                                              method='GET',
                                              meta={
                                                  'PageType': 'HouseInfo',
                                                  'item': Housebaseitem
                                              }))

        if response.meta.get('PageType') == 'HouseInfo':
            logging.debug('HouseInfo')

            houseitem = response.meta.get('item')
            Housebaseitem = copy.deepcopy(houseitem)
            Housebaseitem['SourceUrl'] = response.url

            HouseFloor = check_data_str(Selector(response).xpath('//*[@id="ROOM_MYC"]/text()').extract_first())
            Housebaseitem['HouseFloor'] = HouseFloor
            logging.debug('HouseFloor' + HouseFloor)

            HouseBelongSts = check_data_str(Selector(response).xpath('//*[@id="ROOM_QSZT"]/text()').extract_first())
            Housebaseitem['HouseBelongSts'] = HouseBelongSts
            logging.debug('HouseBelongSts' + HouseBelongSts)

            HouseNature = check_data_str(Selector(response).xpath('//*[@id="ROOM_FWXZ"]/text()').extract_first())
            Housebaseitem['HouseNature'] = HouseNature
            logging.debug('HouseNature' + HouseNature)

            HouseUseType = check_data_str(Selector(response).xpath('//*[@id="ROOM_FWYT"]/text()').extract_first())
            Housebaseitem['HouseUseType'] = HouseUseType
            logging.debug('HouseUseType' + HouseUseType)

            UnitShape = check_data_str(Selector(response).xpath('//*[@id="ROOM_HX"]/text()').extract_first())
            Housebaseitem['UnitShape'] = UnitShape
            logging.debug('UnitShape' + UnitShape)

            BuildingStructure = check_data_str(
                Selector(response).xpath('//*[@id="ROOM_HXJG"]/text()').extract_first())
            Housebaseitem['BuildingStructure'] = BuildingStructure
            logging.debug('BuildingStructure' + BuildingStructure)

            ForecastBuildingArea = check_data_str(
                Selector(response).xpath('//*[@id="ROOM_YCJZMJ"]/text()').extract_first())
            Housebaseitem['ForecastBuildingArea'] = ForecastBuildingArea
            logging.debug('ForecastBuildingArea' + ForecastBuildingArea)

            MeasuredBuildingArea = check_data_str(
                Selector(response).xpath('//*[@id="ROOM_SCJZMJ"]/text()').extract_first())
            Housebaseitem['MeasuredBuildingArea'] = MeasuredBuildingArea
            logging.debug('MeasuredBuildingArea' + MeasuredBuildingArea)

            ForecastInsideOfBuildingArea = check_data_str(
                Selector(response).xpath('//*[@id="ROOM_YCTNJZMJ"]/text()').extract_first())
            Housebaseitem['ForecastInsideOfBuildingArea'] = ForecastInsideOfBuildingArea
            logging.debug('ForecastInsideOfBuildingArea' + ForecastInsideOfBuildingArea)

            MeasuredInsideOfBuildingArea = check_data_str(
                Selector(response).xpath('//*[@id="ROOM_SCTNJZMJ"]/text()').extract_first())
            Housebaseitem['MeasuredInsideOfBuildingArea'] = MeasuredInsideOfBuildingArea
            logging.debug('MeasuredInsideOfBuildingArea' + MeasuredInsideOfBuildingArea)

            ForecastPublicArea = check_data_str(
                Selector(response).xpath('//*[@id="ROOM_YCFTJZMJ"]/text()').extract_first())
            Housebaseitem['ForecastPublicArea'] = ForecastPublicArea
            logging.debug('ForecastPublicArea' + ForecastPublicArea)

            MeasuredSharedPublicArea = check_data_str(
                Selector(response).xpath('//*[@id="ROOM_SCFTJZMJ"]/text()').extract_first())
            Housebaseitem['MeasuredSharedPublicArea'] = MeasuredSharedPublicArea
            logging.debug('MeasuredSharedPublicArea' + MeasuredSharedPublicArea)

            Address = check_data_str(Selector(response).xpath('//*[@id="ROOM_FWZL"]/text()').extract_first())
            Housebaseitem['Address'] = Address
            logging.debug('Address' + Address)
            if UnitShape:
                result.append(Housebaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class SpiderMiddlerDeveloper(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.mainurl = 'http://www.hbczfdc.com:4993/'
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.hbczfdc.com:4993",
            'User-Agent': random.choice(self.settings.get('USER_AGENTS')),
            'Cache-Control': "max-age=0",
            'Content-Type': 'application/x-www-form-urlencoded',
            'Refer': 'http://www.hbczfdc.com:4993/HEMS/CompanyList.aspx?type=1'
        }

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
        if response.meta.get('PageType') == 'DeveloperBase':
            logging.debug('DeveloperBase')

            EVENTARGUMENT = Selector(response).xpath('//*[@id="__EVENTARGUMENT"]/@value').extract_first()
            VIEWSTATE = Selector(response).xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
            EVENTVALIDATION = Selector(response).xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first()

            pagenumstr = Selector(response).xpath('//*[@id="PageNavigator1_LblPageCount"]/text()').extract_first()

            if pagenumstr:
                logging.debug(pagenumstr)
                pagenum = int(pagenumstr)
            else:
                pagenum = 7

            lastpagenum = int(response.meta.get('pagenum'))

            DeveloperTables = Selector(response).xpath('//*[@id="wrapper"]/div[3]/div[1]/div[2]/table/tr')
            if DeveloperTables:
                for DeveloperTable in DeveloperTables:
                    Developerbaseitem = DeveloperBaseItem()
                    QualificationNumber = check_data_str(DeveloperTable.xpath('./td[2]/text()').extract_first())
                    logging.debug('QualificationNumber' + QualificationNumber)
                    Developerbaseitem['QualificationNumber'] = QualificationNumber

                    QualificationLevel = check_data_str(DeveloperTable.xpath('./td[3]/text()').extract_first())
                    logging.debug('QualificationLevel' + QualificationLevel)
                    Developerbaseitem['QualificationLevel'] = QualificationLevel

                    DeveloperName = check_data_str(DeveloperTable.xpath('./td[4]/a/u/text()').extract_first())
                    logging.debug('DeveloperName' + DeveloperName)
                    Developerbaseitem['DeveloperName'] = DeveloperName

                    DeveloperDetailUrl = check_data_str(DeveloperTable.xpath('./td[4]/a/@href').extract_first())
                    logging.debug('DeveloperDetailUrl' + DeveloperDetailUrl)
                    Developerbaseitem['DeveloperDetailUrl'] = DeveloperDetailUrl

                    LegalPersonName = check_data_str(DeveloperTable.xpath('./td[5]/text()').extract_first())
                    logging.debug('LegalPersonName' + LegalPersonName)
                    Developerbaseitem['LegalPersonName'] = LegalPersonName

                    LssueDate = check_data_str(DeveloperTable.xpath('./td[6]/text()').extract_first())
                    logging.debug('LssueDate' + LssueDate)
                    Developerbaseitem['LssueDate'] = LssueDate

                    Developerbaseitem['DeveloperNo'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                                  QualificationNumber +
                                                                  DeveloperName +
                                                                  LssueDate).hex

                    if lastpagenum < pagenum:
                        req_dict = {
                            '__EVENTTARGET': 'PageNavigator1$LnkBtnNext',
                            '__EVENTARGUMENT': EVENTARGUMENT,
                            '__VIEWSTATE': VIEWSTATE,
                            '__EVENTVALIDATION': EVENTVALIDATION,
                            'txtCompanyName': '',
                            'txtZzzsbh': '',
                            'PageNavigator1$txtNewPageIndex': lastpagenum + 1,
                        }
                        req_body = urlparse.urlencode(req_dict)
                        result.append(Request(url=response.url, body=req_body, headers=self.headers, method='POST'
                                              , meta={'PageType': 'DeveloperBase',
                                                      'pagenum': lastpagenum + 1
                                                      }))

                    if DeveloperDetailUrl:
                        InfoUrl = DeveloperDetailUrl.replace("../", self.mainurl)
                        result.append(Request(url=InfoUrl,
                                              headers=self.headers,
                                              method='GET',
                                              meta={'PageType': 'DeveloperInfo',
                                                    'item': Developerbaseitem
                                                    }))

        if response.meta.get('PageType') == 'DeveloperInfo':
            logging.debug('DeveloperInfo')

            developitem = response.meta.get('item')
            Developerbaseitem = copy.deepcopy(developitem)

            BusinessLicenseRegistrationNumber = check_data_str(
                Selector(response).xpath('//*[@id="COMPANY_YYZZBH"]/text()').extract_first())
            Developerbaseitem['BusinessLicenseRegistrationNumber'] = BusinessLicenseRegistrationNumber
            logging.debug('BusinessLicenseRegistrationNumber' + BusinessLicenseRegistrationNumber)

            Territorial = check_data_str(Selector(response).xpath('//*[@id="COMPANY_SD"]/text()').extract_first())
            Developerbaseitem['Territorial'] = Territorial
            logging.debug('Territorial' + Territorial)

            Email = check_data_str(Selector(response).xpath('//*[@id="COMPANY_DZYX"]/text()').extract_first())
            Developerbaseitem['Email'] = Email
            logging.debug('Email' + Email)

            LegalPersonName = check_data_str(
                Selector(response).xpath('//*[@id="COMPANY_FRDB"]/text()').extract_first())
            Developerbaseitem['LegalPersonName'] = LegalPersonName
            logging.debug('LegalPersonName' + LegalPersonName)

            ContactsName = check_data_str(Selector(response).xpath('//*[@id="COMPANY_LXR"]/text()').extract_first())
            Developerbaseitem['ContactsName'] = ContactsName
            logging.debug('ContactsName' + ContactsName)

            ContactsPhone = check_data_str(
                Selector(response).xpath('//*[@id="COMPANY_LXDH"]/text()').extract_first())
            Developerbaseitem['ContactsPhone'] = ContactsPhone
            logging.debug('ContactsPhone' + ContactsPhone)

            PostalCode = check_data_str(Selector(response).xpath('//*[@id="COMPANY_YZBM"]/text()').extract_first())
            Developerbaseitem['PostalCode'] = PostalCode
            logging.debug('PostalCode' + PostalCode)

            RegisteredCapital = check_data_str(
                Selector(response).xpath('//*[@id="COMPANY_ZCZB"]/text()').extract_first())
            Developerbaseitem['RegisteredCapital'] = RegisteredCapital
            logging.debug('RegisteredCapital' + RegisteredCapital)

            EnterpriseIntroduction = check_data_str(
                Selector(response).xpath('//*[@id="COMPANY_QYJJ"]/text()').extract_first())
            Developerbaseitem['EnterpriseIntroduction'] = EnterpriseIntroduction
            logging.debug('EnterpriseIntroduction' + EnterpriseIntroduction)

            ScopeOperation = check_data_str(
                Selector(response).xpath('//*[@id="COMPANY_JYFW"]/text()').extract_first())
            Developerbaseitem['ScopeOperation'] = ScopeOperation
            logging.debug('ScopeOperation' + ScopeOperation)

            TypeCompany = check_data_str(Selector(response).xpath('//*[@id="COMPANY_ZCLX"]/text()').extract_first())
            Developerbaseitem['TypeCompany'] = TypeCompany
            logging.debug('TypeCompany' + TypeCompany)

            QualificationEndDate = check_data_str(
                Selector(response).xpath('//*[@id="COMPANY_YXQX"]/text()').extract_first())
            Developerbaseitem['QualificationEndDate'] = QualificationEndDate
            logging.debug('QualificationEndDate' + QualificationEndDate)

            DateOfApproval = check_data_str(
                Selector(response).xpath('//*[@id="COMPANY_CYRQ"]/text()').extract_first())
            Developerbaseitem['DateOfApproval'] = DateOfApproval
            logging.debug('DateOfApproval' + DateOfApproval)

            Developerbaseitem['SourceUrl'] = response.url

            result.append(Developerbaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):

        return


class SpiderMiddlerConstructionLandPlanning(object):

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
        if response.meta.get('PageType') == 'ConstructionLandPlanningBase':
            logging.debug('ConstructionLandPlanningBase')
            ConstructionLandPlanningbaseitem = ConstructionLandPlanningBaseItem()

            LssuingAuthority = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_FZDW"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['LssuingAuthority'] = LssuingAuthority
            logging.debug('LssuingAuthority' + LssuingAuthority)

            ConstructionPermitNumber = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_ZH"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['ConstructionPermitNumber'] = ConstructionPermitNumber
            logging.debug('ConstructionPermitNumber' + ConstructionPermitNumber)

            LssueDate = check_data_str(Selector(response).xpath('//*[@id="JZGCSGXKZ_FZRQ"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['LssueDate'] = LssueDate
            logging.debug('LssueDate' + LssueDate)

            BuildProjectName = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_GCMC"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['BuildProjectName'] = BuildProjectName
            logging.debug('BuildProjectName' + BuildProjectName)

            BuildAddress = check_data_str(Selector(response).xpath('//*[@id="JZGCSGXKZ_JSDZ"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['BuildAddress'] = BuildAddress
            logging.debug('BuildAddress' + BuildAddress)

            BuildOrganization = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_JSDW"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['BuildOrganization'] = BuildOrganization
            logging.debug('BuildOrganization' + BuildOrganization)

            BuildArea = check_data_str(Selector(response).xpath('//*[@id="JZGCSGXKZ_JSGM"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['BuildArea'] = BuildArea
            logging.debug('BuildArea' + BuildArea)

            DesignOrganization = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_SJDW"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['DesignOrganization'] = DesignOrganization
            logging.debug('DesignOrganization' + DesignOrganization)

            BuildOrganization = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_SGDW"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['BuildOrganization'] = BuildOrganization
            logging.debug('BuildOrganization' + BuildOrganization)

            SuperviseOrganization = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_JLDW"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['SuperviseOrganization'] = SuperviseOrganization
            logging.debug('SuperviseOrganization' + SuperviseOrganization)

            ContractStartDate = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_ZDMJ"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['ContractStartDate'] = ContractStartDate
            logging.debug('ContractStartDate' + ContractStartDate)

            ContractEndDate = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_QDFS"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['ContractEndDate'] = ContractEndDate
            logging.debug('ContractEndDate' + ContractEndDate)

            ContractPrice = check_data_str(Selector(response).xpath('//*[@id="JZGCSGXKZ_QDJG"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['ContractPrice'] = ContractPrice
            logging.debug('ContractPrice' + ContractPrice)

            Remark = check_data_str(Selector(response).xpath('//*[@id="JZGCSGXKZ_BZ"]/text()').extract_first())
            ConstructionLandPlanningbaseitem['Remark'] = Remark
            logging.debug('Remark' + Remark)
            ConstructionLandPlanningbaseitem['ConstructionLandPlanningNo'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                                                        ConstructionPermitNumber +
                                                                                        ContractStartDate +
                                                                                        LssueDate).hex
            if ConstructionPermitNumber:
                result.append(ConstructionLandPlanningbaseitem)

        return result

    def process_spider_exception(self, response, exception, spider):

        return



class SpiderMiddlerConstruction(object):

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
        if response.meta.get('PageType') == 'ConstructionBase':
            logging.debug('ConstructionBase')
            Constructionbaseitem = ConstructionBaseItem()


            LssuingAuthority = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_FZDW"]/text()').extract_first())
            Constructionbaseitem['LssuingAuthority'] = LssuingAuthority
            logging.debug('LssuingAuthority' + LssuingAuthority)

            ConstructionPermitNumber = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_ZH"]/text()').extract_first())
            Constructionbaseitem['ConstructionPermitNumber'] = ConstructionPermitNumber
            logging.debug('ConstructionPermitNumber' + ConstructionPermitNumber)

            LssueDate = check_data_str(Selector(response).xpath('//*[@id="JZGCSGXKZ_FZRQ"]/text()').extract_first())
            Constructionbaseitem['LssueDate'] = LssueDate
            logging.debug('LssueDate' + LssueDate)

            BuildProjectName = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_GCMC"]/text()').extract_first())
            Constructionbaseitem['BuildProjectName'] = BuildProjectName
            logging.debug('BuildProjectName' + BuildProjectName)

            BuildAddress = check_data_str(Selector(response).xpath('//*[@id="JZGCSGXKZ_JSDZ"]/text()').extract_first())
            Constructionbaseitem['BuildAddress'] = BuildAddress
            logging.debug('BuildAddress' + BuildAddress)

            BuildOrganization = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_JSDW"]/text()').extract_first())
            Constructionbaseitem['BuildOrganization'] = BuildOrganization
            logging.debug('BuildOrganization' + BuildOrganization)

            BuildArea = check_data_str(Selector(response).xpath('//*[@id="JZGCSGXKZ_JSGM"]/text()').extract_first())
            Constructionbaseitem['BuildArea'] = BuildArea
            logging.debug('BuildArea' + BuildArea)

            DesignOrganization = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_SJDW"]/text()').extract_first())
            Constructionbaseitem['DesignOrganization'] = DesignOrganization
            logging.debug('DesignOrganization' + DesignOrganization)

            BuildOrganization = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_SGDW"]/text()').extract_first())
            Constructionbaseitem['BuildOrganization'] = BuildOrganization
            logging.debug('BuildOrganization' + BuildOrganization)

            SuperviseOrganization = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_JLDW"]/text()').extract_first())
            Constructionbaseitem['SuperviseOrganization'] = SuperviseOrganization
            logging.debug('SuperviseOrganization' + SuperviseOrganization)

            ContractStartDate = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_ZDMJ"]/text()').extract_first())
            Constructionbaseitem['ContractStartDate'] = ContractStartDate
            logging.debug('ContractStartDate' + ContractStartDate)

            ContractEndDate = check_data_str(
                Selector(response).xpath('//*[@id="JZGCSGXKZ_QDFS"]/text()').extract_first())
            Constructionbaseitem['ContractEndDate'] = ContractEndDate
            logging.debug('ContractEndDate' + ContractEndDate)

            ContractPrice = check_data_str(Selector(response).xpath('//*[@id="JZGCSGXKZ_QDJG"]/text()').extract_first())
            Constructionbaseitem['ContractPrice'] = ContractPrice
            logging.debug('ContractPrice' + ContractPrice)

            Remark = check_data_str(Selector(response).xpath('//*[@id="JZGCSGXKZ_BZ"]/text()').extract_first())
            Constructionbaseitem['Remark'] = Remark
            logging.debug('Remark' + Remark)

            Constructionbaseitem['ConstructionNo'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                                ConstructionPermitNumber +
                                                                ContractStartDate +
                                                                LssueDate).hex
            result.append(Constructionbaseitem)

        return result

    def process_spider_exception(self, response, exception, spider):

        return




