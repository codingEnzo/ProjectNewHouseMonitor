# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


class ProjectBaseNantong(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    ReferencePrice = fields.StringField(default='', max_length=255)  # 参考价格
    OnSaleState = fields.StringField(
        default='', max_length=100, null=False)  # 楼盘状态/在售状态
    LandUse = fields.StringField(default='', max_length=255)  # 土地用途
    Developer = fields.StringField(default='', max_length=255)  # 开发商
    Selltel = fields.StringField(default='', max_length=100)  # 销售热线
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 项目链接


class ProjectInfoNantong(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    OnSaleState = fields.StringField(
        default='', max_length=100, null=False)  # 楼盘状态/在售状态
    LandUse = fields.StringField(default='', max_length=255)  # 土地用途
    RecordName = fields.StringField(default='', max_length=255)  # 备案名
    Decoration = fields.StringField(default='', max_length=255)  # 装修
    HousingCount = fields.StringField(default='', max_length=255)  # 规划户数
    Developer = fields.StringField(default='', max_length=255)  # 开发商
    DistrictName = fields.StringField(default='', max_length=255)  # 行政区
    ProjectAddress = fields.StringField(default='', max_length=255)  # 项目地址
    ApprovalPresaleAmount = fields.StringField(
        default='', max_length=255)  # 批准预售总套数
    HousingOnsoldAmount = fields.StringField(
        default='', max_length=255)  # 住宅可售套数
    ReferencePrice = fields.StringField(default='', max_length=255)  # 参考价格
    EarliestOpeningTime = fields.StringField(
        default='', max_length=255)  # 开盘时间
    LatestDeliversHouseDate = fields.StringField(
        default='', max_length=255)  # 交房时间
    FloorArea = fields.StringField(default='', max_length=100)  # 占地面积
    TotalBuidlingArea = fields.StringField(default='', max_length=100)  # 建筑面积
    FloorAreaRatio = fields.StringField(default='', max_length=100)  # 容积率
    GreeningRate = fields.StringField(default='', max_length=100)  # 绿化率
    ManagementFees = fields.StringField(default='', max_length=100)  # 物业费
    ManagementCompany = fields.StringField(default='', max_length=100)  # 物业公司
    BuildingType = fields.StringField(default='', max_length=100)  # 建筑类别
    ProjectSellAddress = fields.StringField(default='')  # 售楼地址
    SalesAgent = fields.StringField(default='')  # 销售代理
    ConstructionUnit = fields.StringField(default='')  # 施工单位
    ProjectIntro = fields.StringField(default='')  # 项目简介
    ProjectAroundSupporting = fields.StringField(default='')  # 周边配套
    TrafficSituation = fields.StringField(default='')  # 交通情况
    DecorationInfo = fields.StringField(default='')  # 装修情况
    DeveloperIntro = fields.StringField(default='')  # 开发商介绍
    AboutInfo = fields.StringField(default='')  # 相关信息
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 项目详细URL
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'OnSaleState',
            'ApprovalPresaleAmount',
            'HousingOnsoldAmount',
            'ReferencePrice',
            'SourceUrl',
        ]
    }


class PresellInfoNantong(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    PresalePermitNumber = fields.StringField(
        default='', max_length=255)  # 预售证编号
    ApprovalPresaleArea = fields.StringField(
        default='', max_length=255)  # 批准预售面积
    ApprovalPresaleBuildingName = fields.StringField(default='')  # 批准销售房层幢号
    Price = fields.StringField(default='')  # 房层价格
    LssueDate = fields.StringField(default='', max_length=255)  # 批准日期
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'ProjectName',
            'PresalePermitNumber',
        ]
    }


class BuildingInfoNantong(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    PresalePermitNumber = fields.StringField(
        default='', max_length=255)  # 预售证编号
    BuildingName = fields.StringField(default='', max_length=255)  # 楼栋名
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 楼栋销控表链接
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'BuildingUUID',
            'SourceUrl',
        ]
    }


class HouseInfoNantong(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    BuildingName = fields.StringField(default='', max_length=255)  # 楼栋名称
    FloorName = fields.StringField(default='', max_length=255)  # 层名
    HouseNumber = fields.StringField(default='', max_length=255)  # 房号
    HouseState = fields.StringField(default='', max_length=255)  # 当前状态
    HouseStateLatest = fields.StringField(default='', max_length=255)  # 上次状态
    MeasuredBuildingArea = fields.StringField(
        default='', max_length=255)  # 建筑面积
    MeasuredInsideOfBuildingArea = fields.StringField(
        default='', max_length=255)  # 套内面积
    MeasuredSharedPublicArea = fields.StringField(
        default='', max_length=255)  # 公摊面积
    HouseUseType = fields.StringField(default='', max_length=255)  # 房屋功能/用途
    UnitShape = fields.StringField(default='', max_length=255)  # 户型
    TotalPrice = fields.StringField(default='', max_length=255)  # 总价
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 户详细URL
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'BuildingUUID',
            'HouseUUID',
            'HouseState',
            'HouseStateLatest',
            'SourceUrl',
        ]
    }
