# coding = utf-8
import sys
import uuid
import copy
import regex
import traceback
from scrapy import Request
from scrapy import Selector
from HouseNew.models import *
from HouseCrawler.Items.ItemsBJJS import *
from collections import OrderedDict
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


class ProjectBaseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    headers = {'Host': 'www.bjjs.gov.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://www.bjjs.gov.cn',
                'Upgrade-Insecure-Requests': 1,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'http://www.bjjs.gov.cn/eportal/ui?pageId=307678&isTrue=',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'}

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        def get_total_page(string):
            total_page = 0
            try:
                search_result = regex.search(r'checkCurrentPage.+value,(?<pagenum>\d+)',
                                                str(string))
                if search_result:
                    total_page = int(search_result.group(1))
            except Exception:
                traceback.print_exc()
            return total_page

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
            req_dict = {'isTrue': 0,
                        'projectName': '项目名称关键字',
                        'rblFWType': 'q', 'txtYS': '', 'txtZH': '',
                        'txtCQZH': '证号关键字',
                        'developer': '单位名称关键字',
                        'txtaddress': '地址关键字',
                        'isTrue': 1, 'ddlQX': -1, 'rblFWType1': 'q',
                        'ddlYT': -1, 'ddlFW': -1, 'ddlQW': -1, 'ddlQY': -1,
                        'ddlHX': -1, 'ddlJJ': -1, 'currentPage': 1,
                        'pageSize': 15}
            page_count = get_total_page(response.body_as_unicode())
            req_list = []
            print('maxpage', page_count)
            for cur_page in range(1, page_count + 1):
                req_dict['currentPage'] = cur_page
                req_body = urlparse.urlencode(req_dict)
                req_list.append(Request(url=response.url, body=req_body, method='POST',
                                headers=self.headers, meta={'PageType': 'ProjectBase'}))
            result.extend(req_list)
        elif response.request.method == 'POST':
            print('currentpage', Selector(response).xpath('//input[@id="jumpPageBox"]/@value').extract_first())
            project_list = Selector(response).xpath('//table[@cellspacing="0"]/tr[@align="center"]')
            pb_list = []
            for p in project_list:
                parsed_url = urlparse.urlparse(response.url)
                p_host = parsed_url.scheme + "://" + parsed_url.hostname
                p_name = p.xpath('./td[1]/a/text()').extract()[0]
                p_href = urlparse.urljoin(p_host, p.xpath('./td[1]/a/@href').extract()[0])
                p_regname = p.xpath('./td[2]/a/text()').extract()[0]
                p_regtime = p.xpath('./td[3]/text()').extract()[0]
                pb = ProjectBaseItem()
                pb['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + p_regname)
                pb['ProjectName'] = p_name
                pb['ProjectURL'] = p_href
                pb['ProjectRegName'] = p_regname
                pb['ProjectRegTime'] = p_regtime
                pb_list.append(pb)
            result.extend(pb_list)
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

    headers = {'Host': 'www.bjjs.gov.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://www.bjjs.gov.cn',
                'Upgrade-Insecure-Requests': 1,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'http://www.bjjs.gov.cn/eportal/ui?pageId=307678&isTrue=',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'}

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        def get_total_page(string):
            total_page = 0
            try:
                search_result = regex.search(r'checkCurrentPage.+value,(?<pagenum>\d+)',
                                                str(string))
                if search_result:
                    total_page = int(search_result.group(1))
            except Exception:
                traceback.print_exc()
            return total_page

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfo', 'SubProjectList', 'SubProjectInfo'):
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')

        if response.meta.get('PageType') == 'ProjectInfo':
            pinfo_sel = Selector(response)
            pinfo = ProjectInfoItem()
            pinfo['ProjectName'] = pinfo_sel.xpath('//td[@id="项目名称"]/text()').extract()[0]\
                                    .replace('\r\n', '').replace(' ', '')
            pinfo['ProjectAddress'] = pinfo_sel.xpath('//td[@id="坐落位置"]/text()').extract()[0]\
                                    .replace('\r\n', '').replace(' ', '')
            pinfo['ProjectCompany'] = pinfo_sel.xpath('//td[@id="开发企业"]/text()').extract()[0]\
                                    .replace('\r\n', '').replace(' ', '')
            pinfo['ProjectCorporationCode'] = pinfo_sel.xpath('//td[@id="行政相对人代码"]/text()').extract()[0]\
                                    .replace('\r\n', '').replace(' ', '')
            pinfo['ProjectCorporation'] = pinfo_sel.xpath('//td[@id="法定代表人姓名"]/text()').extract()[0]\
                                    .replace('\r\n', '').replace(' ', '')
            pinfo['ProjectRegName'] = pinfo_sel.xpath('//td[@id="预售许可证编号"]/text()').extract()[0]\
                                    .replace('\r\n', '').replace(' ', '')
            pinfo['ProjectRegTime'] = pinfo_sel.xpath('//td[@id="发证日期"]/text()').extract()[0]\
                                    .replace('\r\n', '').replace(' ', '')
            pinfo['ProjectUsage'] = pinfo_sel.xpath('//td[@id="土地用途和使用年限"]/text()').extract()[0]\
                                    .replace('\r\n', '').replace(' ', '')
            pinfo['ProjectArea'] = pinfo_sel.xpath('//td[@id="准许销售面积"]/text()').extract()[0]\
                                    .replace('\r\n', '').replace(' ', '')
            pinfo['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, pinfo['ProjectName'] + pinfo['ProjectRegName'])
            if '点击进入现房销售信息公示' not in response.body_as_unicode():
                pinfo['SubProjectUUID'] = pinfo['ProjectUUID']
                pinfo['SubProjectAddress'] = pinfo['ProjectAddress']
                pinfo['ProjectSaleSum'] = OrderedDict([('null', True)])
                sale_list = pinfo_sel.xpath('//table[@class="cont_titlebg2" and not(@id)]/tr[2]/td/table[1]/tr[position()>1]')
                for sale_item in sale_list:
                    pinfo['ProjectSaleSum']['null'] = False
                    pinfo['ProjectSaleSum'][sale_item.xpath('./td[1]/text()').extract()[0]] = OrderedDict([('已签约套数', int(sale_item.xpath('./td[2]/text()').extract()[0])),
                                                                                                ('已签约面积', float(sale_item.xpath('./td[3]/text()').extract()[0])),
                                                                                                ('成交均价', float(sale_item.xpath('./td[4]/text()').extract()[0]))])
                result.append(pinfo)

            else:
                parsed_url = urlparse.urlparse(response.url)
                pinfo_host = parsed_url.scheme + "://" + parsed_url.hostname
                subproject_list_href = urlparse.urljoin(pinfo_host,
                                    pinfo_sel.xpath('//td[@id="现房销售"]/a/@href').extract()[0])
                req = Request(url=subproject_list_href, meta={'PageType': 'SubProjectList', 'item': pinfo}, method='GET', dont_filter=True)
                result.append(req)

        if response.meta.get('PageType') == 'SubProjectList':
            subpinfo_base = response.meta.get('item')
            subpinfo_sel = Selector(response)
            subpinfo_list = subpinfo_sel.xpath('//tr[@style="font-size:12px;"]')
            req_list = []
            for subpinfo_item in subpinfo_list:
                subpinfo = copy.deepcopy(subpinfo_base)
                subpinfo['ProjectLicenseCode'] = subpinfo_item.xpath('./td[2]/a/text()').extract()[0]
                subpinfo['ProjectLicenseDate'] = subpinfo_item.xpath('./td[3]/text()').extract()[0]\
                                                    .replace('\r\n', '').replace(' ', '')
                parsed_url = urlparse.urlparse(response.url)
                pinfo_host = parsed_url.scheme + "://" + parsed_url.hostname
                subproject_href = urlparse.urljoin(pinfo_host,
                                    subpinfo_item.xpath('./td[2]/a/@href').extract()[0])
                subpinfo['SubProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                    str(subpinfo['ProjectUUID']) + subpinfo['ProjectLicenseCode'] + subproject_href)
                req_list.append(Request(url=subproject_href, meta={'PageType': 'SubProjectInfo', 'item': subpinfo}, method='GET', dont_filter=True))
            result.extend(req_list)

        if response.meta.get('PageType') == 'SubProjectInfo':
            subpinfo_base = response.meta.get('item')
            subpinfo_sel = Selector(response)
            subpinfo = copy.deepcopy(subpinfo_base)
            subpinfo['ProjectSaleSum'] = OrderedDict([('null', True)])
            sale_list = subpinfo_sel.xpath('//table[@class="cont_titlebg2" and not(@id)]/tr[2]/td/table[1]/tr[position()>1]')
            for sale_item in sale_list:
                subpinfo['ProjectSaleSum']['null'] = False
                subpinfo['ProjectSaleSum'][sale_item.xpath('./td[1]/text()').extract()[0]] = OrderedDict([('已签约套数', int(sale_item.xpath('./td[2]/text()').extract()[0])),
                                                                                                ('已签约面积', float(sale_item.xpath('./td[3]/text()').extract()[0])),
                                                                                                ('成交均价', float(sale_item.xpath('./td[4]/text()').extract()[0]))])
            result.append(subpinfo)
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

    headers = {'Host': 'www.bjjs.gov.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://www.bjjs.gov.cn',
                'Upgrade-Insecure-Requests': 1,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'}

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        def get_total_page(string):
            total_page = 0
            try:
                search_result = regex.search(r'checkCurrentPage.+value,(?<pagenum>\d+)',
                                                str(string))
                if search_result:
                    total_page = int(search_result.group(1))
            except Exception:
                traceback.print_exc()
            return total_page

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfo', 'SubProjectInfo', 'SubBuildingList'):
            if result:
                return result
            return []
        print('BuildingListHandleMiddleware')

        if response.meta.get('PageType') in ('ProjectInfo', 'SubProjectInfo'):
            building_list_sel = Selector(response)
            if response.meta.get('PageType') == 'ProjectInfo':
                p_name = building_list_sel.xpath('//td[@id="项目名称"]/text()').extract()[0]\
                                    .replace('\r\n', '').replace(' ', '')
                p_regname = building_list_sel.xpath('//td[@id="预售许可证编号"]/text()').extract()[0]\
                                    .replace('\r\n', '').replace(' ', '')
                p_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + p_regname)
                sp_uuid = p_uuid
            elif response.meta.get('PageType') == 'SubProjectInfo':
                p_uuid = response.meta.get('item').get('ProjectUUID')
                sp_uuid = response.meta.get('item').get('SubProjectUUID')
            if building_list_sel.xpath('//a[text()="查看更多>>"]/@href') != []:
                parsed_url = urlparse.urlparse(response.url)
                p_host = parsed_url.scheme + "://" + parsed_url.hostname
                building_list_href = urlparse.urljoin(p_host,
                                        building_list_sel.xpath('//a[text()="查看更多>>"]/@href').extract_first())
                binfo = BuildingInfoItem()
                binfo['ProjectName'] = building_list_sel.xpath('//td[@id="项目名称"]/text()').extract_first()\
                                        .replace('\r\n', '').replace(' ', '')
                binfo['ProjectUUID'] = p_uuid
                binfo['SubProjectUUID'] = sp_uuid
                building_list_req = Request(url=building_list_href, method='GET',
                                            headers=self.headers, meta={'PageType': 'SubBuildingList', 'item': binfo})
                result.append(building_list_req)
            else:
                building_list = building_list_sel.xpath('//div[@id=""]/table[@class="cont_titlebg2" and not(@id)]/tr[2]/td/span[@id="Span1"]/table/tr[position()>0]')
                for building_item in building_list:
                    binfo = BuildingInfoItem()
                    parsed_url = urlparse.urlparse(response.url)
                    p_host = parsed_url.scheme + "://" + parsed_url.hostname
                    binfo['ProjectName'] = building_list_sel.xpath('//td[@id="项目名称"]/text()').extract_first()\
                                            .replace('\r\n', '').replace(' ', '')
                    binfo['ProjectUUID'] = p_uuid
                    binfo['SubProjectUUID'] = sp_uuid
                    binfo['BuildingName'] = building_item.xpath('./td[1]/text()').extract_first() or ''
                    url_namespace = building_item.xpath('./td[6]/a/@href').extract_first()
                    binfo['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, str(binfo['SubProjectUUID']) + binfo['BuildingName'] + url_namespace)
                    binfo['BuildingSaleNum'] = (building_item.xpath('./td[2]/text()').extract_first() or '0').\
                                                replace('\r\n', '').replace(' ', '').replace('\t', '')
                    binfo['BuildingSaleNum'] = '0' if binfo['BuildingSaleNum'] == '' else binfo['BuildingSaleNum']
                    binfo['BuildingSaleArea'] = (building_item.xpath('./td[3]/text()').extract_first() or '0.0').\
                                                replace('\r\n', '').replace(' ', '').replace('\t', '')
                    binfo['BuildingSaleArea'] = '0.0' if binfo['BuildingSaleArea'] == '' else binfo['BuildingSaleArea']
                    binfo['BuildingSaleStatus'] = (building_item.xpath('./td[4]/text()').extract_first() or '').\
                                                replace('\r\n', '').replace(' ', '').replace('\t', '')
                    binfo['BuildingSalePrice'] = (building_item.xpath('./td[5]/text()').extract_first() or '0.0').\
                                                replace('\r\n', '').replace(' ', '').replace('\t', '')
                    binfo['BuildingSalePrice'] = '0.0' if binfo['BuildingSalePrice'] == '' else binfo['BuildingSalePrice']
                    if url_namespace != "#":
                        binfo['BuildingURL'] = urlparse.urljoin(p_host,
                                                building_item.xpath('./td[6]/a/@href').extract_first() or '')
                    else:
                        pass
                    result.append(binfo)

        if response.meta.get('PageType') == 'SubBuildingList':
            if response.request.method == 'GET':
                binfo_base = response.meta.get('item')
                req_dict = {'currentPage': 1,
                            'pageSize': 20}
                page_count = get_total_page(response.body_as_unicode())
                for cur_page in range(1, page_count + 1):
                    binfo_sub = copy.deepcopy(binfo_base)
                    req_dict['currentPage'] = cur_page
                    req_body = urlparse.urlencode(req_dict)
                    result.append(Request(url=response.url, body=req_body, method='POST',
                                    headers=self.headers, meta={'PageType': 'SubBuildingList', 'item': binfo_sub}))
            elif response.request.method == 'POST':
                binfo_base = response.meta.get('item')
                subbuilding_list = Selector(response).xpath('//span[@id="Span1"]//table/tr[not(@class)]')
                parsed_url = urlparse.urlparse(response.url)
                p_host = parsed_url.scheme + "://" + parsed_url.hostname
                for sub_b in subbuilding_list:
                    binfo = copy.deepcopy(binfo_base)
                    binfo['BuildingName'] = sub_b.xpath('./td[1]/a/text()').extract_first() or ''
                    url_namespace = building_item.xpath('./td[6]/a/@href').extract_first()
                    binfo['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, str(binfo['SubProjectUUID']) + binfo['BuildingName'] + url_namespace)
                    binfo['BuildingSaleNum'] = (sub_b.xpath('./td[2]/text()').extract_first() or '0').\
                                                replace('\r\n', '').replace(' ', '').replace('\t', '')
                    binfo['BuildingSaleNum'] = '0' if binfo['BuildingSaleNum'] == '' else binfo['BuildingSaleNum']
                    binfo['BuildingSaleArea'] = (sub_b.xpath('./td[3]/text()').extract_first() or '0.0').\
                                                replace('\r\n', '').replace(' ', '').replace('\t', '')
                    binfo['BuildingSaleArea'] = '0.0' if binfo['BuildingSaleArea'] == '' else binfo['BuildingSaleArea']
                    binfo['BuildingSaleStatus'] = (sub_b.xpath('./td[4]/text()').extract_first() or '').\
                                                replace('\r\n', '').replace(' ', '').replace('\t', '')
                    binfo['BuildingSalePrice'] = (sub_b.xpath('./td[5]/text()').extract_first() or '0.0').\
                                                replace('\r\n', '').replace(' ', '').replace('\t', '')
                    binfo['BuildingSalePrice'] = '0.0' if binfo['BuildingSalePrice'] == '' else binfo['BuildingSalePrice']
                    if url_namespace != "#":
                        binfo['BuildingURL'] = urlparse.urljoin(p_host,
                                                building_item.xpath('./td[6]/a/@href').extract_first() or '')
                    else:
                        pass
                    result.append(binfo)
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

    headers = {'Host': 'www.bjjs.gov.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://www.bjjs.gov.cn',
                'Upgrade-Insecure-Requests': 1,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'}

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        def get_house_state(string):
            STATE_TAB = {'background:#CCCCCC': '不可售',
                            'background:#33CC00': '可售',
                            'background:#FFCC99': '已预订',
                            'background:#FF0000': '已签约',
                            'background:#ffff00': '已办理预售项目抵押',
                            'background:#d2691e': '网上联机备案',
                            'background:#00FFFF': '资格核验中'}
            state = ''
            for key in STATE_TAB:
                if key in string:
                    state = STATE_TAB[key]
                    break
            return state

        def get_detail_key(string):
            KEY_TAB = {'规划设计用途': 'HouseUsage',
                        '户　　型': 'HouseStructure',
                        '建筑面积': 'HouseBuildingArea',
                        '套内面积': 'HouseInnerArea',
                        '按建筑面积拟售单价': 'HouseBuildingUnitPrice',
                        '按套内面积拟售单价': 'HouseInnerUnitPrice'}
            return KEY_TAB.get(string)

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
            or (not response.meta.get('ProjectUUID')) or (not response.meta.get('SubProjectUUID'))\
            or (not response.meta.get('BuildingUUID')):
                if result:
                    return result
                return []
            floor_list = Selector(response).xpath('//table[@id="table_Buileing"]/tbody/tr[not(@bgcolor)]')
            for floor_item in floor_list:
                cur_floor = floor_item.xpath('./td[1]/text()').extract_first()
                cur_floor_sale = floor_item.xpath('./td[2]/text()').extract_first()
                house_list = floor_item.xpath('./td[3]/div')
                for house_item in house_list:
                    hinfo = HouseInfoItem()
                    hinfo['ProjectName'] = response.meta.get('ProjectName')
                    hinfo['BuildingName'] = response.meta.get('BuildingName')
                    hinfo['ProjectUUID'] = response.meta.get('ProjectUUID')
                    hinfo['SubProjectUUID'] = response.meta.get('SubProjectUUID')
                    hinfo['BuildingUUID'] = response.meta.get('BuildingUUID')
                    hinfo['HouseName'] = house_item.xpath('./a/text()').extract_first()
                    hinfo['HouseFloor'] = cur_floor
                    hinfo['HouseFloorSale'] = cur_floor_sale
                    hinfo['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                    hinfo['BuildingUUID'] + hinfo['HouseName'] + hinfo['HouseFloor'] + hinfo['HouseFloorSale'])
                    hinfo['HouseState'] = get_house_state(house_item.xpath('./@style').extract_first())
                    if house_item.xpath('./span[@class="f12a6"]') != []:
                        hinfo['HouseSubState'] = '已办理预售项目抵押'
                    if house_item.xpath('./a/@href').extract_first() == "#":
                        result.append(hinfo)
                    else:
                        parsed_url = urlparse.urlparse(response.url)
                        p_host = parsed_url.scheme + "://" + parsed_url.hostname
                        houseinfodetail_href = urlparse.urljoin(p_host,
                                                house_item.xpath('./a/@href').extract_first())
                        houseinfodetail_req = Request(url=houseinfodetail_href, method='GET',
                                                        headers=self.headers, meta={'PageType': 'HouseInfoDetail', 'item': hinfo})
                        result.append(houseinfodetail_req)

        if response.meta.get('PageType') == 'HouseInfoDetail':
            hinfo_base = response.meta.get('item')
            houseinfodetail_list = Selector(response).xpath('//div[@id="showDiv"]/table/tr[td[@id="desc"]]')
            for houseinfodetail_item in houseinfodetail_list:
                key_name = get_detail_key(str(houseinfodetail_item.xpath('./td[1]/text()').extract_first()))
                if key_name:
                    hinfo_base[key_name] = houseinfodetail_item.xpath('./td[2]/text()').extract_first()\
                                                .replace('\r\n', '').replace(' ', '').replace('\t', '')\
                                                .replace('平方米', '').replace('元', '').replace('/', '')
            result.append(hinfo_base)

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
