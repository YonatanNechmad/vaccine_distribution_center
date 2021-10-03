# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from Repository import repo
from myDAOs import vaccines
from myDTOs import Vaccine
from myDAOs import suppliers
from myDTOs import Supplier
from myDAOs import clinics
from myDTOs import Clinic
from myDAOs import logistics
from myDTOs import Logistic


def main():
    repo.create_tables()
    summery = [0, 0, 0, 0, 0]
    summery = initTable(summery)
    numOfVec = summery[4]
    summery = summery[0:4]
    repo.setSum(summery, numOfVec)
    makeOrders()


def makeOrders():
    with open(sys.argv[2]) as ordersFile:
        ordersFileLines = ordersFile.readlines()
        for line in ordersFileLines:
            y = line.split(",")
            if len(y) == 3:
                repo.receiveShipment(y[0], int(y[1]), y[2])
            else:
                repo.sendShipment(y[0], int(y[1]))
            with open(sys.argv[3], "a") as output:  # check 'w+'
                output.write('\n')

def initTable(summery):
    # read and use repo
    with open(sys.argv[1]) as configFile:
        configFileLines = configFile.readlines()
        numOfVaccinesLines = int(configFileLines[0].split(',')[0])
        numOfSupplierLines = int(configFileLines[0].split(',')[1])
        numOfClinicsLines = int(configFileLines[0].split(',')[2])
        numOfLogisticLines = int(configFileLines[0].split(',')[3])
        total_inventory = 0
        for i in range(1, numOfVaccinesLines+1):
            myVecLine = configFileLines[i].split(',')
            repo.vaccines.insert(Vaccine(*myVecLine))
            total_inventory = total_inventory + (int(myVecLine[3]))

        summery[0] = total_inventory
        summery[4] = numOfVaccinesLines
        point = 1 + numOfVaccinesLines

        for i in range(point, point + numOfSupplierLines):
            mySupLine = configFileLines[i].split(',')
            repo.suppliers.insert(Supplier(*mySupLine))

        point = point + numOfSupplierLines
        total_demand = 0
        for i in range(point, point + numOfClinicsLines):
            myCliLine = configFileLines[i].split(',')
            repo.clinics.insert(Clinic(*myCliLine))
            total_demand = total_demand + (int(myCliLine[2]))

        summery[1] = total_demand
        point = point + numOfClinicsLines

        for i in range(point, point + numOfLogisticLines):
            myLogLine = configFileLines[i].split(',')
            repo.logistics.insert(Logistic(*myLogLine))

        return summery


if __name__ == '__main__':
    main()
