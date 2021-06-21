#import modules
import json
import pandas as pd
import schedule
import time

#import classes from ./ folder
import timescaledbAccess

#read fibonacci retracements  from json
with open('fibLvl.json') as file:
    fibLvl = json.load(file)

class backAccess:
    def __init__(self):
        self.timescale = timescaledbAccess.timescaleAccess()
        #read if live trading is enabled
        try:
            self.dbTable=env("dbTable")
        except KeyError:
            print("No env variables set.")
            sys.exit(1)

    def calculateResult(self, resultData, i):
        stopId = resultData[resultData[0] == resultData[0].min()]
        percentChange = ((stopId[1] - self.bA[4][i]) / self.bA[4][i]) * 100
        #update dataself.bAse to include buy statement
        sql = ("UPDATE " + self.dbTable + " SET" +
            " resultpercent = '" + str(float(percentChange)) +
            "', stopid = '" + str(float(stopId[0])) +
            "' WHERE id = '" + str(self.bA[0][i]) +
            "';")
        self.timescale.sqlUpdate(sql)

    def validate(self):
        sql = ("SELECT id, symbol, takeprofit, stoploss, askprice" +
            " FROM " + self.dbTable + " WHERE" +
            " resultpercent IS NULL " +
            " AND takeprofit IS NOT NULL;")
        self.bA = pd.DataFrame(self.timescale.sqlQuery(sql))
        if len(self.bA) > 0:
            self.bA[0] = pd.to_numeric(self.bA[0])
            self.bA[2] = pd.to_numeric(self.bA[2])
            self.bA[3] = pd.to_numeric(self.bA[3])
            self.bA[4] = pd.to_numeric(self.bA[4])
            for i, row in self.bA.iterrows():
                sql = ("select id, askprice from " + self.dbTable + " where id > '" + str(self.bA[0][i]) +
                        "' and symbol = '" + str(self.bA[1][i]) + "';")
                validated = pd.DataFrame(self.timescale.sqlQuery(sql))
                if len(validated) > 0:
                    validated[0] = pd.to_numeric(validated[0])
                    validated[1] = pd.to_numeric(validated[1])
                    tpData = validated[validated[1] >= self.bA[2][i]]
                    slData = validated[validated[1] <= self.bA[3][i]]
                    if (len(slData) > 0 and len(slData) > 0 and
                        slData[0].min() < tpData[0].min()):
                        self.calculateResult(slData, i)
                    elif (len(slData) > 0 and len(slData) > 0 and
                        slData[0].min() > tpData[0].min()):
                        self.calculateResult(tpData, i)
                    elif len(slData) > 0:
                        self.calculateResult(slData, i)
                    elif len(tpData) > 0:
                        self.calculateResult(tpData, i)
                    else:
                        pass
        self.timescale.databaseClose()
