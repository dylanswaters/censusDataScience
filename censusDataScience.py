#!usr/bin/python3

class raceProportionsRow:
    'one row to store race proportions, stored as raceProp in censusRow'

    def __init__(self, races):
        #array of 6 columns
        self.race = [0.0]*6
        self.race[0] = races[0]
        self.race[1] = races[1]
        self.race[2] = races[2]
        self.race[3] = races[3]
        self.race[4] = races[4]
        self.race[5] = races[5]

    #leftover test function
    def displayContents(self):
        print("H   W   B   N   A   P")
        for i in range(0, len(self.race)):
            print(self.race[i] + ":", end=' ')
        print("")

    def checkRaceForBigger(self, indexToCheck, valueHigherThan):
        if not self.race[indexToCheck].strip():
            return 0
        if(float(self.race[indexToCheck]) > valueHigherThan):
            return 1
        else:
            return 0

    def checkRaceForBiggerOrEqual(self, indexToCheck, valueHigherThan):
        if not self.race[indexToCheck].strip():
            return 0
        if(float(self.race[indexToCheck]) >= valueHigherThan):
            return 1
        else:
            return 0

    def displayValue(self, index):
        return self.race[index]

    def checkForEmpty(self):
        if not self.race[0].strip():
            return 1
        else:
            return 0


class censusRow:
    'holds one row of census data'

    def selfCheck(self):
        if(self.tract is None):
            self.tract = ""
        if(self.state is None):
            self.state = ""
        if(self.county is None):
            self.county = ""
        if(self.totalPop is None):
            self.totalPop = ""
        if(self.women is None):
            self.women = ""
        if(self.raceProp is None):
            self.raceProp = ""
        if(self.income is None):
            self.income = ""
        if(self.poverty is None):
            self.poverty = ""
        if(self.unemployment is None):
            self.unemployment = ""

    def __init__(self, tract, state, county, totalPop, women, raceProp, income, poverty, unemployment):
        self.tract = tract
        self.state = state
        self.county = county
        self.totalPop = totalPop
        self.women = women
        self.raceProp = raceProp
        self.income = income
        self.poverty = poverty
        self.unemployment = unemployment
        self.selfCheck()

    #leftover test function, prints contents of one tract
    def displayContents(self):
        print("tract: " + self.tract + " state: " + self.state + " county: " + self.county + " totalPop: " + self.totalPop + " Women: " + self.women + " income: " + self.income + " poverty: " + self.poverty + " unemployment " + self.unemployment)
        self.raceProp.displayContents()

def noneToEmptyString(checkStr):
    if(checkStr is None):
        return ""
    if(checkStr is not None):
        return checkStr

def readCensusFile(fileLocation):
    #open the file, skip the first line
    datafile = open(fileLocation, 'r')
    datafile.readline()
    #array to hold censusRow objects
    censusStorage = []

    for line in datafile:
        data = line.split(",")
        #array to store race values
        raceArray = []
        #get races
        for i in range(0, 6):
            #append value if there is one, otherwise append 0
            if(data[i + 6] is not None):
                raceArray.append(data[i+6])
            else:
                raceArray.append(0)
        raceProp = raceProportionsRow(raceArray)
        censusStorage.append(censusRow(noneToEmptyString(data[0]), noneToEmptyString(data[1]), noneToEmptyString(data[2]), noneToEmptyString(data[3]), noneToEmptyString(data[5]), raceProp, noneToEmptyString(data[13]), noneToEmptyString(data[17]), noneToEmptyString(data[36])))
    datafile.close
    return censusStorage

# part 1
def raceDensityCalc(censusStorage):
    print("Part 1")
    hispanicState = ""
    whiteState = ""
    blackState = ""
    nativeState = ""
    asianState = ""
    pacificState = ""
    hispanicHighest = 0
    whiteHighest = 0
    blackHighest = 0
    nativeHighest = 0
    asianHighest = 0
    pacificHighest = 0
    newState = censusStorage[0].state
    raceTotalPop = [0.0]*6
    newStateTotalPop = 0.0
    for i in range(0, len(censusStorage)):
        if(censusStorage[i].state == "Puerto Rico" or censusStorage[i].state == "District of Columbia"):
            continue
        if not censusStorage[i].totalPop.strip():
            continue
        if(censusStorage[i].raceProp.checkForEmpty()):
            continue
        if(censusStorage[i].state == newState):
            # print("total pop: " + censusStorage[i].totalPop)
            # print(censusStorage[i].raceProp.displayContents())
            for j in range(0, 6):
                raceTotalPop[j] += float(censusStorage[i].raceProp.displayValue(j)) * float(censusStorage[i].totalPop)
            newStateTotalPop += float(censusStorage[i].totalPop)
        else:
            if(raceTotalPop[0] > hispanicHighest):
                hispanicHighest = raceTotalPop[0]
                hispanicState = newState
            if(raceTotalPop[1] > whiteHighest):
                whiteHighest = raceTotalPop[1]
                whiteState = newState
            if(raceTotalPop[2] > blackHighest):
                blackHighest = raceTotalPop[2]
                blackState = newState
            if(raceTotalPop[3] > nativeHighest):
                nativeHighest = raceTotalPop[3]
                nativeState = newState
            if(raceTotalPop[4] > asianHighest):
                asianHighest = raceTotalPop[4]
                asianState = newState
            if(raceTotalPop[5] > pacificHighest):
                pacificHighest = raceTotalPop[5]
                pacificState = newState
            newState = censusStorage[i].state
            for j in range(0, 6):
                raceTotalPop[j] = float(censusStorage[i].raceProp.displayValue(j)) * float(censusStorage[i].totalPop)
            newStateTotalPop = float(censusStorage[i].totalPop)
    print("    Most Hispanic State: " + hispanicState)
    print("    Most White State: " + whiteState)
    print("    Most Black State: " + blackState)
    print("    Most Native State: " + nativeState)
    print("    Most Asian State: " + asianState)
    print("    Most Pacific State: " + pacificState)

#part 2
#must find state totals first?
def unemploymentCalc(censusStorage):
    print("Part 2")
    newState = censusStorage[0].state
    newStateUnemployment = 0
    newStatePopulation = 0
    highestUnemployment = 0
    lowestUnemployment = 100
    highestUnemploymentString = ""
    lowestUnemploymentString = ""
    for i in range(0, len(censusStorage)):
        if(censusStorage[i].state == "Puerto Rico" or censusStorage[i].state == "District of Columbia"):
            continue
        if not censusStorage[i].unemployment.strip():
            continue
        if not censusStorage[i].totalPop.strip():
            continue
        if(censusStorage[i].state == newState):
            newStatePopulation += int(censusStorage[i].totalPop)
            newStateUnemployment += float(censusStorage[i].totalPop) * float(censusStorage[i].unemployment)
        else:
            if( (newStateUnemployment / newStatePopulation) > highestUnemployment ):
                highestUnemployment = (newStateUnemployment / newStatePopulation)
                highestUnemploymentString = newState
            if( (newStateUnemployment / newStatePopulation) < lowestUnemployment ):
                lowestUnemployment = (newStateUnemployment / newStatePopulation)
                lowestUnemploymentString = newState
            newState = censusStorage[i].state
            newStatePopulation = int(censusStorage[i].totalPop)
            newStateUnemployment = float(censusStorage[i].totalPop) * float(censusStorage[i].unemployment)
    print("    Highest Unemployment: " + highestUnemploymentString + ": " + str(highestUnemployment) + "%")
    print("    Lowest Unemployment: " + lowestUnemploymentString + ": " + str(lowestUnemployment) + "%")

#part 3
def incomeInequalityCalc(censusStorage):
    print("Part 3")
    for i in range(0, len(censusStorage)):
        if not censusStorage[i].income.strip():
            continue
        if not censusStorage[i].poverty.strip():
            continue
        if(float(censusStorage[i].income) >= 50000 and float(censusStorage[i].poverty) > 50):
            printGeneral(censusStorage, i)

#part 4
def feminineMajorityCalc(censusStorage):
    print("Part 4")
    for i in range(0, len(censusStorage)):
        if not censusStorage[i].women.strip():
            continue
        if not censusStorage[i].totalPop.strip():
            continue
        if(float(censusStorage[i].totalPop) >= 10000 and float(censusStorage[i].women) > 57):
            printGeneral(censusStorage, i)

#part 5
def diverseTractCalc(censusStorage):
    print("Part 5")
    for i in range(0, len(censusStorage)):
        diverseCount = 0
        for j in range(0, 6):
            if(censusStorage[i].raceProp.checkRaceForBiggerOrEqual(j, 15) == 1):
                diverseCount += 1
        if(diverseCount >= 4):
            printGeneral(censusStorage, i)

def printGeneral(censusStorage, i):
    print("    tract: " + censusStorage[i].tract + " county: " + censusStorage[i].county + " state: " + censusStorage[i].state, end =' ')
    if(censusStorage[i].raceProp.checkRaceForBigger(0, 1) == 1):
         print("Hispanic: " + censusStorage[i].raceProp.displayValue(0), end=' ')
    if(censusStorage[i].raceProp.checkRaceForBigger(1, 1) == 1):
        print("White: " + censusStorage[i].raceProp.displayValue(1), end=' ')
    if(censusStorage[i].raceProp.checkRaceForBigger(2, 1) == 1):
        print("Black: " + censusStorage[i].raceProp.displayValue(2), end=' ')
    if(censusStorage[i].raceProp.checkRaceForBigger(3, 1) == 1):
        print("Native: " + censusStorage[i].raceProp.displayValue(3), end=' ')
    if(censusStorage[i].raceProp.checkRaceForBigger(4, 1) == 1):
        print("Asian: " + censusStorage[i].raceProp.displayValue(4), end=' ')
    if(censusStorage[i].raceProp.checkRaceForBigger(5, 1) == 1):
        print("Pacific: " + censusStorage[i].raceProp.displayValue(5), end=' ')
    print("")

censusFileLocation = ("acs2015_census_tract_data.csv")
countyFileLocation = ("acs2015_county_data.csv")
censusStorage = readCensusFile(censusFileLocation)
# for i in range(0, len(censusStorage)):
#      print(censusStorage[i].displayContents())
raceDensityCalc(censusStorage)
unemploymentCalc(censusStorage)
incomeInequalityCalc(censusStorage)
# feminineMajorityCalc(censusStorage)
# diverseTractCalc(censusStorage)
