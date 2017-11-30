# coding = utf-8
import re
import sys
import uuid
import copy
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsGY import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


def get_url_lpid(strUrl):
    res_id = '0'
    match_res = re.search(r'lpid=(\d+)', str(strUrl))
    if match_res:
        res_id = match_res.group(1)
    return res_id


def get_url_sid(strUrl):
    res_id = '0'
    match_res = re.search(r'sid=(\d+)', str(strUrl))
    if match_res:
        res_id = match_res.group(1)
    return res_id


def get_building_base_href(string):
    building_url_base = 'http://www.gyfc.net.cn/pro_query/FloorList.aspx?'
    req_dict = {'yszh': '',
                'qu': ''}
    match = re.search(r"yszh=(?P<yszh>.+)&qu=(?P<qu>.+)", str(string))
    if match:
        req_dict['yszh'] = match.groupdict().get('yszh')
        req_dict['qu'] = match.groupdict().get('qu')
        return building_url_base + urlparse.urlencode(req_dict)
    return None


def get_building_href(buildingCode, baseUrl):
    building_url = 'http://www.gyfc.net.cn/pro_query/index/floorView.aspx?'
    req_dict = {'dongID': '',
                'danyuan': '',
                'qu': '',
                'yszh': '',
                }
    match = re.search(r"dongID=(?P<dongID>.+)&danyuan=(?P<danyuan>.+)&qu=(?P<qu>.+)&yszh=(?P<yszh>.+)", str(baseUrl))
    if match:
        req_dict['yszh'] = match.groupdict().get('yszh')
        req_dict['qu'] = match.groupdict().get('qu')
        req_dict['danyuan'] = '全部'
        req_dict['dongID'] = str(buildingCode)
        return building_url + urlparse.urlencode(req_dict, encoding='gbk')
    return None


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
        if response.meta.get('PageType') not in ('ProjectBase', 'ProjectList', 'SubProjectBase', 'SubProjectList'):
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectBase':
            url_base = 'http://www.gyfc.net.cn/2_proInfo/index.aspx?'
            total_page = int(sel.xpath('//div[@id="ProInfo1_AspNetPager1"]/div[1]/font[2]/b/text()').extract_first() or '0')
            for cur_page in range(1, total_page + 1):
                result.append(Request(url=url_base + urlparse.urlencode({'page': cur_page}), dont_filter=True,
                                        meta={'PageType': 'ProjectList'}))
        elif response.meta.get('PageType') == 'ProjectList':
            project_list = sel.xpath('//div[@style="padding: 5px; width: 750px; border-style: dashed; border-width: 1px; border-color: skyblue;"]')
            for p in project_list:
                p_href = p.xpath('./table/tr[1]/td[3]/a/@href').extract_first()
                result.append(Request(url=p_href, dont_filter=True, meta={'PageType': 'SubProjectBase'}))
        elif response.meta.get('PageType') == 'SubProjectBase':
            sub_project_total_page = sel.xpath('//div[@id="proInfodetail_AspNetPager1"]/div[1]/font[2]/b/text()').extract_first()
            if sub_project_total_page:
                for cur_page in range(1, int(sub_project_total_page) + 1):
                    result.append(Request(url=response.url + '&page=%s' % cur_page, dont_filter=True, meta={'PageType': 'SubProjectList'}))
            else:
                result.append(Request(url=response.url + '&page=1', dont_filter=True, meta={'PageType': 'SubProjectList'}))
        elif response.meta.get('PageType') == 'SubProjectList':
            sub_project_list = sel.xpath('//div[@style="padding: 5px; width: 750px; border-style: dashed; border-width: 1px; border-color: skyblue;"]')
            for sp in sub_project_list:
                p_name = (sp.xpath('./table/tr[1]/td[1]/table/tr[2]/td[2]/text()').extract_first() or '').strip()
                p_regname = (sp.xpath('./table/tr[1]/td[1]/table/tr[1]/td[3]/a/text()').extract_first() or '').strip()
                p_url = (sp.xpath('./table/tr[1]/td[1]/table/tr[1]/td[3]/a/@href').extract_first() or '').strip()
                pb = ProjectBaseItem()
                pb['ProjectName'] = p_name
                pb['ProjectRegName'] = p_regname
                pb['ProjectURL'] = p_url
                pb['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                        p_name + p_regname + get_url_lpid(response.url))
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
            pinfo['ProjectName'] = (sel.xpath('//td[text()="项目名称： "]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectRegName'] = (sel.xpath('//td[text()="预(销)售证号： "]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                    pinfo['ProjectName'] + pinfo['ProjectRegName'] + get_url_lpid(response.url))
            pinfo['ProjectAddress'] = (sel.xpath('//td[text()="座落： "]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectUsage'] = (sel.xpath('//td[text()="项目性质： "]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectCompany'] = (sel.xpath('//td[text()="开发商： "]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectSalePhone'] = (sel.xpath('//td[text()="销售电话： "]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectDescription'] = re.compile(r'<[^>]+>', re.S).sub('', sel.xpath('//table[@id="Table4"]/tr[2]/td').extract()[0]).\
                                            replace(' ', '').replace('\r\n', '').strip()
            pinfo['ProjectArea'] = (sel.xpath('//span[@id="ContentPlaceHolder1_info_all1_listJZMJ"]/text()').extract_first() or '').strip()
            pinfo['ProjectBuildArea'] = (sel.xpath('//span[@id="ContentPlaceHolder1_info_all1_litZDMJ"]/text()').extract_first() or '').strip()
            pinfo['ProjectBuildingNum'] = (sel.xpath('//span[@id="ContentPlaceHolder1_info_all1_litDongCnt"]/font/text()').extract_first() or '').strip()
            pinfo['ProjectAreaCode'] = (sel.xpath('//td[text()="土地使用权证号："]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectAreaPlanCode'] = (sel.xpath('//td[text()="用地规划许可证号："]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectEngPlanCode'] = (sel.xpath('//td[text()="工程规划许可证号："]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectBuildingCode'] = (sel.xpath('//td[text()="施工许可证号："]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectBuildingCompany'] = (sel.xpath('//td[text()="施工单位："]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectDesignCompany'] = (sel.xpath('//td[text()="设计单位："]/following-sibling::td[1]/text()').extract_first() or '').strip()
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
        if response.meta.get('PageType') not in ('SubProjectList', 'BuildingInfo'):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'SubProjectList':
            sub_project_list = sel.xpath('//div[@style="padding: 5px; width: 750px; border-style: dashed; border-width: 1px; border-color: skyblue;"]')
            for sp in sub_project_list:
                p_name = (sp.xpath('./table/tr[1]/td[1]/table/tr[2]/td[2]/text()').extract_first() or '').strip()
                p_regname = (sp.xpath('./table/tr[1]/td[1]/table/tr[1]/td[3]/a/text()').extract_first() or '').strip()
                building_base_url = get_building_base_href((sp.xpath('./table/tr[1]/td[1]/table/tr[1]/td[3]/a/@href').extract_first() or '').strip())
                b_info = BuildingInfoItem()
                b_info['ProjectName'] = p_name
                b_info['ProjectRegName'] = p_regname
                b_info['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                            p_name + p_regname + get_url_lpid(response.url))
                result.append(Request(url=building_base_url, dont_filter=True,
                                        meta={'PageType': 'BuildingInfo', 'item': copy.deepcopy(b_info)}))
        elif response.meta.get('PageType') == 'BuildingInfo':
            building_list = sel.xpath('//select[@id="ContentPlaceHolder1_floor_list1_ddlDong"]/option')
            for building in building_list:
                b_info = copy.deepcopy(response.meta.get('item'))
                if b_info:
                    b_info['BuildingCode'] = (building.xpath('./@value').extract_first() or '').strip()
                    b_info['BuildingName'] = (building.xpath('./text()').extract_first() or '').strip()
                    b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                str(b_info['ProjectUUID']) + b_info['BuildingCode'])
                    b_info['BuildingURL'] = get_building_href(b_info['BuildingCode'], sel.xpath('//iframe/@src').extract_first() or '')
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
            state = {}
            match = re.search(r"(?P<HouseSaleState>.+)\n(?P<HouseBuildingArea>.+)\n(?P<HouseUsage>.+)\n(?P<HouseStructure>.+)\n(?P<HouseType>.+)",
                        str(string)) or\
                        re.search(r"(?P<HouseSaleState>.+)\n(?P<HouseBuildingArea>.+)\n(?P<HouseUsage>.+)\n(?P<HouseStructure>.+)",
                            str(string)) or\
                            re.search(r"(?P<HouseSaleState>.+)\n(?P<HouseBuildingArea>.+)",
                                    str(string))
            if match:
                state = match.groupdict()
            return state

        def get_house_detail(string):
            detail = {}
            match = re.search(r"(?P<HouseUnit>.+)-(?P<HouseFloor>.+)-(?P<HouseNum>.+)",
                        str(string)) or\
                        re.search(r"(?P<HouseFloor>.+)-(?P<HouseNum>.+)",
                            str(string)) or\
                            re.search(r"(?P<HouseNum>.+)",
                                    str(string))
            if match:
                detail = match.groupdict()
            return detail

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
            houseinfodetail_list = sel.xpath('//div[table[tr[td[span]]]]')
            for house in houseinfodetail_list:
                hinfo = HouseInfoItem()
                hinfo['ProjectName'] = response.meta.get('ProjectName')
                hinfo['BuildingName'] = response.meta.get('BuildingName')
                hinfo['ProjectUUID'] = response.meta.get('ProjectUUID')
                hinfo['BuildingUUID'] = response.meta.get('BuildingUUID')
                hinfo['HouseName'] = (house.xpath('./table/tr/td/span/text()').extract_first() or '').strip()
                hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                            hinfo['HouseName'] + str(hinfo['BuildingUUID']) + str((houseinfodetail_list.index(house))) + str(hinfo['ProjectUUID']))
                hinfo['HouseInfoText'] = (house.xpath('./@title').extract_first() or '').strip()
                hinfo.update(get_house_detail(hinfo['HouseName']))
                hinfo.update(get_house_state(hinfo['HouseInfoText']))
                hinfo['HouseReqURL'] = response.request.url
                hinfo['HouseNumCheck'] = str((houseinfodetail_list.index(house), len(houseinfodetail_list)))
                result.append(hinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
