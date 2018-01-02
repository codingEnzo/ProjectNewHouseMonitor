#!/usr/python3
# -*- coding: utf-8 -*-
import sys
import uuid
import re
import copy
import redis
import json
import logging
import random
from scrapy import Request
from scrapy import Selector
from HouseCrawler import settings as setting
from HouseNew.models import *
from HouseCrawler.Items.ItemsWuxi import *
from collections import OrderedDict

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
'''
    Created on 2017-11-29 12:44:32.
'''
contextflag = True

def check_data_num(string):
    result_data = ''
    if string:
        fix_data = string.strip().replace('\r', '').replace('\n', '').replace("㎡","")\
            .replace('\t', '').replace(' ', '').replace(" ","").replace('\t', '').replace('\\', '')\
            .replace('\n', '').replace("一房一价：元","").replace(' ', '').replace("²","")\
            .replace("套", "").replace("幢", "").replace("㎡", "").replace("元", "").replace("m", "")\
            .replace("M","").replace("%","").replace("个","").replace("/","")
        if fix_data !='' and '*' not in fix_data:
            result_data = fix_data
    return result_data
def check_data_str(string):
    result_data = ''
    if string:
        fix_data = string.strip().replace('\r', '').replace('\n', '')\
        .replace('\t', '').replace(' ', '').replace(" ","")
        if fix_data !='' and '*' not in fix_data:
            result_data = fix_data
    return result_data
class SpiderMiddlerProjectBase(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.headers = {
            'User-Agent':random.choice(setting.USER_AGENTS),
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'no-cache',
            'Connection': 'keep - alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.wxhouse.com:9097',
        }
        self.r = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)
        self.mainProjectUrl = 'http://www.wxhouse.com:9097/wwzs/queryLpxxInfo.action?tplLpxx.id='
        self.mainDetailUrl = 'http://www.wxhouse.com:9097/wwzs/queryGltInfo.action?tplLpxx.id='
        self.SoldStatusUrl = 'http://www.wxhouse.com:9097/wwzs/queryXsxzInfo.action?tplLpxx.id='
        self.mainurl = 'http://www.wxhouse.com:9097'


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
        if response.meta.get('PageType') == 'ProjectStart':
            logging.debug("ProjectStart")
            pagenum = check_data_str(Selector(response).xpath('//*[@id="totalPageCount"]/@value').extract_first())
            headers = self.headers
            headers['Referer'] = response.url
            # pagenum = 1
            if pagenum:
                for i in range(int(pagenum)):
                    req_dict = {
                        'tplLpxx.lpxzq': '',
                        'tplLpxx.lpbk': '',
                        'tplYsfw.fwyt': '',
                        'tplLpxx.lpxdm': '',
                        'tppCyqy.qymc': '',
                        'page.currentPageNo': i,
                        'page.pageSize': 15,
                        'page.totalPageCount': int(pagenum),
                    }
                    req_body = urlparse.urlencode(req_dict)
                    result.append(Request(url=response.url,
                                          headers=headers,
                                          method='POST',
                                          body=req_body,
                                          meta={
                                              'PageType': 'ProjectBase'
                                          }))



        if response.meta.get('PageType') == 'ProjectBase':
            logging.debug("ProjectBase")
            headers = self.headers
            headers['Referer'] = response.url
            logging.debug(response.url)
            ProjectTableRaw = Selector(response).xpath('//*[@id="searchForm"]/div[1]/table/tr')
            if ProjectTableRaw:
                for RawData in ProjectTableRaw:
                    ProjectTableCol = RawData.xpath('./td')
                    if ProjectTableCol:
                        for ColData in ProjectTableCol:
                            monitorprojectbaseitem = MonitorProjectBaseItem()
                            ProjectName = check_data_str(ColData.xpath('./a/span/b/text()').extract_first())
                            monitorprojectbaseitem['ProjectName'] = ProjectName

                            ProjectSaleInfostr = check_data_str(ColData.xpath('./span/text()').extract_first())

                            PresalePermitNumber = check_data_str(ColData.xpath('./text()').extract()[3])
                            monitorprojectbaseitem['PresalePermitNumber'] = PresalePermitNumber

                            ProjectSaleInfos = re.findall(r'(\d+)',ProjectSaleInfostr)
                            if len(ProjectSaleInfos)==2:
                                TotalHouseNumber = ProjectSaleInfos[0]
                                monitorprojectbaseitem['TotalHouseNumber'] = TotalHouseNumber
                                OnSoldNumber = ProjectSaleInfos[1]
                                monitorprojectbaseitem['OnSoldNumber'] = OnSoldNumber

                            DetailUrl = ColData.xpath('./a/@href').extract_first()
                            ProjectCode = DetailUrl.replace("/wwzs/queryLpxxInfo.action?tplLpxx.id=","")
                            monitorprojectbaseitem['ProjectCode'] = ProjectCode

                            logging.debug('ProjectCode'+ProjectCode)
                            projectDetailUrl = 'http://www.wxhouse.com:9097'+DetailUrl
                            monitorprojectbaseitem['projectDetailUrl'] = projectDetailUrl

                            ProjectNo = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                   ProjectName + str(PresalePermitNumber)+ProjectCode).hex
                            monitorprojectbaseitem['ProjectNo'] = ProjectNo
                            if projectDetailUrl and DetailUrl:
                                result.append(monitorprojectbaseitem)
                                # result.append(Request(url=projectDetailUrl,
                                #                       headers=headers,
                                #                       method='GET',
                                #                       meta={
                                #                           'PageType': 'ProjectInfo',
                                #                           'ProjectHref': ProjectCode
                                #                       }))


        if response.meta.get('PageType') == 'ProjectInfo':
            logging.debug("ProjectInfo")


            ProjectHref = response.meta.get('ProjectHref')
            headers = self.headers
            headers['Referer'] = response.url

            Projectbaseitem = ProjectBaseItem()
            Projectbaseitem['SourceUrl'] = response.url
            TotalHouseNumber = check_data_num(
                #/html/body/div/div[5]/div[2]/table/tbody/tr[1]/td[2]
                Selector(response).xpath('/html/body/div/div[5]/div[2]/table/tr[1]/td[2]/text()').extract_first())
            Projectbaseitem['TotalHouseNumber'] = TotalHouseNumber
            logging.debug('TotalHouseNumber' + TotalHouseNumber)

            OnSoldNumber = check_data_num(
                Selector(response).xpath('/html/body/div/div[5]/div[2]/table/tr[2]/td[2]/text()').extract_first())
            Projectbaseitem['OnSoldNumber'] = OnSoldNumber
            logging.debug('OnSoldNumber' + OnSoldNumber)

            SoldNumber = check_data_num(
                Selector(response).xpath('/html/body/div/div[5]/div[2]/table/tr[3]/td[2]/text()').extract_first())
            Projectbaseitem['SoldNumber'] = SoldNumber
            logging.debug('SoldNumber' + SoldNumber)

            LimitSoldNumber = check_data_num(
                Selector(response).xpath('/html/body/div/div[5]/div[2]/table/tr[4]/td[2]/text()').extract_first())
            Projectbaseitem['LimitSoldNumber'] = LimitSoldNumber
            logging.debug('LimitSoldNumber' + LimitSoldNumber)

            ProjectName = check_data_str(
                Selector(response).xpath('/html/body/div/div[3]/div[2]/table/tr[1]/td/b[1]/text()').extract_first())
            Projectbaseitem['ProjectName'] = ProjectName
            logging.debug('ProjectName' + ProjectName)

            PresalePermitNumber = check_data_str(
                Selector(response).xpath('/html/body/div/div[3]/div[2]/table/tr[1]/td/b[2]/text()').extract_first())
            Projectbaseitem['PresalePermitNumber'] = PresalePermitNumber
            logging.debug('PresalePermitNumber' + PresalePermitNumber)

            ProjectTemporaryName = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[2]/td[2]/text()').extract_first())
            Projectbaseitem['ProjectTemporaryName'] = ProjectTemporaryName
            logging.debug('ProjectTemporaryName' + ProjectTemporaryName)

            ApprovalPresaleDepartment = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[4]/td[2]/text()').extract_first())
            Projectbaseitem['ApprovalPresaleDepartment'] = ApprovalPresaleDepartment
            logging.debug('ApprovalPresaleDepartment' + ApprovalPresaleDepartment)

            Developer = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[5]/td[2]/a/text()').extract_first())
            Projectbaseitem['Developer'] = Developer
            logging.debug('Developer' + Developer)

            DeveloperUrl = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[5]/td[2]/a/@href').extract_first())
            DeveloperUrl =  self.mainurl + DeveloperUrl
            Projectbaseitem['DeveloperUrl'] = DeveloperUrl
            logging.debug('DeveloperUrl' + DeveloperUrl)

            if DeveloperUrl:
                GetDeveloperUrl =  DeveloperUrl
                #
                # project_base = {
                #     'source_url': GetDeveloperUrl,
                #     'headers': headers,
                #     'method': 'GET',
                #     'meta': {
                #         'PageType': 'DeveloperBase',
                #         'ProjectName': ProjectName
                #     }}
                # project_base_json = json.dumps(project_base, sort_keys=True)
                # self.r.sadd('WuxiCrawler:start_urls', project_base_json)
                result.append(Request(url=GetDeveloperUrl,
                                      headers=headers,
                                      method='GET',
                                      meta={
                                          'PageType': 'DeveloperBase',
                                          'ProjectName': ProjectName
                                      }))

            Cooperator = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[6]/td[2]/text()').extract_first())
            Projectbaseitem['Cooperator'] = Cooperator
            logging.debug('Cooperator' + Cooperator)

            ProjectAddress = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[7]/td[2]/text()').extract_first())
            Projectbaseitem['ProjectAddress'] = ProjectAddress
            logging.debug('ProjectAddress' + ProjectAddress)

            DistrictName = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[8]/td[2]/text()').extract_first())
            Projectbaseitem['DistrictName'] = DistrictName
            logging.debug('DistrictName' + DistrictName)

            ApprovalForApproval = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[9]/td[2]/text()').extract_first())
            Projectbaseitem['ApprovalForApproval'] = ApprovalForApproval
            logging.debug('ApprovalForApproval' + ApprovalForApproval)

            UsePermitNumber = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[10]/td[2]/text()').extract_first())
            Projectbaseitem['UsePermitNumber'] = UsePermitNumber
            logging.debug('UsePermitNumber' + UsePermitNumber)

            OwnedLand = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[11]/td[2]/text()').extract_first())
            Projectbaseitem['OwnedLand'] = OwnedLand
            logging.debug('OwnedLand' + OwnedLand)

            ConstructionPermitNumber = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[12]/td[2]/text()').extract_first())
            Projectbaseitem['ConstructionPermitNumber'] = ConstructionPermitNumber
            logging.debug('ConstructionPermitNumber' + ConstructionPermitNumber)

            CertificateOfUseOfStateOwnedLand = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[13]/td[2]/text()').extract_first())
            Projectbaseitem['CertificateOfUseOfStateOwnedLand'] = CertificateOfUseOfStateOwnedLand
            logging.debug('CertificateOfUseOfStateOwnedLand' + CertificateOfUseOfStateOwnedLand)

            PreSaleAreas = check_data_num(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[14]/td[2]/text()').extract_first())
            Projectbaseitem['PreSaleAreas'] = PreSaleAreas
            logging.debug('PreSaleAreas' + PreSaleAreas)

            SaleCom = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[15]/td[2]/text()').extract_first())
            Projectbaseitem['SaleCom'] = SaleCom
            logging.debug('SaleCom' + SaleCom)

            SaleComPhone = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[16]/td[2]/text()').extract_first())
            Projectbaseitem['SaleComPhone'] = SaleComPhone
            logging.debug('SaleComPhone' + SaleComPhone)

            SaleAddress = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[17]/td[2]/text()').extract_first())
            Projectbaseitem['SaleAddress'] = SaleAddress
            logging.debug('SaleAddress' + SaleAddress)

            SalePhone = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[18]/td[2]/text()').extract_first())
            Projectbaseitem['SalePhone'] = SalePhone
            logging.debug('SalePhone' + SalePhone)

            ManagementCompany = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[19]/td[2]/text()').extract_first())
            Projectbaseitem['ManagementCompany'] = ManagementCompany
            logging.debug('ManagementCompany' + ManagementCompany)

            ProjectNo = uuid.uuid3(uuid.NAMESPACE_DNS, ProjectName + str(PresalePermitNumber)).hex
            Projectbaseitem['ProjectNo'] = ProjectNo
            logging.debug('ProjectNo' + ProjectNo)

            if contextflag and ProjectHref:
                BuildingBaseUrl = self.mainDetailUrl + ProjectHref
                Projectbaseitem['BuildingBaseUrl'] = BuildingBaseUrl
                result.append(Request(url=BuildingBaseUrl,
                                      headers=headers,
                                      method='GET',
                                      meta={
                                          'PageType': 'BuildingBase',
                                          'ProjectName': ProjectName
                                      }))

            if ProjectHref:
                GetSoldStatusUrl = self.SoldStatusUrl + ProjectHref
                Projectbaseitem['GetSoldStatusUrl'] = GetSoldStatusUrl

                SoldStatusUrl = self.SoldStatusUrl + ProjectHref
                result.append(Request(url=SoldStatusUrl,
                                      headers=headers,
                                      method='GET',
                                      meta={
                                          'PageType': 'GetSoldStatus',
                                          'item': Projectbaseitem
                                      }))

        if response.meta.get('PageType') == 'GetSoldStatus':
            logging.debug("GetSoldStatus")

            projectitem = response.meta.get('item')
            Projectbaseitem = copy.deepcopy(projectitem)
            getsoldstatus = Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr')
            typePriceInfonum = 0
            SoldStatusInfo = {'0': '0'}
            for status in getsoldstatus[1:]:
                HouseUseType = check_data_str(status.xpath('./td[1]/text()').extract_first())
                logging.debug('HouseUseType' + HouseUseType)

                TotalNumber = check_data_num(status.xpath('./td[2]/text()').extract_first())
                logging.debug('TotalNumber' + TotalNumber)

                TotalSoldAreas = check_data_num(status.xpath('./td[3]/text()').extract_first())
                logging.debug('TotalSoldAreas' + TotalSoldAreas)

                HaseSoldNumber = check_data_num(status.xpath('./td[4]/text()').extract_first())
                logging.debug('HaseSoldNumber' + HaseSoldNumber)

                HaseSoldAreas = check_data_num(status.xpath('./td[5]/text()').extract_first())
                logging.debug('HaseSoldAreas' + HaseSoldAreas)

                OnSoldNumber = check_data_num(status.xpath('./td[6]/text()').extract_first())
                logging.debug('OnSoldNumber' + OnSoldNumber)

                OnSoldAreas = check_data_num(status.xpath('./td[6]/text()').extract_first())
                logging.debug('OnSoldAreas' + OnSoldAreas)

                keyname = str(typePriceInfonum)
                SoldStatusInfo[keyname] = {
                    'HouseUseType': HouseUseType,
                    'TotalNumber': TotalNumber,
                    'TotalSoldAreas': TotalSoldAreas,
                    'HaseSoldNumber': HaseSoldNumber,
                    'HaseSoldAreas': HaseSoldAreas,
                    'OnSoldNumber': OnSoldNumber,
                    'OnSoldAreas': OnSoldAreas,
                }
                typePriceInfonum = typePriceInfonum + 1
            Projectbaseitem['SoldStatusInfo'] = SoldStatusInfo
            result.append(Projectbaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class SpiderMiddlerBuildingBase(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.headers = {
            'User-Agent':random.choice(setting.USER_AGENTS),
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'no-cache',
            'Connection': 'keep - alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.wxhouse.com:9097',
        }
        self.r = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)



    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        def get_house_sts(sts):
            houseSts = ''
            houseStsClass = {
                'background-color:#33FF00;': '待售',
                'background-color:#FFFF00;': '已售',
                'background-color:#CC9933;': '保留',
                'background-color:#CCCCCC;': '抵押',
                'background-color:#FF9900;': '已预定',
                'background-color:#0000FF;': '自持',
                'background-color:#993300;': '查封',
            }
            if sts in houseStsClass.keys():
                houseSts = houseStsClass[sts]
            return houseSts


        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'BuildingBase':
            logging.debug("BuildingBase")
            ProjectName = response.meta.get('ProjectName')
            buildingTables = Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[1]/td/b')
            for buildingTable in buildingTables:
                buildingUrl = re.search(r"viewGlt\('(.*?)','(.*?)'\)",
                                        buildingTable.xpath('./a/@onclick').extract_first())
                BuildingNum = check_data_str(buildingTable.xpath('./a/text()').extract_first())
                BuildingNo = uuid.uuid3(uuid.NAMESPACE_DNS,
                                        ProjectName + str(buildingUrl.group(1)) + str(buildingUrl.group(2))).hex
                headers = self.headers
                headers['Referer'] = response.url
                randit = random.random()
                houseDetailsUrl = 'http://www.wxhouse.com:9097/wwzs/viewFwGlt.action?lpid=%s&zh=%s&it=%s' \
                               % (str(buildingUrl.group(1)), str(buildingUrl.group(2)), str(randit))
                logging.debug('houseDetails' + houseDetailsUrl)
                if houseDetailsUrl:
                    # project_base = {
                    #     'source_url': houseDetailsUrl,
                    #     'headers': headers,
                    #     'method': 'GET',
                    #     'meta': {
                    #         'PageType': 'BuildingInfo',
                    #         'ProjectName': ProjectName,
                    #         'BuildingNum': BuildingNum,
                    #         'BuildingNo': BuildingNo
                    #     }}
                    #
                    # project_base_json = json.dumps(project_base, sort_keys=True)
                    # self.r.sadd('WuxiCrawler:start_urls', project_base_json)

                    result.append(Request(url = houseDetailsUrl,
                                          headers = headers,
                                          method = 'GET',
                                          meta = {
                                              'PageType': 'BuildingInfo',
                                              'ProjectName': ProjectName,
                                              'BuildingNum': BuildingNum,
                                              'BuildingNo': BuildingNo
                                          }))

        if response.meta.get('PageType') == 'BuildingInfo':
            logging.debug('BuildingInfo')
            ProjectName = response.meta.get('ProjectName')
            BuildingNum = response.meta.get('BuildingNum')
            num = 0
            GetHouses = Selector(response).xpath('/html/body/div[1]/div')
            for GetHouse in GetHouses:
                HouseClass = check_data_str(GetHouse.xpath('./@class').extract_first())
                if HouseClass == 'LPBFW_BOROR':
                    monitorhousebaseitem = MonitorHouseBaseItem()
                    monitorhousebaseitem['ProjectName'] = ProjectName
                    monitorhousebaseitem['BuildingNum'] = BuildingNum
                    HouseTitle = check_data_str(GetHouse.xpath('./@title').extract_first())
                    monitorhousebaseitem['HouseTitle'] = HouseTitle

                    HouseNo = uuid.uuid3(uuid.NAMESPACE_DNS, ProjectName + BuildingNum + str(HouseTitle) + str(num)).hex
                    monitorhousebaseitem['HouseNo'] = HouseNo
                    num = num + 1
                    GetHouseSts = check_data_str(GetHouse.xpath('./div/@style').extract_first())
                    if GetHouseSts:
                        HouseSts = get_house_sts(GetHouseSts)
                        monitorhousebaseitem['HouseSts'] = HouseSts
                        HouseFwid = check_data_str(GetHouse.xpath('./div/@fwid').extract_first())
                        monitorhousebaseitem['HouseFwid'] = HouseFwid
                        HouseLpid = check_data_str(GetHouse.xpath('./div/@lpid').extract_first())
                        monitorhousebaseitem['HouseLpid'] = HouseLpid
                        HouseInfoUrl = 'http://www.wxhouse.com:9097/wwzs/queryYsfwInfo.action?tplYsfw.id=%s&tplYsfw.lpid=%s' % (
                            HouseFwid, HouseLpid)
                        monitorhousebaseitem['HouseInfoUrl'] = HouseInfoUrl
                        monitorhousebaseitem['SourceUrl'] = response.url
                        headers = self.headers
                        headers['Referer'] = response.url
                        # if HouseInfoUrl and HouseSts=='待售':
                        #
                        #     result.append(Request(url=HouseInfoUrl,
                        #                           headers=headers,
                        #                           method='GET',
                        #                           meta={
                        #                               'PageType': 'HouseBase',
                        #                               'ProjectName': ProjectName,
                        #                               'BuildingNum': BuildingNum,
                        #                               'houseNo': HouseNo,
                        #                           }))
                        result.append(monitorhousebaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class SpiderMiddlerDeveloperBase(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.headers = {
            'User-Agent':random.choice(setting.USER_AGENTS),
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'no-cache',
            'Connection': 'keep - alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.wxhouse.com:9097',
        }
        self.r = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)




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
        if response.meta.get('PageType') == 'DeveloperBase':
            Developerbaseitem = DeveloperBaseItem()
            Developerbaseitem['SourceUrl'] = response.url

            ProjectName = response.meta.get('ProjectName')

            DeveloperName = check_data_str(
                Selector(response).xpath('/html/body/div/div[3]/div[2]/table/tr[1]/td/b/text()').extract_first())
            Developerbaseitem['DeveloperName'] = DeveloperName
            logging.debug('DeveloperName' + DeveloperName)

            DeveloperAddress = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[5]/td[2]/text()').extract_first())
            Developerbaseitem['DeveloperAddress'] = DeveloperAddress
            logging.debug('DeveloperAddress' + DeveloperAddress)

            DeveloperFullName = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[1]/td[2]/text()').extract_first())
            Developerbaseitem['DeveloperFullName'] = DeveloperFullName
            logging.debug('DeveloperFullName' + DeveloperFullName)

            DeveloperLevel = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[2]/td[2]/text()').extract_first())
            Developerbaseitem['DeveloperLevel'] = DeveloperLevel
            logging.debug('DeveloperLevel' + DeveloperLevel)

            LegalPerson = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[3]/td[2]/text()').extract_first())
            Developerbaseitem['LegalPerson'] = LegalPerson
            logging.debug('LegalPerson' + LegalPerson)

            SalesManager = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[4]/td[2]/text()').extract_first())
            Developerbaseitem['SalesManager'] = SalesManager
            logging.debug('SalesManager' + SalesManager)

            ZipCode = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[6]/td[2]/text()').extract_first())
            Developerbaseitem['ZipCode'] = ZipCode
            logging.debug('ZipCode' + ZipCode)

            Fax = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[7]/td[2]/text()').extract_first())
            Developerbaseitem['Fax'] = Fax
            logging.debug('Fax' + Fax)

            Web = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[8]/td[2]/text()').extract_first())
            Developerbaseitem['Web'] = Web
            logging.debug('Web' + Web)

            EMail = check_data_str(
                Selector(response).xpath('/html/body/div/div[4]/div[2]/table/tr[9]/td[2]/text()').extract_first())
            Developerbaseitem['EMail'] = EMail
            logging.debug('EMail' + EMail)

            DeveloperNo = uuid.uuid3(uuid.NAMESPACE_DNS, DeveloperFullName + DeveloperAddress).hex

            Developerbaseitem['DeveloperNo'] = DeveloperNo

            Developerbaseitem['ProjectName'] = ProjectName

            result.append(Developerbaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return



class SpiderMiddlerHouseBase(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, settings):
        self.settings = settings
        self.r = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)



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
        if response.meta.get('PageType') == 'HouseBase':
            logging.debug("HouseBase")
            ProjectName = response.meta.get('ProjectName')
            BuildingNum = response.meta.get('BuildingNum')
            HouseNo = response.meta.get('houseNo')

            Housebaseitem = HouseBaseItem()

            Housebaseitem['SourceUrl'] = response.url

            Housebaseitem['ProjectName'] = ProjectName
            logging.debug(ProjectName)

            Housebaseitem['BuildingNum'] = BuildingNum
            logging.debug(BuildingNum)

            Housebaseitem['HouseNo'] = HouseNo
            logging.debug(HouseNo)

            HouseAddress = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[3]/div[2]/table/tr[2]/td[2]/text()').extract_first())
            Housebaseitem['HouseAddress'] = HouseAddress
            logging.debug(HouseAddress)

            HouseCode = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[3]/div[2]/table/tr[1]/td[2]/text()').extract_first())
            Housebaseitem['HouseCode'] = HouseCode
            logging.debug(HouseCode)

            HouseSts = check_data_str(
                Selector(response).xpath('/html/body/div[1]/div[6]/div[2]/span/text()').extract_first())
            Housebaseitem['HouseSts'] = HouseSts
            logging.debug(HouseSts)

            BuildingNumber = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[2]/td[2]/text()').extract_first())
            Housebaseitem['BuildingNumber'] = BuildingNumber
            logging.debug(BuildingNumber)

            UnitNumber = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[3]/td[2]/text()').extract_first())
            Housebaseitem['UnitNumber'] = UnitNumber
            logging.debug(UnitNumber)

            HouseNumber = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[4]/td[2]/text()').extract_first())
            Housebaseitem['HouseNumber'] = HouseNumber
            logging.debug(HouseNumber)

            ActualFloor = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[5]/td[2]/text()').extract_first())
            Housebaseitem['ActualFloor'] = ActualFloor
            logging.debug(ActualFloor)

            TotalFloor = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[6]/td[2]/text()').extract_first())
            Housebaseitem['TotalFloor'] = TotalFloor
            logging.debug(TotalFloor)

            BuildingStructure = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[7]/td[2]/text()').extract_first())
            Housebaseitem['BuildingStructure'] = BuildingStructure
            logging.debug(BuildingStructure)

            HouseType = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[8]/td[2]/text()').extract_first())
            Housebaseitem['HouseUseType'] = HouseType
            logging.debug(HouseType)

            HouseUseType = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[9]/td[2]/text()').extract_first())
            Housebaseitem['HouseUseType'] = HouseUseType
            logging.debug(HouseUseType)

            AreasType = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[10]/td[2]/text()').extract_first())
            Housebaseitem['AreasType'] = AreasType
            logging.debug(AreasType)

            TotalArea = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[11]/td[2]/text()').extract_first())
            Housebaseitem['TotalArea'] = TotalArea
            logging.debug(TotalArea)

            InsideOfBuildingArea = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[12]/td[2]/text()').extract_first())
            Housebaseitem['InsideOfBuildingArea'] = InsideOfBuildingArea
            logging.debug(InsideOfBuildingArea)

            MeasuredSharedPublicArea = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[13]/td[2]/text()').extract_first())
            Housebaseitem['MeasuredSharedPublicArea'] = MeasuredSharedPublicArea
            logging.debug(MeasuredSharedPublicArea)

            hightArea = check_data_num(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[14]/td[2]/text()').extract_first())
            Housebaseitem['hightArea'] = hightArea
            logging.debug('hightArea' + hightArea)

            Remarks = check_data_str(Selector(response).xpath(
                '/html/body/div[1]/div[4]/div[2]/table/tr[15]/td[2]/text()').extract_first())
            Housebaseitem['Remarks'] = Remarks
            logging.debug(Remarks)

            Price = check_data_num(
                Selector(response).xpath('/html/body/div[1]/div[5]/div[2]/span/text()').extract_first())
            Housebaseitem['Price'] = Price
            logging.debug(Price)
            if HouseSts:
                result.append(Housebaseitem)
        return result
    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
