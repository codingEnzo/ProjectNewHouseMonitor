# -*- coding: utf-8 -*-
import uuid
import re
import copy
import redis
import json
import logging
from scrapy import Request
from scrapy import Selector
from HouseCrawler.Items.ItemsNJ import *
'''
    Created on 2017-12-07 15:15:25.
'''
contextflag = True


def check_data_num(string):
    result_data = ''
    if string:
        result_data = string.strip()
        fix_data = {'\r': '', '幢': '', '一房一价：元': '',
                    '\n': '', '套': '', '\\': '', '\t': '',
                    '㎡': '', ' ': '', '/': '', '个': '',
                    "%": '', 'm': '', 'M': '', '²': '',
                    '元': '', ',': '',
                    }
        for r in fix_data:
            result_data = result_data.strip().replace(r, fix_data[r])
    return result_data


def check_data_str(string):
    result_data = ''
    if string:
        result_data = string.strip()
        fix_data = {'\r': '', '\n': '', '\t': '', '</span>': '', '\\': '',
                    ' ': '', '<span>': '', '<br></span>': '', '<br>': '|',
                    }
        for r in fix_data:
            result_data = result_data.strip().replace(r, fix_data[r])
    return result_data


class SpiderMiddlerGetBase(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings
        self.r = redis.Redis(host=self.settings.get(
            'REDIS_HOST') or '10.30.1.18', port=self.settings.get('REDIS_PORT') or 6379)
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.njhouse.com.cn",
            'Cache-Control': "max-age=0",
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
        if response.meta.get('PageType') == 'GetPageBase':
            logging.debug('GetPageBase')
            headers = self.headers
            headers['Refer'] = response.url
            PresalePageNum = re.search(r'共(.*?)页', response.body_as_unicode())
            if PresalePageNum:
                logging.debug('PresalePageNum' + PresalePageNum.group(1))
                for pagenum in range(1, int(PresalePageNum.group(1)) + 1):
                    if 'persalereg' in response.url:
                        persaleUrl = 'http://www.njhouse.com.cn/2016/spf/persalereg.php?dist=&use=&saledate=&pgno=%s' % pagenum
                        result.append(Request(url=persaleUrl, headers=headers, meta={
                                      'PageType': 'PresaleBase'}))
                    elif 'list' in response.url:
                        projectUrl = 'http://www.njhouse.com.cn/2016/spf/list.php?dist=&use=0&saledate=0&pgno=%s' % pagenum
                        result.append(Request(url=projectUrl, headers=headers, meta={
                                      'PageType': 'ProjectBase'}))
                    elif 'qy' in response.url:
                        qyUrl = 'http://www.njhouse.com.cn/2016/qy/index.php?lanmu=&keyword=&pgno=%s' % pagenum
                        result.append(Request(url=qyUrl, headers=headers, meta={
                                      'PageType': 'DeveloperBase'}))
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
        self.r = redis.Redis(host=self.settings.get(
            'REDIS_HOST') or '10.30.1.18', port=self.settings.get('REDIS_PORT') or 6379)
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.njhouse.com.cn",
            'Cache-Control': "max-age=0",
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
            Developerbaseitem = DeveloperBaseItem()

            Developertables = Selector(response).xpath(
                '//*[@id="news_se_frm"]/div[2]/table/tbody/tr')
            if Developertables:
                for Developertable in Developertables:
                    DeveloperName = check_data_str(
                        Developertable.xpath('./td[1]/a/text()').extract_first())
                    logging.debug('DeveloperName' + DeveloperName)
                    Developerbaseitem['DeveloperName'] = DeveloperName

                    DeveloperNo = uuid.uuid3(
                        uuid.NAMESPACE_DNS, str(DeveloperName)).hex
                    Developerbaseitem['DeveloperNo'] = DeveloperNo

                    DeveloperComAddress = check_data_str(
                        Developertable.xpath('./td[2]/text()').extract_first())
                    logging.debug('DeveloperComAddress' + DeveloperComAddress)
                    Developerbaseitem[
                        'DeveloperComAddress'] = DeveloperComAddress

                    DeveloperZipCode = check_data_str(
                        Developertable.xpath('./td[3]/text()').extract_first())
                    logging.debug('DeveloperZipCode' + DeveloperZipCode)
                    Developerbaseitem['DeveloperZipCode'] = DeveloperZipCode

                    DeveloperInfoUrl = check_data_str(
                        Developertable.xpath('./td[1]/a/@href').extract_first())
                    logging.debug('DeveloperInfoUrl' + DeveloperInfoUrl)
                    Developerbaseitem[
                        'DeveloperInfoUrl'] = 'http://www.njhouse.com.cn/2016/qy/' + DeveloperInfoUrl

                    headers = self.headers
                    headers['Refer'] = response.url

                    result.append(Request(url='http://www.njhouse.com.cn/2016/qy/' + DeveloperInfoUrl,
                                          method='GET',
                                          headers=headers,
                                          meta={
                                              'PageType': 'DeveloperInfo',
                                              "item": copy.deepcopy(Developerbaseitem)
                                          }
                                          ))

        if response.meta.get('PageType') == 'DeveloperInfo':
            logging.debug('DeveloperBase')

            Developeritem = response.meta.get('item')
            Developerbaseitem = copy.deepcopy(Developeritem)

            Legalrepresentative = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[2]/text()').extract_first())
            Developerbaseitem['Legalrepresentative'] = Legalrepresentative
            logging.debug('Legalrepresentative' + Legalrepresentative)

            CorporateCode = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[4]/text()').extract_first())
            Developerbaseitem['CorporateCode'] = CorporateCode
            logging.debug('CorporateCode' + CorporateCode)

            GeneralManager = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]/text()').extract_first())
            Developerbaseitem['GeneralManager'] = GeneralManager
            logging.debug('GeneralManager' + GeneralManager)

            ContactNumber = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[4]/text()').extract_first())
            Developerbaseitem['ContactNumber'] = ContactNumber
            logging.debug('ContactNumber' + ContactNumber)

            Businesslicensenumber = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[2]/text()').extract_first())
            Developerbaseitem['Businesslicensenumber'] = Businesslicensenumber
            logging.debug('Businesslicensenumber' + Businesslicensenumber)

            BusinessRegistrationDay = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[4]/td[4]/text()').extract_first())
            Developerbaseitem[
                'BusinessRegistrationDay'] = BusinessRegistrationDay
            logging.debug('BusinessRegistrationDay' + BusinessRegistrationDay)

            LicenseExpiryDate = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[5]/td[2]/text()').extract_first())
            Developerbaseitem['LicenseExpiryDate'] = LicenseExpiryDate
            logging.debug('LicenseExpiryDate' + LicenseExpiryDate)

            RegisteredCapital = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[5]/td[4]/text()').extract_first())
            Developerbaseitem['RegisteredCapital'] = RegisteredCapital
            logging.debug('RegisteredCapital' + RegisteredCapital)

            BusinessRegistrationType = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[6]/td[2]/text()').extract_first())
            Developerbaseitem[
                'BusinessRegistrationType'] = BusinessRegistrationType
            logging.debug('BusinessRegistrationType' +
                          BusinessRegistrationType)

            Email = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[6]/td[4]/text()').extract_first())
            Developerbaseitem['Email'] = Email
            logging.debug('Email' + Email)

            RegisteredAddress = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[7]/td[2]/text()').extract_first())
            Developerbaseitem['RegisteredAddress'] = RegisteredAddress
            logging.debug('RegisteredAddress' + RegisteredAddress)

            BusinessAddress = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[8]/td[2]/text()').extract_first())
            Developerbaseitem['BusinessAddress'] = BusinessAddress
            logging.debug('BusinessAddress' + BusinessAddress)

            BusinessScope = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[9]/td[2]/text()').extract_first())
            Developerbaseitem['BusinessScope'] = BusinessScope
            logging.debug('BusinessScope' + BusinessScope)

            QualificationCertificateNumber = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[10]/td[2]/text()').extract_first())
            Developerbaseitem[
                'QualificationCertificateNumber'] = QualificationCertificateNumber
            logging.debug('QualificationCertificateNumber' +
                          QualificationCertificateNumber)

            QualificationLevel = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[10]/td[4]/text()').extract_first())
            Developerbaseitem['QualificationLevel'] = QualificationLevel
            logging.debug('QualificationLevel' + QualificationLevel)

            QualificationCertificationDate = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[11]/td[2]/text()').extract_first())
            Developerbaseitem[
                'QualificationCertificationDate'] = QualificationCertificationDate
            logging.debug('QualificationCertificationDate' +
                          QualificationCertificationDate)

            QualificationPeriod = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[11]/td[4]/text()').extract_first())
            Developerbaseitem['QualificationPeriod'] = QualificationPeriod
            logging.debug('QualificationPeriod' + QualificationPeriod)

            Approvedfortheday = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[12]/td[2]/text()').extract_first())
            Developerbaseitem['Approvedfortheday'] = Approvedfortheday
            logging.debug('Approvedfortheday' + Approvedfortheday)

            AnnualInspection = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[1]/tbody/tr[12]/td[4]/text()').extract_first())
            Developerbaseitem['AnnualInspection'] = AnnualInspection
            logging.debug('AnnualInspection' + AnnualInspection)

            CompanyProfile = check_data_str(Selector(response).xpath(
                '/html/body/div/div[1]/div[2]/table[4]/tbody/tr/td[2]/text()').extract_first())
            Developerbaseitem['CompanyProfile'] = CompanyProfile
            logging.debug('CompanyProfile' + CompanyProfile)

            result.append(Developerbaseitem)
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
        self.r = redis.Redis(host=self.settings.get(
            'REDIS_HOST') or '10.30.1.18', port=self.settings.get('REDIS_PORT') or 6379)

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
        if response.meta.get('PageType') == 'PresaleBase':
            logging.debug('PresaleBase')

            PresaleTables = Selector(response).xpath(
                '//*[@id="news_se_frm"]/div[3]/table')
            if PresaleTables:
                for PresaleTable in PresaleTables:
                    Presalebaseitem = PresaleBaseItem()
                    Numbering = check_data_str(PresaleTable.xpath(
                        './tbody/tr[1]/td[2]/a/text()').extract_first())
                    logging.debug('Numbering' + Numbering)
                    Presalebaseitem['Numbering'] = Numbering

                    SalesUnit = check_data_str(PresaleTable.xpath(
                        './tbody/tr[1]/td[4]/text()').extract_first())
                    logging.debug('SalesUnit' + SalesUnit)
                    Presalebaseitem['SalesUnit'] = SalesUnit

                    DistrictBelongs = check_data_str(
                        PresaleTable.xpath('./tbody/tr[2]/td[2]/text()').extract_first())
                    logging.debug('DistrictBelongs' + DistrictBelongs)
                    Presalebaseitem['DistrictBelongs'] = DistrictBelongs

                    TheHouseIsLocated = check_data_str(
                        PresaleTable.xpath('./tbody/tr[2]/td[4]/text()').extract_first())
                    logging.debug('TheHouseIsLocated' + TheHouseIsLocated)
                    Presalebaseitem['TheHouseIsLocated'] = TheHouseIsLocated

                    ProjectName = check_data_str(
                        PresaleTable.xpath('./tbody/tr[3]/td[2]/a/font/text()').extract_first())
                    logging.debug('ProjectName' + ProjectName)
                    Presalebaseitem['ProjectName'] = ProjectName

                    PresaleNo = uuid.uuid3(
                        uuid.NAMESPACE_DNS, str(ProjectName + Numbering)).hex
                    logging.debug('PresaleNo' + PresaleNo)
                    Presalebaseitem['PresaleNo'] = PresaleNo

                    LandUseCardNumber = check_data_str(
                        PresaleTable.xpath('./tbody/tr[3]/td[4]/text()').extract_first())
                    logging.debug('LandUseCardNumber' + LandUseCardNumber)
                    Presalebaseitem['LandUseCardNumber'] = LandUseCardNumber

                    OpeningTime = check_data_str(PresaleTable.xpath(
                        './tbody/tr[4]/td[2]/text()').extract_first())
                    logging.debug('OpeningTime' + OpeningTime)
                    Presalebaseitem['OpeningTime'] = OpeningTime

                    LandUseperiod = check_data_str(PresaleTable.xpath(
                        './tbody/tr[4]/td[4]/text()').extract_first())
                    logging.debug('LandUseperiod' + LandUseperiod)
                    Presalebaseitem['LandUseperiod'] = LandUseperiod

                    HousingUseOfNature = check_data_str(
                        PresaleTable.xpath('./tbody/tr[5]/td[2]/text()').extract_first())
                    logging.debug('HousingUseOfNature' + HousingUseOfNature)
                    Presalebaseitem['HousingUseOfNature'] = HousingUseOfNature

                    PlanningPermitNumber = check_data_str(
                        PresaleTable.xpath('./tbody/tr[5]/td[4]/text()').extract_first())
                    logging.debug('PlanningPermitNumber' +
                                  PlanningPermitNumber)
                    Presalebaseitem[
                        'PlanningPermitNumber'] = PlanningPermitNumber

                    result.append(Presalebaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class SpiderMiddlerProject(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings
        self.r = redis.Redis(host=self.settings.get(
            'REDIS_HOST') or '10.30.1.18', port=self.settings.get('REDIS_PORT') or 6379)
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.njhouse.com.cn",
            'Cache-Control': "max-age=0",
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
            AllProjects = Selector(response).xpath(
                '//*[@id="news_se_frm"]/div[3]/table')
            if AllProjects:
                for AllProject in AllProjects:
                    Projectbaseitem = ProjectBaseItem()
                    ProjectName = check_data_str(AllProject.xpath(
                        './tbody/tr[1]/td[3]/a/text()').extract_first())
                    logging.debug('ProjectName' + ProjectName)
                    Projectbaseitem['ProjectName'] = ProjectName

                    ProjectDetailUrl = check_data_str(AllProject.xpath(
                        './tbody/tr[1]/td[3]/a/@href').extract_first())
                    logging.debug('ProjectDetailUrl' + ProjectDetailUrl)
                    Projectbaseitem[
                        'ProjectDetailUrl'] = 'http://www.njhouse.com.cn/2016/spf/' + ProjectDetailUrl

                    PresalePermitNumber = check_data_str(
                        AllProject.xpath('./tbody/tr[1]/td[5]/a/text()').extract_first())
                    logging.debug('PresalePermitNumber' + PresalePermitNumber)
                    Projectbaseitem[
                        'PresalePermitNumber'] = PresalePermitNumber

                    DistrictName = check_data_str(AllProject.xpath(
                        './tbody/tr[2]/td[2]/text()').extract_first())
                    logging.debug('DistrictName' + DistrictName)
                    Projectbaseitem['DistrictName'] = DistrictName

                    NewOpeningTime = check_data_str(AllProject.xpath(
                        './tbody/tr[2]/td[4]/text()').extract_first())
                    logging.debug('NewOpeningTime' + NewOpeningTime)
                    Projectbaseitem['NewOpeningTime'] = NewOpeningTime

                    ProjectType = check_data_str(AllProject.xpath(
                        './tbody/tr[3]/td[2]/text()').extract_first())
                    logging.debug('ProjectType' + ProjectType)
                    Projectbaseitem['ProjectType'] = ProjectType

                    ProjectSalePhoneNumber = check_data_str(
                        AllProject.xpath('./tbody/tr[3]/td[4]/text()').extract_first())
                    logging.debug('ProjectSalePhoneNumber' +
                                  ProjectSalePhoneNumber)
                    Projectbaseitem[
                        'ProjectSalePhoneNumber'] = ProjectSalePhoneNumber

                    ProjectAddress = check_data_str(AllProject.xpath(
                        './tbody/tr[4]/td[2]/text()').extract_first())
                    logging.debug('ProjectAddress' + ProjectAddress)
                    Projectbaseitem['ProjectAddress'] = ProjectAddress

                    ProjectNo = uuid.uuid3(uuid.NAMESPACE_DNS, str(
                        ProjectName + ProjectAddress)).hex
                    logging.debug('ProjectNo' + ProjectNo)
                    Projectbaseitem['ProjectNo'] = ProjectNo

                    if ProjectDetailUrl:
                        nexturl = 'http://www.njhouse.com.cn/2016/spf/' + ProjectDetailUrl
                        headers = self.headers
                        headers['Refer'] = nexturl
                        ProjectInfoUrl = nexturl
                        result.append(Request(url=ProjectInfoUrl, headers=headers, method='GET', meta={
                            "PageType": "ProjectInfo",
                            "item": Projectbaseitem,
                            "ProjectName": ProjectName
                        }))

        if response.meta.get('PageType') == 'ProjectInfo':
            logging.debug('ProjectInfo')
            projectitem = response.meta.get("item")
            ProjectName = response.meta.get("ProjectName")
            Projectbaseitem = copy.deepcopy(projectitem)

            Projectbaseitem['SourceUrl'] = response.url

            Developer = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/div[1]/table/tbody/tr[3]/td[2]/a/text()').extract_first())
            Projectbaseitem['Developer'] = Developer
            logging.debug('Developer' + Developer)

            AgentSaleComs = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/div[1]/table/tbody/tr[4]/td[2]').extract_first())
            logging.debug('AgentSaleComs' + AgentSaleComs)
            Projectbaseitem['AgentSaleComs'] = AgentSaleComs

            PresalePermits = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/div[1]/table/tbody/tr[6]/td[2]/span').extract_first())
            PresalePermitNums = re.findall(
                r'target="_blank">(.*?)</a>', PresalePermits)
            PresalePermit = ''
            for PresalePermitNum in PresalePermitNums:
                if '预售方案' not in PresalePermitNum:
                    PresalePermit = PresalePermit + PresalePermitNum + '|'
                    logging.debug('PresalePermits' + PresalePermit)
                    Projectbaseitem['PresalePermits'] = PresalePermit

            CertificateOfUseOfStateOwnedLand = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/div[1]/table/tbody/tr[7]/td[2]/span/text()').extract_first())
            Projectbaseitem[
                'CertificateOfUseOfStateOwnedLand'] = CertificateOfUseOfStateOwnedLand
            logging.debug('CertificateOfUseOfStateOwnedLand' +
                          CertificateOfUseOfStateOwnedLand)

            LandUsePlanningLicense = check_data_str(Selector(response).xpath(

                '/html/body/div[1]/div[2]/div/div[3]/div/div[1]/table/tbody/tr[8]/td[2]/span/text()').extract_first())
            Projectbaseitem['LandUsePlanningLicense'] = LandUsePlanningLicense
            logging.debug('LandUsePlanningLicense' + LandUsePlanningLicense)

            ProjectPlanningLicense = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/div[1]/table/tbody/tr[9]/td[2]/span').extract_first())
            Projectbaseitem['ProjectPlanningLicense'] = ProjectPlanningLicense
            logging.debug('ProjectPlanningLicense' + ProjectPlanningLicense)

            ConstructionPermitNumbers = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/div[1]/table/tbody/tr[10]/td[2]/span').extract_first())
            Projectbaseitem[
                'ConstructionPermitNumbers'] = ConstructionPermitNumbers
            logging.debug('ConstructionPermitNumbers' +
                          ConstructionPermitNumbers)

            InWebNum = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[1]/td[2]/text()').extract_first())
            Projectbaseitem['InWebNum'] = InWebNum
            logging.debug('InWebNum' + InWebNum)

            InWebAreas = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[2]/td[2]/text()').extract_first())
            Projectbaseitem['InWebAreas'] = InWebAreas
            logging.debug('InWebAreas' + InWebAreas)

            UnsoldNum = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[3]/td[2]/text()').extract_first())
            Projectbaseitem['UnsoldNum'] = UnsoldNum
            logging.debug('UnsoldNum' + UnsoldNum)

            UnsoldAreas = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[4]/td[2]/text()').extract_first())
            Projectbaseitem['UnsoldAreas'] = UnsoldAreas
            logging.debug('UnsoldAreas' + UnsoldAreas)

            GarageUnsoldNum = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[5]/td[2]/text()').extract_first())
            Projectbaseitem['GarageUnsoldNum'] = GarageUnsoldNum
            logging.debug('GarageUnsoldNum' + GarageUnsoldNum)

            GarageUnsoldAreas = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[6]/td[2]/text()').extract_first())
            Projectbaseitem['GarageUnsoldAreas'] = GarageUnsoldAreas
            logging.debug('GarageUnsoldAreas' + GarageUnsoldAreas)

            TodaySubscriptionNum = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[1]/td[4]/text()').extract_first())
            Projectbaseitem['TodaySubscriptionNum'] = TodaySubscriptionNum
            logging.debug('TodaySubscriptionNum' + TodaySubscriptionNum)

            TodayDealNum = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[2]/td[4]/text()').extract_first())
            Projectbaseitem['TodayDealNum'] = TodayDealNum
            logging.debug('TodayDealNum' + TodayDealNum)

            TotalSubscriptionNum = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[3]/td[4]/text()').extract_first())
            Projectbaseitem['TotalSubscriptionNum'] = TotalSubscriptionNum
            logging.debug('TotalSubscriptionNum' + TotalSubscriptionNum)

            TotalSubscriptionAreas = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[4]/td[4]/text()').extract_first())
            Projectbaseitem['TotalSubscriptionAreas'] = TotalSubscriptionAreas
            logging.debug('TotalSubscriptionAreas' + TotalSubscriptionAreas)

            TotalDealNum = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[5]/td[4]/text()').extract_first())
            Projectbaseitem['TotalDealNum'] = TotalDealNum
            logging.debug('TotalDealNum' + TotalDealNum)

            TotalDealAreas = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[6]/td[4]/text()').extract_first())
            Projectbaseitem['TotalDealAreas'] = TotalDealAreas
            logging.debug('TotalDealAreas' + TotalDealAreas)

            BussessMonthPrice = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[1]/td[6]/text()').extract_first())
            Projectbaseitem['BussessMonthPrice'] = BussessMonthPrice
            logging.debug('BussessMonthPrice' + BussessMonthPrice)

            HouseTotalPrice = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[2]/td[6]/text()').extract_first())
            Projectbaseitem['HouseTotalPrice'] = HouseTotalPrice
            logging.debug('HouseTotalPrice' + HouseTotalPrice)

            OfficeTotalPrice = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[3]/td[6]/text()').extract_first())
            Projectbaseitem['OfficeTotalPrice'] = OfficeTotalPrice
            logging.debug('OfficeTotalPrice' + OfficeTotalPrice)

            BussessTotalPrice = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[4]/td[6]/text()').extract_first())
            Projectbaseitem['BussessTotalPrice'] = BussessTotalPrice
            logging.debug('BussessTotalPrice' + BussessTotalPrice)

            HouseMonthPrice = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[5]/td[6]/text()').extract_first())
            Projectbaseitem['HouseMonthPrice'] = HouseMonthPrice
            logging.debug('HouseMonthPrice' + HouseMonthPrice)

            OfficeMonthPrice = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[1]/tbody/tr[6]/td[6]/text()').extract_first())
            Projectbaseitem['OfficeMonthPrice'] = OfficeMonthPrice
            logging.debug('OfficeMonthPrice' + OfficeMonthPrice)

            ProjectManageCom = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[2]/tbody/tr[1]/td[2]/text()').extract_first())
            Projectbaseitem['ProjectManageCom'] = ProjectManageCom
            logging.debug('ProjectManageCom' + ProjectManageCom)

            ProjectBuildCom = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[2]/tbody/tr[1]/td[4]/text()').extract_first())
            Projectbaseitem['ProjectBuildCom'] = ProjectBuildCom
            logging.debug('ProjectBuildCom' + ProjectBuildCom)

            ProjectDesignCom = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[2]/tbody/tr[2]/td[2]/text()').extract_first())
            Projectbaseitem['ProjectDesignCom'] = ProjectDesignCom
            logging.debug('ProjectDesignCom' + ProjectDesignCom)

            ProjectEnvironmentalDesignCom = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[2]/tbody/tr[2]/td[4]/text()').extract_first())
            Projectbaseitem[
                'ProjectEnvironmentalDesignCom'] = ProjectEnvironmentalDesignCom
            logging.debug('ProjectEnvironmentalDesignCom' +
                          ProjectEnvironmentalDesignCom)

            ProjectIntroduce = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/table[2]/tbody/tr[3]/td[2]/text()').extract_first())
            Projectbaseitem['ProjectIntroduce'] = ProjectIntroduce
            logging.debug('ProjectIntroduce' + ProjectIntroduce)
            result.append(Projectbaseitem)

            SalesBaseUrl = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[2]/a[3]/@href').extract_first())
            logging.debug('SalesBaseUrl' + SalesBaseUrl)

            nexturl = 'http://www.njhouse.com.cn/2016/spf/' + SalesBaseUrl
            headers = self.headers
            headers['Referer'] = nexturl
            if SalesBaseUrl:
                result.append(Request(url=nexturl, headers=headers, meta={
                              'PageType': 'BuildingBase', 'ProjectName': ProjectName}))
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class SpiderMiddlerBuilding(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings
        self.r = redis.Redis(host=self.settings.get(
            'REDIS_HOST') or '10.30.1.18', port=self.settings.get('REDIS_PORT') or 6379)
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.njhouse.com.cn",
            'Cache-Control': "max-age=0",
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
        try:
            if response.meta.get('PageType') == 'BuildingBase':
                logging.debug('BuildingBase')
                ProjectName = response.meta.get('ProjectName')

                # /html/body/div[1]/div[2]/div/div[3]/div/div/div[3]/ul/li[1]/div/a

                Buildings = Selector(response).xpath(
                    '/html/body/div[1]/div[2]/div/div[3]/div/div/div[3]/ul/li')
                if Buildings:
                    recodename = []
                    recordnum = 0
                    for Building in Buildings:
                        Buildingbaseitem = BuildingBaseItem()

                        BuildingName = check_data_str(
                            Building.xpath('./div/a/text()').extract_first())
                        logging.debug('BuildingName' + BuildingName)
                        Buildingbaseitem['BuildingName'] = BuildingName

                        BuildingNo = uuid.uuid3(uuid.NAMESPACE_DNS, str(
                            ProjectName) + '|' + str(BuildingName) + '|' + str(recordnum)).hex
                        logging.debug('BuildingNo' + BuildingNo)
                        Buildingbaseitem['BuildingNo'] = BuildingNo
                        recordnum = recordnum + 1

                        BuildingUrl = check_data_str(
                            Building.xpath('./div/a/@href').extract_first())
                        logging.debug('BuildingUrl' + BuildingUrl)
                        Buildingbaseitem[
                            'BuildingUrl'] = 'http://www.njhouse.com.cn/2016/spf/' + BuildingUrl

                        BuildingHouseType = check_data_str(
                            Building.xpath('./table/thead[2]/tr/th[2]/text()').extract_first())
                        logging.debug('BuildingHouseType' + BuildingHouseType)
                        Buildingbaseitem[
                            'BuildingHouseType'] = BuildingHouseType

                        TodaySubscriptionNum = check_data_num(
                            Building.xpath('./div/span/text()').extract_first())
                        logging.debug('TodaySubscriptionNum' +
                                      TodaySubscriptionNum)
                        Buildingbaseitem[
                            'TodaySubscriptionNum'] = TodaySubscriptionNum

                        TodayDealNum = check_data_str(Building.xpath(
                            './div/strong/text()').extract_first())
                        logging.debug('TodayDealNum' + TodayDealNum)
                        Buildingbaseitem['TodayDealNum'] = TodayDealNum

                        PlanOpenDate = check_data_num(
                            Building.xpath('./table/tbody/tr[2]/td[1]/text()').extract_first())
                        logging.debug('PlanOpenDate' + PlanOpenDate)
                        Buildingbaseitem['PlanOpenDate'] = PlanOpenDate

                        InWebNum = check_data_num(Building.xpath(
                            './table/tbody/tr[2]/td[2]/text()').extract_first())
                        logging.debug('InWebNum' + InWebNum)
                        Buildingbaseitem['InWebNum'] = InWebNum

                        CanSaleNum = check_data_num(Building.xpath(
                            './table/tbody/tr[2]/td[3]/text()').extract_first())
                        logging.debug('CanSaleNum' + CanSaleNum)
                        Buildingbaseitem['CanSaleNum'] = CanSaleNum

                        TotalSubscriptionNum = check_data_num(
                            Building.xpath('./table/tbody/tr[2]/td[4]/text()').extract_first())
                        logging.debug('TotalSubscriptionNum' +
                                      TotalSubscriptionNum)
                        Buildingbaseitem[
                            'TotalSubscriptionNum'] = TotalSubscriptionNum

                        TotalDealNum = check_data_num(
                            Building.xpath('./table/tbody/tr[2]/td[5]/text()').extract_first())
                        logging.debug('TotalDealNum' + TotalDealNum)
                        Buildingbaseitem['TotalDealNum'] = TotalDealNum

                        SaleAreas = check_data_num(Building.xpath(
                            './table/tbody/tr[2]/td[6]/text()').extract_first())
                        logging.debug('SaleAreas' + SaleAreas)
                        Buildingbaseitem['SaleAreas'] = SaleAreas

                        MeanPrice = check_data_num(Building.xpath(
                            './table/tbody/tr[2]/td[7]/text()').extract_first())
                        logging.debug('MeanPrice' + MeanPrice)
                        Buildingbaseitem['MeanPrice'] = MeanPrice

                        DealRatio = check_data_num(Building.xpath(
                            './table/tbody/tr[2]/td[8]/text()').extract_first())
                        logging.debug('DealRatio' + DealRatio)
                        Buildingbaseitem['DealRatio'] = DealRatio

                        Buildingbaseitem['SourceUrl'] = response.url

                        result.append(Buildingbaseitem)

                        if BuildingUrl:
                            if BuildingName in recodename:
                                BuildingName = BuildingName + str(recordnum)
                            recodename.append(BuildingName)
                            nexturl = 'http://www.njhouse.com.cn/2016/spf/' + BuildingUrl
                            headers = self.headers
                            headers['Refer'] = response.url
                            result.append(Request(url=nexturl,
                                                  method='GET',
                                                  headers=headers,
                                                  meta={
                                                      "PageType": "HouseBase",
                                                      "ProjectName": ProjectName,
                                                      "BuildingName": BuildingName,
                                                      "isnext": '0'
                                                  }))

        except Exception:
            import traceback
            exc = traceback.format_exc()
            project_base = {
                'err_url': response.url,
                'PageType': 'BuildingBase',
                'Exception': exc
            }
            print(exc)
            project_base_json = json.dumps(project_base, sort_keys=True)
            self.r.sadd('Building_Err_Page', project_base_json)
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
        self.r = redis.Redis(host=self.settings.get(
            'REDIS_HOST') or '10.30.1.18', port=self.settings.get('REDIS_PORT') or 6379)
        self.headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.njhouse.com.cn",
            'Cache-Control': "max-age=0",
        }

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by SBuilding_Err_Pagecrapy to create your
        # spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        def GetHouseSts(string):
            house_class = {
                "ks": "可售",
                "rg": "已认购",
                "qy": "已签约",
                "ba": "已备案",
                "az": "拆迁安置"

            }
            if string in house_class.keys():
                return house_class[string]
            else:
                return "未知"

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'HouseBase':
            logging.debug('HouseBase')
            ProjectName = response.meta.get('ProjectName')
            BuildingName = response.meta.get('BuildingName')

            # /html/body/div[1]/div[2]/div/div[3]/div/div/table[2]/tbody/tr[1]

            HouseTableRows = Selector(response).xpath(
                '/html/body/div[1]/div[2]/div/div[3]/div/div/table[2]/tbody/tr')
            if HouseTableRows:
                recordnum = 0
                for HouseTableRow in HouseTableRows:
                    HouseTableCols = HouseTableRow.xpath('./td')
                    if HouseTableCols:
                        for HouseTableCol in HouseTableCols:
                            Housebaseitem = HouseBaseItem()
                            Housebaseitem['ProjectName'] = ProjectName
                            Housebaseitem['BuildingName'] = BuildingName

                            HouseName = check_data_str(
                                HouseTableCol.xpath('./a[1]/text()').extract_first())
                            logging.debug('HouseName' + HouseName)
                            Housebaseitem['HouseName'] = HouseName

                            HouseType = check_data_str(
                                HouseTableCol.xpath('./@title').extract_first())
                            logging.debug('HouseType' + HouseType)
                            Housebaseitem['HouseType'] = HouseType

                            HouseAresPrice = check_data_str(
                                HouseTableCol.xpath('./a[2]').extract_first())
                            logging.debug('HouseAresPrice' + HouseAresPrice)
                            HouseAresPrices = re.search(
                                r'_blank">(.*?)</a>', HouseAresPrice)
                            if HouseAresPrices:
                                Housebaseitem[
                                    'HouseAresPrice'] = HouseAresPrices.group(1)

                            HouseUrl = check_data_str(
                                HouseTableCol.xpath('./a[1]/@href').extract_first())

                            HouseUrl = 'http://www.njhouse.com.cn/2016/spf/' + HouseUrl
                            logging.debug('HouseUrl' + HouseUrl)
                            Housebaseitem['HouseUrl'] = HouseUrl

                            HouseNo = uuid.uuid3(uuid.NAMESPACE_DNS, str(ProjectName) + '|'
                                                 + str(BuildingName) +
                                                 '|' + str(HouseName) + '|'
                                                 + str(recordnum)).hex
                            recordnum = recordnum + 1
                            Housebaseitem['HouseNo'] = HouseNo

                            HouseStsClass = check_data_str(
                                HouseTableCol.xpath('./@class').extract_first())
                            HouseSts = GetHouseSts(HouseStsClass)
                            Housebaseitem['HouseSts'] = HouseSts

                            if HouseName:
                                if HouseSts == '可售':
                                    nexturl = HouseUrl
                                    headers = self.headers
                                    headers['Refer'] = nexturl
                                    result.append(Request(url=nexturl,
                                                          method='GET',
                                                          headers=headers,
                                                          meta={
                                                              "PageType": "HouseInfo",
                                                              "item": Housebaseitem
                                                          }))
                                else:
                                    result.append(Housebaseitem)

        if response.meta.get('PageType') == 'HouseInfo':
            logging.debug('HouseInfo')
            # /html/body/div[1]/div[1]/div[2]/div/div/div/table/tbody/tr[2]/td[2]
            houseitem = response.meta.get("item")
            Housebaseitem = copy.deepcopy(houseitem)

            houseinfos = {}

            houseinfotablecols = Selector(response).xpath(
                '/html/body/div[1]/div[1]/div[2]/div/div/div/table/tbody/tr')
            for houseinfotablecol in houseinfotablecols:
                houseinfotablerows = houseinfotablecol.xpath('./td')
                lenraw = len(houseinfotablerows)
                for index in range(lenraw // 2):
                    houseinfos[houseinfotablecol.xpath(
                        './td[%d]/text()' % (2 * index + 1)).extract_first()] = houseinfotablecol.xpath(
                        './td[%d]/text()' % (2 * index + 2)).extract_first()
            if houseinfos:
                Housebaseitem['HouseInfo'] = houseinfos

            result.append(Housebaseitem)

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
