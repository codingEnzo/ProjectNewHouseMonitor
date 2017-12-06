# coding = utf-8
import re
import sys
import uuid
import copy
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsTY import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse

HEADERS = {'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'ys.tyfdc.gov.cn'}


def get_pid(string):
    res_pid = '0'
    match_res = re.search(r"propid=(.+)", str(string)) or re.search(r"pid=(.+)", str(string))
    if match_res:
        res_pid = match_res.group(1)
    return res_pid


def get_project_url(string):
    res_url = None
    url_base = 'http://ys.tyfdc.gov.cn/Firsthand/tyfc/publish/p/ProjInfo.do?'
    match_res = re.search(r"showProInfo\('(.+)'\);", str(string))
    if match_res:
        res_url = url_base + urlparse.urlencode({'propid': match_res.group(1)})
    return res_url


def get_company_url(string):
    res_url = None
    url_base = 'http://ys.tyfdc.gov.cn/Firsthand/tyfc/publish/p/OrgInfo.do?'
    match_res = re.search(r"showOrgInfo\('(.+)'\);", str(string))
    if match_res:
        res_url = url_base + urlparse.urlencode({'oid': match_res.group(1)})
    return res_url


def get_building_url(string):
    res_url = None
    url_base = 'http://ys.tyfdc.gov.cn/Firsthand/tyfc/publish/probld/NBView.do?'
    match_res = re.search(r"showNBView\('(.+)','(.+)',.*\);", str(string))
    if match_res:
        res_url = url_base + urlparse.urlencode({'projectid': match_res.group(1), 'nid': match_res.group(2)})
    return res_url


def get_building_info_url(string):
    res_url = None
    url_base = 'http://ys.tyfdc.gov.cn/Firsthand/tyfc/publish/p/ProBLDInfo.do?'
    match_res = re.search(r"showNBInfo\('(.+)'\);", str(string))
    if match_res:
        res_url = url_base + urlparse.urlencode({'bldsignno': match_res.group(1)})
    return res_url


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
        if response.meta.get('PageType') not in ('ProjectBase', 'ProjectList', 'CompanyInfo'):
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectBase':
            url_base = 'http://ys.tyfdc.gov.cn/Firsthand/tyfc/publish/ProjListForPassed.do'
            req_dict = {'pageNo': 1,
                        'pageSize': 10000}
            result.append(Request(url=url_base, body=urlparse.urlencode(req_dict), headers=HEADERS,
                                        method='POST', dont_filter=True,
                                        meta={'PageType': 'ProjectList'}))
        elif response.meta.get('PageType') == 'ProjectList':
            project_list = sel.xpath('//tr[@objid]')
            for p in project_list:
                p_id = (p.xpath('./@objid').extract_first() or '').strip()
                p_name = (p.xpath('./td[2]/a/span/text()').extract_first() or '').strip()
                p_regname = (p.xpath('./td[5]/text()').extract_first() or '').strip()
                p_type = (p.xpath('./td[4]/text()').extract_first() or '').strip()
                p_district = (p.xpath('./td[3]/text()').extract_first() or '').strip()
                p_url = get_project_url((p.xpath('./td[2]/a/@onclick').extract_first() or '').strip())
                pb = ProjectBaseItem()
                pb['ProjectName'] = p_name
                pb['ProjectRegName'] = p_regname
                pb['ProjectURL'] = p_url
                pb['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_id)
                pb['ProjectType'] = p_type
                pb['ProjectDistrict'] = p_district
                p_company_url = get_company_url((p.xpath('./td[6]/a/@onclick').extract_first() or '').strip())
                if p_company_url:
                    result.append(Request(url=p_company_url, dont_filter=True, headers=HEADERS,
                                            meta={'PageType': 'CompanyInfo', 'item': copy.deepcopy(pb)}))
                else:
                    result.append(pb)
        elif response.meta.get('PageType') == 'CompanyInfo':
            pb = response.meta.get('item')
            if pb:
                pb['ProjectCompanyId'] = (sel.xpath('//td[text()="单位编号:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pb['ProjectCompanyName'] = (sel.xpath('//td[text()="企业名称: "]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pb['ProjectCompanyCode'] = (sel.xpath('//td[text()="营业执照号"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pb['ProjectCompanyLevel'] = (sel.xpath('//td[text()="资质等级: "]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pb['ProjectCompanyLevelCode'] = (sel.xpath('//td[text()="资质证书号: "]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pb['ProjectCompanyCorporation'] = (sel.xpath('//td[text()="法定代表人: "]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pb['ProjectCompanyCorporationPhone'] = (sel.xpath('//td[text()="法人电话: "]/following-sibling::td[1]/text()').extract_first() or '').strip()
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
        if response.meta.get('PageType') not in ('ProjectInfo', 'ProjectRegInfo'):
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')

        sel = Selector(response)
        p_id = get_pid(response.url)
        if response.meta.get('PageType') == 'ProjectInfo':
            pinfo = ProjectInfoItem()
            pinfo['ProjectName'] = (sel.xpath('//td[text()="项目名称:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_id)
            pinfo['ProjectAddress'] = (sel.xpath('//td[text()="项目座落:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectSaleRange'] = (sel.xpath('//td[text()="销售范围: "]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectBuildArea'] = (sel.xpath('//td[text()="总规划建筑面积: "]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectSaleArea'] = (sel.xpath('//td[text()="计划销售面积: "]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectSaleBuildingNum'] = (sel.xpath('//td[text()="销售幢数:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectSaleHouseNum'] = (sel.xpath('//td[text()="销售套数:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectLHRatio'] = (sel.xpath('//td[text()="绿化率(%):"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectRJRatio'] = (sel.xpath('//td[text()="容积率: "]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectBuildDate'] = (sel.xpath('//td[text()="开工日期:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectCompleteDate'] = (sel.xpath('//td[text()="竣工日期:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectBuildingCompany'] = (sel.xpath('//td[text()="施工单位:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectDesignCompany'] = (sel.xpath('//td[text()="设计单位: "]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectManageCompany'] = (sel.xpath('//td[text()="监理单位:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectSaleCompany'] = (sel.xpath('//td[text()="销售单位:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            pinfo['ProjectUnitPrice'] = (sel.xpath('//td[text()="参考均价:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
            result.append(Request(url='http://ys.tyfdc.gov.cn/Firsthand/tyfc/publish/p/PermitInfo.do?' + urlparse.urlencode({'propid': p_id}), headers=HEADERS,
                                    dont_filter=True, meta={'PageType': 'ProjectRegInfo', 'item': copy.deepcopy(pinfo)}))
            result.append(Request(url='http://ys.tyfdc.gov.cn/Firsthand/tyfc/publish/ProNBList.do', method='POST',
                                    body=urlparse.urlencode({'pid': p_id, 'pageNo': 1, 'pageSize': 1000}), headers=HEADERS,
                                    dont_filter=True, meta={'PageType': 'BuildingList'}))
        elif response.meta.get('PageType') == 'ProjectRegInfo':
            pinfo = response.meta.get('item')
            if pinfo:
                pinfo['ProjectCompanmy'] = (sel.xpath('//td[text()="企业名称:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pinfo['ProjectUsage'] = (sel.xpath('//td[text()="房屋用途:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pinfo['ProjectBuilding'] = (sel.xpath('//td[text()="项目楼号: "]/following-sibling::td[1]/text()').extract_first() or '').strip()
                pinfo['ProjectRegId'] = (sel.xpath('//td[text()="许可证号:"]/following-sibling::td[1]/text()').extract_first() or '').strip()
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
        if response.meta.get('PageType') not in ('BuildingList', 'BuildingInfo'):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        sel = Selector(response)
        p_id = get_pid(response.request.body)
        if response.meta.get('PageType') == 'BuildingList':
            building_list = sel.xpath('//tr[@objid]')
            for building in building_list:
                b_info = BuildingInfoItem()
                b_info['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_id)
                b_info['BuildingCode'] = (building.xpath('./@objid').extract_first() or '').strip()
                b_info['BuildingName'] = (building.xpath('./td[3]/a/span/text()').extract_first() or '').strip()
                b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                            str(b_info['ProjectUUID']) + b_info['BuildingCode'])
                b_info['BuildingURL'] = get_building_url((building.xpath('./td[3]/a/@onclick').extract_first() or '').strip())
                building_info_url = get_building_info_url((building.xpath('./td[2]/a/@onclick').extract_first() or '').strip())
                if building_info_url:
                    result.append(Request(url=building_info_url, dont_filter=True, headers=HEADERS,
                                            meta={'PageType': 'BuildingInfo', 'item': copy.deepcopy(b_info)}))
                else:
                    result.append(b_info)
        elif response.meta.get('PageType') == 'BuildingInfo':
            b_info = response.meta.get('item')
            if b_info:
                b_info['BuildingMCode'] = (sel.xpath('//td[text()="楼幢测量号"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingBaseArea'] = (sel.xpath('//td[text()="基底面积"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingShareArea'] = (sel.xpath('//td[text()="公摊面积"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingArea'] = (sel.xpath('//td[text()="建筑面积"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingStructure'] = (sel.xpath('//td[text()="建筑结构"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingYear'] = (sel.xpath('//td[text()="建筑年代"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingFloorNum'] = (sel.xpath('//td[text()="总层数"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingFloorAbove'] = (sel.xpath('//td[text()="地上层数"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingFloorBelow'] = (sel.xpath('//td[text()="地下层数"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingUnitNum'] = (sel.xpath('//td[text()="总单元数"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                b_info['BuildingSaleName'] = (sel.xpath('//td[text()="楼幢销售名"]/following-sibling::td[1]/text()').extract_first() or '').strip()
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

        def get_house_state_code(string):
            code = ''
            match = re.search(r"background-color:(.+);", str(string))
            if match:
                code = match.group(1)
            return code

        def get_house_state(string):
            STATE_TAB = {'#c0c0c0': '限制销售',
                            '#f58708': '已预告登记',
                            '#ffff00': '已售',
                            '#ff00ff': '预定',
                            '#adeff7': '非卖房或拆迁安置房',
                            '#ff0000': '已登记',
                            '#00ff00': '可售'}
            state = ''
            for key in STATE_TAB:
                if key in string:
                    state = STATE_TAB[key]
                    break
            return state

        def get_house_substate(b_selector):
            STATE_TAB = {'C': '限制销售',
                            'Z': '已预告登记',
                            'P': '已售',
                            'Q': '预定',
                            'S': '非卖房或拆迁安置房',
                            'X': '已登记',
                            'Y': '可售'}
            state = []
            for b in b_selector:
                s = STATE_TAB.get(str(b.xpath('./text()').extract_first()))
                if s:
                    state.append(s)
            state.sort()
            return ','.join(state)

        def get_house_price(string):
            price = ''
            match = re.search(r"房屋单价：(.+)", str(string))
            if match:
                price = match.group(1)
            return price

        def get_house_detail_url(string):
            res_url = None
            url_base = 'http://ys.tyfdc.gov.cn/Firsthand/tyfc/publish/p/HouseBaseInfo.do?'
            match_res = re.search(r"getHouseBaseInfo\('(.+)'\);", str(string))
            if match_res:
                res_url = url_base + urlparse.urlencode({'HID': match_res.group(1)})
            return res_url

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseInfo', 'HouseList', 'HouseDetail'):
            if result:
                return result
            return []
        print('HouseInfoHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'HouseInfo':
            if (not response.meta.get('BuildingName'))\
            or (not response.meta.get('ProjectUUID')) or (not response.meta.get('BuildingUUID')):
                if result:
                    return result
                return []
            result.append(Request(url=response.url, body=urlparse.urlencode({'pageSize': 100000}), method='POST', dont_filter=True, headers=HEADERS,
                                            meta={'PageType': 'HouseList'}))
        elif response.meta.get('PageType') == 'HouseList':
            houseinfodetail_list = sel.xpath('//td[@class="underline"]/span[@id]')
            for house in houseinfodetail_list:
                hinfo = HouseInfoItem()
                hinfo['BuildingName'] = response.meta.get('BuildingName')
                hinfo['ProjectUUID'] = response.meta.get('ProjectUUID')
                hinfo['BuildingUUID'] = response.meta.get('BuildingUUID')
                hinfo['HouseName'] = (house.xpath('./a/text()').extract_first() or '').strip()
                hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                            hinfo['HouseName'] + str(hinfo['BuildingUUID']) + str(hinfo['ProjectUUID']))
                hinfo['HouseSaleState'] = get_house_state(get_house_state_code((house.xpath('./@title').extract_first() or '').strip()))
                hinfo['HouseSaleSubState'] = get_house_substate(house.xpath('./b'))
                hinfo['HouseUnitPrice'] = get_house_price(house.xpath('./@title').extract_first() or '')
                house_detail_url = get_house_detail_url(house.xpath('./a/@onclick').extract_first())
                if house_detail_url:
                    result.append(Request(url=house_detail_url, dont_filter=True, headers=HEADERS,
                                            meta={'PageType': 'HouseDetail', 'item': copy.deepcopy(hinfo)}))
                else:
                    result.append(hinfo)
        elif response.meta.get('PageType') == 'HouseDetail':
            hinfo = response.meta.get('item')
            if hinfo:
                hinfo['HouseAddress'] = (sel.xpath('//th[text()="房屋坐落"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseId'] = (sel.xpath('//th[text()="房屋编号"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseCode'] = (sel.xpath('//th[text()="房屋编码"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseFloorTotal'] = (sel.xpath('//th[text()="建筑总层数"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseBuildingArea'] = (sel.xpath('//th[text()="建筑面积（平方米）"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseInnerArea'] = (sel.xpath('//th[text()="套内面积（平方米）"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseShareArea'] = (sel.xpath('//th[text()="分摊面积（平方米）"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseUsage'] = (sel.xpath('//th[text()="房屋用途"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseType'] = (sel.xpath('//th[text()="房屋性质"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseStructure'] = (sel.xpath('//th[text()="建筑结构"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseYear'] = (sel.xpath('//th[text()="建成年份"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseGroundCode'] = (sel.xpath('//th[text()="地籍号"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseGroundArea'] = (sel.xpath('//th[text()="宗地面积（平方米）"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseGetGroundType'] = (sel.xpath('//th[text()="土地取得方式"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseGroundType'] = (sel.xpath('//th[text()="土地所有权性质"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                hinfo['HouseGroundLimit'] = (sel.xpath('//th[text()="土地使用期限"]/following-sibling::td[1]/text()').extract_first() or '').strip()
                result.append(hinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
