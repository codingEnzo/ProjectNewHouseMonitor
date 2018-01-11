# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


class ProjectBaseHangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)

    PropertyID = fields.StringField(
        default='', max_length=100, null=False)  # 楼盘id
    sid = fields.StringField(default='33', max_length=100, null=False)  # sid

    ProjectAllrankvalue = fields.StringField(
        default='', max_length=100)  # 综合评分
    ProjectName = fields.StringField(
        default='', max_length=200, null=False)  # 楼盘名称
    PromotionName = fields.StringField(default='', max_length=100)  # 推广名
    DistrictName = fields.StringField(default='', max_length=100)  # 行政区
    RegionName = fields.StringField(default='', max_length=100)  # 街道
    ProjectAddress = fields.StringField(default='', null=False)  # 楼盘地址
    ProjectSellAddress = fields.StringField(default='')  # 售楼地址
    ProjectMainUnitType = fields.StringField(
        default='', max_length=100)  # 主力户型
    ProjectDecoration = fields.StringField(default='', max_length=100)  # 装修情况
    BuildingType = fields.StringField(default='', max_length=100)  # 建筑类型/建筑形式
    LandUse = fields.StringField(default='', max_length=100)  # 物业类型/土地用途
    FloorAreaRatio = fields.StringField(default='', max_length=100)  # 容积率
    GreeningRate = fields.StringField(default='', max_length=100)  # 绿化率
    FloorArea = fields.StringField(default='', max_length=100)  # 占地面积
    CompletionDate = fields.StringField(default='', max_length=100)  # 竣工时间
    TotalBuidlingArea = fields.StringField(default='', max_length=100)  # 总建筑面积
    HousingCount = fields.StringField(default='', max_length=100)  # 总户数
    LatestDeliversHouseDate = fields.StringField(
        default='', max_length=100)  # 预计交付时间
    ParkingInfo = fields.StringField(default='', max_length=100)  # 车位信息
    ManagementFees = fields.StringField(default='', max_length=100)  # 物业费
    ManagementCompany = fields.StringField(default='', max_length=100)  # 物业公司

    PropertyRightsDescription = fields.StringField(
        default='', max_length=100)  # 产权年限
    Developer = fields.StringField(default='', max_length=100)  # 项目公司
    Selltel = fields.StringField(default='', max_length=100)  # 售楼部电话
    OnSaleState = fields.StringField(
        default='', max_length=100, null=False)  # 楼盘状态/在售状态
    TrafficSituation = fields.StringField(default='')  # 交通情况
    ProjectSupporting = fields.StringField(default='')  # 项目配套
    ProjectIntro = fields.StringField(default='')  # 项目简介
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 项目详细URL

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
        ]
    }


class PresellInfoHangzhou(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(
        datetime.datetime.now()), index=True)  # 创建时间
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellID = fields.StringField(
        default='', max_length=100, null=False)  # 预售证id
    PropertyID = fields.StringField(
        default='', max_length=100, null=False)  # 预售证id
    sid = fields.StringField(default='', max_length=100,
                             index=True, null=False)  # sid
    PresellNO = fields.StringField(default='')  # 预售证号/预售证编号
    PresellName = fields.StringField(default='')  # 预售证号/预售证编号

    LssueDate = fields.StringField(default='', max_length=100)  # 预售证核发时间
    Applycorp = fields.StringField(default='', max_length=100)  # 预售证申领单位
    LssuingAuthority = fields.StringField(default='', max_length=100)  # 发证机关

    Bank = fields.StringField(default='', max_length=100)  # 资金监管银行
    BankAccount = fields.StringField(default='', max_length=100)  # 资金监管银行账号
    # 接口返回的字段
    num = fields.IntField(default=0, null=True, blank=True)  # 纳入网上预（销）售总套数
    justnum = fields.IntField(default=0, null=True, blank=True)  # 即将解除限制房产套数
    area = fields.FloatField(default=0.00, null=True,
                             blank=True)  # 纳入网上预（销）售总面积
    justarea = fields.FloatField(
        default=0.00, null=True, blank=True)  # 即将解除限制房产总面积
    avanum = fields.IntField(default=0, null=True, blank=True)  # 可预（销）售总套数
    waitnum = fields.IntField(default=0, null=True, blank=True)  # 待现售房产套数
    avaarea = fields.FloatField(
        default=0.00, null=True, blank=True)  # 可预（销）售总面积
    waitarea = fields.FloatField(
        default=0.00, null=True, blank=True)  # 可预（销）售总套数
    resideavanum = fields.IntField(
        default=0, null=True, blank=True)  # 其中可预（销）售住宅总套数
    limitnum = fields.IntField(default=0, null=True, blank=True)  # 限制房产套数
    resideavaarea = fields.FloatField(
        default=0.00, null=True, blank=True)  # 可预（销）售住宅总面积
    limitarea = fields.FloatField(
        default=0.00, null=True, blank=True)  # 限制房产总面积
    dealnum = fields.IntField(default=0, null=True, blank=True)  # 已预（销）售总套数
    notnum = fields.IntField(default=0, null=True, blank=True)  # 未纳入网上销售房产套数
    dealarea = fields.FloatField(
        default=0.00, null=True, blank=True)  # 已预（销）售总面积
    notarea = fields.IntField(default=0, null=True, blank=True)  # 未纳入网上销售房产总面积
    plannum = fields.IntField(default=0, null=True, blank=True)  # 已预定套数
    planarea = fields.IntField(default=0, null=True, blank=True)  # 已预定总面积

    OpeningDate = fields.StringField(default='', max_length=100)  # 开盘时间
    ApprovalProjectName = fields.StringField(
        default='', max_length=100)  # 预售审批项目名称
    PresellURL = fields.URLField(default=None, null=True, blank=True)  # 预售价地址
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
        ]
    }


class BuildingInfoHangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingID = fields.StringField(
        default='', max_length=100, null=False)  # 楼栋id
    BuildingName = fields.StringField(
        default='', max_length=100, null=False)  # 楼栋名
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'BuildingUUID',
        ]
    }


class HouseInfoHangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingName = fields.StringField(
        default='', max_length=100, null=False)  # 楼栋名
    UnitName = fields.StringField(
        default='', max_length=100, null=True, blank=True)  # 单元
    HouseNO = fields.StringField(default='', max_length=255)  # 户号
    RoughPrice = fields.StringField(default='', null=False)  # 毛坯单价
    HousePrice = fields.StringField(default='', null=False)  # 总价
    HouseBuildingArea = fields.StringField(default='', null=False)  # 建筑面积
    HouseInnerArea = fields.StringField(default='', null=False)  # 套内面积
    HouseState = fields.StringField(default='', max_length=50)  # 当前状态
    HouseStateLatest = fields.StringField(
        default='', max_length=255, null=False, blank=True)
    HouseType = fields.StringField(default='', max_length=50)  # 户型
    HouseFloor = fields.StringField(default='', null=False)  # 户楼层
    BuildingFloor = fields.StringField(default='', null=False)  # 总楼层
    HouseLocated = fields.StringField(default='', max_length=255)  # 坐落
    HouseUsage = fields.StringField(default='', max_length=50)  # 房屋用途
    HouseStructure = fields.StringField(default='', max_length=50)  # 房屋结构
    RoomRate = fields.StringField(default='', null=False)  # 得房率
    HouseManagementFees = fields.StringField(default='', null=False)  # 物业费
    HouseOrientation = fields.StringField(default='', max_length=50)  # 朝向
    DeclarationTime = fields.StringField(default='', max_length=50)  # 申报时间
    HouseURL = fields.URLField(default=None, null=True, blank=True)  # 户详情地址
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'BuildingUUID',
            'HouseUUID',
            'HouseState',
            'HouseStateLatest',
        ]
    }


class IndexHouseInfoHangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    RegionUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    Region = fields.StringField(default='', null=False)
    SignCount = fields.StringField(default='', null=False)
    BookCount = fields.StringField(default='', null=False)
    SaleCount = fields.StringField(default='', null=False)


class IndexInfoHangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    RegionUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    Region = fields.StringField(default='', null=False)
    SignCount = fields.StringField(default='', null=False)
    SaleArea = fields.StringField(default='', null=False)
