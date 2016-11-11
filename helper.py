'''
@title: helper.py
@author: Nathan North
@org: Northern Finance
@description: Analytics driver for finance program
'''
from cipher import ENCODE, DECODE
import datetime, json, os, time

class OPS:
    def __init__(self):
        #Directory
        self.workingDir = ''

        #Profile
        self.username = ''
        self.password = ''

        #File Names
        self.filename = ''
        self.userDataFile = ''
        self.transDataFile = ''
        self.fDataFiles = []

        #Stored Data
        self.fDATA = []
        self.uDATA = []
        self.tDATA = []
        self.bDATA = []
        self.sDATA = []

        #Forms
        self.formData = {}

        #Search
        self.searchParams = []

        #Plots
        self.daysInView = 20
        self.daysAgo = 20
        self.plotAccount = ''
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.xLabels = []
        self.plotYData = []
        self.startDate = ''
        self.endDate = ''

        #Analytics Values
        self.totalspend = 0
        self.totalgain = 0
        self.netvalue = 0
        self.numoftrans = 0
        self.totalsavings = 0
        self.totalchecking = 0


        #Error handling
        self.error = None

    '''
    findDataFiles: Finds all files that could contain a user's financial data.

    SET: None
    INPUT: None
    '''
    def evalFiles(self):
        self.workingDir = os.getcwd()
        allFiles = os.listdir(self.workingDir)
        tempFiles = []
        for item in allFiles:
            if item.endswith('.txt') and item.startswith('0x55'):
                try:
                    with open(item, 'r') as datafile:
                        for line in datafile:
                            plainText = DECODE(line.strip('\n'), self.password)
                            #DECODE LINE HERE
                            row = json.loads(plainText)
                            if row['type']:
                                tempFiles.append(item)
                                break
                except:
                    pass

        self.fDataFiles = tempFiles
        try:
            self.userDataFile = tempFiles[-1]
        except:
            pass



    '''
    readFinanceData: Reads in the three different types of data from two possible
    data files.

    SET: filename
    INPUT: datatype
    '''
    def readFinanceData(self, datatype, filename):
        with open(filename, 'r') as datafile:
            if datatype == 'user':
                self.uDATA = []
                for line in datafile:
                    row = line.strip('\n')
                    #DECODE LINE HERE
                    plainText = DECODE(row, self.password)
                    entry = json.loads(plainText)
                    if entry['type'] == 'user':
                        self.uDATA.append(entry)
            elif datatype == 'bank':
                self.bDATA = []
                for line in datafile:
                    row = line.strip('\n')
                    #DECODE LINE HERE
                    plainText = DECODE(row, self.password)
                    entry = json.loads(plainText)
                    if entry['type'] == 'bank':
                        self.bDATA.append(entry)
            elif datatype == 'trans':
                self.tDATA = []
                for line in datafile:
                    row = line.strip('\n')
                    #DECODE LINE HERE
                    plainText = DECODE(row, self.password)
                    entry = json.loads(plainText)
                    self.tDATA.append(entry)
            elif datatype == 'all':
                self.uDATA = []
                self.bDATA = []
                for line in datafile:
                    row = line.strip('\n')
                    #DECODE LINE HERE
                    plainText = DECODE(row, self.password)
                    entry = json.loads(plainText)
                    if entry['type'] == 'user':
                        self.uDATA.append(entry)
                    elif entry['type'] == 'bank':
                        self.bDATA.append(entry)


    '''
    writeFinanceData: writes the parameter fDATA to a file. Two write styles
    exist. One to simply add data to the file, the other to overwrite the
    entire file with new data.

    SET: fDATA
    INPUT: style
    '''
    def writeFinanceData(self, style, filename):
        #fDATA is a single dictionary with some data
        if style == 'add':
            with open(filename, 'a') as datafile:
                row = json.dumps(self.fDATA)
                #ENCODE LINE HERE
                cipherText = ENCODE(row, self.password)
                datafile.write(cipherText + '\n')
        elif style == 'update':
            with open(filename, 'w') as datafile:
                for category in self.fDATA:
                    for entry in category:
                        row = json.dumps(entry)
                        #ENCODE LINE HERE
                        cipherText = ENCODE(row, self.password)
                        datafile.write(cipherText + '\n')


    '''
    createUserProfile: Is used once when the user logs in for the very first
    time. Builds the user file and creates credentials for the user later on.

    SET: formData
    INPUT: None
    '''
    def createUserProfile(self):
        self.error = None
        self.password = self.formData['password']
        uniqueID = int(time.time())
        letterNr = ord('U')
        letterNt = ord('T')
        filename = format(letterNr, '#04x')
        tfilename = format(letterNt, '#04x')
        self.userDataFile = filename + str(uniqueID) + '.txt'
        self.transDataFile = tfilename + str(uniqueID) + '.txt'
        entry = {'type':'user', 'tfilename':self.transDataFile}
        try:
            bDATE = self.formData['birthday']
            bDATE = datetime.datetime.strptime(bDATE, '%m/%d/%Y')
            if bDATE > datetime.datetime.today():
                self.error = "You can't be born in the future."
                return 0
        except:
            self.error = 'Invalid Birthday'
            return 0
        if len(self.formData['password']) < 5:
            self.error = 'Invalid Password'
            return 0
        else:
            dKeys = self.formData.keys()
            for item in dKeys:
                entry[item] = self.formData[item]
            self.uDATA = entry
            self.fDATA = entry
            self.writeFinanceData('add', self.userDataFile)


    '''
    updateProfile: User can re-enter his or her information incase they prefer a
    new password or a different nickname etc.

    SET: formData
    INPUT: None
    '''
    def updateProfile(self):
        self.error = None
        entry = {'type':'user', 'tfilename':self.transDataFile}
        try:
            bDATE = self.formData['birthday']
            bDATE = datetime.datetime.strptime(bDATE, '%m/%d/%Y')
            if bDATE > datetime.datetime.today():
                self.error = "You can't be born in the future."
                return 0
        except:
            self.error = 'Invalid Birthday'
            return 0
        if len(self.formData['password']) < 5:
            self.error = 'Invalid Password'
            return 0
        else:
            dKeys = self.formData.keys()
            for item in dKeys:
                if self.formData[item] == '':
                    self.error = 'Must complete all fields.'
                    return 0
                entry[item] = self.formData[item]
            self.uDATA = [entry]
            self.fDATA = [[entry], self.bDATA]
            self.writeFinanceData('update', self.userDataFile)


    '''
    signin: compares the data in the finance file to the user credentials to
    determine access.

    SET: formData
    INPUT: None
    '''
    def signin(self):
        self.error = None
        self.password = self.formData['inputPassword']
        self.evalFiles()
        if len(self.fDataFiles) < 1:
            self.error = 'Invalid credentials, or you must create an account first.'
        userfiles = []
        count = 0
        for item in self.fDataFiles:
            self.readFinanceData('user', item)
            if self.formData['inputEmail'] != self.uDATA[0]['email']:
                self.error = 'Invalid Username'
            elif self.formData['inputPassword'] != self.uDATA[0]['password']:
                self.error = 'Invalid Password'
            else:
                count += 1
                userfiles.append(item)
                self.userDataFile = item
                self.transDataFile = self.uDATA[0]['tfilename']
                self.error = None
        filenums = []
        if count > 1:
            for item in userfiles:
                itemnumber = item.replace('.txt', '')
                itemnumber = itemnumber.replace('0x55', '')
                filenums.append(int(itemnumber))
            filenum = max(filenums)
            item = '0x55' + str(filenum) + '.txt'
            #self.filename = item
            self.readFinanceData('user', item)
            self.userDataFile = item
            self.transDataFile = self.uDATA[0]['tfilename']


    '''
    addBankAccount: Adds the bank account to the data file. This is executed
    when the user sumbits the request on the add account page.

    SET: formData
    INPUT: None
    '''
    def addBankAccount(self):
        self.error = None
        entry = {'type':'bank'}
        dKeys = self.formData.keys()
        for item in dKeys:
            if item == 'accountNumber':
                for element in self.bDATA:
                    if element['accountNumber'] == self.formData['accountNumber']:
                        self.error = 'Account number is not unique.'
                        return 0
            elif item == 'inceptiondate':
                try:
                    bDATE = datetime.datetime.strptime(self.formData['inceptiondate'], '%m/%d/%Y')
                    if bDATE > datetime.datetime.today():
                        self.error = "Account can't be created in the future."
                        return 0
                except:
                    self.error = 'Invalid Date'
                    return 0
            elif item == 'balance':
                try:
                    testvalue = float(self.formData['balance'])
                except:
                    self.error = 'Invalid account balance.'
                    return 0
            entry[item] = self.formData[item]
        self.bDATA.append(entry)
        self.fDATA = entry
        self.writeFinanceData('add', self.userDataFile)
        entryTime = str(datetime.datetime.now())
        entry = {'type':'trans', 'trNumber':str(int(time.time()*1000)), 'entryTime':entryTime, 'transType':'deposit', 'tags':'CREATION'}
        entry['description'] = 'This is the transaction associated with the creation of this account. DO NOT DELETE.'
        entry['bank'] = self.formData['name']
        entry['account'] = self.formData['accountType']
        entry['amount'] = self.formData['balance']
        bDATE = datetime.datetime.strptime(self.formData['inceptiondate'], '%m/%d/%Y')
        entry['transactionDate'] = self.formData['inceptiondate']
        entry['accountNumber'] = self.formData['accountNumber']
        self.tDATA.append(entry)
        self.fDATA = entry
        self.writeFinanceData('add', self.transDataFile)


    '''
    addTransaction: Adds the transaction to the transaction data file and updates
    the object values for the necessary financial data.

    SET: formData
    INPUT: None
    '''
    def addTransaction(self):
        self.error = None
        entryTime = str(datetime.datetime.now())
        entry = {'type':'trans', 'trNumber':str(int(time.time()*1000)), 'entryTime':entryTime}
        try:
            item = self.formData['account'].split('-')
            entry['bank'] = item[0].strip(' ')
            entry['account'] = item[1].strip(' ')
            entry['accountNumber'] = item[2].strip('(# )')
        except:
            self.error = 'Please add an account'
            return 0
        entry['tags'] = self.formData['tags'].upper()
        entry['transType'] = self.formData['transType']
        if self.formData['transType'] == 'transfer':
            entry['amount'] = round(0.0-float(self.formData['amount']), 2)
            if self.formData['toAccount'] != 'N/A':
                item = self.formData['toAccount'].split('-')
                entry['toBank'] = item[0].strip(' ')
                entry['toAccount'] = item[1].strip(' ')
                entry['toAccountNumber'] = item[2].strip('(# )')
            else:
                self.error = 'Select bank to transfer to'
                return 0
        else:
            entry['amount'] = round(float(self.formData['amount']), 2)

        try:
            bDATE = datetime.datetime.strptime(self.formData['transactionDate'], '%m/%d/%Y')
            entry['transactionDate'] = self.formData['transactionDate']
        except:
            self.error = 'Invalid Date'
            return 0

        entry['description'] = self.formData['description']
        self.tDATA.append(entry)
        self.fDATA = entry
        self.writeFinanceData('add', self.transDataFile)
        if entry['transType'] == 'transfer':
            entry1 = entry.copy()
            entry1['amount'] = abs(float(entry['amount']))
            entry1['fromBank'] = entry['bank']
            entry1['fromAccount'] = entry['account']
            entry1['fromAccountNumber'] = entry['accountNumber']
            entry1['bank'] = entry['toBank']
            entry1['account'] = entry['toAccount']
            entry1['accountNumber'] = entry['toAccountNumber']
            entry1.pop('toBank')
            entry1.pop('toAccount')
            entry1.pop('toAccountNumber')
            self.tDATA.append(entry1)
            self.fDATA = entry1
            self.writeFinanceData('add', self.transDataFile)



    '''
    updateAccountBalance: Updates the user data file to hold the current value
    of the bank account. Is executed after a transaction is added.

    SET: formData
    INPUT: None
    '''
    def updateAccountBalance(self):
        self.error = None
        for entry in self.bDATA:
            accountInfo = self.formData['account'].split('-')
            if accountInfo[2].strip('(# )') == entry['accountNumber']:
                if self.formData['transType'] == 'deposit':
                    entry['balance'] = round(float(entry['balance']) + float(self.formData['amount']), 2)
                elif self.formData['transType'] == 'transfer':
                    entry['balance'] = round(float(entry['balance']) - float(self.formData['amount']), 2)
                    for searchEntry in self.bDATA:
                        toAccountInfo = self.formData['toAccount'].split('-')
                        if toAccountInfo[2].strip('(# )') == searchEntry['accountNumber']:
                            searchEntry['balance'] = round(float(searchEntry['balance']) + float(self.formData['amount']), 2)
                elif self.formData['transType'] == 'withdrawl':
                    entry['balance'] = round(float(entry['balance']) - float(self.formData['amount']), 2)
        self.fDATA = [self.uDATA, self.bDATA]
        self.writeFinanceData('update', self.userDataFile)


    '''
    searchTransactions: Used on the transactions page to search through
    previous transactions.

    SET: formData
    INPUT: None
    '''
    def searchTransactions(self):
        values = self.formData['parameters'].split(',')
        self.searchParams = []
        for value in values:
            self.searchParams.append(value.replace(' ', ''))
        self.sDATA = []
        find = []
        for entry in self.tDATA:
            found = False
            for item in self.searchParams:
                item = item.replace(' ', '')
                if found:
                    break
                if item.startswith('=?'):
                    item = item.replace('=?', '')
                    if item[0] == '$':
                        entryValue = entry['amount']
                        entryValue = float(entryValue)
                        searchValue = float(item[1:])
                        if entryValue < (searchValue + 5) and entryValue > (searchValue - 5):
                            self.sDATA.append(entry)
                            found = True
                    elif item[0] in 'Dd':
                        entryValue = entry['transactionDate'].replace(' ', '')
                        try:
                            #MAke dates happen here.
                            entryValue = datetime.datetime.strptime(entryValue, '%m/%d/%Y')
                            searchValue = datetime.datetime.strptime(item[1:], '%m/%d/%Y')
                            if entryValue == searchValue:
                                self.sDATA.append(entry)
                                found = True
                        except:
                            pass
                else:
                    for fKey in entry:
                        if found:
                            break

                        entryValue = entry[fKey]
                        try:
                            entryValue = entryValue.replace(' ', '').upper()
                        except:
                            entryValue = str(entryValue)
                            entryValue = entryValue.replace(' ', '').upper()

                        if item.upper() in entryValue:
                            self.sDATA.append(entry)
                            found = True

    '''
    deleteTransaction: removes the desired transaction from the data file
    and from RAM

    SET: formData
    INPUT: None
    '''
    def deleteTransaction(self):
        self.error = None
        mark = []
        i = 0
        for item in self.tDATA:
            if item['trNumber'] == self.formData['trNumber']:
                for entry in self.bDATA:
                    if item['accountNumber'] == entry['accountNumber']:
                        if item['transType'] == 'deposit':
                            entry['balance'] = round(float(entry['balance']) - float(item['amount']), 2)
                        elif item['transType'] == 'transfer':
                            entry['balance'] = round(float(entry['balance']) - float(item['amount']), 2)
                        elif item['transType'] == 'withdrawl':
                            entry['balance'] = round(float(entry['balance']) + float(item['amount']), 2)
                self.fDATA = [self.uDATA, self.bDATA]
                self.writeFinanceData('update', self.userDataFile)
                mark.append(i)
            i += 1
        for dex in reversed(mark):
            del self.tDATA[dex]

        self.fDATA = [self.tDATA]
        self.writeFinanceData('update', self.transDataFile)


    '''
    linePlot: Takes the information from the client, formats it, and returns the
    desired data to plot.

    SET: formData
    INPUT: None
    '''
    def linePlot(self):
        self.daysAgo = 20
        self.daysInView = 20
        try:
            accountNumber = self.formData['account'].split('-')
            self.plotAccount = accountNumber[2].strip(' (# ) ')
        except:
            self.plotAccount = self.bDATA[0]['accountNumber']
        try:
            timeEntry = self.formData['time'].split(',')
            if len(timeEntry) > 1:
                self.daysAgo = abs(int(timeEntry[0]))
                self.daysInView = abs(int(timeEntry[1]))
            else:
                self.daysAgo = abs(int(self.formData['time']))
                self.daysInView = 20
        except:
            pass
        for entry in self.bDATA:
            if entry['type'] == 'bank':
                if self.plotAccount.replace(' ', '') == entry['accountNumber'].replace(' ', ''):
                    accountVal = float(entry['balance'])
                    break
        if self.daysAgo <= self.daysInView:
            upperBound = datetime.datetime.today()
        elif self.daysAgo > self.daysInView:
            upperBound = datetime.datetime.today() - datetime.timedelta(days=self.daysAgo) + datetime.timedelta(days=self.daysInView)
            self.daysAgo = self.daysInView
        self.xLabels = []
        days = []
        for i in range(self.daysAgo):
            day = upperBound - datetime.timedelta(days=i)
            days.append(day)
            self.xLabels.insert(0, day.day)
        self.startDate = self.months[days[-1].month-1] + ' ' + str(days[-1].day) + ', ' + str(days[-1].year)
        self.endDate = self.months[days[0].month-1] + ' ' + str(days[0].day) + ', ' + str(days[0].year)
        for transaction in self.tDATA:
            if self.plotAccount.replace(' ', '') == transaction['accountNumber'].replace(' ', ''):
                tdate = datetime.datetime.strptime(transaction['transactionDate'], '%m/%d/%Y')
                if tdate > days[0]:
                    if transaction['transType'] == 'deposit':
                        accountVal = accountVal - float(transaction['amount'])
                    elif transaction['transType'] == 'withdrawl':
                        accountVal = accountVal + float(transaction['amount'])
                    elif transaction['transType'] == 'transfer':
                        accountVal = accountVal - float(transaction['amount'])
        self.plotYData = [accountVal]
        for day in days:
            dayVal = 0
            for transaction in reversed(self.tDATA):
                if self.plotAccount.replace(' ', '') == transaction['accountNumber'].replace(' ', ''):
                    tdate = datetime.datetime.strptime(transaction['transactionDate'], '%m/%d/%Y')
                    if tdate.day == day.day and tdate.month == day.month and tdate.year == day.year:
                        if transaction['transType'] == 'deposit':
                            dayVal = dayVal - float(transaction['amount'])
                        elif transaction['transType'] == 'withdrawl':
                            dayVal = dayVal + float(transaction['amount'])
                        elif transaction['transType'] == 'transfer':
                            dayVal = dayVal - float(transaction['amount'])
            accountVal = accountVal + dayVal
            self.plotYData.insert(0, accountVal)
        self.plotYData.pop(0)



    '''
    pie: goes through the data and makes it presentable for the pie chart

    SET: None
    INPUT: None
    '''
    def pie(self):
        TAG = {}
        data = []
        taglist = []
        self.totalspend = 0
        self.totalgain = 0
        for entry in self.tDATA:
            if entry['transType'] == 'withdrawl':
                try:
                    TAG[entry['tags']] += float(entry['amount'])
                except:
                    TAG[entry['tags']] = float(entry['amount'])
                taglist.append(entry['tags'])
                self.totalspend += float(entry['amount'])
            elif entry['transType'] == 'deposit':
                self.totalgain += float(entry['amount'])
        self.xLabels = list(set(taglist))
        for l in self.xLabels:
            perc = round((int(TAG[l])/self.totalspend)*100, 2)
            data.append(perc)
        self.xLabels = json.dumps(self.xLabels)
        self.plotYData = data
        self.netvalue = self.totalgain - self.totalspend

    def genAnalytics(self):
        i = 0
        self.numoftrans = 0
        self.totalsavings = 0
        self.totalchecking = 0
        for entry in self.tDATA:
            if entry['tags'] == 'CREATION':
                pass
            else:
                self.numoftrans += 1
            if entry['account'].upper() == 'SAVINGS':
                self.totalsavings += float(entry['amount'])
            elif entry['account'].upper() == 'CHECKING':
                self.totalchecking += float(entry['amount'])
            i += 1
