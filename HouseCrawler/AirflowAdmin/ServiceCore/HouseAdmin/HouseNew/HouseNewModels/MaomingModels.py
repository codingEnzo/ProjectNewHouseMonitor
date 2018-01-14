# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


# Maoming Model
class IndexInfoMaoming(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(
        datetime.datetime.now()), max_length=255, index=True)
    District = fields.StringField(default='', max_length=255, null=False)
    Date = fields.StringField(default='', max_length=255, null=False)
    HouseSaleInfo = fields.DictField(default={'code': 0}, null=False)
    OfficeSaleInfo = fields.DictField(default={'code': 0}, null=False)
    BussinessSaleInfo = fields.DictField(default={'code': 0}, null=False)
    OtherSaleInfo = fields.DictField(default={'code': 0}, null=False)
    AllSaleInfo = fields.DictField(default={'code': 0}, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'Date',
            'District'
        ]
    }


class ProjectBaseMaoming(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(
        datetime.datetime.now()), max_length=255, index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectDistrict = fields.StringField(
        default='', max_length=255, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectURL',
            'ProjectName'
        ]
    }


class ProjectInfoMaoming(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectCompany = fields.StringField(default='', max_length=255, null=False)
    CompanyUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    ProjectBuildingNum = fields.StringField(
        default='', max_length=255, null=False)
    ProjectDistrict = fields.StringField(
        default='', max_length=255, null=False)
    ProjectEngPlanLicense = fields.StringField(
        default='', max_length=255, null=False)
    ProjectPlanBuildingArea = fields.StringField(
        default='', max_length=255, null=False)
    ProjectLandLicense = fields.StringField(
        default='', max_length=255, null=False)
    ProjectLandArea = fields.StringField(
        default='', max_length=255, null=False)
    ProjectLandYearLimit = fields.StringField(
        default='', max_length=255, null=False)
    ProjectUsage = fields.StringField(default='', max_length=255, null=False)
    ProjectEngBuildingLicense = fields.StringField(
        default='', max_length=255, null=False)
    ProjectBuildingArea = fields.StringField(
        default='', max_length=255, null=False)
    ProjectSaleInfo = fields.DictField(default={'code': 0}, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'ProjectDistrict'
        ]
    }


class BuildingInfoMaoming(Document):
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
    BuildingRegUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                       binary=False, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    meta = {
        'indexes': [
            'BuildingName',
            'BuildingURL',
            'ProjectUUID',
            'BuildingUUID',
            'BuildingRegUUID',
            'ProjectName'

        ]
    }


class HouseInfoMaoming(Document):

    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=255, null=False)
    HouseSaleState = fields.StringField(default='', max_length=255, null=False)
    HouseFloor = fields.StringField(default='', max_length=255, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                 binary=False, null=False)
    HouseInnerArea = fields.StringField(default='', max_length=255, null=False)
    HouseBuildingArea = fields.StringField(
        default='', max_length=255, null=False)
    HouseUsage = fields.StringField(default='', max_length=255, null=False)
    HouseRegUnitPrice = fields.StringField(
        default='', max_length=255, null=False)
    HouseRegTotalPrice = fields.StringField(
        default='', max_length=255, null=False)
    HouseDealUnitPrice = fields.StringField(
        default='', max_length=255, null=False)
    HouseDealTotalPrice = fields.StringField(
        default='', max_length=255, null=False)
    HouseOrientation = fields.StringField(
        default='', max_length=255, null=False)
    HouseVisaDate = fields.StringField(default='', max_length=255, null=False)
    HouseManageCompany = fields.StringField(
        default='', max_length=255, null=False)
    HouseManagePrice = fields.StringField(
        default='', max_length=255, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=255, null=False)
    meta = {
        'indexes': [
            'HouseName',
            'BuildingName',
            'ProjectUUID',
            'BuildingUUID',
            'HouseUUID'
        ]
    }


class PreSellInfoMaoming(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    PreRegName = fields.StringField(default='', max_length=255, null=False)
    PreRegUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                  binary=False, null=False)
    PreHouseArea = fields.StringField(default='', max_length=255, null=False)
    PreHouseNum = fields.StringField(default='', max_length=255, null=False)
    PreLandLicense = fields.StringField(default='', max_length=255, null=False)
    PreLandUsage = fields.StringField(default='', max_length=255, null=False)
    PreLimitDate = fields.StringField(default='', max_length=255, null=False)
    PreDistrict = fields.StringField(default='', max_length=255, null=False)
    PreOpenDate = fields.StringField(default='', max_length=255, null=False)
    PreBankList = fields.ListField(default=[], null=False)
    PreInfoDetail = fields.DictField(default={'code': 0}, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'PreRegUUID'
        ]
    }


class CompanyInfoMaoming(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    CompanyName = fields.StringField(default='', max_length=255, null=False)
    CompanyUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    CompanyAddress = fields.StringField(default='', max_length=255, null=False)
    CompanyRegName = fields.StringField(default='', max_length=255, null=False)
    CompanyDeveloperRegName = fields.StringField(
        default='', max_length=255, null=False)
    CompanyRegDate = fields.StringField(default='', max_length=255, null=False)
    CompanyLevelLicense = fields.StringField(
        default='', max_length=255, null=False)
    CompanyRegCapital = fields.StringField(
        default='', max_length=255, null=False)
    CompanyLevel = fields.StringField(default='', max_length=255, null=False)
    CompanyType = fields.StringField(default='', max_length=255, null=False)
    CompanyConnect = fields.StringField(default='', max_length=255, null=False)
    CompanyPhone = fields.StringField(default='', max_length=255, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'CompanyUUID'
        ]
    }
