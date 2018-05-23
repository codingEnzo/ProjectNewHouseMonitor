# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


# Zhongshan Model
class ProjectBaseZhongshan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectAdminArea = fields.StringField(
        default='', max_length=255, null=False)
    PresaleNum = fields.StringField(default='', max_length=255, null=False)
    ProjectPermitDate = fields.StringField(
        default='', max_length=255, null=False)
    ProjectPermitFlat = fields.StringField(
        default='', max_length=255, null=False)
    ProjectForsaleFlat = fields.StringField(
        default='', max_length=255, null=False)
    ProjectInfoURL = fields.StringField(default='', max_length=255, null=False)
    ProjectSaleHistoryURL = fields.StringField(
        default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp', 'ProjectUUID', 'ProjectName', 'PresaleNum',
            'ProjectInfoURL', 'ProjectSaleHistoryURL'
        ]
    }


class ProjectInfoZhongshan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    ProjectCompany = fields.StringField(default='', max_length=255, null=False)
    ProjectPermitDate = fields.StringField(
        default='', max_length=255, null=False)
    ProjectPresaleValid = fields.StringField(
        default='', max_length=255, null=False)
    ProjectTerminateCount = fields.StringField(
        default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectCompany',
        ]
    }


class BuildingInfoZhongshan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingSaleStatus = fields.StringField(
        default='', max_length=255, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    BuildingPermitFlat = fields.StringField(
        default='', max_length=255, null=False)
    BuildingSold = fields.StringField(default='', max_length=255, null=False)
    BuildingAvailable = fields.StringField(
        default='', max_length=255, null=False)
    BuildingStartDate = fields.StringField(
        default='', max_length=255, null=False)
    BuildingEndDate = fields.StringField(
        default='', max_length=255, null=False)
    BuildingTerminateCounts = fields.StringField(
        default='', max_length=255, null=False)
    # Tmp Testing
    BuildingHouseInfoURLArgs = fields.StringField(
        default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoZhongshan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    HouseUUID = fields.UUIDField(
        default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=255, null=False)
    HouseUsage = fields.StringField(default='', max_length=255, null=False)
    HouseSaleState = fields.StringField(default='', max_length=255, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=255, null=False)
    HouseFloor = fields.StringField(default='', max_length=255, null=False)
    HouseSharedArea = fields.StringField(
        default='', max_length=255, null=False)
    HouseBuildArea = fields.StringField(default='', max_length=255, null=False)
    HouseInternalArea = fields.StringField(
        default='', max_length=255, null=False)
    HouseType = fields.StringField(default='', max_length=255, null=False)
    HouseAddress = fields.StringField(default='', max_length=255, null=False)
    HouseContractNum = fields.StringField(
        default='', max_length=255, null=False)
