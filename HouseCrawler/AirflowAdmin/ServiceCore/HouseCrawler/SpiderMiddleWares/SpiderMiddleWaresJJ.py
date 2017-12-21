# coding = utf-8
import re
import sys
import uuid
import copy
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsJJ import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


def get_url_id(strUrl):
    res_id = '0'
    match_res = re.search(r'pid=(\d+)', str(strUrl))
    if match_res:
        res_id = match_res.group(1)
    return res_id


def get_url_sid(strUrl):
    res_id = '0'
    match_res = re.search(r'sid=(\d+)', str(strUrl))
    if match_res:
        res_id = match_res.group(1)
    return res_id


def get_building_href(string1, string2):
    building_url_base = 'http://www.jjzzfdc.com.cn/WebClient/ClientService/bldg_query.aspx?'
    req_dict = {'sid': '',
                'pid': ''}
    match_sid = re.search(r"javascript:queryBySid\('\" \+ (\d+) \+ \"'", str(string1))
    match_pid = re.search(r'pid=(\d+)', str(string2))
    if match_sid and match_pid:
        req_dict['sid'] = match_sid.group(1)
        req_dict['pid'] = match_pid.group(1)
        return building_url_base + urlparse.urlencode(req_dict)
    return None


def get_total_page(string):
    total_page = 0
    try:
        search_result = re.search(r'/(\d+)页',
                                        str(string))
        if search_result:
            total_page = int(search_result.group(1))
    except Exception:
        import traceback
        traceback.print_exc()
    return total_page


class ProjectBaseHandleMiddleware(object):
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
        if response.meta.get('PageType') not in ('ProjectBase', 'ProjectList'):
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectBase':
            project_list = sel.xpath('//tr[td[img]]')
            for p in project_list:
                p_id = get_url_id(p.xpath('./td[2]/b/a/@href').extract_first() or '')
                p_name = p.xpath('./td[2]/b/a/text()').extract_first() or ''
                p_href = urlparse.urljoin(response.url,
                                            p.xpath('./td[2]/b/a/@href').extract_first() or '')
                p_description = ''.join(p.xpath('./td[2]/text()').extract()).strip()
                pb = ProjectBaseItem()
                pb['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + p_id)
                pb['ProjectName'] = p_name
                pb['ProjectURL'] = p_href
                pb['ProjectDescription'] = p_description
                result.append(pb)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class ProjectInfoHandleMiddleware(object):
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
        if response.meta.get('PageType') not in ('ProjectInfo', ):
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectInfo':
            pinfo = ProjectInfoItem()
            pinfo['ProjectName'] = (sel.xpath('//td[font[text()="项目名称"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                    pinfo['ProjectName'] + get_url_id(response.url))
            pinfo['ProjectCompany'] = (sel.xpath('//td[font[text()="开 发 商"]]/following-sibling::td[1]/a/font/text()').extract_first() or '').strip()
            pinfo['ProjectAddress'] = (sel.xpath('//td[font[text()="项目地点"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectUsage'] = (sel.xpath('//td[font[text()="项目性质"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectArea'] = (sel.xpath('//td[font[text()="用地面积"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectBuildArea'] = (sel.xpath('//td[font[text()="总建筑面积"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectRongjiRatio'] = (sel.xpath('//td[font[text()="容积率（%）"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectLvdiRatio'] = (sel.xpath('//td[font[text()="绿化率（%）"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectInvestment'] = (sel.xpath('//td[font[text()="总投资（万元）"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectBuildDate'] = (sel.xpath('//td[font[text()="开工日期"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectBuildingCompany'] = (sel.xpath('//td[font[text()="施工单位"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectManageCompany'] = (sel.xpath('//td[font[text()="物业管理"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectDesignCompany'] = (sel.xpath('//td[font[text()="设计单位"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            result.append(pinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class BuildingListHandleMiddleware(object):
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
        if response.meta.get('PageType') not in ('ProjectInfo', 'BuildingInfo'):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectInfo':
            p_name = (sel.xpath('//td[font[text()="项目名称"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
            p_id = get_url_id(response.url)
            building_list = sel.xpath('//table[@id="table588"]/tr[@class]')
            for b in building_list:
                b_info = BuildingInfoItem()
                b_info['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + p_id)
                b_info['ProjectName'] = p_name
                b_info['BuildingName'] = (b.xpath('./td[1]/text()').extract_first() or '').strip()
                b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                            b_info['BuildingName'] + p_id)
                b_info['BuildingRegName'] = (b.xpath('./td[2]/text()').extract_first() or '').strip()
                b_info['BuildingArea'] = (b.xpath('./td[3]/text()').extract_first() or '').strip()
                b_info['BuildingRegDate'] = (b.xpath('./td[4]/text()').extract_first() or '').strip()
                b_info['BuildingRegPrice'] = (b.xpath('./td[5]/text()').extract_first() or '').strip()
                b_info['BuildingSalingNum'] = (b.xpath('./td[6]/text()').extract_first() or '').strip()
                b_info['BuildingType'] = (b.xpath('./td[7]/text()').extract_first() or '').strip()
                b_info['BuildingSaleState'] = (b.xpath('./td[8]/text()').extract_first() or '').strip()
                building_info_url = get_building_href(b.xpath('./td[9]/script').extract_first() or '', response.url)
                if building_info_url:
                    result.append(Request(url=building_info_url, method='GET',
                                meta={'PageType': 'BuildingInfo', 'item': copy.deepcopy(b_info)}))
                else:
                    result.append(b_info)
        elif response.meta.get('PageType') == 'BuildingInfo':
            b_info = response.meta.get('item')
            if b_info:
                b_info['BuildingPlanAreaCode'] = (sel.xpath('//td[b[text()="用地规划"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingRegName'] = (sel.xpath('//td[b[text()="预售证号"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingPlanEngCode'] = (sel.xpath('//td[b[text()="工程规划"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingBuildEngCode'] = (sel.xpath('//td[b[text()="工程施工"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingAreaCode'] = (sel.xpath('//td[b[text()="国土证号"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingZZHouseNum'] = (sel.xpath('//td[b[text()="住宅套数"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingFZZHouseNum'] = (sel.xpath('//td[b[text()="非住宅套数"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingSalingNum'] = (sel.xpath('//td[b[text()="现可售套数"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingSoldNum'] = (sel.xpath('//td[b[text()="已售套数"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingZZUnitPrice'] = (sel.xpath('//td[b[text()="住宅销售均价"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingFZZUnitPrice'] = (sel.xpath('//td[b[text()="非住宅销售均价"]]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingURL'] = urlparse.urljoin('http://www.jjzzfdc.com.cn/WebClient/ClientService/',
                                            'proxp.aspx?key=WWW_LPB_001&params={sid}'.format(sid=get_url_sid(response.url)))
                b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                            str(b_info['BuildingUUID']) + str(b_info['BuildingURL']))
                result.append(b_info)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class HouseInfoHandleMiddleware(object):
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

        def get_house_state(string):
            STATE_TAB = {'#0033FF': '已公示',
                            '#FFFFFF': '不可售',
                            '#00FF00': '可售',
                            '#0099FF': '可现售',
                            '#C4A93C': '已销售上报',
                            '#F3F394': '已定',
                            '#99CC00': '已签,公租已签',
                            '#CC99FF': '公租备案(完全),备案,公租备案',
                            '#FFCC99': '在建工程抵押,工程最高额',
                            '#AAAAAA': '共管房'}
            state = ''
            for key in STATE_TAB:
                if key == string:
                    state = STATE_TAB[key]
                    break
            return state

        def get_project_unitprice(BuildingUUID, houseTime=str(datetime.datetime.now())):

            result = 0.0
            timebase = datetime.datetime.strptime(houseTime, "%Y-%m-%d %H:%M:%S.%f")
            time_lowbound = str(timebase - datetime.timedelta(days=1))
            time_upbound = str(timebase + datetime.timedelta(days=1))
            cur_info = BuildingInfo.objects.filter(BuildingUUID=BuildingUUID,
                                                    CurTimeStamp__lt=time_upbound,
                                                    CurTimeStamp__gt=time_lowbound).\
                            latest('CurTimeStamp') or\
                        BuildingInfo.objects.filter(BuildingUUID=BuildingUUID).\
                            latest('CurTimeStamp')
            if cur_info:
                try:
                    cur_unit_price = float(cur_info.BuildingZZUnitPrice)
                    if cur_unit_price > 0:
                        result = cur_unit_price
                        return result
                except Exception:
                    pass
                try:
                    cur_unit_price = float(cur_info.BuildingFZZUnitPrice)
                    if cur_unit_price > 0:
                        result = cur_unit_price
                        return result
                except Exception:
                    pass
            return result

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseInfo', ):
            if result:
                return result
            return []
        print('HouseInfoHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'HouseInfo':
            if (not response.meta.get('ProjectName')) or (not response.meta.get('BuildingName'))\
            or (not response.meta.get('ProjectUUID')) or (not response.meta.get('BuildingUUID')):
                if result:
                    return result
                return []
            houseinfodetail_list = sel.xpath('//Result')
            for house in houseinfodetail_list:
                hinfo = HouseInfoItem()
                hinfo['ProjectName'] = response.meta.get('ProjectName')
                hinfo['BuildingName'] = response.meta.get('BuildingName')
                hinfo['ProjectUUID'] = response.meta.get('ProjectUUID')
                hinfo['BuildingUUID'] = response.meta.get('BuildingUUID')
                hinfo['HouseName'] = house.xpath('./ONAME/text()').extract_first() or ''
                hinfo['HouseOSEQ'] = house.xpath('./OSEQ/text()').extract_first() or ''
                hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                        hinfo['HouseName'] + hinfo['HouseOSEQ'] + str(hinfo['BuildingUUID']))
                hinfo['HouseFloor'] = house.xpath('./FORC/text()').extract_first() or ''
                hinfo['HouseKey'] = house.xpath('./KEY/text()').extract_first() or ''
                hinfo['HouseSTR_2'] = house.xpath('./STR_2/text()').extract_first() or ''
                hinfo['HouseSTR_3'] = house.xpath('./STR_3/text()').extract_first() or ''
                hinfo['HouseSTR_5'] = house.xpath('./STR_5/text()').extract_first() or ''
                hinfo['HouseSattribute'] = house.xpath('./SATTRIBUTE/text()').extract_first() or ''
                hinfo['HouseBuildingArea'] = house.xpath('./BAREA/text()').extract_first() or ''
                hinfo['HouseInnerArea'] = house.xpath('./PAREA/text()').extract_first() or ''
                hinfo['HouseSaleState'] = get_house_state(hinfo['HouseKey'])
                hinfo['HouseUnitPrice'] = str(get_project_unitprice(hinfo['BuildingUUID']))
                result.append(hinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
