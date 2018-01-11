# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


# Suzhou Models
class ApprovalBaseSuzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default='', max_length=255, null=False)
    PresalePermitNumber = fields.StringField(
        default='', max_length=255, null=False)
    PresalePPCORPName = fields.StringField(
        default='', max_length=255, null=False)
    PresaleProName = fields.StringField(default='', max_length=255, null=False)
    PresaleProAddress = fields.StringField(
        default='', max_length=255, null=False)
    PresalePreSumArea = fields.StringField(
        default='', max_length=255, null=False)
    PresaleZGArea = fields.StringField(default='', max_length=255, null=False)
    PresaleZGCount = fields.StringField(default='', max_length=255, null=False)
    PresaleFZGArea = fields.StringField(default='', max_length=255, null=False)
    PresaleFZGCount = fields.StringField(
        default='', max_length=255, null=False)
    PresaleQTArea = fields.StringField(default='', max_length=255, null=False)
    PresaleQTCount = fields.StringField(default='', max_length=255, null=False)
    PresalePPIDate = fields.StringField(default='', max_length=255, null=False)
    PresaleJZIDate = fields.StringField(default='', max_length=255, null=False)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    SourceUrl = fields.URLField(default=None, blank=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'PresalePermitNumber',
            'NewCurTimeStamp'
        ]
    }


class ProjectBaseSuzhou(Document):

    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    project_no = fields.StringField(default='', max_length=255, null=False)
    project_addr = fields.StringField(default='', max_length=255, null=False)
    project_name = fields.StringField(default='', max_length=255, null=False)
    project_area = fields.StringField(default='', max_length=255, null=False)
    project_com_name = fields.StringField(
        default='', max_length=255, null=False)
    project_building_num = fields.StringField(
        default='', max_length=255, null=False)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    SourceUrl = fields.URLField(default=None, blank=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'project_no',
            'NewCurTimeStamp',


        ]
    }


class BuildingBaseSuzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    project_no = fields.StringField(default='', max_length=255, null=False)
    project_name = fields.StringField(default='', max_length=255, null=False)
    building_no = fields.StringField(default='', max_length=255, null=False)
    building_name = fields.StringField(default='', max_length=255, null=False)
    building_areas = fields.StringField(default='', max_length=255, null=False)
    building_house_num = fields.StringField(
        default='', max_length=255, null=False)
    building_total_floor = fields.StringField(
        default='', max_length=255, null=False)
    project_area = fields.StringField(default='', max_length=255, null=False)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    SourceUrl = fields.URLField(default=None, blank=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'project_no',
            'building_no',
            'NewCurTimeStamp',

        ]
    }


class HouseBaseSuzhou(Document):

    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    project_no = fields.StringField(default='', max_length=255, null=False)
    project_name = fields.StringField(default='', max_length=255, null=False)
    building_no = fields.StringField(default='', max_length=255, null=False)
    building_name = fields.StringField(default='', max_length=255, null=False)
    house_no = fields.StringField(default='', max_length=255, null=False)
    house_name = fields.StringField(default='', max_length=255, null=False)
    house_sts = fields.StringField(default='', max_length=255, null=False)
    HSE_Located = fields.StringField(default='', max_length=255, null=False)
    HSE_LevelCode = fields.StringField(default='', max_length=255, null=False)
    Hes_LevelName = fields.StringField(default='', max_length=255, null=False)
    Hse_URCode = fields.StringField(default='', max_length=255, null=False)
    HSE_CellCode = fields.StringField(default='', max_length=255, null=False)
    Hse_Type_Room = fields.StringField(default='', max_length=255, null=False)
    Hse_Type_Hall = fields.StringField(default='', max_length=255, null=False)
    HSE_Bathroom = fields.StringField(default='', max_length=255, null=False)
    SHSE_ISPOLICY = fields.StringField(default='', max_length=255, null=False)
    Hse_Class = fields.StringField(default='', max_length=255, null=False)
    PH_Cdate = fields.StringField(default='', max_length=255, null=False)
    HSE_Ownership = fields.StringField(default='', max_length=255, null=False)
    # 土地分割转让许可证编号
    HSE_LDTPermit_SN = fields.StringField(
        default='', max_length=255, null=False)
    # 抵押情况
    ddl_ProTypeopt = fields.StringField(default='', max_length=255, null=False)

    # 装修情况
    hf_name = fields.StringField(default='', max_length=255, null=False)
    # 抵押起始日期
    lb_ProStar = fields.StringField(default='', max_length=255, null=False)
    # 抵押终止日期
    lb_ProEnd = fields.StringField(default='', max_length=255, null=False)
    # 套内建筑面积（平方米）
    SFLOOR_IN = fields.StringField(default='', max_length=255, null=False)
    # 分摊建筑面积（平方米）
    SFLOOR_FH = fields.StringField(default='', max_length=255, null=False)
    # 总建筑面积（平方米）
    AreaAll = fields.StringField(default='', max_length=255, null=False)
    # 总价格（元）
    Hse_TSUM = fields.StringField(default='', max_length=255, null=False)
    # 单价（元/平方米）
    SFLOOR_PRICE = fields.StringField(default='', max_length=255, null=False)
    # 公安门牌号
    Address = fields.StringField(default='', max_length=255, null=False)
    # 房屋层高是否超过2.2米

    HSE_IsLevelHeigh = fields.StringField(
        default='', max_length=255, null=False)

    # 房屋层高（米）
    LevelHeigh = fields.StringField(default='', max_length=255, null=False)
    house_stsLatest = fields.StringField(
        default='', max_length=255, null=False)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    SourceUrl = fields.URLField(default=None, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'project_no',  # 项目编号
            'building_no',  # 楼栋编号
            'house_no',  # 房间编号
            'NewCurTimeStamp',

        ]
    }
#


class ProjectallBaseSuzhou(Document):

    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    project_add = fields.StringField(default='', max_length=255, null=False)
    project_num = fields.StringField(default='', max_length=255, null=False)
    change_data = fields.StringField(default='', max_length=1023, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'project_add',
            'project_num',
        ]
    }
