# coding = utf-8
import re
import sys
import uuid
import copy
import json
import itertools
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsCQ import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse

headers = {'Host': 'www.cq315house.com',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': 1,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'}


def get_json(strRes):
    strRes = str(strRes).replace("'", '"').replace('\\', ' ')
    return json.loads(strRes)


def get_url_id(strUrl):
    res_id = '0'
    match_res = re.search(r'id=(\d+)', str(strUrl).lower())
    if match_res:
        res_id = match_res.group(1)
    return res_id


def get_href(strHref):
    res_href = ''
    match_res = re.search(r"'(.+)','_blank'", str(strHref))
    if match_res:
        res_href = match_res.group(1)
    return res_href


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
        if response.meta.get('PageType') not in ('ProjectBase', 'ProjectList', 'ProjectDetailInfo'):
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectBase':
            base_url = 'http://www.cq315house.com/315web/webservice/GetMyData999.ashx?'
            req_dict = {'projectname': '',
                        'site': '',
                        'kfs': '',
                        'projectaddr': '',
                        'pagesize': 99999,
                        'pageindex': 1,
                        'roomtype': '',
                        'buildarea': ''}
            sel = Selector(response)
            district_list = sel.xpath('//*[@id="ddlXzq"]/option[text()]/@value').extract()
            type_list = sel.xpath('//*[@id="ddlHouseType"]/option[text()]/@value').extract()
            for item in itertools.product(district_list, type_list):
                if item.count('') > 0:
                    continue
                req_dict['site'] = item[0]
                req_dict['roomtype'] = item[1]
                url = base_url + urlparse.urlencode(req_dict)
                result.append(Request(url=url, method='GET', dont_filter=True,
                                headers=headers, meta={'PageType': 'ProjectList'}))
        elif response.meta.get('PageType') == 'ProjectList':
            project_list = get_json(response.body_as_unicode())
            print('get project count', len(project_list))
            for p in project_list:
                p_href_base = 'http://www.cq315house.com/315web/webservice/GetMyData112.ashx?projectId=%s'
                p_href_detail = 'http://www.cq315house.com/315web/webservice/TJLJcjQuery1.ashx?'
                p_id = p.get('PARENTJECTID') or ''
                p_district = p.get('F_SITE') or ''
                p_name = p.get('ZPROJECT') or ''
                p_href = p_href_base % p_id
                p_address = p.get('F_ADDR') or ''
                p_company = p.get('ENTERPRISENAME') or ''
                req_dict = {'projectname': '',
                            'parprojectid': p_id,
                            'site': p_district,
                            'pagesize': 10,
                            'pageindex': 1}
                pb = ProjectBaseItem()
                pb['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + p_id)
                pb['ProjectName'] = p_name
                pb['ProjectDistrict'] = p_district
                pb['ProjectURL'] = p_href
                pb['ProjectAddress'] = p_address
                pb['ProjectCorporation'] = p_company
                result.append(Request(url=p_href_detail + urlparse.urlencode(req_dict), method='GET', dont_filter=True,
                                headers=headers, meta={'PageType': 'ProjectDetailInfo', 'item': pb}))
        elif response.meta.get('PageType') == 'ProjectDetailInfo':
            project_detail_list = get_json(response.body_as_unicode())
            pb = copy.deepcopy(response.meta.get('item'))
            if len(project_detail_list) > 0:
                project_detail = project_detail_list.pop()
                pb['ProjectBaseName'] = project_detail.get('F_PROJECT_NAME')
                pb['ProjectSoldNum'] = project_detail.get('CJ')
                pb['ProjectSoldArea'] = project_detail.get('MJ')
            result.append(pb)
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
        if response.meta.get('PageType') not in ('ProjectInfo', ):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfo':
            subp_list = get_json(response.body_as_unicode())
            for subp_info in subp_list:
                b_info_base = BuildingInfoItem()
                b_info_base['ProjectBaseName'] = subp_info.get('PARENTPROJNAME') or ''
                b_info_base['ProjectName'] = subp_info.get('F_PROJECT_NAME') or ''
                b_info_base['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                b_info_base['ProjectName'] + get_url_id(response.url))
                b_info_base['ProjectAddress'] = subp_info.get('F_ADDR') or ''
                b_info_base['ProjectCorporation'] = subp_info.get('F_ENTERPRISE_NAME') or ''
                b_info_base['BuildingRegName'] = subp_info.get('F_PRESALE_CERT') or ''
                b_info_base['BuildingRegHouseNum'] = subp_info.get('PRESALECOUNT') or ''
                b_info_base['BuildingRegArea'] = subp_info.get('PRESALEAREA') or ''
                b_name_list = (subp_info.get('F_BLOCK') or '').split()
                b_id_list = (subp_info.get('BUILDID') or '').split()
                for b_name, b_id in zip(b_name_list, b_id_list):
                    b_info = copy.deepcopy(b_info_base)
                    b_url_base = 'http://www.cq315house.com/315web/HtmlPage/ShowRoomsNew.aspx?'
                    b_info['BuildingName'] = b_name
                    b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                b_info['BuildingRegName'] + b_id)
                    req_dict = {'block': b_name, 'buildingid': b_id}
                    b_info['BuildingURL'] = b_url_base + urlparse.urlencode(req_dict)
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
            STATE_TAB = {'525316': '预定',
                            '524292': '可售',
                            '2621444': '已售',
                            '655360': '限制销售',
                            '2365461': '已登记'}
            state = ''
            for key in STATE_TAB:
                if key == str(string):
                    state = STATE_TAB[key]
                    break
            return state

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

        if response.meta.get('PageType') == 'HouseInfo':
            if (not response.meta.get('ProjectName')) or (not response.meta.get('BuildingName'))\
            or (not response.meta.get('ProjectUUID')) or (not response.meta.get('BuildingUUID')):
                if result:
                    return result
                return []
            house_list = get_json(Selector(response).xpath('//input[@id="DataHF"]/@value').extract_first()).pop().get('rooms')
            for house in house_list:
                hinfo = HouseInfoItem()
                hinfo['ProjectName'] = response.meta.get('ProjectName')
                hinfo['BuildingName'] = response.meta.get('BuildingName')
                hinfo['ProjectUUID'] = response.meta.get('ProjectUUID')
                hinfo['BuildingUUID'] = response.meta.get('BuildingUUID')
                hinfo['HouseName'] = house.get('location')
                hinfo['HoueseRegID'] = house.get('fjh')
                hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, b_info['BuildingRegName'] + b_id)
                hinfo['HoueseID'] = house.get('id')
                hinfo['HouseFloor'] = house.get('flr')
                hinfo['HouseRoomNum'] = house.get('rn')
                hinfo['HouseBuildingArea'] = house.get('bArea')
                hinfo['HouseInnerArea'] = house.get('iArea')
                hinfo['HouseShareArea'] = house.get('sArea')
                hinfo['HouseStructure'] = house.get('stru')
                hinfo['HouseRoomType'] = house.get('rType')
                hinfo['HouseUsage'] = house.get('use')
                hinfo['HouseSaleState'] = get_house_state(house.get('status'))
                hinfo['HouseInnerUnitPrice'] = house.get('nsjg')
                hinfo['HouseBuildingUnitPrice'] = house.get('nsjmjg')
                hinfo['HouseType'] = house.get('F_STATE')
                result.append(hinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
