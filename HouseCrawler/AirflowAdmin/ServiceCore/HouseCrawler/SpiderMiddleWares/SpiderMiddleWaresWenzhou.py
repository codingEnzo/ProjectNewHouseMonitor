# -*- coding: utf-8 -*-
import sys
import uuid
import re
import json
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsWenzhou import *

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


def get_house_state(string):
    STATE_TAB = {
        'G1': '可售',
        'G2': '安置房',
        'G3': '自留房',
        'G4': '非出售',
        'G10': '已认购',
        'G5': '已签预订协议',
        'G6': '已签合同',
        'G7': '合同已登记',
        'G8': '已认购',

        'B1': '可售',
        'B2': '安置房',
        'B3': '自留房',
        'B4': '非出售',
        'B10': '已认购',
        'B5': '已签预订协议',
        'B6': '已签合同',
        'B7': '合同已登记',
        'B8': '已认购',
        'B': '不在项目内',
    }
    state = ''
    for key in STATE_TAB:
        if key in string:
            state = STATE_TAB[key]
            break
    return state


def check_data_num(string):
    result_data = ''
    if string:
        fix_data = string.strip().replace('\r', '').replace('\n', '').replace("㎡", "") \
            .replace('\t', '').replace('\\', '').replace('n', '').replace('t', '').replace("一房一价：元", "") \
            .replace(' ', '').replace("套", "").replace("幢", "").replace("㎡", "") \
            .replace("元", "").replace("m", "").replace("M", "") \
            .replace("%", "").replace("个", "").replace("/", "")
        if fix_data != '' and '*' not in fix_data:
            result_data = fix_data
        return result_data


def check_data_str(string):
    result_data = ''
    if string:
        fix_data = string.strip().replace('\r', '').replace('\n', '') \
            .replace('\t', '').replace(' ', '').replace(" ", "")
        if fix_data != '' and '*' not in fix_data:
            result_data = fix_data
    return result_data


class SpiderMiddlerProjectBase(object):
    def __init__(self, settings):
        self.settings = settings
        self.headers = {'Host': 'www.wzfg.com',
                        'Connection': 'keep-alive',
                        'Cache-Control': 'max-age=0',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.94 Chrome/62.0.3202.94 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        }

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
        try:
            if response.meta.get('PageType') == 'ProjectStart':
                pagenumhref = check_data_str(
                        Selector(response).xpath('//*[@id="aButton"]/tr/td[2]/table/tr/td[16]/a/@href').extract_first())
                pagenum = re.search(r'goPage\((.*?)\)', pagenumhref)
                if pagenum:
                    pagenum = pagenum.group(1)
                    for i in range(int(pagenum)):

                        mainurl = 'http://www.wzfg.com/realweb/stat/ProjectSellingList.jsp?currPage={currPage}&permitNo=&projectName=&projectAddr=&region=&num={num}'.format(
                            currPage = i, num = i)
                        page_req = Request(url = mainurl,
                                headers = self.headers,
                                meta = {
                                    'PageType': 'ProjectBase',
                                })
                        result.append(page_req)
            if response.meta.get('PageType') == 'ProjectBase':
                ProjectLists = Selector(response).xpath('/html/body/table[1]/tr/td/table[3]/tr')
                if len(ProjectLists) > 1:
                    for index in ProjectLists[1:]:
                        ProjectUrl = check_data_str(index.xpath('./@onclick').extract_first())
                        ProjectMainUrl = 'http://www.wzfg.com/realweb/stat/'
                        ProjectUrl = ProjectMainUrl + re.search(r"\'(.*?)\'", ProjectUrl).group(1)

                        PresalePermitNumber = check_data_str(index.xpath('./td[2]/text()').extract_first())

                        ProjectAddress = check_data_str(index.xpath('./td[4]/text()').extract_first())

                        OpeningDate = check_data_str(index.xpath('./td[5]/text()').extract_first())

                        RegionName = check_data_str(index.xpath('./td[6]/text()').extract_first())

                        # http://www.wzfg.com/realweb/stat/FirstHandProjectInfo.jsp?projectID=9001938
                        # http://www.wzfg.com/realweb/stat/FirsHadProjecIfo.jsp?projecID=9001906

                        project_base_req = Request(url = ProjectUrl,
                                                   headers=self.headers,
                                                   meta={
                                                       'PageType': 'ProjectInfo',
                                                       'PresalePermitNumber': PresalePermitNumber,
                                                       'ProjectAddress': ProjectAddress,
                                                       'OpeningDate': OpeningDate,
                                                       'RegionName': RegionName,
                                                   })
                        result.append(project_base_req)


            if response.meta.get('PageType') == 'ProjectInfo':
                Projectbaseitem = ProjectBaseItem()
                Projectbaseitem['ProjectUrl'] = response.url
                Projectbaseitem['PresalePermitNumber'] = response.meta.get('PresalePermitNumber')
                Projectbaseitem['ProjectAddress'] = response.meta.get('ProjectAddress')
                Projectbaseitem['OpeningDate'] = response.meta.get('OpeningDate')
                Projectbaseitem['RegionName'] = response.meta.get('RegionName')
                DeveloperName = check_data_str(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[1]/td[2]/a/text()').extract_first())
                Projectbaseitem['DeveloperName'] = DeveloperName
                PresalePermitNumber = check_data_str(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[2]/td[2]/text()').extract_first())
                Projectbaseitem['PresalePermitNumber'] = PresalePermitNumber
                LssueDate = check_data_str(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[3]/td[2]/text()').extract_first())
                Projectbaseitem['LssueDate'] = LssueDate
                RegionName = check_data_str(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[4]/td[2]/text()').extract_first())
                Projectbaseitem['RegionName'] = RegionName

                Samplearea = check_data_str(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[5]/td[2]/text()').extract_first())
                Projectbaseitem['Samplearea'] = Samplearea

                TotalBuidlingArea = check_data_num(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[6]/td[2]/text()').extract_first())
                Projectbaseitem['TotalBuidlingArea'] = TotalBuidlingArea

                ProjectName = check_data_str(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[7]/td[2]/text()').extract_first())
                Projectbaseitem['ProjectName'] = ProjectName

                ProjectAddress = check_data_str(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[8]/td[2]/text()').extract_first())
                Projectbaseitem['ProjectAddress'] = ProjectAddress

                StartDate = check_data_str(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[9]/td[2]/text()').extract_first())
                Projectbaseitem['StartDate'] = StartDate

                ProjectSaleAddress = check_data_str(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[10]/td[2]/text()').extract_first())
                Projectbaseitem['ProjectSaleAddress'] = ProjectSaleAddress

                ProjectSalePhone = check_data_str(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[11]/td[2]/text()').extract_first())
                Projectbaseitem['ProjectSalePhone'] = ProjectSalePhone
                # //*[@id="typePriceInfo"]/table/tbody/tr[2]
                typePriceInfo = {}
                typePriceInfos = Selector(response).xpath('//*[@id="typePriceInfo"]/table/tr')
                typePriceInfonum = 0
                if typePriceInfos:
                    for PriceInfo in typePriceInfos[1:]:
                        keyname = str(typePriceInfonum)
                        typePriceInfo[keyname] = {
                            'HouseType': check_data_str(
                                    PriceInfo.xpath('./td[1]/text()').extract_first()),
                            'HouseUseType': check_data_str(
                                    PriceInfo.xpath('./td[2]/text()').extract_first()),
                            'HouseNum': check_data_num(
                                    PriceInfo.xpath('./td[3]/text()').extract_first()),
                            'HousePrice': check_data_num(
                                    PriceInfo.xpath('./td[5]/text()').extract_first()),
                            'Detail': check_data_num(
                                    PriceInfo.xpath('./td[6]/text()').extract_first()),
                        }
                        typePriceInfonum = typePriceInfonum + 1
                else:
                    typePriceInfo = {'0': '0'}

                Projectbaseitem['typePriceInfo'] = typePriceInfo if typePriceInfo != {} else {'0':'0'}

                TotalHouseNum = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[2]/td[2]/a/text()').extract_first())
                Projectbaseitem['TotalHouseNum'] = TotalHouseNum

                TotalHouseAreas = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[2]/td[3]/text()').extract_first())
                Projectbaseitem['TotalHouseAreas'] = TotalHouseAreas

                SalingHouseNum = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[3]/td[2]/a/text()').extract_first())
                Projectbaseitem['SalingHouseNum'] = SalingHouseNum

                SalingHouseAreas = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[3]/td[3]/text()').extract_first())
                Projectbaseitem['SalingHouseAreas'] = SalingHouseAreas

                SalingDwellingNum = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[4]/td[2]/a/text()').extract_first())
                Projectbaseitem['SalingDwellingNum'] = SalingDwellingNum

                SalingDwellingAreas = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[4]/td[3]/text()').extract_first())
                Projectbaseitem['SalingDwellingAreas'] = SalingDwellingAreas

                SubscribedNum = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[5]/td[2]/a/text()').extract_first())
                Projectbaseitem['SubscribedNum'] = SubscribedNum

                SubscribedAreas = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[5]/td[3]/text()').extract_first())
                Projectbaseitem['SubscribedAreas'] = SubscribedAreas

                SoldNum = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[6]/td[2]/a/text()').extract_first())
                Projectbaseitem['SoldNum'] = SoldNum

                SoldAreas = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[6]/td[3]/text()').extract_first())
                Projectbaseitem['SoldAreas'] = SoldAreas

                RegisteredNum = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[7]/td[2]/a/text()').extract_first())
                Projectbaseitem['RegisteredNum'] = RegisteredNum

                RegisteredAreas = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[7]/td[3]/text()').extract_first())
                Projectbaseitem['RegisteredAreas'] = RegisteredAreas

                PlacementofhousingNum = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[8]/td[2]/a/text()').extract_first())
                Projectbaseitem['PlacementofhousingNum'] = PlacementofhousingNum

                PlacementofhousingAreas = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[8]/td[3]/text()').extract_first())
                Projectbaseitem['PlacementofhousingAreas'] = PlacementofhousingAreas

                RestrictedpropertyNum = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[9]/td[2]/a/text()').extract_first())
                Projectbaseitem['RestrictedpropertyNum'] = RestrictedpropertyNum

                RestrictedpropertyAreas = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[9]/td[3]/text()').extract_first())
                Projectbaseitem['RestrictedpropertyAreas'] = RestrictedpropertyAreas

                NonsalesNum = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[10]/td[2]/a/text()').extract_first())
                Projectbaseitem['NonsalesNum'] = NonsalesNum

                NonsalesAreas = check_data_num(Selector(response).xpath(
                        '//*[@id="withdrawInfo"]/table/tr/td/table/tr[10]/td[3]/text()').extract_first())
                Projectbaseitem['NonsalesAreas'] = NonsalesAreas

                ProjectNo = uuid.uuid3(uuid.NAMESPACE_DNS, str(ProjectName)).hex
                Projectbaseitem['ProjectNo'] = ProjectNo


                DeveloperInfoUrl = check_data_str(
                        Selector(response).xpath('//*[@id="saleInfo"]/table/tr[1]/td[2]/a/@href').extract_first())
                DeveloperBaseUrl = 'http://www.wzfg.com/cyzt/devcompany/CorporationView.jsp?devCompanyID='
                if DeveloperInfoUrl:
                    DeveloperInfoUrl = DeveloperBaseUrl + re.search(r'\((.*?)\)', DeveloperInfoUrl).group(1)
                    Projectbaseitem['DeveloperInfoUrl'] = DeveloperInfoUrl

                    # DeveloperInfo_req = Request(url = DeveloperInfoUrl,
                    #                             headers=self.headers,
                    #                             meta={
                    #                                 'PageType': 'DeveloperInfo',
                    #                                 'ProjectName': ProjectName,
                    #                                 'ProjectNo': ProjectNo
                    #                             })
                    # result.append(DeveloperInfo_req)

                result.append(Projectbaseitem)

                # building
                BuildingDetails = Selector(response).xpath('//*[@id="tdBldList"]/a')
                if len(BuildingDetails) > 1:
                    for index in BuildingDetails[1:]:
                        buildingbaseitem = BuildingBaseItem()
                        buildingbaseitem['ProjectName'] = ProjectName
                        buildingbaseitem['ProjectNo'] = ProjectNo

                        BuildingInfo = index.xpath('./@title').extract_first()
                        for data in BuildingInfo.split("\n"):
                            if '地址' in data:
                                buildingbaseitem['BuildingAddress'] = check_data_str(data.split("：")[1])
                            if '总层数' in data:
                                buildingbaseitem['BuildingTotalFloor'] = check_data_str(data.split("：")[1])
                            if '户室数' in data:
                                buildingbaseitem['BuildingHouseNum'] = check_data_str(data.split("：")[1])
                            if '总建筑面积' in data:
                                buildingbaseitem['BuildingAreas'] = check_data_str(data.split("：")[1])
                            if '建筑结构' in data:
                                buildingbaseitem['BuildingStructure'] = check_data_str(data.split("：")[1])
                            if '项目测算面积' in data:
                                buildingbaseitem['BuildingPreAreas'] = check_data_str(data.split("：")[1])
                        buildingbaseitem['BuildingInfo'] = check_data_str(BuildingInfo)
                        BuildingId = check_data_str(index.xpath('./@id').extract_first())
                        buildingbaseitem['BuildingId'] = BuildingId
                        buildingtablexpath = '//*[@id="%s"]/tr' % BuildingId.replace("d", "t")
                        BuildingName = check_data_str(index.xpath('./text()').extract_first())
                        buildingbaseitem['BuildingName'] = BuildingName

                        BuildingNo = uuid.uuid3(uuid.NAMESPACE_DNS, str(ProjectName + BuildingName)).hex
                        buildingbaseitem['BuildingNo'] = BuildingNo
                        result.append(buildingbaseitem)
                        # //*[@id="Bt683148|5、6幢"]
                        buildingtable = Selector(response).xpath('//*[@id="tdRooms"]')
                        HouseDetails = buildingtable.xpath(buildingtablexpath)

                        if HouseDetails:
                            rechousenum = 0
                            for HouseDetail in HouseDetails:
                                HouseRealFloor = check_data_str(HouseDetail.xpath('./td[1]/a/text()').extract_first())

                                HouseInfos = HouseDetail.xpath('./td[2]/a')
                                if HouseInfos:
                                    for index in HouseInfos:
                                        housebaseitem = HouseBaseItem()
                                        housebaseitem['ProjectName'] = ProjectName
                                        housebaseitem['ProjectNo'] = ProjectNo
                                        housebaseitem['BuildingName'] = BuildingName
                                        housebaseitem['BuildingNo'] = BuildingNo
                                        housebaseitem['HouseRealFloor'] = HouseRealFloor
                                        HouseId = check_data_str(index.xpath('./@id').extract_first())
                                        housebaseitem['HouseId'] = HouseId
                                        HouseAreas = check_data_num(index.xpath('./@title').extract_first())
                                        housebaseitem['HouseAreas'] = HouseAreas
                                        HouseNum = check_data_str(index.xpath('./text()').extract_first())
                                        housebaseitem['HouseNum'] = HouseNum
                                        housebaseitem['HouseNo'] = uuid.uuid3(uuid.NAMESPACE_DNS, str(
                                                ProjectName + BuildingName + HouseNum + str(rechousenum))).hex
                                        rechousenum = rechousenum + 1
                                        HouseClass = check_data_str(index.xpath('./@class').extract_first())
                                        housebaseitem['HouseClass'] = HouseClass
                                        housebaseitem['HouseSts'] = get_house_state(HouseClass)
                                        result.append(housebaseitem)

        except:
            pass
            # project_base = {
            #     'err_url': response.url,
            #     'PageType': 'ProjectBase'
            # }
            # project_base_json = json.dumps(project_base, sort_keys = True)
            # self.r.sadd('Developer_Err_Page', project_base_json)
        return result


class SpiderMiddlerDeveloperInfo(object):
    def __init__(self, settings):
        self.settings = settings
        self.headers = {'Host': 'www.wzfg.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.94 Chrome/62.0.3202.94 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Referer': 'http://www.wzfg.com/realweb/stat/ProjectSellingList.jsp',
                        'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'DeveloperInfo':
            Developerbaseitem = DeveloperBaseItem()
            ProjectName = response.meta.get('ProjectName')
            ProjectNo = response.meta.get('ProjectNo')
            Developerbaseitem['ProjectName'] = ProjectName
            Developerbaseitem['ProjectNo'] = ProjectNo

            Developerbaseitem['DeveloperUrl'] = response.url

            DeveloperName = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[2]/td[2]/text()').extract_first())
            Developerbaseitem['DeveloperName'] = DeveloperName

            DeveloperNo = uuid.uuid3(uuid.NAMESPACE_DNS, str(DeveloperName)).hex
            Developerbaseitem['DeveloperNo'] = DeveloperNo

            LegalRepresentative = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[2]/td[4]/text()').extract_first())
            Developerbaseitem['LegalRepresentative'] = LegalRepresentative

            BusinessLicenseNumber = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[3]/td[2]/text()').extract_first())
            Developerbaseitem['BusinessLicenseNumber'] = BusinessLicenseNumber

            DeveloperComAddress = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[3]/td[4]/text()').extract_first())
            Developerbaseitem['DeveloperComAddress'] = DeveloperComAddress

            RegisteredCapital = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[4]/td[2]/text()').extract_first())
            Developerbaseitem['RegisteredCapital'] = RegisteredCapital

            DeveloperPhoneNumber = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[4]/td[4]/text()').extract_first())
            Developerbaseitem['DeveloperPhoneNumber'] = DeveloperPhoneNumber

            QualificationGrade = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[5]/td[2]/text()').extract_first())
            Developerbaseitem['QualificationGrade'] = QualificationGrade

            CertificateNumber = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[5]/td[4]/text()').extract_first())
            Developerbaseitem['CertificateNumber'] = CertificateNumber

            Fax = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[6]/td[2]/text()').extract_first())
            Developerbaseitem['Fax'] = Fax

            ZipCode = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[6]/td[4]/text()').extract_first())
            Developerbaseitem['ZipCode'] = ZipCode

            Email = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[7]/td[2]/text()').extract_first())
            Developerbaseitem['Email'] = Email

            Web = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[7]/td[4]/text()').extract_first())
            Developerbaseitem['Web'] = Web

            Remarks = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[8]/td[2]/text()').extract_first())
            Developerbaseitem['Remarks'] = Remarks

            Registrar = check_data_str(
                    Selector(response).xpath('/html/body/form/table[2]/tr[9]/td[2]/text()').extract_first())
            Developerbaseitem['Registrar'] = Registrar

            result.append(Developerbaseitem)

        return result

    def process_spider_exception(self, response, exception, spider):
        return
