import urllib2
import json

apiUrl = "http://www.nhtsa.gov/webapi/api/SafetyRatings"
outputFormat = "?format=json" 

class CarApplication(object):
    def __init__(self):

        print "This program will let you search through NTSHA's database of 5 star saftey rating vehicles\n"
        
        self.yearList = []
        self.makeList = []
        self.modelList = []
        self.variantDict = {}

        self.desiredYear = 0
        self.desiredMake = ""
        self.desiredModel = ""
        self.desiredVariant = ""
    def getListResponse(self, apiParam, key):
        daList = []
        
        response = urllib2.urlopen(apiUrl + apiParam + outputFormat)
        json_obj = json.load(response)

        for objectCollection in json_obj['Results']:
                # Loop each vehicle in the vehicles collection
            daList.append(str(objectCollection[key]))

        return daList
    def getDictionaryResponse(self, apiParam):
        daDict = {}

        value = "VehicleDescription"
        key = "VehicleId"
        
        response = urllib2.urlopen(apiUrl + apiParam + outputFormat)
        json_obj = json.load(response)

        for objectCollection in json_obj['Results']:
                # Loop each vehicle in the vehicles collection
            daDict[objectCollection[key]] = str(objectCollection[value])

        return daDict

    def getDetailedResponse(self, apiParam):
        self.car = Car(self.desiredYear, self.desiredMake, self.desiredModel, self.desiredVariant)
        response = urllib2.urlopen(apiUrl + apiParam + outputFormat)
        json_obj = json.load(response)

        for objectCollection in json_obj['Results']:
                # Loop each vehicle in the vehicles collection

            self.car.overallRating = objectCollection["OverallRating"]
            self.car.overallFrontCrashRating = objectCollection["OverallFrontCrashRating"]
            self.car.frontCrashDriversideRating = objectCollection["FrontCrashDriversideRating"]
            self.car.overallSideCrashrating = objectCollection["OverallFrontCrashRating"]
            self.car.sideCrashDriversideRating = objectCollection["SideCrashDriversideRating"]
            self.car.sideCrashPassengersideRating = objectCollection["SideCrashPassengersideRating"]
            self.car.rolloverRating = objectCollection["RolloverRating"]
            self.car.rolloverRating2 = objectCollection["RolloverRating2"]
            self.car.rolloverPossibility = objectCollection["RolloverPossibility"]
            self.car.rolloverPossibility2 = objectCollection["RolloverPossibility2"]
            self.car.sidePoleCrashRating = objectCollection["SidePoleCrashRating"]

            self.car.NHTSAElectronicStabilityControl = objectCollection.get("NHTSAElectronicStabilityControl")
            self.car.complaintsCount = objectCollection["ComplaintsCount"]
            self.car.recallsCount = objectCollection["RecallsCount"]
            self.car.investigationCount = objectCollection["InvestigationCount"]
            
            
    
    def populateYearList(self):
        self.yearList = self.getListResponse("", "ModelYear")
    def populateMakeList(self):
        self.makeList = self.getListResponse("/modelyear/" + self.desiredYear, "Make")
    def populateModelList(self):
        self.modelList = self.getListResponse("/modelyear/" + self.desiredYear + "/make/" + self.desiredMake, "Model")
    def populateVariantDict(self):
        self.variantList = self.getDictionaryResponse("/modelyear/" + self.desiredYear + "/make/" + self.desiredMake + "/model/" + self.desiredModel)
    def setDesiredYear(self):
        self.populateYearList()
        for x in self.yearList:
            print x
        self.desiredYear = raw_input("What year do you want? ")
    def setDesiredMake(self):
        self.populateMakeList()
        for x in self.makeList:
            print x
        print '\n'
        self.desiredMake = raw_input("What make do you want? ")
    def setDesiredModel(self):
        self.populateModelList()
        for x in self.modelList:
            print x
        print '\n'
        self.desiredModel = raw_input("What model do you want? ")
    def setVariant(self): # vehicle id
        self.populateVariantDict()
        print self.variantList.items()
        print '\n'
        self.desiredVariant = raw_input("What variant do you want (Type down the vehicle id)? ")
    def setDetailedInfo(self):
        self.getDetailedResponse("/VehicleId/" + self.desiredVariant)
        

class Car(object):
    def __init__(self, year, make, model, variant):
        self.year = year
        self.make = make
        self.model = model
        self.variant = variant

        #if you are using this for statistical data you might want to make these integers
        self.overallRating = ""
        self.overallFrontCrashRating = ""
        self.frontCrashDriversideRating = ""
        self.overallSideCrashrating = ""
        self.sideCrashDriversideRating = ""
        self.sideCrashPassengersideRating = ""
        self.rolloverRating = ""
        self.rolloverRating2 = ""
        self.rolloverPossibility = ""
        self.rolloverPossibility2 = ""
        self.sidePoleCrashRating = ""

        self.NHTSAElectronicStabilityControl = ""
        self.complaintsCount = ""
        self.recallsCount = ""
        self.investigationCount = ""

    def __repr__(self):
        s = ""
        
        s += "Year: %s\nMake: %s\nModel: %s\nVehicle ID: %s\n\n" % (self.year, self.make, self.model, self.variant)

        s += "Overall Rating: %s\n" % self.overallRating
        s += "Overall Front Crash Rating: %s\n" % self.overallFrontCrashRating
        s += "Front Crash driver side Rating: %s\n" % self.frontCrashDriversideRating
        s += "Overall Side Crash Rating: %s\n" % self.overallSideCrashrating
        s += "Side Crash Driverside Rating: %s\n" % self.sideCrashDriversideRating
        s += "Side Crash passenger side Rating: %s\n" % self.sideCrashPassengersideRating
        s += "Rollover Rating 1: %s\n" % self.rolloverRating
        s += "Rollover Rating 2: %s\n" % self.rolloverRating2
        s += "Rollover Possibility 1: %s\n" % self.rolloverPossibility
        s += "Rollover Possibility 2: %s\n" % self.rolloverPossibility2
        s += "Side Pole Crash Rating: %s\n" % self.sidePoleCrashRating
        if (self.NHTSAElectronicStabilityControl != "None"):
            s += "NHTSA Electronic Stability Control: %s\n" % self.NHTSAElectronicStabilityControl
        s += "Complaints count: %s\n" % self.complaintsCount
        s += "Recalls Count: %s\n" % self.recallsCount
        s += "Investigation Count: %s\n" % self.investigationCount

        return s
#start of main
app = CarApplication()
app.setDesiredYear()
app.setDesiredMake()
app.setDesiredModel()
app.setVariant()
app.setDetailedInfo()
print app.car
goodbye = raw_input("Goodbye")
