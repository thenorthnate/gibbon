'''
@title: thegibbon.py
@author: Nathan North
@org: North
@version: 1.0

@description: Use this script to keep track of financial information!
@loc: App runs at - http://127.0.0.1:5000/
'''

#IMPORTS
from flask import Flask, render_template, redirect, url_for, request, session
from cipher import ENCODE, DECODE
from helper import OPS
import os, datetime, time, json

#CONSTANTS
SECRET_KEY = 'development key'

#INIT
F = OPS()

#FUNCTONS
app = Flask(__name__)
app.config.from_object(__name__)
port = os.getenv("PORT")

if port is None:
    port = 5000

@app.route('/help')
def help():
    if F.password == '':
        return redirect(url_for('logout'))
    return render_template('help.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if F.password == '':
        return redirect(url_for('logout'))
    F.formData = {}
    if request.method == 'POST':
        F.formData = request.form
        F.updateProfile()
        if F.error == None:
            return redirect(url_for('home'))
    return render_template('profile.html',
                            error=F.error)


@app.route('/')
def index():
    return render_template('cover_index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if F.password == '':
        return redirect(url_for('logout'))
    confirm = False
    F.error = None
    nickName = ''
    F.formData = {}
    try:
        if F.bDATA == [] or F.uDATA == []:
            F.readFinanceData('all', F.userDataFile)
            F.transDataFile = F.uDATA[0]['tfilename']
        nickName = ' ' + F.uDATA[0]['nickName']
        if F.tDATA == []:
            F.readFinanceData('trans', F.transDataFile)
    except:
        pass
    if request.method == 'POST':
        F.formData = request.form
        F.addTransaction()
        if F.error:
            pass
        else:
            F.updateAccountBalance()
            confirm = True
    return render_template('home.html',
                            bDATA=F.bDATA,
                            nickName=nickName,
                            confirm=confirm,
                            error=F.error)


@app.route('/history', methods=['GET', 'POST'])
def history():
    if F.password == '':
        return redirect(url_for('logout'))
    F.formData = {}
    try:
        desiredAccount = F.bDATA[0]['name'] + ' - ' + F.bDATA[0]['accountType'] + ', #' + F.bDATA[0]['accountNumber']
        F.linePlot()
        if request.method == 'POST':
            desiredAccount = request.form['account'].split('-')
            desiredAccount = desiredAccount[0].strip(' ') + ' - ' + desiredAccount[1].strip(' ') + ', #' + desiredAccount[2].strip(' (# ) ')
            F.formData = request.form
            F.linePlot()
    except:
        F.xLabels = ['A', 'B', 'C']
        F.plotYData = [1,2,3]
        desiredAccount = 'Not Found'
        F.startDate = 'N/A'
        F.endDate = 'N/A'
    return render_template('history.html',
                            xLabels=F.xLabels,
                            Ydata=F.plotYData,
                            bDATA=F.bDATA,
                            desiredAccount=desiredAccount,
                            startDate=F.startDate,
                            endDate=F.endDate)


@app.route('/createprofile', methods=['GET', 'POST'])
def createprofile():
    F.error = None
    F.formData = {}
    if request.method == 'POST':
        F.formData = request.form
        F.createUserProfile()
        if F.error == None:
            return redirect(url_for('login'))
    return render_template('createprofile.html', error = F.error)

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if F.password == '':
        return redirect(url_for('logout'))
    F.formData = {}
    dispTDATA = []
    for item in reversed(F.tDATA):
        dispTDATA.append(item)
    if request.method == 'POST':
        if request.form['submit'] == 'searchButton':
            F.formData = request.form
            F.searchTransactions()
            dispTDATA = []
            for item in reversed(F.sDATA):
                dispTDATA.append(item)
        elif request.form['submit'] == 'deleteButton':
            F.formData = request.form
            F.deleteTransaction()
            dispTDATA = []
            for item in reversed(F.tDATA):
                dispTDATA.append(item)
            dispTDATA = dispTDATA[0:20]
    else:
        dispTDATA = dispTDATA[0:20]
    return render_template('transactions.html', transactionData = dispTDATA)

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if F.password == '':
        return redirect(url_for('logout'))
    F.pie()
    return render_template('analysis.html',
                            xLabels=F.xLabels,
                            plotYData=F.plotYData,
                            totalspend=round(F.totalspend),
                            totalgain=round(F.totalgain, 2))


@app.route('/addaccount', methods=['GET', 'POST'])
def addaccount():
    if F.password == '':
        return redirect(url_for('logout'))
    F.formData = {}
    F.error = None
    if request.method == 'POST':
        F.formData = request.form
        F.addBankAccount()
        if F.error == None:
            return redirect(url_for('home'))
    return render_template('addaccount.html',
                            error=F.error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    F.formData = {}
    F.error = None
    if request.method == 'POST':
        F.formData = request.form
        F.signin()

        if F.error == None:
            session['logged_in'] = True
            return redirect(url_for('home'))

    return render_template('login.html', error = F.error)

@app.route('/logout')
def logout():
    F.uDATA = []
    F.bDATA = []
    F.tDATA = []
    session['logged_in'] = False
    return redirect(url_for('index'))


#START APP
if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
