# coding = utf-8
import re
import sys
import uuid
import copy
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsNC import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


def get_url_id(strUrl):
    res_id = '0'
    match_res = re.search(r'CaseId=(\d+)', str(strUrl))
    if match_res:
        res_id = match_res.group(1)
    return res_id


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
            base_url = 'http://www.xjqfdc.cn/House/ListPreSell?'
            req_dict = {'page': '',
                        'Place': '',
                        'LicenceId': '',
                        'Developer': '',
                        'Project': '',
                        'Date': ''}
            total_page = get_total_page(response.body_as_unicode())
            for page in range(total_page):
                req_dict['page'] = page
                url = base_url
                body = urlparse.urlencode(req_dict)
                result.append(Request(url=url + body, method='GET', dont_filter=True,
                                meta={'PageType': 'ProjectList'}))
        elif response.meta.get('PageType') == 'ProjectList':
            project_list = sel.xpath('//table[@class="house_table"]/tbody/tr')
            for p in project_list:
                p_id = get_url_id(p.xpath('./td[2]/a/@href').extract_first() or '')
                p_name = p.xpath('./td[4]/a/text()').extract_first() or ''
                p_href = urlparse.urljoin(response.url,
                                            p.xpath('./td[2]/a/@href').extract_first() or '')
                p_address = p.xpath('./td[5]/text()').extract_first() or ''
                p_regname = p.xpath('./td[2]/a/text()').extract_first() or ''
                p_regdate = p.xpath('./td[6]/text()').extract_first() or ''
                p_company = p.xpath('./td[3]/text()').extract_first() or ''
                pb = ProjectBaseItem()
                pb['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + p_id)
                pb['ProjectRegUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_regname + p_id)
                pb['ProjectName'] = p_name
                pb['ProjectURL'] = p_href
                pb['ProjectAddress'] = p_address
                pb['ProjectRegName'] = p_regname
                pb['ProjectRegDate'] = p_regdate
                pb['ProjectCompany'] = p_company
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
            pinfo['ProjectName'] = sel.xpath('//td[text()="项目名称："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                    pinfo['ProjectName'] + get_url_id(response.url))
            pinfo['ProjectCompany'] = sel.xpath('//td[text()="公司名称："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectRegName'] = sel.xpath('//td[text()="预售许可证："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectSalePhone'] = sel.xpath('//td[text()="售楼电话："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectAddress'] = sel.xpath('//td[text()="项目坐落："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectUsage'] = sel.xpath('//td[text()="规划用途："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectArea'] = sel.xpath('//td[text()="土地面积："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectUseArea'] = sel.xpath('//td[text()="占地面积："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectBuildArea'] = sel.xpath('//td[text()="建筑面积："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectRongjiRatio'] = sel.xpath('//td[text()="容 积 率："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectLvdiRatio'] = sel.xpath('//td[text()="绿 地 率："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectBuildingRatio'] = sel.xpath('//td[text()="建筑密度："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectInvestment'] = sel.xpath('//td[text()="工程投资："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectBuildDate'] = sel.xpath('//td[text()="开工日期："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectCompleteDate'] = sel.xpath('//td[text()="竣工日期："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectBuildingCompany'] = sel.xpath('//td[text()="施工单位："]/following-sibling::td[1]/text()').extract_first() or ''
            pinfo['ProjectMeasureCompany'] = sel.xpath('//td[text()="测绘单位："]/following-sibling::td[1]/text()').extract_first() or ''
            sale_sum_t = sel.xpath('//tr[@class="title"]/following-sibling::tr[not(@class)]')
            if len(sale_sum_t) == 3:
                pinfo['ProjectSaleSum'] = {
                    '住宅': {
                        '套数': {
                            'Sum': sale_sum_t[0].xpath('./td[2]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[2]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[2]/text()').extract_first() or '',
                        },
                        '面积': {
                            'Sum': sale_sum_t[0].xpath('./td[3]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[3]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[3]/text()').extract_first() or '',
                        }
                    },
                    '商业': {
                        '套数': {
                            'Sum': sale_sum_t[0].xpath('./td[4]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[4]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[4]/text()').extract_first() or '',
                        },
                        '面积': {
                            'Sum': sale_sum_t[0].xpath('./td[5]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[5]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[5]/text()').extract_first() or '',
                        }
                    },
                    '写字楼': {
                        '套数': {
                            'Sum': sale_sum_t[0].xpath('./td[6]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[6]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[6]/text()').extract_first() or '',
                        },
                        '面积': {
                            'Sum': sale_sum_t[0].xpath('./td[7]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[7]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[7]/text()').extract_first() or '',
                        }
                    },
                    '车库车位': {
                        '套数': {
                            'Sum': sale_sum_t[0].xpath('./td[8]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[8]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[8]/text()').extract_first() or '',
                        },
                        '面积': {
                            'Sum': sale_sum_t[0].xpath('./td[9]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[9]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[9]/text()').extract_first() or '',
                        }
                    },
                    '其他': {
                        '套数': {
                            'Sum': sale_sum_t[0].xpath('./td[10]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[10]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[10]/text()').extract_first() or '',
                        },
                        '面积': {
                            'Sum': sale_sum_t[0].xpath('./td[11]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[11]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[11]/text()').extract_first() or '',
                        }
                    }
                }
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
        if response.meta.get('PageType') not in ('ProjectInfo', 'HouseInfo'):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectInfo':
            p_name = sel.xpath('//td[text()="项目名称："]/following-sibling::td[1]/text()').extract_first() or ''
            p_id = get_url_id(response.url)
            building_list = sel.xpath('//table[@class="house_table"]//td[a[span]]/a')
            for b in building_list:
                b_info = BuildingInfoItem()
                b_info['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + p_id)
                b_info['ProjectName'] = p_name
                b_info['BuildingName'] = b.xpath('./span/strong/text()').extract_first() or ''
                b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                            b_info['BuildingName'] + p_id)
                b_info['BuildingURL'] = urlparse.urljoin(response.url,
                                            b.xpath('./@href').extract_first() or '')
                result.append(Request(url=b_info['BuildingURL'], method='GET', dont_filter=True,
                                meta={'PageType': 'HouseInfo',
                                        'ProjectName': b_info['ProjectName'],
                                        'BuildingName': b_info['BuildingName'],
                                        'ProjectUUID': b_info['ProjectUUID'],
                                        'BuildingUUID': b_info['BuildingUUID'],
                                        'item': copy.deepcopy(b_info)}))
        elif response.meta.get('PageType') == 'HouseInfo':
            b_info = response.meta.get('item')
            if b_info:
                b_info['BuildingUsage'] = sel.xpath('//td[text()="设计用途："]/following-sibling::td[1]/text()').extract_first() or ''
                b_info['BuildingStructure'] = sel.xpath('//td[text()="建筑结构："]/following-sibling::td[1]/text()').extract_first() or ''
                b_info['BuildingTotalFloor'] = sel.xpath('//td[text()="总 层 数："]/following-sibling::td[1]/text()').extract_first() or ''
                b_info['BuildingTotalArea'] = sel.xpath('//td[text()="总 面 积："]/following-sibling::td[1]/text()').extract_first() or ''
                sale_sum_t = sel.xpath('//tr[@class="title"]/following-sibling::tr[not(@class) and td[@class="c"]]')
            if len(sale_sum_t) == 3:
                b_info['BuildingSaleSum'] = {
                    '住宅': {
                        '套数': {
                            'Sum': sale_sum_t[0].xpath('./td[2]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[2]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[2]/text()').extract_first() or '',
                        },
                        '面积': {
                            'Sum': sale_sum_t[0].xpath('./td[3]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[3]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[3]/text()').extract_first() or '',
                        }
                    },
                    '商业': {
                        '套数': {
                            'Sum': sale_sum_t[0].xpath('./td[4]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[4]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[4]/text()').extract_first() or '',
                        },
                        '面积': {
                            'Sum': sale_sum_t[0].xpath('./td[5]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[5]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[5]/text()').extract_first() or '',
                        }
                    },
                    '写字楼': {
                        '套数': {
                            'Sum': sale_sum_t[0].xpath('./td[6]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[6]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[6]/text()').extract_first() or '',
                        },
                        '面积': {
                            'Sum': sale_sum_t[0].xpath('./td[7]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[7]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[7]/text()').extract_first() or '',
                        }
                    },
                    '车库车位': {
                        '套数': {
                            'Sum': sale_sum_t[0].xpath('./td[8]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[8]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[8]/text()').extract_first() or '',
                        },
                        '面积': {
                            'Sum': sale_sum_t[0].xpath('./td[9]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[9]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[9]/text()').extract_first() or '',
                        }
                    },
                    '其他': {
                        '套数': {
                            'Sum': sale_sum_t[0].xpath('./td[10]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[10]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[10]/text()').extract_first() or '',
                        },
                        '面积': {
                            'Sum': sale_sum_t[0].xpath('./td[11]/text()').extract_first() or '',
                            'Saling': sale_sum_t[1].xpath('./td[11]/text()').extract_first() or '',
                            'Sold': sale_sum_t[2].xpath('./td[11]/text()').extract_first() or '',
                        }
                    }
                }
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
            STATE_TAB = {'sty_1': '已限制',
                            'sty_2': '已抵押',
                            'sty_3': '已报审',
                            'sty_4': '已备案',
                            'sty_5': '可销售',
                            'sty_6': '不可售'}
            state = ''
            for key in STATE_TAB:
                if key == string:
                    state = STATE_TAB[key]
                    break
            return state

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseInfo', 'HouseInfoDetail'):
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
            houseinfodetail_tr = sel.xpath('//table[@id="jqLouPanBiao"]/tbody/tr')
            for tr in houseinfodetail_tr:
                cur_floor = tr.xpath('./td[1]/text()').extract_first() or ''
                for house in tr.xpath('./td[@class and position()>0]'):
                    hinfo = HouseInfoItem()
                    hinfo['ProjectName'] = response.meta.get('ProjectName')
                    hinfo['BuildingName'] = response.meta.get('BuildingName')
                    hinfo['ProjectUUID'] = response.meta.get('ProjectUUID')
                    hinfo['BuildingUUID'] = response.meta.get('BuildingUUID')
                    hinfo['HouseName'] = house.xpath('./a/text()').extract_first() or ''
                    hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, hinfo['HouseName'] + str(hinfo['BuildingUUID']))
                    hinfo['HouseFloor'] = cur_floor
                    hinfo['HouseSaleState'] = get_house_state(house.xpath('./@class').extract_first())
                    if house.xpath('./a/@href').extract_first():
                        houseinfodetail_href = urlparse.urljoin(response.url,
                                                    house.xpath('./a/@href').extract_first())
                        houseinfodetail_req = Request(url=houseinfodetail_href, method='GET',
                                            meta={'PageType': 'HouseInfoDetail', 'item': copy.deepcopy(hinfo)})
                        result.append(houseinfodetail_req)
                    else:
                        result.append(hinfo)

        elif response.meta.get('PageType') == 'HouseInfoDetail':
            hinfo = response.meta.get('item')
            if hinfo:
                hinfo['HouseStructure'] = sel.xpath('//td[text()="结　　构："]/following-sibling::td[1]/text()').extract_first() or ''
                hinfo['HouseBuildingArea'] = sel.xpath('//td[text()="建筑面积："]/following-sibling::td[1]/text()').extract_first() or ''
                hinfo['HouseInnerArea'] = sel.xpath('//td[text()="套内面积："]/following-sibling::td[1]/text()').extract_first() or ''
                hinfo['HouseShareArea'] = sel.xpath('//td[text()="分摊面积："]/following-sibling::td[1]/text()').extract_first() or ''
                hinfo['HouseUsage'] = sel.xpath('//td[text()="房屋用途："]/following-sibling::td[1]/text()').extract_first() or ''
                hinfo['HouseFloorAt'] = sel.xpath('//td[text()=" 所 在 层： "]/following-sibling::td[1]/text()').extract_first() or ''
                hinfo['HouseFloorTotal'] = sel.xpath('//td[text()=" 总 层 数： "]/following-sibling::td[1]/text()').extract_first() or ''
                hinfo['HousePreUnitPrice'] = sel.xpath('//td[text()=" 预售申请单价： "]/following-sibling::td[1]/text()').extract_first() or ''
                hinfo['HouseStructureType'] = sel.xpath('//td[text()="房屋户型："]/following-sibling::td[1]/text()').extract_first() or ''
                hinfo['HouseContract'] = sel.xpath('//td[text()="合 同 号："]/following-sibling::td[1]/text()').extract_first() or ''
                result.append(hinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
