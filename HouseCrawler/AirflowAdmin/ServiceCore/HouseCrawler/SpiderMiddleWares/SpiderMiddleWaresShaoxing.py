# coding = utf-8
import logging
import sys
import uuid
import regex
import time

from HouseCrawler.Items.ItemsShaoxing import *
from scrapy import Request

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
logger = logging.getLogger(__name__)

debug = False


def get_project_state(src):
    img_dict = {
        '/content/images/icon_selling.gif': '在售',
        '/content/images/shouwan.gif': '售完',
        '/content/images/daishou.gif': '待售',
    }
    try:
        return img_dict[src]
    except:
        return ''




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
            try:
                t = response.xpath('//*[@id="ctl00_ConBody_List1_lblPage"]/div/div[2]/a[last()]/text()').extract_first()
                total_page = int(t)
            except:
                import traceback
                traceback.print_exc()
            if debug:
                return 1
            return total_page

        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectBase':
            return result if result else []
        # print('ProjectBaseHandleMiddleware')
        result = list(result)
        curPage = response.meta.get('curPage')
        if curPage and curPage == 1:
            total_page = get_totla_page(response)
            for page in range(1, total_page + 1):

                req = Request(url='http://www.sxhouse.com.cn/loupan/list.aspx?t=&tm=&regioncode=&hk=&price=&page={curPage}&odb=&k=&vid='.format(curPage=page),
                              headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                dont_filter=True,
                                meta={'PageType': 'ProjectBase'})
                result.append(req)

        else:
            div_arr = response.xpath('//ul[@class="h-list h-list-full newhouse-list"]/li/div')
            for div in div_arr:
                projectBaseItem = ProjectBaseItem()
                projectBaseItem['ProjectName'] = div.xpath('./div/a/h5/text()').extract_first()
                projectBaseItem['OnSaleState'] = get_project_state(div.xpath('./div/a/h5/img/@src').extract_first())

                p_arr = div.xpath('div[last()]/p')
                if len(p_arr) == 1:
                    AveragePrice = p_arr[0].xpath('em/text()').extract_first()
                    projectBaseItem['AveragePrice'] = AveragePrice if AveragePrice else ''
                elif len(p_arr) == 2:
                    try:
                        count_text = p_arr[0].xpath('em/text()').extract_first()
                        count_text_arr = count_text.split('/')
                        projectBaseItem['OnsoldAmount'] = count_text_arr[0]
                        projectBaseItem['ApprovalPresaleAmount'] = count_text_arr[1]
                    except:
                        pass
                    AveragePrice = p_arr[1].xpath('em/text()').extract_first()
                    projectBaseItem['AveragePrice'] = AveragePrice if AveragePrice else ''
                url = div.xpath('div[1]/a/@href').extract_first()
                if url:
                    url = 'http://www.sxhouse.com.cn' + url
                    projectBaseItem['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, url)
                    projectBaseItem['SourceUrl'] = url
                    result.append(projectBaseItem)
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
        result = list(result)
        # print('ProjectInfoHandleMiddleware')
        projectInfoItem = ProjectInfoItem()
        projectInfoItem['SourceUrl'] = response.url
        projectInfoItem['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, projectInfoItem['SourceUrl'])
        projectInfoItem['ProjectName'] = response.xpath(
            '//th[starts-with(text(),"楼盘名称")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['Developer'] = response.xpath(
            '//th[starts-with(text(),"开发商")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['DistrictName'] = response.xpath(
            '//th[starts-with(text(),"所在区域")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['AreaRange'] = response.xpath(
            '//th[starts-with(text(),"面积范围")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['FloorArea'] = response.xpath(
            '//th[starts-with(text(),"占地面积")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['TotalBuidlingArea'] = response.xpath(
            '//th[starts-with(text(),"建筑面积")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['PriceStart'] = response.xpath(
            '//th[starts-with(text(),"起")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['EarliestOpeningTime'] = response.xpath(
            '//th[starts-with(text(),"开盘时间")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['AveragePrice'] = response.xpath(
            '//th[starts-with(text(),"均")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['GreeningRate'] = response.xpath(
            '//th[starts-with(text(),"绿化率")]/following-sibling::td[1]/text()').extract_first()
        src = response.xpath('//th[starts-with(text(),"销售状态")]/following-sibling::td[1]/img/@src').extract_first()
        projectInfoItem['OnSaleState'] = get_project_state(src)
        projectInfoItem['FloorAreaRatio'] = response.xpath(
            '//th[starts-with(text(),"容积率")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['LandUse'] = response.xpath(
            '//th[starts-with(text(),"物业类型")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['ParkingSpaceAmount'] = response.xpath(
            '//th[starts-with(text(),"车")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['FloorCondition'] = response.xpath(
            '//th[starts-with(text(),"楼层状况")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['PresalePermitNumber'] = response.xpath(
            '//th[starts-with(text(),"预售证")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['Contacts'] = response.xpath(
            '//th[starts-with(text(),"联系人")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['Selltel'] = response.xpath(
            '//b[starts-with(text(),"售楼热线")]/../following-sibling::td[1]/b/text()').extract_first()
        projectInfoItem['ManagementCompany'] = response.xpath(
            '//th[starts-with(text(),"物业公司")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['SellAddress'] = response.xpath(
            '//th[starts-with(text(),"售楼地址")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['DecorationCondition'] = response.xpath(
            '//th[starts-with(text(),"装修状况")]/following-sibling::td[1]/text()').extract_first()
        projectInfoItem['ProjectAddress'] = response.xpath(
            '//th[starts-with(text(),"详细地址")]/following-sibling::td[1]/text()').extract_first()
        ProjectIntro = response.xpath('//h3[contains(text(),"楼盘简介")]/following-sibling::div[1]').re(r'.*')
        projectInfoItem['ProjectIntro'] = remove_html_tag(ProjectIntro)
        TrafficSituation = response.xpath('//h3[contains(text(),"交通")]/following-sibling::div[1]').re(r'.*')
        projectInfoItem['TrafficSituation'] = remove_html_tag(TrafficSituation)
        ProjectSupporting = response.xpath('//h3[contains(text(),"周边配套")]/following-sibling::div[1]').re(r'.*')
        projectInfoItem['ProjectSupporting'] = remove_html_tag(ProjectSupporting)
        result.append(projectInfoItem)
        try:
            url = response.url
            hid = url[url.rindex('/') + 1:url.rindex('.')]
            source_url = 'http://www.sxhouse.com.cn/com/ajaxpage/ajaxnewhousesall.aspx?hid={hid}&refreshtime={timestamp}'.format(
                hid=hid, timestamp=round(time.time() * 1000))
            buildingList_req = Request(url=source_url,
                                       headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                       dont_filter=True,
                                       meta={
                                           'PageType': 'BuildingList',
                                           'ProjectUUID': str(projectInfoItem['ProjectUUID']),
                                           'ProjectName': projectInfoItem['ProjectName']
                                       })
            result.append(buildingList_req)
        except:
            pass
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
        # print('BuildingListHandleMiddleware')
        result = list(result)

        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')

        li_arr = response.xpath('//input[@value="销售情况"]/../..')
        for li in li_arr:
            buildingItem = BuildingInfoItem()
            buildingItem['ProjectUUID'] = ProjectUUID
            buildingItem['ProjectName'] = ProjectName

            onclick = li.xpath('span/input/@onclick').extract_first()
            text = li.xpath('p/text()').extract_first()
            try:
                t = regex.search(r'showHistoryCJ\((?<pid>.+),(?<hid>.+),(?<sectionID>.+)\)', onclick)
                url = 'http://www.sxhouse.com.cn/Loupan/saledetail.aspx?pid={pid}&hid={hid}&sectionID={sectionID}' \
                    .format(pid=t.group(1), hid=t.group(2), sectionID=t.group(3))
                buildingItem['BuildingURL'] = url
                buildingItem['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, ProjectUUID + url)
                arr = text.split(' ')
                buildingItem['BuildingName'] = arr[0]
                buildingItem['ApprovalPresaleAmount'] = arr[1][1:-1]
                buildingItem['SoldAmount'] = arr[2][3:-1]
                buildingItem['OnsoldAmount'] = arr[3][3:-1]
                buildingItem['LimitAmount'] = arr[4][3:arr[4].index('套')]
                result.append(buildingItem)

                houseList_req = Request(url = buildingItem['BuildingURL'],
                                        headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                        dont_filter=True,
                                        meta={
                                            'PageType': 'HouseList',
                                            'ProjectUUID': ProjectUUID,
                                            'BuildingUUID': str(buildingItem['BuildingUUID']),
                                            'ProjectName': buildingItem['ProjectName'],
                                            'BuildingName': buildingItem['BuildingName'],
                                        })
                result.append(houseList_req)

            except:
                pass
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
        def get_house_state(color):
            colors = {'#66ff66': '未售', '#0033ff': '预定', '#ff0000': '已售', '#ffff66': '售中或锁定',
                      '#990000': '按揭/抵押', '#666666': '不可售', '#0099ff': '附房'}
            try:
                return colors[color.lower()]
            except:
                return ''

        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'HouseList':
            return result if result else []
        result = list(result)
        # print('HouseListHandleMiddleware')

        ProjectUUID = response.meta.get('ProjectUUID')
        BuildingUUID = response.meta.get('BuildingUUID')
        ProjectName = response.meta.get('ProjectName')
        BuildingName = response.meta.get('BuildingName')

        tr_arr = response.xpath('//div[@class="floordetail"]/table/tbody/tr')
        for tr in tr_arr[1:]:
            ActualFloor = tr.xpath('./td[1]/text()').extract_first()
            td_arr = tr.xpath('./td[2]/table/tbody/tr/td')
            for td in td_arr:
                houseInfoItem = HouseInfoItem()
                houseInfoItem['ProjectUUID'] = ProjectUUID
                houseInfoItem['BuildingUUID'] = BuildingUUID
                houseInfoItem['ProjectName'] = ProjectName
                houseInfoItem['BuildingName'] = BuildingName
                color = td.xpath('./@bgcolor').extract_first()
                houseInfoItem['HouseState'] = get_house_state(color)
                houseInfoItem['ActualFloor'] = ActualFloor
                # 判断是否有链接
                href = td.xpath('./a/@href').extract_first()
                if href:
                    t = regex.search(
                        r"showRoom\('(?<houseNO>.+)','0','1','(?<BuildingStructure>.+)','(?<ActualFloor>.+)','(?<FloorName>.+)','(?<HouseUseType>.+)','(?<MeasuredBuildingArea>.+)','(?<MeasuredInsideOfBuildingArea>.+)','(?<MeasuredSharedPublicArea>.+)','(?<HouseSalePrice>.+)','(?<HouseSalePriceUpdateTime>.+)'\)",
                        href)
                    if t is None:
                        return result
                    houseInfoItem['HouseNO'] = t.group(1)
                    houseInfoItem['BuildingStructure'] = t.group(2)
                    houseInfoItem['ActualFloor'] = t.group(3)
                    houseInfoItem['FloorName'] = t.group(4)
                    houseInfoItem['HouseUseType'] = t.group(5)
                    houseInfoItem['MeasuredBuildingArea'] = t.group(6)
                    houseInfoItem['MeasuredInsideOfBuildingArea'] = t.group(7)
                    houseInfoItem['MeasuredSharedPublicArea'] = t.group(8)
                    houseInfoItem['HouseSalePrice'] = t.group(9) if t.group(9) == '0' else t.group(9) + '元/㎡'
                    houseInfoItem['HouseSalePriceUpdateTime'] = t.group(10)
                    url = 'http://www.sxhouse.com.cn/Loupan/room.aspx?rn={HouseNO}&state=0&sg=1&rs={BuildingStructure}&cf={ActualFloor}&nf={FloorName}&bs={HouseUseType}&ra={MeasuredBuildingArea}&rr={MeasuredInsideOfBuildingArea}&rb={MeasuredSharedPublicArea}&Rpc={HouseSalePrice}&pupd={HouseSalePriceUpdateTime}'
                    url = url.format(
                        HouseNO=houseInfoItem['HouseNO'],
                        BuildingStructure=urlparse.quote(houseInfoItem['BuildingStructure']),
                        ActualFloor=houseInfoItem['ActualFloor'],
                        FloorName=houseInfoItem['FloorName'],
                        HouseUseType=urlparse.quote(houseInfoItem['HouseUseType']),
                        MeasuredBuildingArea=houseInfoItem['MeasuredBuildingArea'],
                        MeasuredInsideOfBuildingArea=houseInfoItem['MeasuredInsideOfBuildingArea'],
                        MeasuredSharedPublicArea=houseInfoItem['MeasuredSharedPublicArea'],
                        HouseSalePrice=houseInfoItem['HouseSalePrice'],
                        HouseSalePriceUpdateTime=houseInfoItem['HouseSalePriceUpdateTime'])
                    houseInfoItem['SourceUrl'] = url
                else:
                    title = td.xpath('./b/@title').extract_first()
                    HouseNO = td.xpath('./b/text()').extract_first()
                    if title:
                        title = title.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
                        t = regex.search(r'建筑面积：(?<a1>.+)套内面积：(?<a2>.+)分摊面积：(?<a3>.+)', title)
                        houseInfoItem['MeasuredBuildingArea'] = t.group(1)
                        houseInfoItem['MeasuredInsideOfBuildingArea'] = t.group(2)
                        houseInfoItem['MeasuredSharedPublicArea'] = t.group(3)
                    houseInfoItem['HouseNO'] = HouseNO
                houseInfoItem['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                        BuildingUUID + houseInfoItem['ActualFloor'] + houseInfoItem[
                                                            'HouseNO'])
                result.append(houseInfoItem)
        return result