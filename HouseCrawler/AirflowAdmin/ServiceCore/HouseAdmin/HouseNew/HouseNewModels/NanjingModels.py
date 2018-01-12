# -*- coding: utf-8 -*-
import uuid
import datetime
from django_mongoengine import *
from django_mongoengine import fields


class ProjectBaseNanjing(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    ProjectNo = fields.StringField(default='', max_length=255, null=False)

    ProjectName = fields.StringField(default='', max_length=255,)
    ProjectDetailUrl = fields.URLField(default=None, null=True, blank=True)
    PresalePermitNumber = fields.StringField(default='', max_length=255,)
    DistrictName = fields.StringField(default='', max_length=255,)
    NewOpeningTime = fields.StringField(default='', max_length=255,)
    ProjectType = fields.StringField(default='', max_length=255,)
    ProjectSalePhoneNumber = fields.StringField(default='', max_length=255,)
    ProjectAddress = fields.StringField(default='', max_length=255,)
    Developer = fields.StringField(default='', max_length=255,)
    AgentSaleComs = fields.StringField(default='', max_length=10240,)

    PresalePermits = fields.StringField(default='', max_length=10240,)
    CertificateOfUseOfStateOwnedLand = fields.StringField(
        default='', max_length=10240,)
    LandUsePlanningLicense = fields.StringField(default='', max_length=10240,)
    ProjectPlanningLicense = fields.StringField(default='', max_length=10240,)
    ConstructionPermitNumbers = fields.StringField(
        default='', max_length=10240,)
    InWebNum = fields.StringField(default='', max_length=255,)
    InWebAreas = fields.StringField(default='', max_length=255,)
    UnsoldNum = fields.StringField(default='', max_length=255,)
    UnsoldAreas = fields.StringField(default='', max_length=255,)
    GarageUnsoldNum = fields.StringField(default='', max_length=255,)
    GarageUnsoldAreas = fields.StringField(default='', max_length=255,)
    TodaySubscriptionNum = fields.StringField(default='', max_length=255,)
    TodayDealNum = fields.StringField(default='', max_length=255,)
    TotalSubscriptionNum = fields.StringField(default='', max_length=255,)
    TotalSubscriptionAreas = fields.StringField(default='', max_length=255,)
    TotalDealNum = fields.StringField(default='', max_length=255,)
    TotalDealAreas = fields.StringField(default='', max_length=255,)
    BussessMonthPrice = fields.StringField(default='', max_length=255,)
    HouseTotalPrice = fields.StringField(default='', max_length=255,)
    OfficeTotalPrice = fields.StringField(default='', max_length=255,)
    BussessTotalPrice = fields.StringField(default='', max_length=255,)
    HouseMonthPrice = fields.StringField(default='', max_length=255,)
    OfficeMonthPrice = fields.StringField(default='', max_length=255,)
    ProjectManageCom = fields.StringField(default='', max_length=255,)
    ProjectBuildCom = fields.StringField(default='', max_length=255,)
    ProjectDesignCom = fields.StringField(default='', max_length=255,)
    ProjectEnvironmentalDesignCom = fields.StringField(
        default='', max_length=255,)
    ProjectIntroduce = fields.StringField(default='', max_length=102400)
    SourceUrl = fields.URLField(default=None, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectNo',
        ]
    }


class BuildingBaseNanjing(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    BuildingNo = fields.StringField(default='', max_length=255, null=False)
    ProjectName = fields.StringField(default='', max_length=255, )

    BuildingName = fields.StringField(default='', max_length=255,)
    BuildingUrl = fields.URLField(default=None, null=True, blank=True)
    BuildingHouseType = fields.StringField(default='', max_length=255,)
    TodaySubscriptionNum = fields.StringField(default='', max_length=255,)
    TodayDealNum = fields.StringField(default='', max_length=255,)
    PlanOpenDate = fields.StringField(default='', max_length=255,)
    InWebNum = fields.StringField(default='', max_length=255,)
    CanSaleNum = fields.StringField(default='', max_length=255,)
    TotalSubscriptionNum = fields.StringField(default='', max_length=255,)
    TotalDealNum = fields.StringField(default='', max_length=255,)
    SaleAreas = fields.StringField(default='', max_length=255,)
    MeanPrice = fields.StringField(default='', max_length=255,)
    DealRatio = fields.StringField(default='', max_length=255,)
    SourceUrl = fields.URLField(default=None, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'BuildingNo',
        ]
    }


class HouseBaseNanjing(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    HouseNo = fields.StringField(default='', max_length=255, null=False)
    HouseSts = fields.StringField(default='', max_length=255, null=False)
    HouseStsLatest = fields.StringField(default='', max_length=255, null=False)

    ProjectName = fields.StringField(default='', max_length=255,)
    BuildingName = fields.StringField(default='', max_length=255,)
    HouseName = fields.StringField(default='', max_length=255,)
    HouseType = fields.StringField(default='', max_length=255,)
    HouseAresPrice = fields.StringField(default='', max_length=255,)
    HouseUrl = fields.URLField(default=None, null=True, blank=True)
    ForecastBuildingArea = fields.StringField(default='', max_length=255,)
    ForecastInsideOfBuildingArea = fields.StringField(
        default='', max_length=255,)
    HouseInfo = fields.DictField(default={"defult": "0"}, index=True)
    ForecastPublicArea = fields.StringField(default='', max_length=255,)
    SourceUrl = fields.URLField(default=None, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'HouseNo',
        ]
    }


class DeveloperBaseNanjing(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    DeveloperNo = fields.StringField(default='', max_length=255, null=False)

    DeveloperName = fields.StringField(default='', max_length=255,)
    DeveloperComAddress = fields.StringField(default='', max_length=255,)
    DeveloperZipCode = fields.StringField(default='', max_length=255,)
    DeveloperInfoUrl = fields.URLField(default=None, null=True, blank=True)
    Legalrepresentative = fields.StringField(default='', max_length=255,)
    CorporateCode = fields.StringField(default='', max_length=255,)
    GeneralManager = fields.StringField(default='', max_length=255,)
    ContactNumber = fields.StringField(default='', max_length=255,)
    Businesslicensenumber = fields.StringField(default='', max_length=255,)
    BusinessRegistrationDay = fields.StringField(default='', max_length=255,)
    LicenseExpiryDate = fields.StringField(default='', max_length=255,)
    RegisteredCapital = fields.StringField(default='', max_length=255,)
    BusinessRegistrationType = fields.StringField(default='', max_length=255,)
    Email = fields.StringField(default='', max_length=255,)
    RegisteredAddress = fields.StringField(default='', max_length=255,)
    BusinessAddress = fields.StringField(default='', max_length=255,)
    BusinessScope = fields.StringField(default='', max_length=255,)
    QualificationCertificateNumber = fields.StringField(
        default='', max_length=255,)
    QualificationLevel = fields.StringField(default='', max_length=255,)
    QualificationCertificationDate = fields.StringField(
        default='', max_length=255,)
    QualificationPeriod = fields.StringField(default='', max_length=255,)
    Approvedfortheday = fields.StringField(default='', max_length=255,)
    AnnualInspection = fields.StringField(default='', max_length=255,)
    CompanyProfile = fields.StringField(default='', max_length=102400,)
    SourceUrl = fields.URLField(default=None, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'DeveloperNo',
        ]
    }


class PresaleBaseNanjing(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    change_data = fields.StringField(default='', max_length=1023, null=False)
    PresaleNo = fields.StringField(default='', max_length=255, null=False)

    Numbering = fields.StringField(default='', max_length=255,)
    SalesUnit = fields.StringField(default='', max_length=255,)
    DistrictBelongs = fields.StringField(default='', max_length=255,)
    TheHouseIsLocated = fields.StringField(default='', max_length=255,)
    ProjectName = fields.StringField(default='', max_length=255,)
    LandUseCardNumber = fields.StringField(default='', max_length=255,)
    OpeningTime = fields.StringField(default='', max_length=255,)
    LandUseperiod = fields.StringField(default='', max_length=255,)
    HousingUseOfNature = fields.StringField(default='', max_length=255,)
    PlanningPermitNumber = fields.StringField(default='', max_length=255,)
    SourceUrl = fields.URLField(default=None, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'PresaleNo',
        ]
    }
