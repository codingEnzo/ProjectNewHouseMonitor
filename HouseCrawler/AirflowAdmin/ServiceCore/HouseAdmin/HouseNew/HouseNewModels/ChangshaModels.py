# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


class ProjectBaseChangsha(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectRegUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                      binary=False, null=False)
    ProjectRegName = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectRegDate = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectURLCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class ProjectInfoChangsha(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBaseLicenseCode = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildingNum = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBasePrice = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSaleAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSalePhone = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectHouseNum = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBusLine = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectTotalArea = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildingArea = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectDesignCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSaleAgent = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectManageCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectFinishAt = fields.StringField(
        default='', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class BuildingInfoChangsha(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegName = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingRegDate = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingAreaLicenceCode = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingEngPlanLicenceCode = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingAreaPlanLicenceCode = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingBuildLicenceCode = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingRegArea = fields.StringField(
        default='', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'BuildingRegName',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoChangsha(Document):
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
    HouseBuildingArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseShareArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseType = fields.StringField(default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=1024, null=False)
    HouseDType = fields.StringField(default='', max_length=1024, null=False)
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
