# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseDalian


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoDalian
    fields_map = {'RecordTime': 'CurTimeStamp',
                  'ProjectName': 'ProjectName',
                  'PromotionName': '',
                  'RealEstateProjectID': '',
                  'ProjectUUID': 'ProjectUUID',
                  'DistrictName': '',
                  'RegionName': '',
                  'ProjectAddress': 'ProjectAddress',
                  'ProjectType': '',
                  'OnSaleState': '',
                  'LandUse': '',
                  'HousingCount': '',
                  'Developer': 'ProjectCompany',
                  'FloorArea': '',
                  'TotalBuidlingArea': '',
                  'BuildingType': '',
                  'HouseUseType': '',
                  'PropertyRightsDescription': '',
                  'ProjectApproveData': '',
                  'ProjectBookingData': '',
                  'LssueDate': '',
                  'PresalePermitNumber': 'ProjectRegName',
                  'HouseBuildingCount': '',
                  'ApprovalPresaleAmount': '',
                  'ApprovalPresaleArea': '',
                  'AveragePrice': '',
                  'EarliestStartDate': '',
                  'CompletionDate': '',
                  'EarliestOpeningTime': '',
                  'LatestDeliversHouseDate': '',
                  'PresaleRegistrationManagementDepartment': '',
                  'LandLevel': '',
                  'GreeningRate': '',
                  'FloorAreaRatio': '',
                  'ManagementFees': '',
                  'ManagementCompany': '',
                  'OtheRights': '',
                  'CertificateOfUseOfStateOwnedLand': '',
                  'ConstructionPermitNumber': '',
                  'QualificationNumber': '',
                  'LandUsePermit': 'ProjectAreaPlanLicenseCode',
                  'BuildingPermit': 'ProjectPlanLicenseCode',
                  'LegalPersonNumber': '',
                  'LegalPerson': 'ProjectCorporation',
                  'SourceUrl': 'SourceUrl',
                  'Decoration': '',
                  'ParkingSpaceAmount': '',
                  'Remarks': '',
                  'ExtraJson': '',
                  }


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoDalian
    fields_map = {'RecordTime': 'CurTimeStamp',
                  'ProjectName': 'ProjectName',
                  'RealEstateProjectID': '',
                  'ProjectUUID': 'ProjectUUID',
                  'BuildingName': 'BuildingName',
                  'BuildingID': '',
                  'BuildingUUID': 'BuildingUUID',
                  'UnitName': '',
                  'UnitID': '',
                  'UnitUUID': '',
                  'PresalePermitNumber': 'BuildingRegName',
                  'Address': 'BuildingAddress',
                  'OnTheGroundFloor': '',
                  'TheGroundFloor': '',
                  'EstimatedCompletionDate': '',
                  'HousingCount': 'BuildingHouseNum',
                  'Floors': '',
                  'ElevatorHouse': '',
                  'IsHasElevator': '',
                  'ElevaltorInfo': '',
                  'BuildingStructure': '',
                  'BuildingType': '',
                  'BuildingHeight': '',
                  'BuildingCategory': '',
                  'Units': '',
                  'UnsoldAmount': '',
                  'BuildingAveragePrice': '',
                  'BuildingPriceRange': '',
                  'BuildingArea': 'BuildingArea',
                  'Remarks': '',
                  'SourceUrl': 'BuildingURL',
                  'ExtraJson': '',
                  }


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoDalian
    fields_map = {'RecordTime': 'CurTimeStamp',
                  'CaseTime': '',
                  'ProjectName': 'ProjectName',
                  'RealEstateProjectID': '',
                  'ProjectUUID': 'ProjectUUID',
                  'BuildingName': 'BuildingName',
                  'BuildingID': '',
                  'BuildingUUID': 'BuildingUUID',
                  'DistrictName': '',
                  'UnitName': '',
                  'UnitID': '',
                  'UnitUUID': '',
                  'HouseNumber': '',
                  'HouseName': 'HouseName',
                  'HouseID': '',
                  'HouseUUID': 'HouseUUID',
                  'Address': '',
                  'FloorName': 'HouseFloor',
                  'ActualFloor': '',
                  'FloorCount': '',
                  'FloorType': '',
                  'FloorHight': '',
                  'UnitShape': '',
                  'UnitStructure': '',
                  'Rooms': '',
                  'Halls': '',
                  'Kitchens': '',
                  'Toilets': '',
                  'Balconys': '',
                  'UnenclosedBalconys': '',
                  'HouseShape': '',
                  'Dwelling': '',
                  'ForecastBuildingArea': '',
                  'ForecastInsideOfBuildingArea': '',
                  'ForecastPublicArea': '',
                  'MeasuredBuildingArea': '',
                  'MeasuredInsideOfBuildingArea': '',
                  'MeasuredSharedPublicArea': '',
                  'MeasuredUndergroundArea': '',
                  'Toward': '',
                  'HouseType': '',
                  'HouseNature': '',
                  'Decoration': '',
                  'NatureOfPropertyRight': '',
                  'HouseUseType': 'HouseUsage',
                  'BuildingStructure': '',
                  'HouseSalePrice': '',
                  'SalePriceByBuildingArea': '',
                  'SalePriceByInsideOfBuildingArea': '',
                  'IsMortgage': '',
                  'IsAttachment': '',
                  'IsPrivateUse': '',
                  'IsMoveBack': '',
                  'IsSharedPublicMatching': '',
                  'SellState': '',
                  'SellSchedule': '',
                  'HouseState': 'HouseSaleState',
                  'HouseStateLatest': 'HouseSaleStateLatest',
                  'HouseLabel': '',
                  'HouseLabelLatest': '',
                  'TotalPrice': '',
                  'Price': '',
                  'PriceType': '',
                  'DecorationPrice': '',
                  'Remarks': '',
                  'SourceUrl': '',
                  'ExtraJson': '',
                  }
