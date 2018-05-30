# -*- coding: utf-8 -*-
import urllib.parse as urlparse
import uuid

import demjson

import regex
from scrapy import Selector
from scrapy.http import Request

from ..Items.ItemsZS import (BuildingInfoItem, HouseInfoItem, ProjectBaseItem,
                             ProjectInfoItem)


class BaseMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    @staticmethod
    def process_spider_exception(response, exception, spider):
        return


class ProjectBaseHandleMiddleware(BaseMiddleware):
    headers = {
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":
        "gzip, deflate",
        "Accept-Language":
        "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control":
        "no-cache",
        "Connection":
        "keep-alive",
        "Content-Type":
        "application/x-www-form-urlencoded",
        "Host":
        "www.zsfdc.gov.cn:9043",
        "Origin":
        "http://www.zsfdc.gov.cn:9043",
        "Pragma":
        "no-cache",
        "Referer":
        "http://www.zsfdc.gov.cn:9043/pub_ProjectQuery.aspx",
        "Upgrade-Insecure-Requests":
        "1",
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1)"
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239"
        ".84 Safari/537.36"
    }

    post_data = {
        "__EVENTTARGET":
        "",
        "__EVENTARGUMENT":
        "",
        "__VIEWSTATE":
        "l8/n7t5xZXl71XhNsvXC//rkgvZGegJbm/N43RyLKSydPjrV9nPgAw9H3j963UpASG75tmTE8LKNyEJUi8mE3FLNsJ0K0+rFBRTznAzomtx3/5Ih9ZvpVC9p4g6IXCirRqUpRstU+vOz5wQjd6GOkBHvSbTIfMGB9Wi96RHTIriqjkuf9k11BZR89VAQEqgAuHKugzlN+Dm4coYpcnhXWoWZLQajNh3AL4X54kNIQd41f0dzku0Tk9IXR49lpT2qtFILrKiGpaX9BLdRbSIiE0Zt+TYieL/Pp//vzJYvOHr9pJgDVdFoCNFDx6zffWaQix3H5zVz1/TT4NQd7hVVSTrNmCRLgyH8bCty5DuJL8dXCBTz7eStsA7R3ZfV8TQjY0XfH7Od20+c2bk16zkgrOKFVDBf7gW8g7XV5ER5DSi+UQMa4+6tBnyFvjwezxSVaR0d8JuInicWSELfVyqbcsuUmfiUTChH/FC3b7s2PuYqwVubOQLeuz+6055YduIiQOaIbJHjns0H2ZlyAqfsgZbMFDbKHY63Fae6OPHNi3xAMDfGNVe32TrSEyP6XDd6oIxcP/qXwbBGlZDRnopnJrwvvO5EJPd6pazE2mW5erXBW1JxgFpoiKjz5UIHyNUoP78ufxvd+ueqiXs/IVw8GqU2RkcKt1fuTf0cknYMve5kJjgHF4Rn79I/dVH1D4ELfNOQSXGCkzEaiTBK341W1GS6a4JPNB2UZnOmdLmYyO1kGNdEIdAlw10wgCou1Y9xHWn1y4mVwpGARvL4+xGqn+D+4MNK4ZFJjFmgyMm3PNXRH36FDxlukU0WHCt5gawupsxU8fTk1eUARGJFtt2UZ0vp5zUiNJQx7htKYwD89Lzut1KswJ3w5ONhxH0bmcqywQekR5KSzLo0qWcxnIYBE2zvx33O1LyBfiRFZSdsCQeBRqYe2d7MROGSH85m1EE2rCFOSgwCFey+KRa4rqZMjJbq2j41QkdN99nkAEuRTGslhMw5VXsYVHBJCnXZeeV+jt8k0pmIvFpqY0J5l3E1pJM3kkjpIKU+0HIckTlzjiJQynhMZaAjtsxaU9g5S8AbYSBjtNc7EVgd3wEEQVvtOSRkw4MACkKlitAouA==",
        "__EVENTVALIDATION":
        "SYf959dYiECdQD8FElc7P7iJmgeoGeI9EqPkA8bAieDy6c7zYQIbAqPFfaf16//1ReElmNoI/YBbwNWrOXEdX15+C7OO9y0zf3KEZTpIlNylgR8DKgZHerxi5pZlk2RZC9nPzscOulXP1lSKO0N7iFqmBg0jEj/fYMrikVi6M5Svf4/0iLHgIEIKJ0qacr4D06CVRzArxCBtZs4rF1cPwWyn4hZ4sYEeLF3I0TCQBtHWt5bEGMel9Px68kJdBeXo08L2eDHBM4ML7RsSXrWWv4KfhHf6H8Vn5H2XVsrU+6XNj5hGvEkxcZ49dGw7I2E2U9vk92qrJuBZiGIjJ9qd0RBD6Zb8SgqnTGkuuX6WZwdAM4EqHkeJif2kEFbsawALRl1cts+tWf97Uidi",
        "searchinput":
        "",
        "ctl00$ContentPlaceHolder1$tbxProjectName":
        "",
        "ctl00$ContentPlaceHolder1$ddlDistrict":
        "01",
        "ctl00$ContentPlaceHolder1$tbxAddress":
        "",
        "ctl00$ContentPlaceHolder1$tbxDeveloper":
        "",
        "ctl00$ContentPlaceHolder1$tbxPrescaleCert":
        "",
        "ctl00$ContentPlaceHolder1$ImageButton1.x":
        "20",
        "ctl00$ContentPlaceHolder1$ImageButton1.y":
        "15",
        "ctl00$ContentPlaceHolder1$newPage":
        "",
    }
    url = "http://www.zsfdc.gov.cn:9043/pub_ProjectQuery.aspx"

    def process_spider_output(self, response, result, spider):
        result = list(result)
        print(response)
        if not (200 <= response.status < 300):    # common case
            if result:
                return result
            return []

        if response.meta.get('PageType') not in (
                'ProjectInitial',
                'ProjectBase',
        ):
            if result:
                return result
            return []

        sel = Selector(text=response.body_as_unicode())
        if response.meta.get('PageType') == 'ProjectInitial':
            print('ProjectBaseHandleMiddleware -- ProjectInitial')
            area = response.meta.get("ProjectAdminArea", "")
            num = response.meta.get("ProjectAdminAreaNum", "")
            page_div = sel.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_pageInfo"]/text()'
            ).extract_first() or ''
            total_page_count, current_page = self.extract_page(page_div)
            result_container = list()
            if current_page == 1 and total_page_count != 0:
                for page in range(1, total_page_count + 1):
                    self.post_data["ctl00$ContentPlaceHolder1$newPage"] = str(
                        page)
                    self.post_data[
                        "ctl00$ContentPlaceHolder1$ddlDistrict"] = num
                    body = urlparse.urlencode(self.post_data)
                    r = Request(
                        self.url,
                        body=body,
                        method="POST",
                        headers=self.headers,
                        meta={
                            'PageType': 'ProjectBase',
                            'ProjectAdminArea': area,
                            'ProjectAdminNum': num
                        })
                    result_container.append(r)
            result.extend(result_container)

        elif response.meta.get('PageType') == 'ProjectBase':
            print('ProjectBaseHandleMiddleware -- ProjectBase')
            table = sel.xpath('//*[@id="ctl00_ContentPlaceHolder1_gvProject"]')
            area = response.meta.get("ProjectAdminArea", "")
            # num = response.meta.get("ProjectAdminAreaNum", "")
            if table:
                rows = table[0].xpath(
                    './tr[@class="listrow2"] | ./tr[@class="listrow1"]')
                item_list = []
                url_prefix = 'http://www.zsfdc.gov.cn:9043/'
                for row in rows:
                    item = ProjectBaseItem()
                    project = row.xpath(
                        './td[1]/span/text()').extract_first() or ''
                    presale = row.xpath(
                        './td[2]/span/text()').extract_first() or ''
                    permit_date = row.xpath(
                        './td[3]/span/text()').extract_first() or ''
                    permit_flat = row.xpath(
                        './td[4]/span/text()').extract_first() or ''
                    forsale_flat = row.xpath(
                        './td[5]/span/text()').extract_first() or ''
                    project_info = row.xpath(
                        './td[6]/a/@href').extract_first() or ''
                    project_sale = row.xpath(
                        './td[7]/a/@href').extract_first() or ''
                    item['ProjectAdminArea'] = area
                    item['ProjectName'] = project
                    item['PresaleNum'] = presale
                    item['ProjectPermitDate'] = permit_date
                    item['ProjectPermitFlat'] = permit_flat
                    item['ProjectForsaleFlat'] = forsale_flat
                    item['ProjectInfoURL'] = url_prefix + project_info
                    item['ProjectSaleHistoryURL'] = url_prefix + project_sale
                    item['ProjectUUID'] = uuid.uuid3(
                        uuid.NAMESPACE_DNS,
                        area + project + presale + project_info)
                    if project:
                        item_list.append(item)
                result.extend(item_list)

        return result

    @staticmethod
    def extract_page(text):
        result = regex.search(r'分(\d+.*?)页.*第(\d+.*?)页', text)
        result.groups()
        if result:
            return int(result.group(1)), int(result.group(2))
        return 0, 1


class ProjectInfoHandleMiddleware(BaseMiddleware):
    headers = {
        'Host':
        'www.zsfdc.gov.cn:9043',
        'Connection':
        'keep-alive',
        'Content-Length':
        '85',
        'Pragma':
        'no-cache',
        'Cache-Control':
        'no-cache',
        'Accept':
        'text/html, */*',
        'Origin':
        'http://www.zsfdc.gov.cn:9043',
        'X-Requested-With':
        'XMLHttpRequest',
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Content-Type':
        'application/x-www-form-urlencoded',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh-CN,zh;q=0.9'
    }

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):
            if result:
                return result
            return []

        if response.meta.get('PageType') not in ('ProjectInfo',
                                                 'BuildingInfo'):
            if result:
                return result
            return []

        sel = Selector(text=response.body_as_unicode())
        if response.meta.get('PageType') == 'ProjectInfo':
            item = ProjectInfoItem()
            item['ProjectUUID'] = response.meta.get('ProjectUUID')
            item['ProjectName'] = response.meta.get('ProjectName')
            item['PresaleNum'] = response.meta.get('PresaleNum')
            item['ProjectPermitDate'] = response.meta.get('ProjectPermitDate')
            company = sel.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Layout1_Label3"]/text()'
            ).extract_first(default='')
            address = sel.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Layout1_Label4"]/text()'
            ).extract_first(default='')
            presale_valid = sel.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Layout1_Label7"]/text()'
            ).extract_first(default='')
            terminate_time = sel.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_Layout1_Label8"]/text()'
            ).extract_first(default='')
            # 省略销售历史
            item['ProjectCompany'] = company.strip()
            item['ProjectAddress'] = address.strip()
            item['ProjectPresaleValid'] = presale_valid.strip()
            item['ProjectTerminateCount'] = terminate_time.strip()
            result.append(item)

            building_table = sel.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_gvBuild"]')
            b_rows = building_table.xpath(
                './tr[@class="listrow2"] | ./tr[@class="listrow1"]')
            building_list = []
            for i, b_row in enumerate(b_rows):
                b_vals = b_row.xpath('./td/span/text()').extract()
                b_raw_house_url = b_row.xpath('./td/a/@href').extract_first()
                b_house_args = self.extract_url(b_raw_house_url)
                if b_house_args:
                    recnumgather, buildnum = b_house_args[0]
                    sbk = self.extract_session_sbk(
                        response.headers.getlist('Set-Cookie'))
                    sid = self.extract_session_sid(
                        response.headers.getlist('Set-Cookie'))
                    b_item = BuildingInfoItem()
                    b_item['ProjectUUID'] = response.meta.get('ProjectUUID')
                    b_item['ProjectName'] = response.meta.get('ProjectName')
                    b_item['BuildingSaleStatus'] = b_vals[0]
                    b_item['BuildingName'] = b_vals[1]
                    b_item['BuildingPermitFlat'] = b_vals[2]
                    b_item['BuildingSold'] = b_vals[3]
                    b_item['BuildingAvailable'] = b_vals[4]
                    b_item['BuildingStartDate'] = b_vals[5]
                    b_item['BuildingEndDate'] = b_vals[6]
                    b_item['BuildingTerminateCounts'] = b_vals[7]
                    b_item['HouseInfoURLArgs'] = ';'.join(
                        (recnumgather, buildnum, sbk, item['ProjectAddress'],
                         sid))
                    b_item['BuildingUUID'] = uuid.uuid3(
                        uuid.NAMESPACE_DNS, item['ProjectUUID'] +
                        b_item['BuildingName'] + recnumgather + buildnum)
                    building_list.append(b_item)
            result.extend(building_list)

        return result

    @staticmethod
    def extract_url(text):
        result = regex.search(r"recnumgather=(\d+).buildnum=(\d+)", text)
        return result.groups() if result else '', ''

    @staticmethod
    def extract_session_sbk(session_list):
        sbk = None
        for i, session in enumerate(session_list):
            if b'sbk' in session:
                sbk = session
                break
        if sbk:
            value = regex.search(r"sbk=(.*?);", str(sbk))
            return value.group(1) if value else ''

        return ''

    @staticmethod
    def extract_session_sid(session_list):
        sbk = None
        for i, session in enumerate(session_list):
            if b'ASP.NET_SessionId' in session:
                sbk = session
                break
        if sbk:
            value = regex.search(r"ASP.NET_SessionId=(.*?);", str(sbk))
            return value.group(1) if value else ''

        return ''


class HouseInfoHandleMiddleware(BaseMiddleware):
    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):
            if result:
                return result
            return []

        if response.meta.get('PageType') not in ('HouseInfo', ):
            if result:
                return result
            return []

        if response.meta.get('PageType') == 'HouseInfo':
            print('HouseInfoHandleMiddleware')
            raw_data = response.body_as_unicode()
            json_data = demjson.decode(raw_data[1:-1])
            if json_data.get('succ') in (True, 'true', 'True'):
                #admraw_datain_area = response.meta.get('ProjectAdminArea')
                project_uuid = response.meta.get('ProjectUUID')
                building_uuid = response.meta.get('BuildingUUID')
                project_name = response.meta.get('ProjectName')
                building_name = response.meta.get('BuildingName')
                raw_build_table = json_data.get('buildtable')
                sel = Selector(text=raw_build_table)
                table = sel.xpath('//table/tr[@class="brw"]')[1:]
                floor_indexes = {}
                for i, row in enumerate(table):
                    floor = row.xpath(
                        './td[@class="blt"]/text()').extract_first(default='')
                    rooms = row.xpath('.//*/@id').extract()
                    if floor and rooms:
                        for room in rooms:
                            floor_indexes[room] = floor
                raw_build_list = json_data.get('buildlist')
                build_list = demjson.decode(raw_build_list[1:-1])
                house_info_list = []
                for j, (house_id, house_info) in enumerate(build_list.items()):
                    house_id_ix = 'hd_{}'.format(str(house_id))
                    house_floor = floor_indexes.get(house_id_ix, '')
                    house_shared_area = house_info.get('aa', '')
                    house_build_area = house_info.get('ba', '')
                    house_internal_area = house_info.get('ia', '')
                    house_status = house_info.get('hp', '')
                    house_type = house_info.get('ht', '')
                    house_address = house_info.get('si', '')
                    house_usage = house_info.get('hu', '')
                    house_name = house_info.get('dn', '')
                    # house_owner = house_info.get('on', '')
                    house_contract_num = house_info.get('cer', '')
                    item = HouseInfoItem()
                    item['HouseUUID'] = uuid.uuid3(
                        uuid.NAMESPACE_DNS,
                        project_uuid + building_uuid + str(house_id))
                    item['ProjectUUID'] = project_uuid
                    item['ProjectName'] = project_name
                    item['BuildingUUID'] = building_uuid
                    item['BuildingName'] = building_name
                    item['HouseName'] = house_name
                    item['HouseUsage'] = house_usage
                    item['HouseSaleState'] = house_status
                    item['HouseFloor'] = house_floor
                    item['HouseSharedArea'] = house_shared_area
                    item['HouseBuildArea'] = house_build_area
                    item['HouseInternalArea'] = house_internal_area
                    item['HouseType'] = house_type
                    item['HouseAddress'] = house_address
                    item['HouseContractNum'] = house_contract_num
                    house_info_list.append(item)
                result.extend(house_info_list)
        return result
