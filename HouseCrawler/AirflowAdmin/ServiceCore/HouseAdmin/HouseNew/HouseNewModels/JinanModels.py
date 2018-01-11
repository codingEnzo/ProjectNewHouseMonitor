# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


# Jinan Model
class ProjectBaseJinan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(
        datetime.datetime.now()), max_length=255, index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    ProjectCompany = fields.StringField(default='', max_length=255, null=False)
    ProjectSaleNum = fields.StringField(default='', max_length=255, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectURL',
            'ProjectName'
        ]
    }


class ProjectInfoJinan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    ProjectCompany = fields.StringField(default='', max_length=255, null=False)
    ProjectDistrict = fields.StringField(
        default='', max_length=255, null=False)
    ProjectScale = fields.StringField(default='', max_length=255, null=False)
    ProjectBuildingNum = fields.StringField(
        default='', max_length=255, null=False)
    ProjectSaleAddress = fields.StringField(
        default='', max_length=255, null=False)
    ProjectSalePhone = fields.StringField(
        default='', max_length=255, null=False)
    ProjectManageCompany = fields.StringField(
        default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'ProjectDistrict'
        ]
    }


class BuildingInfoJinan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    BuildingRegName = fields.StringField(
        default='', max_length=255, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingSaleNum = fields.StringField(
        default='', max_length=255, null=False)
    BuildingSaleArea = fields.StringField(
        default='', max_length=255, null=False)
    BuildingAvailabeNum = fields.StringField(
        default='', max_length=255, null=False)
    BuildingAvailabeArea = fields.StringField(
        default='', max_length=255, null=False)
    BuildingSoldNum = fields.StringField(
        default='', max_length=255, null=False)
    BuildingSoldArea = fields.StringField(
        default='', max_length=255, null=False)
    BuildingNameAlias = fields.StringField(
        default='', max_length=255, null=False)
    BuildingDevCompany = fields.StringField(
        default='', max_length=255, null=False)
    BuildingDevCredential = fields.StringField(
        default='', max_length=255, null=False)
    BuildingArea = fields.StringField(default='', max_length=255, null=False)
    BuildingDistrict = fields.StringField(
        default='', max_length=255, null=False)
    BuildingDecoration = fields.StringField(
        default='', max_length=255, null=False)
    BuildingUsage = fields.StringField(default='', max_length=255, null=False)
    BuildingIsMortgage = fields.StringField(
        default='', max_length=255, null=False)
    BuildingAreaCode = fields.StringField(
        default='', max_length=255, null=False)
    BuildingEngPlanCode = fields.StringField(
        default='', max_length=255, null=False)
    BuildingEngCode = fields.StringField(
        default='', max_length=255, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingSaleDict = fields.DictField(default={'code': 0}, null=False)
    meta = {
        'indexes': [
            'BuildingName',
            'BuildingURL',
            'ProjectUUID',
            'BuildingUUID'
        ]
    }


class HouseInfoJinan(Document):

    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=255, null=False)
    HouseID = fields.StringField(default='', max_length=255, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                 binary=False, null=False)
    HouseSaleState = fields.StringField(default='', max_length=255, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=255, null=False)
    HouseArea = fields.StringField(default='', max_length=255, null=False)
    HouseUnitArea = fields.StringField(default='', max_length=255, null=False)
    HouseApportioArea = fields.StringField(
        default='', max_length=255, null=False)
    HouseUsage = fields.StringField(default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'HouseName',
            'BuildingName',
            'ProjectUUID',
            'BuildingUUID',
            'HouseUUID'
        ]
    }


class SignInfoJinan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    SaleDict = fields.DictField(default={'code': 0}, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp'
        ]
    }
