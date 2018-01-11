# -*- coding: utf-8 -*-
import uuid
import datetime
from django_mongoengine import *
from django_mongoengine import fields


class SearchProjectBaseFuzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)

    SearchProjectuuid = fields.StringField(
        default='', max_length=255, null=False)

    Presalelicensenumber = fields.StringField(
        default='', max_length=255, null=False)
    Projectname = fields.StringField(default='', max_length=255, null=False)
    Permittedarea = fields.StringField(default='', max_length=255, null=False)
    Presalebuildingno = fields.StringField(
        default='', max_length=255, null=False)
    Approvaldate = fields.StringField(default='', max_length=255, null=False)
    Planenddate = fields.StringField(default='', max_length=255, null=False)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            # 'Presalelicensenumber',
            'SearchProjectuuid',
            # 'Projectname',
            # 'Permittedarea',
            # 'Presalebuildingno',
            # 'Approvaldate',
            # 'Planenddate',
            # 'change_data',

        ]
    }


class ProjectinfoBaseFuzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)

    projectuuid = fields.StringField(default='', max_length=255, null=False)
    Projectname = fields.StringField(default='', max_length=255, null=False)

    projectcounty = fields.StringField(default='', max_length=255, null=False)
    projectcomname = fields.StringField(default='', max_length=255, null=False)
    projectaddr = fields.StringField(default='', max_length=255, null=False)
    totalnum = fields.IntField(default=0, null=False)
    totalareas = fields.IntField(default=0, null=False)
    totalhousenum = fields.IntField(default=0, null=False)
    totalhouseareas = fields.IntField(default=0, null=False)
    cansalenum = fields.IntField(default=0, null=False)
    cansaleareas = fields.IntField(default=0, null=False)
    cansalehousenum = fields.IntField(default=0, null=False)
    cansalehouseareas = fields.IntField(default=0, null=False)
    prebuynum = fields.IntField(default=0, null=False)
    prebuyareas = fields.IntField(default=0, null=False)
    prebuyhousenum = fields.IntField(default=0, null=False)
    prebuyhouseareas = fields.IntField(default=0, null=False)
    salednum = fields.IntField(default=0, null=False)
    saledareas = fields.IntField(default=0, null=False)
    saledhousenum = fields.IntField(default=0, null=False)
    saledhouseareas = fields.IntField(default=0, null=False)
    registerednum = fields.IntField(default=0, null=False)
    registeredareas = fields.IntField(default=0, null=False)
    registeredhousenum = fields.IntField(default=0, null=False)
    registeredhouseareas = fields.IntField(default=0, null=False)

    projectprice = fields.StringField(default='', max_length=255, null=False)
    projectpricehouse = fields.StringField(
        default='', max_length=255, null=False)
    projectpriceback = fields.StringField(
        default='', max_length=255, null=False)
    projectpricehouseback = fields.StringField(
        default='', max_length=255, null=False)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ApprovalUrl = fields.StringField(default='', max_length=1024, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            # 'Projectname',
            # 'projectcounty',
            'projectuuid',
            # 'projectcomname',
            # 'projectaddr',
            # 'totalnum',
            # 'totalareas',
            # 'totalhousenum',
            # 'totalhouseareas',
            # 'cansalenum',
            # 'cansaleareas',
            # 'cansalehousenum',
            # 'cansalehouseareas',
            # 'prebuynum',
            # 'prebuyareas',
            # 'prebuyhousenum',
            # 'prebuyhouseareas',
            # 'salednum',
            # 'saledareas',
            # 'saledhousenum',
            # 'saledhouseareas',
            # 'registerednum',
            # 'registeredareas',
            # 'registeredhousenum',
            # 'registeredhouseareas',
            # 'projectprice',
            # 'projectpricehouse',
            # 'projectpriceback',
            # 'projectpricehouseback',
            #
            # 'change_data'
        ]
    }


class ApprovalBaseFuzhou(Document):

    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    projectno = fields.StringField(default='', max_length=255, null=False)
    projectname = fields.StringField(default='', max_length=255, null=False)
    Approvalno = fields.StringField(default='', max_length=255, null=False)
    Supervisionno = fields.StringField(default='', max_length=255, null=False)
    Supervisionbank = fields.StringField(
        default='', max_length=255, null=False)
    Approvaldate = fields.StringField(default='', max_length=255, null=False)
    Totalnum = fields.IntField(default=0, null=False)
    Totalhousenum = fields.IntField(default=0, null=False)
    Totalareas = fields.FloatField(
        default=0.00, max_digits=10, decimal_places=2)
    Totalhouseareas = fields.FloatField(
        default=0.00, max_digits=10, decimal_places=2)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            # 'projectno',
            # 'projectname',
            'Approvalno',
            # 'Supervisionno',
            # 'Supervisionbank',
            # 'Approvaldate',
            # 'Totalnum',
            # 'Totalhousenum',
            # 'Totalareas',
            # 'Totalhouseareas',
            # 'change_data',

        ]
    }


class BuildingBaseFuzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    projectno = fields.StringField(default='', max_length=255, null=False)
    projectname = fields.StringField(default='', max_length=255, null=False)

    Approvalno = fields.StringField(default='', max_length=255, null=False)
    buildingname = fields.StringField(default='', max_length=255, null=False)
    buildingno = fields.StringField(default='', max_length=255, null=False)
    buildingtotalnum = fields.IntField(default=0, null=False)
    buildingtotalareas = fields.FloatField(
        default=0.00, max_digits=10, decimal_places=2)
    buildinghousenum = fields.IntField(default=0, null=False)
    buildinghouseareas = fields.FloatField(
        default=0.00, max_digits=10, decimal_places=2)
    house_url = fields.StringField(default='', max_length=1023, null=False)

    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)

    change_data = fields.StringField(default='', max_length=1023, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'projectno',
            # 'projectname',
            'Approvalno',
            # 'buildingname',
            'buildingno',
            # 'buildingtotalnum',
            # 'buildingtotalareas',
            # 'buildinghousenum',
            # 'buildinghouseareas',
            # 'change_data',

        ]
    }


class HouseBaseFuzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    project_no = fields.StringField(default='', max_length=255, null=False)
    project_name = fields.StringField(default='', max_length=1020, null=False)
    Approvalno = fields.StringField(default='', max_length=255, null=False)
    building_no = fields.StringField(default='', max_length=255, null=False)
    building_name = fields.StringField(default='', max_length=255, null=False)
    house_no = fields.StringField(default='', max_length=255, null=False)
    house_floor = fields.StringField(default='', max_length=255, null=False)
    house_num = fields.StringField(default='', max_length=255, null=False)
    house_class = fields.StringField(default='', max_length=255, null=False)
    house_use_type = fields.StringField(default='', max_length=255, null=False)
    house_layout = fields.StringField(default='', max_length=255, null=False)
    house_area_pr_yc = fields.StringField(
        default='', max_length=510, null=False)
    house_area_pr_tn = fields.StringField(
        default='', max_length=255, null=False)
    house_area_pr_ft = fields.StringField(
        default='', max_length=255, null=False)
    house_area_pr_dx = fields.StringField(
        default='', max_length=255, null=False)
    house_area_real_yc = fields.StringField(
        default='', max_length=255, null=False)
    house_area_real_tn = fields.StringField(
        default='', max_length=255, null=False)
    house_area_real_ft = fields.StringField(
        default='', max_length=255, null=False)
    house_area_real_dx = fields.StringField(
        default='', max_length=255, null=False)
    house_sts = fields.StringField(default='', max_length=255, null=False)
    change_data = fields.StringField(default='', max_length=1023, null=False)

    house_stsLatest = fields.StringField(
        default='', max_length=255, null=False)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'project_no',  # 项目编号
            # 'project_name',
            'Approvalno',  # 开盘单元编号
            'building_no',  # 楼栋编号
            # 'building_name',
            'house_no',  # 房间编号
            # 'house_floor',  # 名义层/实际层
            # 'house_num',   # 室号
            # 'house_class',  # 房屋种类（动迁房 配套商品房 动迁安置房）
            # 'house_use_type',  # 房屋类型（居住）
            # 'house_layout',   # 房型（几室几厅）
            # 'house_area_pr_yc',   # 预测建筑面积
            # 'house_area_pr_tn',  # 预测套内面积
            # 'house_area_pr_ft',  # 预测分摊面积
            # 'house_area_pr_dx',   # 预测地下面积
            # 'house_area_real_yc',   # 实测建筑面积
            # 'house_area_real_tn',   # 实测套内面积
            # 'house_area_real_ft',  # 实测分摊面积
            # 'house_area_real_dx',   # 实测地下面积
            # 'house_sts',  # 状态
            # 'change_data'
        ]
    }
