# -*- coding: utf-8 -*-
import base64
import json
import uuid

from scrapy import Request

from HouseCrawler.Items.ItemsCZ import *


# correct_val: b'"buse"', b'"ipage"'
def cracker(rows, correct_val):
    parsed_string = base64.b64decode(rows)
    need_repaired = parsed_string.split(b',')
    sick = need_repaired[0]
    repairing = sick.split(b':')
    repairing[0] = correct_val
    recovery = b'[{' + b':'.join(repairing)
    need_repaired[0] = recovery
    fin = b','.join(need_repaired)
    fin_rows = json.loads(fin.decode())
    return fin_rows


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
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectBase', 'ProjectBaseList'):
            if result:
                return result
            return []
        print('ProjectBaseHandleMiddleware')

        if response.request.method == 'GET':
            if response.meta.get('PageType') == 'ProjectBase':
                raw_data = json.loads(response.text)
                if isinstance(raw_data, str):
                    raw_data = json.loads(raw_data)
                total_entries = raw_data.get('Total')
                if total_entries:
                    total_pages = round(int(total_entries) / 10)
                    for i in range(1, total_pages + 1):
                        ysz_page_url_list = 'http://gs.czfdc.com.cn/newxgs/Pages/Code/Xjfas.ashx?' \
                                            'kfs=&lpmc=&method=GetYszData&page={page}&ysxkz='.format(page=i)
                        result.append(Request(ysz_page_url_list, meta={'PageType': 'ProjectBaseList'}))

            elif response.meta.get('PageType') == 'ProjectBaseList':
                raw_data = json.loads(response.text)
                if isinstance(raw_data, str):
                    raw_data = json.loads(raw_data)
                current_page_rows = raw_data.get('Rows')
                if current_page_rows:
                    for i, row in enumerate(current_page_rows):
                        p_base = ProjectBaseItem()
                        p_base['ProjectName'] = row.get('PRJNAME', '')
                        p_base['ProjectPresaleNum'] = row.get('PRENUM', '')
                        p_base['ProjectPresaleId'] = row.get('psaleid', '')
                        p_base['ProjectPresaleDate'] = row.get('PresaleCertificateDate', '')
                        p_base['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                           p_base['ProjectName'] + p_base['ProjectPresaleId'])
                        p_base['ProjectURL'] = 'http://gs.czfdc.com.cn/newxgs/Pages/Code/Xjfas.ashx?' \
                                               'id={}&method=GetLpJbqk'.format(p_base['ProjectPresaleId'])
                        p_base['ProjectRecordURL'] = 'http://gs.czfdc.com.cn/newxgs/Pages/Code/Xjfas.ashx?' \
                                                     'id={}&method=GetLpXmxx'.format(p_base['ProjectPresaleId'])
                        p_base['ProjectBuildingListURL'] = 'http://gs.czfdc.com.cn/newxgs/Pages/Code/Xjfas.ashx?' \
                                                           'id={}&method=GetLpLzList'.format(p_base['ProjectPresaleId'])
                        result.append(p_base)
        return result

    @staticmethod
    def process_spider_exception(response, exception, spider):
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
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectInfo', 'ProjectRecord'):
            if result:
                return result
            return []
        print('ProjectInfoHandleMiddleware')
        if response.request.method == 'GET' and response.meta.get('PageType') == 'ProjectInfo':
            raw_data = json.loads(response.text)
            if raw_data:
                info_data = raw_data[0]
                if info_data:
                    p_info = ProjectInfoItem()
                    p_info['ProjectUUID'] = response.meta['ProjectUUID']
                    p_info['ProjectName'] = response.meta['ProjectName']
                    p_info['ProjectCompany'] = info_data.get('NAME', '') or ''
                    p_info['ProjectAddress'] = info_data.get('BSIT', '') or ''
                    p_info['ProjectRegion'] = info_data.get('CZAREA', '') or ''
                    p_info['ProjectPresaleArea'] = str(info_data.get('YSROOMBAREA', '') or '')
                    p_info['ProjectPresaleHouseNum'] = str(info_data.get('YSCANSALEROOMNUMS', '') or 0.0)
                    p_info['ProjectPresaleBuildingRange'] = info_data.get('CONSNUM', '') or ''
                    p_info['ProjectSalesAgency'] = info_data.get('SalesAgency', '') or ''
                    p_info['ProjectSupervisorBank'] = info_data.get('jgyh', '') or ''
                    p_info['ProjectSupervisorAccount'] = info_data.get('jgzh', '') or ''
                    p_info['ProjectBankGuarantee'] = info_data.get('dbyh', '') or ''
                    result.append(
                        Request(response.meta['ProjectRecordURL'], meta={'PageType': 'ProjectRecord', 'Item': p_info}))

        elif response.request.method == 'GET' and response.meta.get('PageType') == 'ProjectRecord':
            p_info = response.meta['Item']
            raw_data = json.loads(response.text)
            rows = raw_data.get('Rows')
            if rows:
                fin_rows = cracker(rows, b'"buse"')
                records = []
                for i, row in enumerate(fin_rows):
                    if isinstance(row, dict):
                        record = {
                            'HouseUsage': row.get('buse', ''),
                            'HouseTotalNum': str(row.get('zts', 0.0)),
                            'HouseRecordNum': str(row.get('ybats', 0.0)),
                            'HouseNotRecordNum': str(row.get('wbats', 0.0)),
                            'HouseTotalArea': str(row.get('zmj', 0.0)),
                            'HouseRecordArea': str(row.get('ysybamj', 0.0)),
                        }
                        records.append(record)
                p_info['ProjectRecordsInfo'] = records
            result.append(p_info)

        return result

    @staticmethod
    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class BuildingInfoHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('BuildingInfo', 'HouseInfo'):
            if result:
                return result
            return []
        print('BuildingInfoHandleMiddleware')
        if response.request.method == 'GET' and response.meta.get('PageType') == 'BuildingInfo':
            raw_data = json.loads(response.text)
            if raw_data:
                for i, building in enumerate(raw_data):
                    house_id = building.get('houseid', '')
                    b_info = BuildingInfoItem()
                    b_info['ProjectUUID'] = response.meta['ProjectUUID']
                    b_info['ProjectName'] = response.meta['ProjectName']
                    b_info['ProjectPresaleNum'] = response.meta['ProjectPresaleNum']
                    b_info['BuildingName'] = building.get('housenum', '')
                    b_info['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                        b_info['ProjectUUID'] + b_info['ProjectName'] + house_id)
                    b_info['BuildingURL'] = 'http://gs.czfdc.com.cn/newxgs/Pages/Code/Xjfas.ashx?' \
                                            'method=GetShowData&houseID={}&saleSate=&cell='.format(house_id)
                    meta = response.meta
                    meta['PageType'] = 'HouseInfo'
                    meta['BuildingName'] = b_info['BuildingName']
                    meta['BuildingUUID'] = b_info['BuildingUUID']
                    result.append(b_info)
                    result.append(Request(b_info['BuildingURL'], meta=meta))

        elif response.request.method == 'GET' and response.meta.get('PageType') == 'HouseInfo':
            cells = cracker(response.text, b'"ipage"')
            if isinstance(cells, list):
                for i, cell in enumerate(cells):
                    h_info = HouseInfoItem()
                    h_info['ProjectUUID'] = response.meta['ProjectUUID']
                    h_info['ProjectName'] = response.meta['ProjectName']
                    h_info['ProjectPresaleNum'] = response.meta['ProjectPresaleNum']
                    h_info['BuildingName'] = response.meta['BuildingName']
                    h_info['BuildingUUID'] = response.meta['BuildingUUID']
                    h_info['HouseBuildingArea'] = str(cell.get('BuildingArea', ''))
                    h_info['HouseContractPrice'] = str(cell.get('ContractPrice', ''))
                    h_info['HouseUsage'] = cell.get('buse', '') or ''
                    h_info['HouseLabel'] = cell.get('roomlabel', '') or ''
                    h_info['HouseCurCell'] = cell.get('curcell', '') or ''
                    h_info['HouseSaleStatus'] = cell.get('svl', '') or ''
                    h_info['HouseUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                     str(h_info['BuildingUUID']) + cell.get('roomid', '') or '' +
                                                     h_info['HouseLabel'])
                    result.append(h_info)

        return result

    @staticmethod
    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
