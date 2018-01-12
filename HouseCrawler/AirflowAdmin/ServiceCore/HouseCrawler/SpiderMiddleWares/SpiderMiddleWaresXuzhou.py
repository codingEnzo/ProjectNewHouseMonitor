# coding = utf-8
import json
import logging
import sys
import uuid

import math
import regex
from scrapy import Request
from HouseCrawler.Items.ItemsXuzhou import *

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
logger = logging.getLogger(__name__)

debug = False


def getParamsDict(url):
    query = urlparse.urlparse(url).query
    return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])


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
            if debug:
                return 1
            try:
                string = string[1:-1].replace('\\', '')
                d = json.loads(string)
                total_count = int(d['Table'][0]['Column1'])
                total_page = math.ceil(total_count / 10)
            except:
                pass
            return total_page

        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') not in ('ProjectBase', 'ProjectBaseLoad'):
            return result if result else []
        # print('ProjectBaseHandleMiddleware')
        result = list(result)
        if response.meta.get('PageType') == 'ProjectBaseLoad':
            datalist = [('DataList5', '丰县'), ('DataList6', '沛县'), ('DataList7', '睢宁县'), ('DataList8', '邳州市'),
                        ('DataList9', '新沂市')]
            for data in datalist:
                elements = response.xpath('//*[@id="{xpath_id}"]/tr/td/table/tr/td[2]/a'.format(xpath_id = data[0]))
                for element in elements:
                    href = 'http://www.xzhouse.com.cn/' + element.xpath('@href').extract_first()
                    param = getParamsDict(href)
                    ProjectName = element.xpath('@title').extract_first()

                    projectInfoItem = ProjectInfoItem()
                    projectInfoItem['ProjectName'] = ProjectName
                    projectInfoItem['ProjectID'] = param.get('corpID')
                    projectInfoItem['DistrictName'] = data[1]

                    projectInfoItem[
                        'SourceUrl'] = 'http://www.xzhouse.com.cn/ItemDetail.aspx?xmmc={ProjectName}&Flag=1&corpID={ProjectID}'.format(
                            ProjectName = urlparse.quote(projectInfoItem['ProjectName'], encoding = 'gbk'),
                            ProjectID = projectInfoItem['ProjectID'])
                    projectInfoItem['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                                projectInfoItem['ProjectID'] + projectInfoItem[
                                                                    'ProjectName'])
                    req = Request(
                            url = projectInfoItem['SourceUrl'],
                            headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                            meta = {'PageType': 'ProjectInfo', 'projectInfoItem': projectInfoItem, 'count': 1},
                            dont_filter = True)
                    result.append(req)
        elif response.meta.get('PageType') == 'ProjectBase':
            if response.meta.get('GetPage'):
                DistrictName = response.meta.get('DistrictName')
                total_page = get_totla_page(response.body_as_unicode())
                for page in range(total_page):
                    body = "{'CurrentPageIndex':" + str(page) + ",'whereContent':'I_Dist|" + DistrictName + "'}"
                    req = Request(url='http://www.xzhouse.com.cn/xlxx.aspx/GridBind',
                            method='POST',
                            headers=self.settings.get('POST_DEFAULT_REQUEST_HEADERS'),
                            dont_filter=True,
                            body=body,
                            meta={
                                'PageType': 'ProjectBase', 'param': body, 'count': 1
                            })
                    result.append(req)
            else:
                string = response.body_as_unicode()
                string = string[1:-1].replace('\\', '')
                data = None
                try:
                    data = json.loads(string)
                except:
                    # 重新请求这个接口
                    count = response.meta.get('count')
                    body = response.meta.get('body')
                    if count <= 3:
                        count = count + 1
                        ret_req = Request(url = 'http://www.xzhouse.com.cn/xlxx.aspx/GridBind',
                                          method='POST',
                                          headers=self.settings.get('POST_DEFAULT_REQUEST_HEADERS'),
                                          dont_filter=True,
                                          body=body,
                                          meta={'PageType': 'ProjectBase', 'param': body, 'count': count})
                        result.append(ret_req)

                if isinstance(data, dict):
                    projectList = data['Table1']
                    for d in projectList:
                        projectInfoItem = ProjectInfoItem()
                        projectInfoItem['ProjectName'] = d['I_ItName']
                        projectInfoItem['Developer'] = d['I_CoName']
                        projectInfoItem['DistrictName'] = d['I_Dist']
                        projectInfoItem['RegionName'] = d['I_Zone']
                        projectInfoItem['ProjectAddress'] = d['I_ItSite']
                        projectInfoItem['ProjectID'] = d['CorpInfo_id']
                        projectInfoItem[
                            'SourceUrl'] = 'http://www.xzhouse.com.cn/ItemDetail.aspx?xmmc={ProjectName}&Flag=1&corpID={ProjectID}'.format(
                                ProjectName = urlparse.quote(projectInfoItem['ProjectName'], encoding = 'gbk'),
                                ProjectID = projectInfoItem['ProjectID'])
                        projectInfoItem['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                                    projectInfoItem['ProjectID'] + projectInfoItem[
                                                                        'ProjectName'])
                        req = Request(
                                url = projectInfoItem['SourceUrl'],
                                headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                meta = {'PageType': 'ProjectInfo', 'projectInfoItem': projectInfoItem, 'count': 1},
                                dont_filter = True)
                        result.append(req)
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
                if isinstance(string, list):
                    string = ''.join(string)
                re_h = regex.compile(r'<[^>]+>', regex.S)
                return re_h.sub('', string)
            except:
                return ''

        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectInfo':
            return result if result else []
        # print('ProjectInfoHandleMiddleware')
        result = list(result)
        projectInfoItem = response.meta.get('projectInfoItem')
        # 验证网页内容是否跟网址一致,不一致的话就重新请求该页面
        action = response.xpath('//*[@id="form1"]/@action').extract_first()
        if action is None or not action.endswith('corpID={ProjectID}'.format(ProjectID=projectInfoItem['ProjectID'])):
            count = response.meta.get('count')
            if count < 6:
                count += 1
                req = Request(
                        url = projectInfoItem['SourceUrl'],
                        headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                        meta = {'PageType': 'ProjectInfo', 'projectInfoItem': projectInfoItem, 'count': count},
                        dont_filter = True)
                result.append(req)
            return result

        # 部分项目信息页面的信息为空,如果为空则保存从列表带过来的信息
        page_ProjectName = response.xpath(
                '//span[text()="项目名称:"]/../following-sibling::td[1]/strong/text()').extract_first()
        if page_ProjectName:  # 网页有内容才爬
            projectInfoItem['PromotionName'] = response.xpath(
                    '//span[text()="推广名称:"]/../following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['Developer'] = response.xpath(
                    '//span[text()="开发企业:"]/../following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['SellAddress'] = response.xpath(
                    '//span[text()="售楼地址:"]/../following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['ProjectAddress'] = response.xpath(
                    '//span[text()="项目地址:"]/../following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['EarliestStartDate'] = response.xpath(
                    '//span[text()="开工时间:"]/../following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['CompletionDate'] = response.xpath(
                    '//span[text()="竣工时间:"]/../following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['PropertyRightsDescription'] = response.xpath(
                    '//td[contains(text(),"使用年限")]/following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['GreeningRate'] = response.xpath(
                    '//td[contains(text(),"绿化率")]/following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['Decoration'] = response.xpath(
                    '//td[contains(text(),"装修情况")]/following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['FloorAreaRatio'] = response.xpath(
                    '//td[contains(text(),"容积率")]/following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['AveragePrice'] = response.xpath(
                    '//td[contains(text(),"均价")]/following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['TotalBuidlingArea'] = response.xpath(
                    '//td[contains(text(),"建筑面积")]/following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['ManagementFees'] = response.xpath(
                    '//td[contains(text(),"物业费")]/following-sibling::td[1]/strong/text()').extract_first()
            projectInfoItem['ParkingSpaceAmount'] = response.xpath(
                    '//td[contains(text(),"停车位")]/following-sibling::td[1]/strong/text()').extract_first()
            ProjectIntro_text = response.xpath('//*[@id="div1"]').re(r'.+')
            projectInfoItem['ProjectIntro'] = remove_html_tag(ProjectIntro_text)
            ProjectSupporting_text = response.xpath('//*[@id="div2"]').re(r'.+')
            projectInfoItem['ProjectSupporting'] = remove_html_tag(ProjectSupporting_text)
            result.append(projectInfoItem)

        # 不管项目信息有没有都要爬取预售证
        tr_arr = response.xpath('//strong[text()="预售许可证号"]/../../../following-sibling::table/tr')
        for tr in tr_arr:
            href = tr.xpath('td[1]/a/@href').extract_first()
            LssueDate = tr.xpath('td[3]/a/span/text()').extract_first()
            req = Request(url = 'http://www.xzhouse.com.cn/' + href,
                          headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                          meta = {
                              'PageType': 'PresellInfo',
                              'ProjectUUID': str(projectInfoItem['ProjectUUID']),
                              'LssueDate': LssueDate
                          }, dont_filter = True)
            result.append(req)
        return result


# 预售证
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
        ProjectUUID = response.meta.get('ProjectUUID')
        LssueDate = response.meta.get('LssueDate')
        presellInfoItem = PresellInfoItem()
        presellInfoItem['SourceUrl'] = response.url
        presellInfoItem['ProjectUUID'] = ProjectUUID
        presellInfoItem['LssueDate'] = LssueDate
        presellInfoItem['PresellUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                    ProjectUUID + presellInfoItem['SourceUrl'].upper())
        presellInfoItem['ProjectName'] = response.xpath('//*[@id="lblItemName"]/text()').extract_first()
        presellInfoItem['DistrictName'] = response.xpath('//*[@id="lblDist"]/text()').extract_first()
        presellInfoItem['ProjectAddress'] = response.xpath('//*[@id="lblItemSite"]/text()').extract_first()
        presellInfoItem['RegionName'] = response.xpath('//*[@id="lblZone"]/text()').extract_first()
        presellInfoItem['Developer'] = response.xpath('//*[@id="lblCorpName"]/text()').extract_first()
        presellInfoItem['LandUse'] = response.xpath('//*[@id="lblPlUse"]/text()').extract_first()
        presellInfoItem['BuildingPermit'] = response.xpath('//*[@id="lblItPlLicNum"]/text()').extract_first()
        presellInfoItem['CertificateOfUseOfStateOwnedLand'] = response.xpath(
                '//*[@id="lblItLaUseLic"]/text()').extract_first()
        presellInfoItem['LandCertificate'] = response.xpath('//*[@id="lblLaCertNum"]/text()').extract_first()
        presellInfoItem['ConstructionPermitNumber'] = response.xpath('//*[@id="lblIStruLicNum"]/text()').extract_first()
        presellInfoItem['FloorArea'] = response.xpath('//*[@id="lblLaAcre"]/text()').extract_first()
        presellInfoItem['EarliestStartDate'] = response.xpath('//*[@id="lblWoSDate"]/text()').extract_first()
        presellInfoItem['PresalePermitNumber'] = response.xpath('//*[@id="lblPreSellCert"]/text()').extract_first()
        presellInfoItem['CompletionDate'] = response.xpath('//*[@id="lblWoFinDate"]/text()').extract_first()
        presellInfoItem['FloorArea'] = response.xpath('//*[@id="lblLaAcre"]/text()').extract_first()
        presellInfoItem['ApprovalPresaleAmount'] = response.xpath('//*[@id="lblSumSuits"]/text()').extract_first()
        presellInfoItem['SoldAmount'] = response.xpath('//*[@id="lblSelledSuits"]/text()').extract_first()
        presellInfoItem['UnsoldAmount'] = response.xpath('//*[@id="lblCanSellSuits"]/text()').extract_first()
        presellInfoItem['ApprovalPresaleArea'] = response.xpath('//*[@id="lblSumArea"]/text()').extract_first()
        presellInfoItem['SoldArea'] = response.xpath('//*[@id="lblSelledArea"]/text()').extract_first()
        presellInfoItem['UnsoldArea'] = response.xpath('//*[@id="lblCanSellArea"]/text()').extract_first()
        lblSellRate = response.xpath('//*[@id="lblSellRate"]/text()').extract_first()
        presellInfoItem['SoldRatio'] = lblSellRate + '%' if lblSellRate else ''
        result.append(presellInfoItem)

        # 获取楼栋链接
        href_arr = response.xpath('//a[text()="点此查看"]/@href').extract()
        for href in href_arr:
            building_req = Request(url = 'http://www.xzhouse.com.cn/' + href,
                                   headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                   meta = {
                                       'PageType': 'BuildingInfo',
                                       'ProjectUUID': presellInfoItem['ProjectUUID'],
                                       'PresellUUID': str(presellInfoItem['PresellUUID']),
                                       'ProjectName': presellInfoItem['ProjectName'],
                                       'PresalePermitNumber': presellInfoItem['PresalePermitNumber'],
                                   }, dont_filter = True)
            result.append(building_req)
        return result


class BuildingInfoHandleMiddleware(object):
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
        if response.meta.get('PageType') != 'BuildingInfo':
            return result if result else []
        # print('BuildingInfoHandleMiddleware')
        ProjectUUID = response.meta.get('ProjectUUID')
        PresellUUID = response.meta.get('PresellUUID')
        ProjectName = response.meta.get('ProjectName')
        PresalePermitNumber = response.meta.get('PresalePermitNumber')

        buildingItem = BuildingInfoItem()
        buildingItem['PresellUUID'] = PresellUUID
        buildingItem['ProjectUUID'] = ProjectUUID
        buildingItem['ProjectName'] = ProjectName
        buildingItem['PresalePermitNumber'] = PresalePermitNumber
        buildingItem['SourceUrl'] = response.url
        buildingItem['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, PresellUUID+buildingItem['SourceUrl'].upper())
        string = response.xpath('//*[@id="Label1"]/text()').extract_first()
        try:
            buildingItem['BuildingName'] = string[string.rindex('：') + 1:]
        except:
            buildingItem['BuildingName'] = ''
        buildingItem['ApprovalPresaleAmount'] = response.xpath('//*[@id="lblSumSuits"]/text()').extract_first()
        buildingItem['SoldAmount'] = response.xpath('//*[@id="lblSelledSuits"]/text()').extract_first()
        buildingItem['UnsoldAmount'] = response.xpath('//*[@id="lblCanSellSuits"]/text()').extract_first()
        buildingItem['ApprovalPresaleArea'] = response.xpath('//*[@id="lblSumArea"]/text()').extract_first()
        buildingItem['SoldArea'] = response.xpath('//*[@id="lblSelledArea"]/text()').extract_first()
        buildingItem['UnsoldArea'] = response.xpath('//*[@id="lblCanSellArea"]/text()').extract_first()

        result.append(buildingItem)
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
        if response.meta.get('PageType') not in ('HouseList', 'HouseInfo'):
            return result if result else []
        result = list(result)
        # print('HouseInfoHandleMiddleware')
        ProjectUUID = response.meta.get('ProjectUUID')
        PresellUUID = response.meta.get('PresellUUID')
        BuildingUUID = response.meta.get('BuildingUUID')
        ProjectName = response.meta.get('ProjectName')
        PresalePermitNumber = response.meta.get('PresalePermitNumber')
        BuildingName = response.meta.get('BuildingName')

        if response.meta.get('PageType') == 'HouseList':
            href_arr = response.xpath('//a[starts-with(@href,"houseDetail.aspx?ID=")]/@href').extract()
            for href in href_arr:
                house_info_req = Request(url = 'http://www.xzhouse.com.cn/' + href,
                                         headers = self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                         dont_filter = True,
                                         meta = {'PageType': 'HouseInfo',
                                                 'PresellUUID': PresellUUID,
                                                 'ProjectUUID': ProjectUUID,
                                                 'BuildingUUID': BuildingUUID,
                                                 'ProjectName': ProjectName,
                                                 'PresalePermitNumber': PresalePermitNumber,
                                                 'BuildingName': BuildingName,
                                                 })
                result.append(house_info_req)
        elif response.meta.get('PageType') == 'HouseInfo':
            houseDetailItem = HouseInfoItem()
            houseDetailItem['SourceUrl'] = response.url
            houseDetailItem['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, BuildingUUID+houseDetailItem['SourceUrl'].upper())
            houseDetailItem['ProjectUUID'] = ProjectUUID
            houseDetailItem['PresellUUID'] = PresellUUID
            houseDetailItem['BuildingUUID'] = BuildingUUID
            houseDetailItem['ProjectName'] = ProjectName
            houseDetailItem['PresalePermitNumber'] = PresalePermitNumber
            houseDetailItem['BuildingName'] = BuildingName

            houseDetailItem['UnitName'] = response.xpath('//*[@id="lblCeCode"]/text()').extract_first()
            houseDetailItem['HouseNumber'] = response.xpath('//*[@id="lblRoNum"]/text()').extract_first()
            houseDetailItem['HouseUseType'] = response.xpath('//*[@id="lblHoUse"]/text()').extract_first()
            houseDetailItem['BuildingStructure'] = response.xpath('//*[@id="lblHoStru"]/text()').extract_first()
            houseDetailItem['MeasuredBuildingArea'] = response.xpath('//*[@id="lblStruArea"]/text()').extract_first()
            houseDetailItem['MeasuredInsideOfBuildingArea'] = response.xpath(
                    '//*[@id="lblInArea"]/text()').extract_first()
            houseDetailItem['MeasuredSharedPublicArea'] = response.xpath(
                    '//*[@id="lblShareArea"]/text()').extract_first()
            houseDetailItem['HouseState'] = response.xpath('//*[@id="lblHoState"]/text()').extract_first()
            houseDetailItem['ContractRecordNumber'] = response.xpath('//*[@id="lblBaRecNum"]/text()').extract_first()
            houseDetailItem['ContractRecordDate'] = response.xpath('//*[@id="lblBaRecDate"]/text()').extract_first()


            #2018年01月10日要求增加图片爬取
            image_urls = []
            src_arr = response.xpath('//img[starts-with(@src,"houseMap.aspx")]/@src').extract()
            for src in src_arr:
                image_urls.append('http://www.xzhouse.com.cn/'+src)

            imageItem = UnitshapeImageInfoItem()
            imageItem['SourceUrl'] = response.url
            imageItem['ProjectUUID'] = ProjectUUID
            imageItem['PresellUUID'] = PresellUUID
            imageItem['BuildingUUID'] = BuildingUUID
            imageItem['HouseUUID'] = houseDetailItem['HouseUUID']
            imageItem['ImageUrls'] = image_urls

            result.append(houseDetailItem)
            result.append(imageItem)
        return result