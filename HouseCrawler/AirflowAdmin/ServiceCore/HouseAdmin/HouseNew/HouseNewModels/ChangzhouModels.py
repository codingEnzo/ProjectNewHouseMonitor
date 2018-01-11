# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields

# 常州 ORM


class ProjectBaseChangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleNum = fields.StringField(
        default='', max_length=255, null=False)
    ProjectPresaleId = fields.StringField(
        default='', max_length=255, null=False)
    ProjectPresaleDate = fields.StringField(
        default='', max_length=255, null=False)
    ProjectURL = fields.StringField(default='', max_length=255, null=False)
    ProjectRecordURL = fields.StringField(
        default='', max_length=255, null=False)
    ProjectBuildingListURL = fields.StringField(
        default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectURL',
            'ProjectRecordURL',
            'ProjectBuildingListURL',
        ]
    }


class ProjectInfoChangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectCompany = fields.StringField(default='', max_length=255, null=False)
    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    ProjectRegion = fields.StringField(default='', max_length=255, null=False)
    # ProjectRegionNum = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleArea = fields.StringField(
        default='', max_length=255, null=False)
    ProjectPresaleHouseNum = fields.StringField(
        default='', max_length=255, null=False)
    ProjectPresaleBuildingRange = fields.StringField(
        default='', max_length=255, null=False)
    ProjectSalesAgency = fields.StringField(
        default='', max_length=255, null=False)
    ProjectSupervisorBank = fields.StringField(
        default='', max_length=255, null=False)
    ProjectSupervisorAccount = fields.StringField(
        default='', max_length=255, null=False)
    ProjectBankGuarantee = fields.StringField(
        default='', max_length=255, null=False)
    ProjectRecordsInfo = fields.ListField(
        default=[], max_length=1024, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectCompany',
        ]
    }


class BuildingInfoChangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleNum = fields.StringField(
        default='', max_length=255, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    BuildingURL = fields.StringField(default='', max_length=255, null=False)
    BuildingArea = fields.StringField(default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectPresaleNum',
            'BuildingUUID',
            'BuildingName'
        ]
    }


class HouseInfoChangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleNum = fields.StringField(
        default='', max_length=255, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                 binary=False, null=False)
    HouseBuildingArea = fields.StringField(
        default='', max_length=255, null=False)
    HouseContractPrice = fields.StringField(
        default='', max_length=255, null=False)
    HouseUsage = fields.StringField(default='', max_length=255, null=False)
    HouseLabel = fields.StringField(default='', max_length=255, null=False)
    HouseCurCell = fields.StringField(default='', max_length=255, null=False)
    HouseSaleStatus = fields.StringField(
        default='', max_length=255, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectPresaleNum',
            'BuildingUUID',
            'BuildingName',
            'HouseUUID',
            'HouseUsage',
            'HouseLabel',
            'HouseSaleStatus',
            'HouseSaleStateLatest'
        ]
    }
