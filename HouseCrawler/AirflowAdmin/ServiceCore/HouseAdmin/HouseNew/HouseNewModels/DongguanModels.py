# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


class ProjectBaseDongguan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSaleSum = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectURLCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectURL',
        ]
    }


class ProjectInfoDongguan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectOpenDate = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAlias = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectUsage = fields.StringField(default='', max_length=1024, null=False)
    ProjectArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectHouseNum = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectCorporation = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectRegName = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAreaPlanLicenseCode = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectPlanLicenseCode = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectConstructionLicenseCode = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectConstructionCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAuthenticFlag = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSaleArea = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSaleNum = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSaledArea = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSaledNum = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectUnavailableArea = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectUnavailableNum = fields.StringField(
        default='', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectRegName',
        ]
    }


class BuildingInfoDongguan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectRegName = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingFloorNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingHouseNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingUsage = fields.StringField(default='', max_length=1024, null=False)
    BuildingSaleArea = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
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


class HouseInfoDongguan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                 binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=1024, null=False)
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=1024, null=False)
    HouseRecordState = fields.StringField(
        default='', max_length=1024, null=False)
    HouseRecordStateLatest = fields.StringField(
        default='', max_length=1024, null=False)
    HousePledgeState = fields.StringField(
        default='', max_length=1024, null=False)
    HousePledgeStateLatest = fields.StringField(
        default='', max_length=1024, null=False)
    HouseAttachState = fields.StringField(
        default='', max_length=1024, null=False)
    HouseAttachStateLatest = fields.StringField(
        default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(
        default='0.0', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(
        default='0.0', max_length=1024, null=False)
    HouseShareArea = fields.StringField(
        default='0.0', max_length=1024, null=False)
    HouseUnitPrice = fields.StringField(default='0.0', null=False)
    HousePrice = fields.StringField(default='0.0', null=False)
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
