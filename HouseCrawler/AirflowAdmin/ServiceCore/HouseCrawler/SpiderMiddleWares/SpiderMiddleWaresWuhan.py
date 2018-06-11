# coding = utf-8
import logging
import sys
import uuid

import regex

from scrapy import Request
from HouseCrawler.Items.ItemsWuhan import *

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
logger = logging.getLogger(__name__)

debug = False


def getParamsDict(url):
    query = urlparse.urlparse(url).query
    return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])


class ProjectListHandleMiddleware(object):
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
            try:
                t = response.xpath('//a[starts-with(@href,"javascript:_submit")][last()]/@href').extract_first()
                total_page = int(regex.search('submit\((?<page>\d+)\)', t).group(1))
            except Exception:
                pass
            if debug:
                return 1
            return total_page

        result = list(result)
        if not (200 <= response.status < 300):
            return result if result else []
        if response.meta.get('PageType') != 'ProjectList':
            return result if result else []
        print('ProjectListHandleMiddleware')
        if response.request.method == 'GET':
            total_page = get_totla_page(response)
            for page in range(1, total_page + 1):
                list_req = Request(url=response.url,
                                   headers=self.settings.get('POST_DEFAULT_REQUEST_HEADERS'),
                                   method='POST',
                                   body=urlparse.urlencode({
                                       'shiqs': '',
                                       'xiangMmc': '',
                                       'menPhm': '',
                                       'kaifs': '',
                                       'pageNo': str(page),
                                   }),
                                   dont_filter=True,
                                   meta={'PageType': 'ProjectList'})
                result.append(list_req)
        else:
            tr_arr = response.xpath('//*[@id="jvForm"]/div[2]/table[1]/tr')
            for tr in tr_arr[1:]:
                urltext = tr.xpath('td[1]/a/@onclick').extract_first('')

                c = regex.search("\('(?<url>.*)'\)", urltext)
                if c:
                    url = urlparse.urljoin(response.url, c.group(1))
                    # print(url)
                    param = getParamsDict(url)
                    project = ProjectInfoItem()
                    project['SourceUrl'] = url
                    project['RealEstateProjectID'] = param.get('dengJh', '')
                    project['ProjectName'] = tr.xpath('/td[1]/a/text()').extract_first('')
                    project['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                        project['RealEstateProjectID'] + project['ProjectName'])
                    project['HousingCount'] = tr.xpath('/td[2]/text()').extract_first('')
                    project['HouseSoldCount'] = tr.xpath('/td[3]/text()').extract_first('')
                    project['HouseCount'] = tr.xpath('/td[4]/text()').extract_first('')
                    project['UnHouseSoldCount'] = tr.xpath('/td[5]/text()').extract_first('')
                    project['UnHouseCount'] = tr.xpath('/td[6]/text()').extract_first('')

                    req = Request(url=url,
                                  headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                  dont_filter=True,
                                  meta={'PageType': 'ProjectInfo',
                                        'item': project})
                    result.append(req)

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
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectInfo':
            return result if result else []
        result = list(result)
        print('ProjectInfoHandleMiddleware')
        project = response.meta.get('item')

        if not project['ProjectName']:
            project['ProjectName'] = response.xpath('//*[@id="xiangmmc"]/text()').extract_first('')
        project['ProjectAddress'] = response.xpath('//*[@id="MenPhm"]/text()').extract_first('')
        project['EarliestStartDate'] = response.xpath('//*[@id="kaigsj"]/text()').extract_first('')
        project['CompletionDate'] = response.xpath('//*[@id="jungsj"]/text()').extract_first('')
        project['FloorArea'] = response.xpath('//*[@id="TuDmj"]/text()').extract_first('')
        project['PropertyRightsDescription'] = response.xpath('//*[@id="ShiYnx"]/text()').extract_first('')
        project['LandUse'] = response.xpath('//*[@id="TuDyt"]/text()').extract_first('')
        project['LandLevel'] = response.xpath('//*[@id="TuDdj"]/text()').extract_first('')
        project['TotalBuidlingArea'] = response.xpath('//*[@id="JianZmj"]/text()').extract_first('')
        project['FloorAreaRatio'] = response.xpath('//*[@id="rongjl"]/text()').extract_first('')
        if not project['HousingCount']:
            project['HousingCount'] = response.xpath('//*[@id="zts"]/text()').extract_first('')
        project['HouseBuildingCount'] = response.xpath('//*[@id="ZDongS"]/text()').extract_first('')
        project['ProjectBookingData'] = response.xpath('//*[@id="xiaossj"]/text()').extract_first('')
        project['OtheRights'] = response.xpath('//*[@id="TaXql"]/text()').extract_first('')

        project['LandUsePermit'] = response.xpath('//*[@id="JianzYDGHXKZH"]/text()').extract_first('')
        project['CertificateOfUseOfStateOwnedLand'] = response.xpath('//*[@id="TuDsyqzh"]/text()').extract_first('')
        project['BuildingPermit'] = response.xpath('//*[@id="JianZghxkzh"]/text()').extract_first('')
        project['ConstructionPermitNumber'] = response.xpath('//*[@id="ShiGxkzh"]/text()').extract_first('')
        project['PresalePermitNumber'] = response.xpath('//*[@id="shangPfysxkz"]/text()').extract_first('')
        project['QualificationNumber'] = response.xpath('//*[@id="KaiFQYZZ"]/text()').extract_first('')

        project['Developer'] = response.xpath('//*[@id="KaiFs"]/text()').extract_first('')
        project['Contact'] = response.xpath('//*[@id="LianXdh"]/text()').extract_first('')
        project['PresaleRegistrationManagementDepartment'] = response.xpath('//*[@id="shiqs"]/text()').extract_first('')

        result.append(project)
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
        result = list(result)
        print('BuildingListHandleMiddleware')
        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')

        tr_arr = response.xpath('//div[@class="tabls"]/table[last()]/tr')
        for tr in tr_arr[1:]:
            building = BuildingInfoItem()
            building['ProjectUUID'] = ProjectUUID
            building['ProjectName'] = ProjectName

            urltext = tr.xpath('./td[1]/a/@onclick').extract_first('')
            c = regex.search("\('(?<url>.*)'\)", urltext)
            if c:
                url = urlparse.urljoin(response.url, c.group(1))
                param = getParamsDict(url)
                building['SourceUrl'] = url
                building['BuildingID'] = param.get('houseDengJh', '')
                building['BuildingName'] = tr.xpath('/td[1]/a/text()').extract_first('')
                building['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                      ProjectUUID + building['BuildingID'] + building['BuildingName'])

                building['BuildingStructure'] = tr.xpath('/td[2]/text()').extract_first('')
                building['Floors'] = tr.xpath('/td[3]/text()').extract_first('')
                building['HousingCount'] = tr.xpath('/td[4]/text()').extract_first('')
                result.append(building)
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
        def get_house_state(key):
            state_dict = {
                '#CCFFFF': '未销售',
                '#FF0000': '已网上销售',
                '#FFFF00': '已抵押',
                '#CC0099': '已查封',
                '#000000': '限制出售',
                '#FFFFFF': '状态不明',
            }
            return state_dict.get(key, '')

        if not (200 <= response.status < 300):
            return result if result else []
        if response.meta.get('PageType') not in ('HouseList', 'HouseInfoDetail'):
            return result if result else []
        result = list(result)
        if response.meta.get('PageType') == 'HouseList':
            print('HouseListHandleMiddleware')
            ProjectUUID = response.meta.get('ProjectUUID')
            ProjectName = response.meta.get('ProjectName')
            BuildingUUID = response.meta.get('BuildingUUID')
            BuildingName = response.meta.get('BuildingName')
            tr_arr = response.xpath('//div[@class="xinjia"]/table/tr')
            for tr in tr_arr[1:]:
                td_arr = tr.xpath('./td[@bgcolor]')
                for td in td_arr:
                    house = HouseInfoItem()
                    house['ProjectUUID'] = ProjectUUID
                    house['ProjectName'] = ProjectName
                    house['BuildingUUID'] = BuildingUUID
                    house['BuildingName'] = BuildingName

                    house['BuildingNumber'] = tr.xpath('./td[1]/text()').extract_first('')
                    house['UnitName'] = tr.xpath('./td[2]/text()').extract_first('')
                    house['FloorName'] = tr.xpath('./td[3]/text()').extract_first('')
                    house['HouseName'] = td.xpath('./a/text() |./text()')

                    house['HouseUrl'] = td.xpath(
                        './a/@href | ./font/a/@href').extract_first('')
                    house['HouseName'] = td.xpath(
                        './a/text() | ./font/a/text()').extract_first('')

                    house['HouseState'] = get_house_state(td.xpath('@bgcolor').extract_first(''))
                    house['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                    house['ProjectName'] +
                                                    house['BuildingName'] +
                                                    house['BuildingNumber'] +
                                                    house['UnitName'] +
                                                    house['HouseName'])

                    parmam = getParamsDict(house['HouseUrl'])
                    if parmam.get('gid') == '00000000-0000-0000-0000-000000000000':
                        result.append(house)
                    else:
                        result.append(Request(url=house['HouseUrl'], method='GET', headers={
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'zh-CN,zh;q=0.9',
                            'Cache-Control': 'max-age=0',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                        },
                                              meta={'PageType': 'HouseInfoDetail', 'item': house}))
        elif response.meta.get('PageType') == 'HouseInfoDetail':
            # 暂时未遇到改版后能访问的url,2018-06-08
            hinfo = response.meta.get('item')
            if hinfo:
                hinfo['House_located'] = response.xpath(
                    '//tr[1]/td[2]/text()').extract_first(default='').strip()
                hinfo['Pre_sale_license_number'] = response.xpath(
                    '//tr[2]/td[2]/text()').extract_first(default='').strip()
                hinfo['Predicted_area'] = response.xpath(
                    '//tr[3]/td[2]/text()').extract_first(default='').strip()
                hinfo['Measured_area'] = response.xpath(
                    '//tr[4]/td[2]/text()').extract_first(default='').strip()
                hinfo['Record_unit_price'] = urlparse.urljoin(response.url, response.xpath(
                    '//tr[5]/td[2]/img/@src').extract_first(default='').strip())
                result.append(hinfo)

        return result
