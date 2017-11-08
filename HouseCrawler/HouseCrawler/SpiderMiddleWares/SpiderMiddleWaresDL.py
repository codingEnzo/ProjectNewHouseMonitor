# coding = utf-8
import re
import sys
import uuid
import copy
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsDL import *
from requests_toolbelt.multipart.encoder import MultipartEncoder
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


boundary_text = "----WebKitFormBoundaryLnjCII2eV7SFAauA"
headers = {'Host': 'www.dlfd.gov.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://www.bjjs.gov.cn',
                'Upgrade-Insecure-Requests': 1,
                'Content-Type': 'multipart/form-data; boundary={boundary_text}'.format(boundary_text=boundary_text),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'}


def get_url_id(strUrl):
    res_id = '0'
    match_res = re.search(r'id=(\d+)', str(strUrl))
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
        if response.meta.get('PageType') != 'ProjectBase':
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        if response.request.method == 'GET':
            req_dict = {'tree_id': '',
                        'newsId': '',
                        'QY': '',
                        'XMMC': '',
                        'KFSMC': '',
                        'pageNo': '',
                        'next': ''}
            try:
                total_page = int(re.search(r'共(\d+)页', response.body_as_unicode()).group(1))
            except Exception:
                total_page = 62
            for pageNo in range(1, total_page + 1):
                req_dict['pageNo'] = str(pageNo)
                req_body = MultipartEncoder(fields=req_dict, boundary=boundary_text).to_string()
                result.append(Request(url=response.url, body=req_body, method='POST',
                                headers=headers, meta={'PageType': 'ProjectBase'}))
        elif response.request.method == 'POST':
            print('current page', re.search(r'第(\d+)页', response.body_as_unicode()).group(1))
            project_list = Selector(response).xpath('//tr[not(@id) and @bgcolor="#FFFFFF" or @bgcolor="#e6f1ff"]')[:-1]
            for p in project_list:
                p_district = (p.xpath('./td[1]/text()').extract_first() or '').replace('\xa0', '')
                p_name = (p.xpath('./td[2]/a/text()').extract_first() or '').replace('\xa0', '')
                p_href = urlparse.urljoin(response.url,
                            get_href(p.xpath('./td[2]/a/@href').extract_first()))
                p_address = (p.xpath('./td[3]/text()').extract_first() or '').replace('\xa0', '')
                p_company = (p.xpath('./td[4]/text()').extract_first() or '').replace('\xa0', '')
                pb = copy.deepcopy(response.meta.get('item') or ProjectBaseItem())
                pb['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + get_url_id(p_href))
                pb['ProjectName'] = p_name
                pb['ProjectDistrict'] = p_district
                pb['ProjectURL'] = p_href
                pb['ProjectAddress'] = p_address
                pb['ProjectCorporation'] = p_company
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
        if response.meta.get('PageType') not in ('ProjectInfo', 'ProjectDetailInfo'):
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfo':
            info_sel = Selector(response)
            pinfo = ProjectInfoItem()
            pinfo['ProjectName'] = info_sel.xpath('//form/table[3]/tr/td/table/tr/td/table/tr[2]/td/table/tr[1]/td/table/tr[1]/td[2]/text()').extract_first().strip()
            pinfo['ProjectAddress'] = info_sel.xpath('//form/table[3]/tr/td/table/tr/td/table/tr[2]/td/table/tr[1]/td/table/tr[3]/td[2]/text()').extract_first().strip()
            pinfo['ProjectCompany'] = info_sel.xpath('//form/table[3]/tr/td/table/tr/td/table/tr[2]/td/table/tr[1]/td/table/tr[2]/td[2]/text()').extract_first().strip()
            pinfo['ProjectRegName'] = info_sel.xpath('//form/table[3]/tr/td/table/tr/td/table/tr[2]/td/table/tr[1]/td/table/tr[1]/td[4]/text()').extract_first().strip()
            pinfo['ProjectAreaPlanLicenseCode'] = info_sel.xpath('//form/table[3]/tr/td/table/tr/td/table/tr[2]/td/table/tr[1]/td/table/tr[2]/td[4]/text()').extract_first().strip()
            pinfo['ProjectPlanLicenseCode'] = info_sel.xpath('//form/table[3]/tr/td/table/tr/td/table/tr[2]/td/table/tr[1]/td/table/tr[3]/td[4]/text()').extract_first().strip()
            pinfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, pinfo['ProjectName'] + get_url_id(response.url))
            sale_tr = info_sel.xpath('//form/table[3]/tr/td/table/tr/td/table/tr[2]/td/table/tr[1]/td/table/tr[4]/td/table/tr')
            sale_sum = {}
            for tr in sale_tr:
                key_name = tr.xpath('./td[1]/strong/text()').extract_first().replace('套数：', '').strip()
                sale_sum[key_name] = {'numSum': tr.xpath('./td[2]/span/text()').extract_first().replace('套', '').strip(),
                        'areaSum': tr.xpath('./td[4]/span/text()').extract_first().replace('平米', '').strip(),
                        'numSaling': tr.xpath('./td[6]/span/text()').extract_first().replace('套', '').strip(),
                        'areaSaling': tr.xpath('./td[8]/span/text()').extract_first().replace('平米', '').strip()}
            pinfo['ProjectSaleSum'] = sale_sum
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

        building_base_sel = Selector(response)
        if response.meta.get('PageType') == 'ProjectInfo':
            req_dict = {'XMBH': '',
                        'XMID': '',
                        'pageNo': '',
                        'next': ''}
            try:
                total_page = int(re.search(r'共(\d+)页', response.body_as_unicode()).group(1))
            except Exception:
                total_page = 62
            for pageNo in range(1, total_page + 1):
                req_dict['pageNo'] = str(pageNo)
                req_dict['XMBH'] = building_base_sel.xpath('//input[@name="XMBH"]/@value').extract_first() or '0'
                req_dict['XMID'] = building_base_sel.xpath('//input[@name="XMID"]/@value').extract_first() or '0'
                req_body = MultipartEncoder(fields=req_dict, boundary=boundary_text).to_string()
                result.append(Request(url=response.url, body=req_body, method='POST',
                                headers=headers, meta={'PageType': 'BuildingInfo'}))
        elif response.meta.get('PageType') == 'BuildingInfo':
            p_name = building_base_sel.xpath('//form/table[3]/tr/td/table/tr/td/table/tr[2]/td/table/tr[1]/td/table/tr[1]/td[2]/text()').extract_first().strip()
            for building_info in building_base_sel.xpath('//form/table[3]//tr/td/table//tr/td/table//tr[2]/td/table//tr[3]/td/table//tr[3]/td/table//tr/td/table//tr/td/table/tr')[1:-1]:
                b_info = BuildingInfoItem()
                b_info['ProjectName'] = p_name
                b_info['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + get_url_id(response.url))
                b_info['BuildingName'] = building_info.xpath('./td[1]/@title').extract_first() or ''
                b_info['BuildingRegName'] = building_info.xpath('./td[2]/@title').extract_first() or ''
                b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + get_url_id(response.url) + b_info['BuildingRegName'] + b_info['BuildingName'])
                b_info['BuildingHouseNum'] = (building_info.xpath('./td[4]/text()').extract_first() or '').replace('套', '').strip()
                b_info['BuildingAddress'] = building_info.xpath('./td[3]/@title').extract_first() or ''
                b_info['BuildingArea'] = (building_info.xpath('./td[5]/text()').extract_first() or '').replace('平米', '').strip()
                b_info['BuildingURL'] = urlparse.urljoin(response.url, building_info.xpath('./td[1]/a/@href').extract_first())
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
            STATE_TAB = {'red': '不可售（因超建、查封、物业用房、回迁安置等原因）',
                            'black': '可售',
                            '#00CC00': '已售',
                            'blue': '已被开发企业抵押给金融机构，暂不可售'}
            state = ''
            for key in STATE_TAB:
                if key in string:
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

        if response.meta.get('PageType') == 'HouseInfo':
            if (not response.meta.get('ProjectName')) or (not response.meta.get('BuildingName'))\
            or (not response.meta.get('ProjectUUID')) or (not response.meta.get('BuildingUUID')):
                if result:
                    return result
                return []
            iframe_src = Selector(response).xpath('//iframe/@src').extract_first()
            houseinfodetail_href = urlparse.urljoin(response.url, iframe_src)
            response.meta.update({'PageType': 'HouseInfoDetail'})
            houseinfodetail_req = Request(url=houseinfodetail_href, method='GET',
                                            headers=headers, meta=response.meta)
            result.append(houseinfodetail_req)

        elif response.meta.get('PageType') == 'HouseInfoDetail':
            houseinfodetail_tr = Selector(response).xpath('//table[@class="table_lb1"]/tr')
            for tr in houseinfodetail_tr:
                cur_floor = tr.xpath('./td[1]/text()').extract_first().replace('第[', '').replace(']层', '')
                for house in tr.xpath('./td[@style="cursor:hand"]'):
                    hinfo = HouseInfoItem()
                    hinfo['ProjectName'] = response.meta.get('ProjectName')
                    hinfo['BuildingName'] = response.meta.get('BuildingName')
                    hinfo['ProjectUUID'] = response.meta.get('ProjectUUID')
                    hinfo['BuildingUUID'] = response.meta.get('BuildingUUID')
                    hinfo['HouseName'] = house.xpath('./font/text()').extract_first() or ''
                    hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, hinfo['HouseName'] + get_url_id(response.url))
                    hinfo['HouseFloor'] = cur_floor
                    hinfo['HouseSaleState'] = get_house_state(house.xpath('./font/@color').extract_first())
                    hinfo['HouseInfoStr'] = house.xpath('./@title').extract_first() or ''
                    result.append(hinfo)

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
