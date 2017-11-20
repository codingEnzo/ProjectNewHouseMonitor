# coding = utf-8
import re
import sys
import uuid
import json
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsCS import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


def get_json(strRes):
    strRes = str(strRes).replace("'", '"').replace('\\', ' ').\
                replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    return json.loads(strRes)


def get_url_id(strUrl):
    res_id = '0'
    match_res = re.search(r'CaseId=(\d+)', str(strUrl))
    if match_res:
        res_id = match_res.group(1)
    return res_id


def get_href(strHref):
    res_href = ''
    match_res = re.search(r"'(.+)','_blank'", str(strHref))
    if match_res:
        res_href = match_res.group(1)
    return res_href


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
            project_list = sel.xpath('//table[@class="house_table"]/tr')
            for p in project_list:
                p_id = get_url_id(p.xpath('./td[2]/a/@href').extract_first() or '')
                p_name = p.xpath('./td[4]/text()').extract_first() or ''
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
        if response.meta.get('PageType') not in ('ProjectInfo', ):
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

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfo', ):
            if result:
                return result
            return []
        print('HouseInfoHandleMiddleware')

        sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectInfo':
            building_list = sel.xpath('//div[@class="hs_table"]/table/tr[not(@class) and td]')
            house_table_list = sel.xpath('//div[@class="hs_table"]/table/tr[@class="hs_table1"]/td/div/table')
            if (building_list == []) or (house_table_list == []):
                if result:
                    return result
                return []
            for building_info, house_table in zip(building_list, house_table_list):
                p_name = sel.xpath('//body/div/div/div[1]/table/tr[1]/th/text()').extract_first() or ''
                b_name = building_info.xpath('./td[2]/text()').extract_first() or ''
                breg_name = building_info.xpath('./td[1]/text()').extract_first() or ''
                p_uuid = uuid.uuid3(uuid.NAMESPACE_DNS,
                                    p_name + get_url_id(response.url))
                b_uuid = uuid.uuid3(uuid.NAMESPACE_DNS,
                                            breg_name + b_name + get_url_id(response.url))
                house_list = house_table.xpath('./tr[not(th)]')
                for house in house_list:
                    hinfo = HouseInfoItem()
                    hinfo['ProjectName'] = p_name
                    hinfo['BuildingName'] = b_name
                    hinfo['ProjectUUID'] = p_uuid
                    hinfo['BuildingUUID'] = b_uuid
                    hinfo['HouseName'] = house.xpath('./td[1]/text()').extract_first() or ''
                    hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, hinfo['HouseName'] + str(b_uuid))
                    hinfo['HouseFloor'] = house.xpath('./td[2]/text()').extract_first() or ''
                    hinfo['HouseBuildingArea'] = house.xpath('./td[5]/text()').extract_first() or ''
                    hinfo['HouseInnerArea'] = house.xpath('./td[6]/text()').extract_first() or ''
                    hinfo['HouseShareArea'] = house.xpath('./td[7]/text()').extract_first() or ''
                    hinfo['HouseType'] = house.xpath('./td[4]/text()').extract_first() or ''
                    hinfo['HouseUsage'] = house.xpath('./td[3]/text()').extract_first() or ''
                    hinfo['HouseSaleState'] = house.xpath('./td[9]/text()').extract_first() or ''
                    hinfo['HouseDType'] = house.xpath('./td[5]/text()').extract_first() or ''
                    result.append(hinfo)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
