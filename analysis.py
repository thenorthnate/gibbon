'''
@title: analysis.py
@author: Nathan North
@org: Northern Finance
@description: Analytics driver for finance program
'''

def loaddata():
    fdata = []
    with open('fdata.txt', 'r') as datafile:
        for line in datafile:
            fdata.append(line)
    return fdata
