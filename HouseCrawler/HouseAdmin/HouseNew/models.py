# encoding = utf-8
import uuid
import datetime
from django_mongoengine import *
from django_mongoengine import fields


class AreaSaleInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    AreaUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    AreaName = fields.StringField(default='', max_length=255, null=False)
    AreaSaleNumDay = fields.StringField(default='', max_length=255, null=False)
    AreaSaleNumSum = fields.StringField(default='', max_length=255, null=False)
    AreaSaleAreaDay = fields.StringField(default='', max_length=255, null=False)
    AreaSaleAreaSum = fields.StringField(default='', max_length=255, null=False)
    AreaSalePriceDay = fields.StringField(default='', max_length=255, null=False)
    AreaSalePriceSum = fields.StringField(default='', max_length=255, null=False)
    AreaSumFlag = fields.BooleanField(default=False, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectURL',
        ]
    }


class ProjectBase(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectDistrict = fields.StringField(default='', max_length=255, null=False)
    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    ProjectSaleSum = fields.StringField(default='', max_length=255, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectURL',
        ]
    }


class ProjectInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    ProjectUsage = fields.StringField(default='', max_length=255, null=False)
    ProjectArea = fields.StringField(default='', max_length=255, null=False)
    ProjectHouseNum = fields.StringField(default='', max_length=255, null=False)
    ProjectCompany = fields.StringField(default='', max_length=255, null=False)
    ProjectCorporation = fields.StringField(default='', max_length=255, null=False)
    ProjectRegName = fields.StringField(default='', max_length=255, null=False)
    ProjectAreaPlanLicenseCode = fields.StringField(default='', max_length=255, null=False)
    ProjectPlanLicenseCode = fields.StringField(default='', max_length=255, null=False)
    ProjectConstructionLicenseCode = fields.StringField(default='', max_length=255, null=False)
    ProjectConstructionCompany = fields.StringField(default='', max_length=255, null=False)
    ProjectAuthenticFlag = fields.StringField(default='', max_length=255, null=False)
    ProjectSaleArea = fields.StringField(default='', max_length=255, null=False)
    ProjectSaleNum = fields.StringField(default='', max_length=255, null=False)
    ProjectSaledArea = fields.StringField(default='', max_length=255, null=False)
    ProjectSaledNum = fields.StringField(default='', max_length=255, null=False)
    ProjectUnavailableArea = fields.StringField(default='', max_length=255, null=False)
    ProjectUnavailableNum = fields.StringField(default='', max_length=255, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectRegName',
        ]
    }


class BuildingInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectRegName = fields.StringField(default='', max_length=255, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    BuildingFloorNum = fields.StringField(default='', max_length=255, null=False)
    BuildingHouseNum = fields.StringField(default='', max_length=255, null=False)
    BuildingUsage = fields.StringField(default='', max_length=255, null=False)
    BuildingSaleArea = fields.StringField(default='', max_length=255, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'ProjectRegName',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=255, null=False)
    HouseFloor = fields.StringField(default='', max_length=255, null=False)
    HouseSaleState = fields.StringField(default='', max_length=255, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=255, null=False)
    HouseRecordState = fields.StringField(default='', max_length=255, null=False)
    HouseRecordStateLatest = fields.StringField(default='', max_length=255, null=False)
    HousePledgeState = fields.StringField(default='', max_length=255, null=False)
    HousePledgeStateLatest = fields.StringField(default='', max_length=255, null=False)
    HouseAttachState = fields.StringField(default='', max_length=255, null=False)
    HouseAttachStateLatest = fields.StringField(default='', max_length=255, null=False)
    HouseUsage = fields.StringField(default='', max_length=255, null=False)
    HouseBuildingArea = fields.StringField(default='', max_length=255, null=False)
    HouseInnerArea = fields.StringField(default='', max_length=255, null=False)
    HouseShareArea = fields.StringField(default='', max_length=255, null=False)
    HouseUnitPrice = fields.FloatField(default=0.0, null=False)
    HousePrice = fields.FloatField(default=0.0, null=False)
    HousePriceFlag = fields.BooleanField(default=False, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'BuildingName',
            'ProjectUUID',
            'BuildingUUID',
            'HouseUUID',
            'HouseName'
        ]
    }


class ProjectCountInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectSalingNum = fields.IntField(default=0, index=True)
    ProjectSaledNum = fields.IntField(default=0, index=True)
    meta = {
        'indexes': [
            'RecordID',
            'CurTimeStamp',
        ]
    }


class BuildingCountInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    BuildingPreSalingNum = fields.IntField(default=0, index=True)
    BuildingPreSaledNum = fields.IntField(default=0, index=True)
    BuildingSalingNum = fields.IntField(default=0, index=True)
    BuildingCompletedSalingNum = fields.IntField(default=0, index=True)
    BuildingOpeningNum = fields.IntField(default=0, index=True)
    BuildingSaledNum = fields.IntField(default=0, index=True)
    meta = {
        'indexes': [
            'RecordID',
            'CurTimeStamp',
        ]
    }


class HouseCountInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    HouseUnavailableNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    HouseAvailableNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    HouseReserveNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    HouseContractNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    HouseRecordNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    HouseAuditNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    meta = {
        'indexes': [
            'RecordID',
            'CurTimeStamp',
        ]
    }
