# coding = utf-8
import logging
import uuid

import regex
from HouseCrawler.Items.ItemsNT import *
from scrapy import Request

logger = logging.getLogger(__name__)

debug = False


def get_projectState(string):
    state_arr = {'NewEstate': '新盘', 'newestate': '新盘', 'SoldOutEstate': '售罄', 'HotEstate': '热销', 'LateEstate': '尾盘', }
    return state_arr.get(string,'')


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
                logger.info('debuging...')
                return 1
            try:
                t = response.xpath('//a[starts-with(@href,"/house/_______")][last()-1]/span/text()').extract_first()
                total_page = int(t)
            except Exception:
                pass
            return total_page

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectBase':
            return result if result else []
        # print('ProjectBaseHandleMiddleware')
        curPage = response.meta.get('curPage')
        if curPage and curPage == 1:
            total_page = get_totla_page(response)
            for page in range(1, total_page + 1):
                url = 'http://newhouse.ntfdc.net/house/' if page == 1 else 'http://newhouse.ntfdc.net/house/_______{curPage}/'.format(
                    curPage=page)
                base_req = Request(url=url,
                                   headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                   dont_filter=True,
                                   meta={'PageType': 'ProjectBase'})
                result.append(base_req)
        else:
            li_arr = response.xpath('//div[@class="lplist"]/ul/li')

            for li in li_arr:
                # 获取列表每一行信息
                projectBaseItem = ProjectBaseItem()
                href = 'http://newhouse.ntfdc.net' + li.xpath('./div[1]/a/@href').extract_first()
                projectBaseItem['SourceUrl'] = href
                projectBaseItem['ProjectName'] = li.xpath('./div[1]/a/text()').extract_first()
                projectBaseItem['OnSaleState'] = get_projectState(li.xpath('./div[1]/img/@alt').extract_first())
                projectBaseItem['LandUse'] = li.xpath('./div[1]/span/text()').extract_first()
                projectBaseItem['Selltel'] = li.xpath('./div[2]/strong/text()').extract_first()
                Developer_text = li.xpath('./div[3]/text()').extract_first()
                if Developer_text:
                    Developer_text = Developer_text.replace('开发商：', '')
                projectBaseItem['Developer'] = Developer_text
                price_text = li.xpath('./div[6]/span/text()').extract_first()
                if price_text and price_text != '待定':
                    price_text = price_text + '元/㎡'
                projectBaseItem['ReferencePrice'] = price_text
                projectBaseItem['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, href)
                result.append(projectBaseItem)

                # 获取项目信息
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
        def remove_html_tag(string):
            try:
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
        projectInfoItem = ProjectInfoItem()
        projectInfoItem['SourceUrl'] = response.url
        projectInfoItem['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, projectInfoItem['SourceUrl'])
        projectInfoItem['ProjectName'] = response.xpath('//div[@class="house_name"]/h3/text()').extract_first()
        string = response.xpath('//div[@class="house_name"]/div/img/@alt').extract_first()
        projectInfoItem['OnSaleState'] = get_projectState(string)
        projectInfoItem['LandUse'] = response.xpath('//div[@class="house_name"]/div[2]/text()').extract_first()
        projectInfoItem['RecordName'] = response.xpath('//strong[text()="备 案 名："]/../text()').extract_first()
        projectInfoItem['Decoration'] = response.xpath('//strong[text()="装修状态："]/../text()').extract_first()
        projectInfoItem['HousingCount'] = response.xpath('//strong[text()="规划户数："]/../text()').extract_first()
        projectInfoItem['Developer'] = response.xpath('//strong[text()="开 发 商："]/../text()').extract_first()
        projectInfoItem['DistrictName'] = response.xpath('//strong[text()="所属区域："]/../div[1]/text()').extract_first()
        projectInfoItem['ProjectAddress'] = response.xpath('//strong[text()="项目地址："]/../text()').extract_first()
        projectInfoItem['ApprovalPresaleAmount'] = response.xpath(
            '//strong[text()="批准预售总套数:"]/../div[1]/text()').extract_first()
        projectInfoItem['HousingOnsoldAmount'] = response.xpath(
            '//strong[text()="住宅可售套数："]/../div[1]/text()').extract_first()
        projectInfoItem['ReferencePrice'] = response.xpath('//strong[text()="参考均价："]/../span[1]/text()').extract_first()
        projectInfoItem['EarliestOpeningTime'] = response.xpath('//strong[text()="开盘时间："]/../text()').extract_first()
        projectInfoItem['LatestDeliversHouseDate'] = response.xpath(
            '//strong[text()="交房时间："]/../text()').extract_first()
        projectInfoItem['FloorArea'] = response.xpath('//strong[text()="占地面积："]/../text()').extract_first()
        projectInfoItem['TotalBuidlingArea'] = response.xpath('//strong[text()="建筑面积："]/../text()').extract_first()
        projectInfoItem['FloorAreaRatio'] = response.xpath('//strong[text()="容 积 率："]/../text()').extract_first()
        projectInfoItem['GreeningRate'] = response.xpath('//strong[text()="绿 化 率："]/../div[1]/text()').extract_first()
        projectInfoItem['ManagementFees'] = response.xpath('//strong[text()="物 业 费："]/../text()').extract_first()
        projectInfoItem['ManagementCompany'] = response.xpath(
            '//strong[text()="物业管理："]/../div[1]/text()').extract_first()
        projectInfoItem['BuildingType'] = response.xpath('//strong[text()="建筑类别："]/../text()').extract_first()
        projectInfoItem['ProjectSellAddress'] = response.xpath(
            '//strong[text()="售楼处地址："]/../div[1]/text()').extract_first()
        projectInfoItem['SalesAgent'] = response.xpath('//strong[text()="销售代理："]/../text()').extract_first()
        projectInfoItem['ConstructionUnit'] = response.xpath('//strong[text()="施工单位："]/../text()').extract_first()
        projectInfoItem['ProjectIntro'] = response.xpath('//li[text()="项目情况"]/@data-value').extract_first()
        projectInfoItem['ProjectAroundSupporting'] = response.xpath('//li[text()="周边配套"]/@data-value').extract_first()
        projectInfoItem['TrafficSituation'] = response.xpath('//li[text()="交通情况"]/@data-value').extract_first()
        projectInfoItem['DecorationInfo'] = response.xpath('//li[text()="装修情况"]/@data-value').extract_first()
        projectInfoItem['DeveloperIntro'] = response.xpath('//li[text()="开发商介绍"]/@data-value').extract_first()
        projectInfoItem['AboutInfo'] = response.xpath('//li[text()="相关信息"]/@data-value').extract_first()
        result.append(projectInfoItem)

        # 获取销售许可证
        url = 'http://newhouse.ntfdc.net' + response.xpath('//li/a[text()="销售许可证"]/@href').extract_first()
        presell_req = Request(url=url,
                              headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                              dont_filter=True,
                              meta={'PageType': 'PresellInfo',
                                    'ProjectUUID': str(projectInfoItem['ProjectUUID']),
                                    'ProjectName': projectInfoItem['ProjectName'],
                                    })
        result.append(presell_req)
        # 获取楼栋列表
        buildingList_href = 'http://newhouse.ntfdc.net' + response.xpath('//li/a[text()="销售公示"]/@href').extract_first()
        buildingList_req = Request(
            url=buildingList_href,
            headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
            dont_filter=True,
            meta={
                'PageType': 'BuildingList',
                'ProjectUUID': str(projectInfoItem['ProjectUUID']),
                'ProjectName': projectInfoItem['ProjectName'],
            })
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
        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'PresellInfo':
            return result if result else []
        # print('PresellInfoHandleMiddleware')
        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')
        tr_arr = response.xpath('//div[@class="house_salestrends"]/following-sibling::div[1]/table/tr')
        if len(tr_arr) > 1:
            for tr in tr_arr[1:]:
                presellItem = PresellInfoItem()
                presellItem['ProjectUUID'] = ProjectUUID
                presellItem['ProjectName'] = ProjectName
                presellItem['PresalePermitNumber'] = tr.xpath('./td[1]/text()').extract_first()
                presellItem['PresellUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                        ProjectUUID + presellItem['PresalePermitNumber'])
                presellItem['ApprovalPresaleArea'] = tr.xpath('./td[2]/text()').extract_first()
                presellItem['ApprovalPresaleBuildingName'] = tr.xpath('./td[3]/text()').extract_first()
                presellItem['Price'] = tr.xpath('./td[4]/text()').extract_first()
                presellItem['LssueDate'] = tr.xpath('./td[5]/text()').extract_first()
                result.append(presellItem)
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
        # print('BuildingListHandleMiddleware')
        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')
        dt_arr = response.xpath('//dt[starts-with(text(),"预售许可证号")]')
        for dt in dt_arr:
            dt_text = dt.xpath('text()').extract_first()
            PresalePermitNumber = dt_text[7:] if dt_text else ''
            a_arr = dt.xpath('./following-sibling::dd/a')
            for a in a_arr:
                buildingInfoItem = BuildingInfoItem()
                buildingInfoItem['ProjectUUID'] = ProjectUUID
                buildingInfoItem['ProjectName'] = ProjectName
                buildingInfoItem['PresalePermitNumber'] = PresalePermitNumber
                buildingInfoItem['BuildingName'] = a.xpath('text()').extract_first()
                href = 'http://newhouse.ntfdc.net' + a.xpath('@href').extract_first()
                buildingInfoItem['SourceUrl'] = href
                buildingInfoItem['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, href)
                result.append(buildingInfoItem)

                # houseList_req = Request(url=href,
                #                         headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                #                         dont_filter=True,
                #                         meta={
                #                             'PageType': 'HouseList',
                #                             'ProjectUUID': ProjectUUID,
                #                             'ProjectName': ProjectName,
                #                             'BuildingUUID': str(buildingInfoItem['BuildingUUID']),
                #                         })
                # result.append(houseList_req)
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
        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')
        BuildingUUID = response.meta.get('BuildingUUID')
        div_arr = response.xpath('//div[@class="line"]')
        for div in div_arr:
            FloorName = div.xpath('./div[1]/text()').extract_first()
            a_arr = div.xpath('./div[2]/div/a')
            for a in a_arr:
                onclick = a.xpath('@onclick').extract_first()
                try:
                    t = regex.search(r"open\('(?<url>.+)','','", onclick)
                    href = 'http://newhouse.ntfdc.net' + t.group(1)
                    houseInfo_req = Request(url=href,
                                            headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                            dont_filter=True,
                                            meta={
                                                'PageType': 'HouseInfo',
                                                'ProjectUUID': ProjectUUID,
                                                'ProjectName': ProjectName,
                                                'BuildingUUID': BuildingUUID,
                                                'FloorName': FloorName
                                            })
                    result.append(houseInfo_req)
                    house_base = {
                        'source_url': href,
                        'meta': {
                            'PageType': 'HouseInfo',
                            'ProjectUUID': ProjectUUID,
                            'ProjectName': ProjectName,
                            'BuildingUUID': BuildingUUID,
                            'FloorName': FloorName
                        }
                    }
                    # house_base_json = json.dumps(house_base, sort_keys=True)
                    # r.sadd(self.settings.get('REDIS_KEY'), house_base_json)
                    result.append(Request(house_base.get('source_url'), meta=house_base.get('meta')))
                except:
                    pass
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
        FloorName = response.meta.get('FloorName')

        houseInfoItem = HouseInfoItem()
        houseInfoItem['SourceUrl'] = response.url
        houseInfoItem['ProjectUUID'] = ProjectUUID
        houseInfoItem['ProjectName'] = ProjectName
        houseInfoItem['BuildingUUID'] = BuildingUUID
        houseInfoItem['FloorName'] = FloorName
        houseInfoItem['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, houseInfoItem['SourceUrl'])

        houseInfoItem['BuildingName'] = response.xpath('//table/tr[3]/td[2]/text()').extract_first()
        houseInfoItem['HouseNumber'] = response.xpath('//table/tr[3]/td[4]/text()').extract_first()
        houseInfoItem['MeasuredBuildingArea'] = response.xpath('//table/tr[4]/td[2]/text()').extract_first()
        houseInfoItem['MeasuredInsideOfBuildingArea'] = response.xpath('//table/tr[4]/td[4]/text()').extract_first()
        houseInfoItem['MeasuredSharedPublicArea'] = response.xpath('//table/tr[5]/td[2]/text()').extract_first()
        houseInfoItem['HouseState'] = response.xpath('//table/tr[5]/td[4]/text()').extract_first()
        houseInfoItem['HouseUseType'] = response.xpath('//table/tr[6]/td[2]/text()').extract_first()
        houseInfoItem['UnitShape'] = response.xpath('//table/tr[6]/td[4]/text()').extract_first()
        houseInfoItem['TotalPrice'] = response.xpath('//table/tr[7]/td[2]/text()').extract_first()

        result.append(houseInfoItem)
        return result
