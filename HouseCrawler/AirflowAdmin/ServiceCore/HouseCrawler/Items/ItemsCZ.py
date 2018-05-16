# coding = utf-8
from scrapy_djangoitem import DjangoItem

from HouseNew.models import ProjectBaseChangzhou, ProjectInfoChangzhou, BuildingInfoChangzhou, HouseInfoChangzhou


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseChangzhou


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoChangzhou
    fields_map = {'RecordTime': '',
                  'ProjectName': 'ProjectName',
                  'PromotionName': '',
                  'RealEstateProjectID': '',
                  'ProjectUUID': 'ProjectUUID',
                  'DistrictName': '',
                  'RegionName': 'ProjectRegion',
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
                  'PresalePermitNumber': '',
                  'HouseBuildingCount': '',
                  'ApprovalPresaleAmount': 'ProjectPresaleHouseNum',
                  'ApprovalPresaleArea': 'ProjectPresaleArea',
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
                  'LandUsePermit': '',
                  'BuildingPermit': '',
                  'LegalPersonNumber': '',
                  'LegalPerson': '',
                  'SourceUrl': 'SourceUrl',
                  'Decoration': '',
                  'ParkingSpaceAmount': '',
                  'Remarks': '',
                  'ExtraJson': '',
                  }


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoChangzhou
    fields_map = {'RecordTime': '',
                  'ProjectName': 'ProjectName',
                  'ProjectUUID': 'ProjectUUID',
                  'RealEstateProjectID': '',
                  'BuildingName': 'BuildingName',
                  'BuildingID': '',
                  'BuildingUUID': 'BuildingUUID',
                  'UnitName': '',
                  'UnitID': '',
                  'UnitUUID': '',
                  'PresalePermitNumber': '',
                  'Address': '',
                  'OnTheGroundFloor': '',
                  'TheGroundFloor': '',
                  'EstimatedCompletionDate': '',
                  'HousingCount': '',
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
    django_model = HouseInfoChangzhou
    fields_map = {'RecordTime': '',
                  'CaseTime': '',
                  'ProjectName': 'ProjectName',
                  'ProjectUUID': 'ProjectUUID',
                  'RealEstateProjectID': '',
                  'BuildingName': 'BuildingName',
                  'BuildingUUID': 'BuildingUUID',
                  'BuildingID': '',
                  'DistrictName': '',
                  'UnitName': 'UnitName',
                  'UnitID': '',
                  'UnitUUID': '',
                  'HouseNumber': '',
                  'HouseName': 'HouseLabel',
                  'HouseID': '',
                  'HouseUUID': 'HouseUUID',
                  'Address': '',
                  'FloorName': '',
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
                  'MeasuredBuildingArea': 'HouseBuildingArea',
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
                  'HouseState': 'HouseSaleStatus',
                  'HouseStateLatest': 'HouseSaleStateLatest',
                  'HouseLabel': '',
                  'HouseLabelLatest': '',
                  'TotalPrice': '',
                  'Price': 'HouseContractPrice',
                  'PriceType': '',
                  'DecorationPrice': '',
                  'Remarks': '',
                  'SourceUrl': '',
                  'ExtraJson': '',
                  }
