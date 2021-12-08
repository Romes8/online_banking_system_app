from django.db import connection
from django.db.models import Max
from django.http import request
from django.http.response import HttpResponse
from onlinebanking_app.models import Transactions, CreditCards, DebitCards,Clients
import json
from datetime import date

#test

def cashback():
    cursor = connection.cursor()
    try:
        print("Cashback done")
        #return cursor.callproc("Cashback")
    finally:
        cursor.close()

# Native query
def highest_transaction(param):
    cursor = connection.cursor()
    try:
        mydict = dict()
        result = cursor.execute("SELECT * FROM accounts WHERE id='{}'".format(param))
        if result == 0:
            return "No client with this account id found."
        cursor.execute("CALL highestTransaction({})".format(param))
        for record in cursor.fetchall():
            mydict = {
                "accountNumber": record[0], 
                "amount": float(record[1]), 
                "typeOfTransaction": record[2], 
                "status": record[3], 
                "date": record[4]
                }
        return json.dumps(mydict, indent=2)
    finally:
        cursor.close()

# Object-Relational-Mapper ORM 
    """
    mydict = {}
    query = Transactions.objects.aggregate(Max('amount'))
    highest_transaction = Transaction.objects.get(amount=query['amount__max'])
    mydict = {
        "accountNumber": highest_transaction.account.accountnumber,
        "amount": highest_transaction.amount,
        "typeOfTransaction": highest_transaction.typeoftransaction.type,
        "status": highest_transaction.status,
        "date": highest_transaction.date
    }
    return json.dumps(mydict, indent=2)
    """


def show_cards(param):
    cursor = connection.cursor()
    try:
        id = 0
        mydict = dict()
        result = cursor.execute("SELECT * FROM Clients WHERE SSN='{}'".format(param))
        if result == 0:
            return "No client with this SSN found."
        cursor.execute("CALL show_cards('{}')".format(param))
        for record in cursor.fetchall():
            id += 1
            mydict[id] = {"firstName": record[0], "lastName": record[1], "type": record[2], "number": record[3], "date": record[4], "type2": record[5]}
        return json.dumps(mydict, indent=2, sort_keys=False)
    finally:
        cursor.close()
      

    """
    id = 0
    mydict = {}
    client= Clients.objects.get(ssn=param)
    accounts = AccountCustomers.objects.filter(client=client.id)
    for account in accounts:
        account_id = account.account
        credit_cards = CreditCards.objects.filter(account=account_id)
        for card in credit_cards:
            id += 1
            mydict[id] = {
                "firstName": client.firstName,
                "lastName": client.lastName,
                "type": card.typeofcard.type,
                "number": card.number,
                "date": card.expiry_date,
                "type2": 'Credit Card'
            }
        debit_cards = DebitCards.objects.filter(account=account_id)
        for card in debit_cards:
            id += 1
            mydict[id] = {
                "firstName": client.firstName,
                "lastName": client.lastName,
                "type": card.typeofcard.type,
                "number": card.number,
                "date": card.expiry_date,
                "type2": 'Credit Card'
            }
    return json.dump(mydict, indent=2, sort_keys=False)  
    """


def show_transactions(account_number, start_date, end_date):
    cursor = connection.cursor()
    try:
        mydict = dict()
        result = cursor.execute("SELECT * FROM accounts WHERE accountNumber='{}'".format(account_number))
        if result == 0:
            return "No client with this account number found."
        cursor.execute("CALL ShowTransactions({},'{}','{}')".format(account_number,start_date,end_date))
        for record in cursor.fetchall():
            if account_number in mydict:
                mydict[account_number].append({"typeOfTransaction": record[0], "amount": float(record[1]), "status": record[2], "date": record[3]})
            else:
                mydict[account_number] = [{"typeOfTransaction": record[0], "amount": float(record[1]), "status": record[2], "date": record[3]}]
        return json.dumps(mydict, indent=2)
    finally:
        cursor.close()


def check_loans(accountId):
    cursor = connection.cursor()
    try:
        id = 0
        mydict = dict()
        result = cursor.execute("SELECT * FROM accounts WHERE id='{}'".format(accountId))
        if result == 0:
            return "No client with this account id found."
        cursor.execute("CALL loan_duration_left({})".format(accountId))
        for record in cursor.fetchall():
            print(record)
            id += 1
            mydict[id] = {"typeOfLoan": record[0], "Months left": record[1]}
        return json.dumps(mydict, indent=2)
    finally:
        cursor.close()

from pymongo import MongoClient
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect


# connect to the mongoclient
client = MongoClient("mongodb+srv://Roman:Databases2021@bankingsystem1.kubpg.mongodb.net/test")

# get the database
db = client['onlinebankingsystem']
cl = db["client"]
tr = db["transactions"]

def mongo_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if cl.count({"login.username":username}):
            for record in cl.find({"login.username":username}):
                if check_password(password, record["login"]["password"]):
                    return "Loged in successfully"
        return 'username or password not correct'
    else:
        render(request, "login.html")
 
def mongo_highest_transaction(client_id):
    if cl.count({"_id":client_id}):
        for x in tr.aggregate([
            {"$match": {"client_id": client_id}},
            {"$sort": {"amount": -1}},
            {"$limit": 1},
            {"$lookup":{
                "from":"client",
                "let":{"id": "$client_id"},
                "pipeline":[
                    {"$match":{"$expr": {"$eq": ["$$id", "$_id"]}}},
                    {"$project":{"_id":0,"firstname":1,"lastname":1}}
                ],
                "as": "client"
            }}
        ]):
            return json.dumps(x, indent=2) 
    else:
        return "No client with this ID found."


def mongo_show_cards(client_id):
    if cl.count({"_id":client_id}):
        for x in cl.aggregate([
            {"$match":{"_id": client_id}},
            { "$project": {
                    "firstname" : 1,
                    "lastname": 1,
                    "cards": {"credit_card": 1, "debit_card": 1}
                }}]):
            return json.dumps(x, indent=2) 
    else:
        return "Client does not exist. Please enter a valid client ID."


def mongo_show_loans(client_id):
    if cl.count({"_id":client_id}):
        for x in cl.aggregate([
            {"$match":{"_id": client_id}},
            { "$project": {
                    "firstname" : 1,
                    "lastname": 1,
                    "loans": 1
                }}]):
            return json.dumps(x, indent=2)
    else:
        return "No client with this ID found."

def mongo_show_transactions(request, client_id):
    data = []
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        if cl.count({"_id": client_id}):
            for x in tr.find({"client_id": client_id, "date": {"$gte": start_date, "$lte": end_date}}):
                data.append(x)
            if not data:
                return "No transaction in this period. Please input another start/end date."
            return json.dumps(data, indent=2)
        else:
            return "Client does not exist. Please enter a valid cient ID."

def mongo_send(request):
    if request.method == "POST":
        client_id = int(request.POST.get("client_id"))
        account_number = request.POST.get("account_number")
        amount = float(request.POST.get("amount"))
        cur_date = date.today().strftime("%Y-%m-%d")
        if cl.count({"_id":client_id}):
            if cl.count({"accounts.number": account_number}):
                amount = float(amount)
                with client.start_session() as session:
                    with session.start_transaction():
                        cl.update({ "_id": client_id, "accounts.number": account_number}, 
                            {"$inc": { "accounts.$.balance": -amount}, 
                                "$set": {"accounts.$.lastUpdate": cur_date}})
                        tr.insert({"_id":tr.count(), "account_number": account_number, "amount": amount, 
                            "status": "send", "date": cur_date, "client_id": client_id})
                        
                return "Transaction Successful"
            else:
                return "Account doesnt exist. Please enter a valid account number."
        else :
            return "Client does not exist. Please enter a valid client ID"
            
def mongo_received(request):
    if request.method == "POST":
        client_id = int(request.POST.get("client_id"))
        account_number = request.POST.get("account_number")
        amount = float(request.POST.get("amount"))
        cur_date = date.today().strftime("%Y-%m-%d")
        if cl.count({"_id":client_id}):
            if cl.count({"accounts.number": account_number}):
                amount = float(amount)
                with client.start_session() as session:
                        with session.start_transaction():
                            cl.update({ "_id": client_id, "accounts.number": account_number}, 
                            {"$inc": { "accounts.$.balance": amount}, "$set": {"accounts.$.lastUpdate": cur_date}})
                            tr.insert({"_id":tr.count(), "account_number": account_number, "amount": amount, 
                            "status": "received", "date": cur_date, "client_id": client_id})
                
                return "Transaction Successful"
            else:
                return "Account doesnt exist. Please enter a valid account number."
        else :
            return "Client does not exist. Please enter a valid client ID"


from onlinebanking_app.neo4j_models import Client, Account, Transaction
from neomodel import db

def neo4j_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        client = Client.nodes.get_or_none(username=username)
        if client:
            if check_password(password, client.password):
                return "Loged in successfully"
        return "Username or password invalid"
    return render(request, "login.html")

def neo4j_highest_transaction(client_id):
    client = Client.nodes.get(id=client_id)
    if client:
        data = []
        max = 0
        for account in client.account:
            for transaction in account.transactions:
                if transaction.amount > max:
                    max = transaction.amount
            transaction = account.transactions.get(amount=max)
            account_number = account.number
        data.append({
            "accountnumber": account_number,
            "amount": transaction.amount,
            "status": transaction.status,
            "date": transaction.date.strftime("%y-%m-%d")
        })
        return json.dumps(data, indent=2)
    return HttpResponse("Client doesn't exist")

def neo4j_show_cards(client_id):
    id = 0
    data = dict()
    client = Client.nodes.get_or_none(id=client_id)
    if client:
        for creditcard in client.creditcard:
            id += 1
            data[id] = {
                "firstName": client.firstname,
                "lastName": client.lastname,
                "type": creditcard.type,
                "number": creditcard.number,
                "date": creditcard.expiredate,
                "fee": creditcard.fee,
                "type2": "Credit Card"
            }
        for debitcard in client.debitcard:
            id += 1
            data[id] = {
                "firstName": client.firstname,
                "lastName": client.lastname,
                "type": debitcard.type,
                "number": debitcard.number,
                "date": debitcard.expiredate,
                "type2": "Debit Card"
            }
        return json.dumps(data, indent=2)
    return HttpResponse("Client doesn't exist") 

def neo4j_show_loans(client_id):
    data = []
    client = Client.nodes.get_or_none(id=client_id)
    if client:
        for loan in client.loan:
            data.append({
                "firstName": client.firstname,
                "lastName": client.lastname,
                "type": loan.type,
                "amount": loan.amount,
                "monthlyfee": loan.monthlyfee,
                "datestart": loan.datestart,
                "dateend": loan.dateend
            })
        return json.dumps(data, indent=2)
    return HttpResponse("Client doesn't exist")

from datetime import datetime
def neo4j_show_transactions(request, client_id):
    data = []
    if request.method == "POST":
        start_date = datetime.strptime(request.POST.get("start_date"), '%y-%m-%d')
        end_date = datetime.strptime(request.POST.get("end_date"), '%y-%m-%d')
        client = Client.nodes.get_or_none(id=client_id)
        if client:
            for account in client.account:
                for transaction in account.transactions.filter(date__gte=start_date, date__lte=end_date):
                    data.append({
                        "account_number": account.number,
                        "amount": transaction.amount,
                        "status": transaction.status,
                        "date": transaction.date.strftime("%y-%m-%d")
                    })
            return json.dumps(data, indent=2)
        return HttpResponse("Client doesn't exist")


@db.transaction
def neo4j_send(request):
    if request.method == "POST":
        client_id = int(request.POST.get("client_id"))
        account_number = request.POST.get("account_number")
        amount = float(request.POST.get("amount"))
        cur_date = date.today()
        client = Client.nodes.get_or_none(id=client_id)
        if client:
            account = Account.nodes.get_or_none(number=account_number)
            if account:
                print(account)
                account.balance -= amount
                account.save()
                transaction = Transaction(amount=amount, status='send', date=cur_date).save()
                transaction.accounts.connect(account)
                return HttpResponse("Transaction successfull")
            return HttpResponse("No such account")
        return HttpResponse("Client doesn't exist")


@db.transaction
def neo4j_receive(request):
    if request.method == "POST":
        client_id = int(request.POST.get("client_id"))
        account_number = request.POST.get("account_number")
        amount = float(request.POST.get("amount"))
        cur_date = date.today()
        client = Client.nodes.get_or_none(id=client_id)
        if client:
            account = Account.nodes.get_or_none(number=account_number)
            if account:
                print(account)
                account.balance += amount
                account.save()
                transaction = Transaction(amount=amount, status='receive', date=cur_date).save()
                transaction.accounts.connect(account)
                return HttpResponse("Transaction successfull")
            return HttpResponse("No such account")
        return HttpResponse("Client doesn't exist")