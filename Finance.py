'''
@Title: Finance.py
@Author: Nathan North
@Org: North

@Description: A location to test ideas and implement functions that will end up
in the helper file.


'''

#IMPORTS
import datetime
import time
import os
import json

#CONSTANTS
tFileName = 'temp.txt'
oFileName = 'north_finance.txt'
outData = []


#FUNCTIONS

def readFinanceData(filename, datatype):
    uDATA = []
    tDATA = []
    bDATA = []
    with open(filename, 'r') as datafile:
        if datatype == 'user':
            for line in datafile:
                row = line.strip('\n')
                entry = json.loads(row)
                if entry['type'] == 'user':
                    uDATA.append(entry)
            return uDATA
        elif datatype == 'bank':
            for line in datafile:
                row = line.strip('\n')
                entry = json.loads(row)
                if entry['type'] == 'bank':
                    bDATA.append(entry)
            return bDATA
        elif datatype == 'trans':
            for line in datafile:
                row = line.strip('\n')
                entry = json.loads(row)
                if entry['type'] == 'trans':
                    tDATA.append(entry)
            return tDATA

def writeFinanceData(fDATA, filename):
    #fDATA is a single dictionary with some data
    with open(filename, 'a') as datafile:
        row = json.dumps(fDATA)
        datafile.write(row + '\n')

def mailMan(formData, action, filename='', fDATA=[]):
    #Carries/formats data from the UI to the backend and data file
    #fDATA is any one of the three styles of data depending on which action is taken
    if action == 'createUserProfile':
        error = None
        entry = {'type':'user'}
        try:
            bDATE = formData['birthday']
            bDATE = datetime.datetime.strptime(bDATE, '%m/%d/%Y')
        except:
            error = 'Invalid Birthday'
            return error

        if len(formData['password']) < 5:
            error = 'Invalid Password'
            return error
        else:
            dKeys = formData.keys()
            for item in dKeys:
                entry[item] = formData[item]

            fDATA.append(entry)
            filename = 'fdata_' + formData['firstName'][0].upper() + formData['lastName'].upper() + '.txt'
            writeFinanceData(entry, filename)
        return error, fDATA

    elif action == 'addBankAccount':
        entry = {'type':'bank'}
        dKeys = formData.keys()
        for item in dKeys:
            entry[item] = formData[item]
        fDATA.append(entry)
        writeFinanceData(entry, filename)
        return fDATA

    elif action == 'addTransaction':
        tNUM = 1
        entry = {'type':'trans', 'trnumber':tNUM}
        dKeys = formData.keys()
        for item in dKeys:
            if item == 'account':
                item = formData['account'].split('-')
                entry['bank'] = item[0].strip(' ')
                entry['account'] = item[1].strip(' ')
            else:
                entry[item] = formData[item]
        fDATA.append(entry)
        writeFinanceData(entry, filename)
        return fDATA, tNUM

    elif action == 'search':
        values = formData['parameters'].split(',')
        parameters = []
        for value in values:
            parameters.append(value.replace(' ', ''))
        return parameters

def shipper(fDATA, action, parameters):
    #Formats data from the backend and sends it to the UI
    #fDATA is any LIST of DICTIONARIES
    #action describes which action to take on the data
    #parameters is any LIST of necessary parameters used in the function
    if action == 'search':
        sDATA = []
        for entry in fDATA:
            found = False
            for fKey in entry:
                if found:
                    break
                for item in parameters:
                    if found:
                        break
                    if item in entry[fKey]:
                        sDATA.append(entry)
                        found = True
        return sDATA

    elif action == 'linePlot':
        vMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'September', 'October', 'November', 'December']
        plotYData = []
        today = datetime.date.today()
        if timeFrame == '1year':
            startingDate = today - datetime.timedelta(days=365)
            startMonth = startingDate.month
            xLabels = vMonths[startMonth:]
            for i in range(startMonth):
                xLabels.append(vMonths[i])
        elif timeFrame == '1month':
            startingDate = today - datetime.timedelta(days=30)
            xLabels = [startingDate.day]
            for i in range(30):
                date = startingDate + datetime.timedelta(days=1)
                day = date.day
                xLabels.append(day)
        elif timeFrame == '1week':
            startingDate = today - timedelta(days=7)
            xLabels = [startingDate.day]
            for i in range(7):
                date = startingDate + datetime.timedelta(days=1)
                day = date.day
                xLabels.append(day)
        elif timeFrame == 'today':
            xLabels = []
            startingDate = today
            for i in range(today.hour):
                xLabels.append(i)
        elif timeFrame == 'wholeHistory':
            xLabels = []
        for transaction in fDATA:
            tdate = transaction['transactiondate']
            transDate = datetime.datetime.strptime(tdate, '%m/%d/%Y')
            if transDate > startingDate:
                plotYData.append(transaction)
        return plotYData, xLabels
