# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


class ProjectInfoXuzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectID = fields.StringField(default='', null=False, max_length=255)
    DistrictName = fields.StringField(default='', max_length=255)  # 行政区
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    OnSaleState = fields.StringField(default='', max_length=255)  # 销售状态
    PromotionName = fields.StringField(default='', max_length=255)  # 推广名
    Developer = fields.StringField(default='', max_length=255)  # 开发商
    SaleAddress = fields.StringField(default='', max_length=255)  # 售楼处地址
    ProjectAddress = fields.StringField(default='', max_length=255)  # 项目地址
    HouseUseType = fields.StringField(default='', max_length=255)  # 房屋类型
    EarliestOpeningDate = fields.StringField(
        default='', max_length=255)  # 开盘时间
    PropertyRightsDescription = fields.StringField(
        default='', max_length=255)  # 使用年限
    GreeningRate = fields.StringField(default='', max_length=255)  # 绿化率
    FloorAreaRatio = fields.StringField(default='', max_length=255)  # 容积率
    AveragePrice = fields.StringField(default='', max_length=255)  # 拟售均价
    TotalBuidlingArea = fields.StringField(default='', max_length=255)  # 建筑面积
    ManagementFees = fields.StringField(default='', max_length=255)  # 物业费
    ParkingSpaceAmount = fields.StringField(default='', max_length=255)  # 车位
    ProjectIntro = fields.StringField(default='')  # 项目介绍
    ProjectSupporting = fields.StringField(default='')  # 项目配套
    ProjectPoint = fields.StringField(default='')  # 项目坐标
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 项目详细URL

    ApprovalPresaleAmount = fields.StringField(
        default='', max_length=255)  # 总入网套数
    ApprovalPresaleArea = fields.StringField(
        default='', max_length=255)  # 总入网面积
    SoldAmount = fields.StringField(default='', max_length=255)  # 已销售套数
    SoldArea = fields.StringField(default='', max_length=255)  # 已销售面积
    UnsoldAmount = fields.StringField(default='', max_length=255)  # 可售套数
    UnsoldArea = fields.StringField(default='', max_length=255)  # 可售面积

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectID',
            'DistrictName',
            'ProjectName',
            'PromotionName',
            'Developer',
            'AveragePrice',
            'SourceUrl',
        ]
    }


class PresellInfoXuzhou(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    PresellUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectID = fields.StringField(default='', max_length=255)  # 项目id
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    DistrictName = fields.StringField(default='', max_length=255)  # 行政区
    RegionName = fields.StringField(default='', max_length=255)  # 区位
    Developer = fields.StringField(default='', max_length=255)  # 开发商
    ConstructionPermitNumber = fields.StringField(default='')  # 施工许可证
    ProjectApproval = fields.StringField(default='')  # 立项批文
    CertificateOfUseOfStateOwnedLand = fields.StringField(default='')  # 用地许可证
    LandUse = fields.StringField(default='', max_length=255)  # 土地用途
    LandCertificate = fields.StringField(default='')  # 土地证
    FloorArea = fields.StringField(default='')  # 土地面积
    PlanUse = fields.StringField(default='')  # 规划用途
    PresalePermitNumber = fields.StringField(default='')  # 预售证号
    PresellID = fields.StringField(default='')  # 预售证id
    PresaleArea = fields.StringField(default='')  # 预售建筑面积
    LssueDate = fields.StringField(default='')  # 发证日期
    MonitBank = fields.StringField(default='')  # 监管银行
    MonitAccount = fields.StringField(default='')  # 监管账号
    SaleAddress = fields.StringField(default='')  # 销售地点
    SalePhone = fields.StringField(default='')  # 销售电话
    SaleScope = fields.StringField(default='')  # 包含楼盘
    ApprovalPresaleAmount = fields.StringField(
        default='', max_length=255)  # 总入网套数
    SoldAmount = fields.StringField(default='', max_length=255)  # 已销售套数
    UnsoldAmount = fields.StringField(default='', max_length=255)  # 可售套数
    TotalArea = fields.StringField(default='', max_length=255)  # 总面积
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'ProjectID',
            'PresellID',
            'ProjectName',
            'DistrictName',
            'RegionName',
            'UnsoldAmount',
        ]
    }


class BuildingInfoXuzhou(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectID = fields.StringField(default='', max_length=255)  # 项目id
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    PresalePermitNumber = fields.StringField(
        default='', max_length=255)  # 预售证号
    BuildingName = fields.StringField(default='', max_length=255)  # 楼栋名称
    BuildingID = fields.StringField(default='', max_length=255)  # 楼栋id
    ApprovalPresaleAmount = fields.StringField(
        default='', max_length=255)  # 总入网套数
    SoldAmount = fields.StringField(default='', max_length=255)  # 已销售套数
    UnsoldAmount = fields.StringField(default='', max_length=255)  # 可售套数
    ApprovalPresaleArea = fields.StringField(
        default='', max_length=255)  # 总入网面积
    SoldArea = fields.StringField(default='', max_length=255)  # 已销售面积
    UnsoldArea = fields.StringField(default='', max_length=255)  # 可售面积
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'BuildingUUID',
            'ProjectID',
            'ProjectName',
            'PresalePermitNumber',
            'BuildingName',
            'BuildingID',
            'UnsoldAmount',
        ]
    }


class HouseInfoXuzhou(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    PresalePermitNumber = fields.StringField(
        default='', max_length=255)  # 预售证号
    BuildingName = fields.StringField(default='', max_length=255)  # 楼栋名称
    UnitName = fields.StringField(default='', max_length=255)  # 单元号
    HouseID = fields.StringField(default='', max_length=255)  # 户id
    HouseName = fields.StringField(default='', max_length=255)  # 户名
    HouseUseType = fields.StringField(default='', max_length=255)  # 房屋功能/用途
    BuildingStructure = fields.StringField(default='', max_length=255)  # 房屋结构
    MeasuredBuildingArea = fields.StringField(
        default='', max_length=255)  # 实测建筑面积
    MeasuredInsideOfBuildingArea = fields.StringField(
        default='', max_length=255)  # 实测套内面积
    MeasuredSharedPublicArea = fields.StringField(
        default='', max_length=255)  # 实测公摊面积
    ContractRecordNumber = fields.StringField(
        default='', max_length=255)  # 合同备案号
    HouseState = fields.StringField(default='', max_length=255)  # 当前状态
    HouseStateLatest = fields.StringField(default='', max_length=255)  # 上次状态
    ProjectID = fields.StringField(default='', max_length=255)  # 项目id
    HouseMapID = fields.StringField(default='')  # 户型图id
    DataIndex = fields.StringField(default='')  # 该户在jsonArray中的顺序
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'PresellUUID',
            'PresalePermitNumber',
            'BuildingUUID',
            'BuildingName',
            'HouseUUID',
            'HouseState',
            'HouseStateLatest',
        ]
    }
