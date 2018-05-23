# -*- coding: utf-8 -*-
import urllib.parse as urlparse

from scrapy import Selector
from scrapy.http import Request


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
    pass


class HouseInfoHandleMiddleware(BaseMiddleware):
    pass
