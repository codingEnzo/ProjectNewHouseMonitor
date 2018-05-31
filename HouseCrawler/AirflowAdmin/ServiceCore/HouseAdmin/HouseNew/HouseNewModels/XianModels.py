# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


class ProjectBaseXian(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectRoomType = fields.StringField(
        default='', max_length=255, null=False)
    ProjectHotSales = fields.StringField(
        default='', max_length=255, null=False)
    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    ProjectCompany = fields.StringField(default='', max_length=255, null=False)
    ProjectPhoneNum = fields.StringField(
        default='', max_length=255, null=False)
    ProjectPrice = fields.StringField(default='', max_length=255, null=False)
    ProjectBaseSubURL = fields.StringField(
        default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectBaseSubURL',
        ]
    }


class ProjectInfoXian(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectCompany = fields.StringField(default='', max_length=255, null=False)
    ProjectDueDate = fields.ListField(default=[], max_length=1024, null=False)
    ProjectInfoURL = fields.StringField(default='', max_length=255, null=False)
    ProjectCompanyURL = fields.StringField(
        default='', max_length=255, null=False)
    ProjectPresaleURL = fields.StringField(
        default='', max_length=255, null=False)

    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    ProjectSalesAddress = fields.StringField(
        default='', max_length=255, null=False)
    ProjectCityArea = fields.StringField(
        default='', max_length=255, null=False)
    ProjectTradeCircle = fields.StringField(
        default='', max_length=255, null=False)
    PropertyType = fields.StringField(default='', max_length=255, null=False)
    ProjectFirstDueDate = fields.StringField(
        default='', max_length=255, null=False)
    ProjectMainRoomType = fields.StringField(
        default='', max_length=255, null=False)
    ProjectDekoration = fields.StringField(
        default='', max_length=255, null=False)
    ProjectBuildType = fields.StringField(
        default='', max_length=255, null=False)
    ProjectBrief = fields.StringField(default='', max_length=255, null=False)
    ProjectTotalFlat = fields.StringField(
        default='', max_length=255, null=False)
    PropertyCost = fields.StringField(default='', max_length=255, null=False)
    ProjectSupplyType = fields.StringField(
        default='', max_length=255, null=False)
    ProjectContainRoomType = fields.StringField(
        default='', max_length=255, null=False)
    ProjectLoopLine = fields.StringField(
        default='', max_length=255, null=False)
    ProjectParkingSpace = fields.StringField(
        default='', max_length=255, null=False)
    LandUseLife = fields.StringField(default='', max_length=255, null=False)
    PeripheryEducation = fields.StringField(
        default='', max_length=255, null=False)
    PeripheryCommerce = fields.StringField(
        default='', max_length=255, null=False)
    PeripheryBank = fields.StringField(default='', max_length=255, null=False)
    PeripheryHospital = fields.StringField(
        default='', max_length=255, null=False)
    PeripheryTraffic = fields.StringField(
        default='', max_length=255, null=False)
    PeripheryRestaurant = fields.StringField(
        default='', max_length=255, null=False)
    PeripheryOthers = fields.StringField(
        default='', max_length=255, null=False)
    BuildingStructure = fields.StringField(
        default='', max_length=255, null=False)
    BuildingArea = fields.StringField(default='', max_length=255, null=False)
    BuildingFloorSpace = fields.StringField(
        default='', max_length=255, null=False)
    MaxBuildingFlats = fields.StringField(
        default='', max_length=255, null=False)
    MinBuildingFlats = fields.StringField(
        default='', max_length=255, null=False)
    ProjectDevCompany = fields.StringField(
        default='', max_length=255, null=False)
    PropertyCompany = fields.StringField(
        default='', max_length=255, null=False)
    Point = fields.StringField(default='', max_length=255, null=False)
    ProjectBookingData = fields.StringField(default='', max_length=255, null=False)
    AveragePrice = fields.StringField(default='', max_length=255, null=False)
    Decoration = fields.StringField(default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectPresaleURL',
        ]
    }


class PresaleInfoXian(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    PresaleCode = fields.StringField(default='', max_length=255, null=False)
    PresaleUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingRecordName = fields.StringField(
        default='', max_length=255, null=False)
    DevCompany = fields.StringField(default='', max_length=255, null=False)
    LicenseDate = fields.StringField(default='', max_length=255, null=False)
    SuperviseBank = fields.StringField(default='', max_length=255, null=False)
    SuperviseBankAccount = fields.StringField(
        default='', max_length=255, null=False)
    BuildingList = fields.StringField(default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'PresaleUUID',
            'PresaleCode',
            # 'BuildingList'
        ]
    }


class BuildingInfoXian(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    PresaleUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresaleCode = fields.StringField(default='', max_length=255, null=False)
    BuildingUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    BuildingURL = fields.StringField(default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'PresaleUUID',
            'PresaleCode',
            'BuildingName',
            'BuildingUUID',
            'BuildingURL',
            # 'BuildingList'
        ]
    }


class HouseInfoXian(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    BuildingUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    BuildingNum = fields.StringField(default='', max_length=255, null=False)
    HouseUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUnit = fields.StringField(default='', max_length=255, null=False)
    HouseRoomNum = fields.StringField(default='', max_length=255, null=False)
    HouseFloor = fields.StringField(default='', max_length=255, null=False)
    HouseRoomType = fields.StringField(default='', max_length=255, null=False)
    HouseUsage = fields.StringField(default='', max_length=255, null=False)
    HouseType = fields.StringField(default='', max_length=255, null=False)
    HouseBuildingArea = fields.StringField(
        default='', max_length=255, null=False)
    HouseSaleState = fields.StringField(default='', max_length=255, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'BuildingUUID',
            'BuildingName',
            'HouseUUID',
            'HouseUnit',
            'HouseRoomNum',
            'HouseSaleState',
            'HouseSaleStateLatest',
        ]
    }