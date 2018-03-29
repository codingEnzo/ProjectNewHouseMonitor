# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


class ProjectDetailTianjin(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    RecordTime = fields.StringField(
        default=str(datetime.datetime.now()), index=True)

    CheackTimeLatest = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectUrl = fields.URLField(default=None, null=True, blank=True)
    ProjectName = fields.StringField(default='')
    RegionName = fields.StringField(default='')

    ProjectAddress = fields.StringField(default='')

    Developer = fields.StringField(default='')
    HouseUseNonhousingPrice = fields.StringField(default='')
    HouseUseHousingPrice = fields.StringField(default='')
    EarliestOpeningTime = fields.StringField(default='')

    GreeningRate = fields.StringField(default='', null=False)
    FloorAreaRatio = fields.StringField(default='', null=False)

    DistrictName = fields.StringField(default='', null=False)
    ManagementFees = fields.StringField(default='', null=False)
    ManagementCompany = fields.StringField(default='', null=False)
    TotalBuidlingArea = fields.StringField(default='', null=False)
    FloorArea = fields.StringField(default='', null=False)

    ParkingSpaceAmount = fields.StringField(default='', null=False)
    ProjectInformation = fields.StringField(default='', null=False)
    ProjectTradeArea = fields.StringField(default='', null=False)
    BuildingStructure = fields.StringField(default='', null=False)

    Project_LivingTime = fields.StringField(default='', null=False)
    Project_Feature = fields.StringField(default='', null=False)
    Project_Business = fields.StringField(default='', null=False)
    Project_Traffic = fields.StringField(default='', null=False)
    Project_Introduce = fields.StringField(default='', null=False)
    Project_Surround = fields.StringField(default='', null=False)
    Project_BuildingInformation = fields.StringField(default='', null=False)
    Project_Information = fields.StringField(default='', null=False)
    Project_PlanType = fields.StringField(default='', null=False)
    Project_Type = fields.StringField(default='', null=False)
    meta = {
        'indexes': [
            'RecordTime',
            'ProjectName',
            'RegionName',
            'ProjectAddress',
            'Developer',
        ]
    }


class BuildingDetailTianjin(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    RecordTime = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    CheackTimeLatest = fields.StringField(
        default=str(datetime.datetime.now()), index=True)

    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectUrl = fields.URLField(default=None, null=True, blank=True)
    SourceUrl = fields.URLField(default=None, null=True, blank=True)
    ProjectName = fields.StringField(default='')
    RegionName = fields.StringField(default='')
    BuildingID = fields.StringField(default='')
    BuildingUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingName = fields.StringField(default='')
    BuildingNumber = fields.StringField(default='')
    SalePermitNumber = fields.StringField(default='')  # 销售许可证号
    OpeningTime = fields.StringField(default='')  # 开盘时间
    HouseSalePrice = fields.StringField(default='')  # 住宅参考均价
    HouseSalePrice_Not = fields.StringField(default='')  # 非住宅参考均价
    OnsoldAmount = fields.StringField(default='')  # 可售套数
    HouseAmount = fields.StringField(default='')  # 房产数量

    meta = {
        'indexes': [
            'ProjectUUID',
            'ProjectUrl',
            'ProjectName',
            'BuildingID',
            'BuildingUUID',
            'BuildingName',
            'BuildingNumber',
            'SalePermitNumber',
            'OpeningTime',
            'HouseSalePrice',
            'HouseSalePrice_Not',
            'OnsoldAmount',
            'HouseAmount',
        ]
    }


class HouseDetailTianjin(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    RecordTime = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    CheackTimeLatest = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='')
    BuildingName = fields.StringField(default='')
    UnitName = fields.StringField(default='')
    BuildingNumber = fields.StringField(default='')
    UnitID = fields.StringField(default='')
    BuildingID = fields.StringField(default='')
    HouseUrl = fields.StringField(default='')
    SalePermitNumber = fields.StringField(default='')  # 销售许可证号
    FloorName = fields.StringField(default='')  # 层名
    HouseName = fields.StringField(default='')
    HouseUseType = fields.StringField(default='')  # 用途
    UnitShape = fields.StringField(default='')  # 户型
    Toward = fields.StringField(default='')
    FloorHight = fields.StringField(default='')  # 层高
    BuildingStructure = fields.StringField(default='')  # 建筑结构
    HouseSaleState = fields.StringField(default='')  # 销售状态
    HouseSaleStateLatest = fields.StringField(default='')  # 上次状态
    MeasuredBuildingArea = fields.StringField(default='')  # 实测建筑面积
    MeasuredInsideOfBuildingArea = fields.StringField(default='')  # 实测套内面积
    MeasuredSharedPublicArea = fields.StringField(default='')  # 实测公摊面积
    SalePriceByInsideOfBuildingArea = fields.StringField(
        default='')  # 按套内面积拟售单价
    meta = {
        'indexes': [
            'ProjectUUID',
            'BuildingUUID',
            'HouseUUID',
            'ProjectName',
            'BuildingName',
            'UnitName',
            'BuildingNumber',
            'UnitID',
            'BuildingID',
            'HouseUrl',
            'SalePermitNumber',
            'FloorName',
            'HouseName',
            'HouseUseType',
            'UnitShape',
            'HouseSaleState',
            'HouseSaleStateLatest',
            'MeasuredBuildingArea',
            'MeasuredInsideOfBuildingArea',
            'MeasuredSharedPublicArea',
            'SalePriceByInsideOfBuildingArea',
        ]
    }
