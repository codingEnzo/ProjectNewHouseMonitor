# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


# Chongqing Model
class ProjectBaseChongqing(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectBaseName = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectCorporation = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSoldNum = fields.StringField(
        default='0', max_length=1024, null=False)
    ProjectSoldArea = fields.StringField(
        default='0.0', max_length=1024, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectURLCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectCorporation'
        ]
    }


class BuildingInfoChongqing(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectBaseName = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectCorporation = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingRegName = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingZZHouseNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingFZZHouseNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingZZHouseNumSaling = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingFZZHouseNumSaling = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingRegHouseNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingRegArea = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectBaseName',
            'ProjectName',
            'ProjectUUID',
            'BuildingRegName',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoChongqing(Document):
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
    HoueseID = fields.StringField(default='', max_length=1024, null=False)
    HoueseRegID = fields.StringField(default='', max_length=1024, null=False)
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseRoomNum = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseShareArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseStructure = fields.StringField(
        default='', max_length=1024, null=False)
    HouseRoomType = fields.StringField(default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateCode = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=1024, null=False)
    HouseInnerUnitPrice = fields.StringField(
        default='', max_length=1024, null=False)
    HouseBuildingUnitPrice = fields.StringField(
        default='', max_length=1024, null=False)
    HouseType = fields.StringField(default='', max_length=1024, null=False)
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
