from django.db import connection
import json
#test

def cashback():
    cursor = connection.cursor()
    try:
        print("Cashback done")
        #return cursor.callproc("Cashback")
    finally:
        cursor.close()


def highest_transaction(param):
    cursor = connection.cursor()
    try:
        mydict = dict()
        cursor.execute("CALL highestTransaction({})".format(param))
        for record in cursor.fetchall():
            mydict = {"accountNumber": record[0], "amount": float(record[1]), "typeOfTransaction": record[2], "status": record[3], "date": record[4]}
        return json.dumps(mydict, indent=2)
    finally:
        cursor.close()


def show_cards(param):
    cursor = connection.cursor()
    try:
        id = 0
        mydict = dict()
        cursor.execute("CALL show_cards('{}')".format(param))
        for record in cursor.fetchall():
            id += 1
            mydict[id] = {"firstName": record[0], "lastName": record[1], "type": record[2], "number": record[3], "date": record[4], "type2": record[5]}

        return json.dumps(mydict, indent=2, sort_keys=False)
    finally:
        cursor.close()


def show_transactions(account_number, start_date, end_date):
    cursor = connection.cursor()
    try:
        mydict = dict()
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
        cursor.execute("CALL loan_duration_left({})".format(accountId))
        for record in cursor.fetchall():
            print(record)
            id += 1
            mydict[id] = {"typeOfLoan": record[0], "Months left": record[1]}
        return json.dumps(mydict, indent=2)
    finally:
        cursor.close()




from pymongo import MongoClient
# connect to the mongoclient
client = MongoClient('mongodb+srv://Roman:Databases2021@bankingsystem1.kubpg.mongodb.net/test')

# get the database
db = client['onlinebankingsystem']
cl = db["client"]
tr = db["transactions"]

def mongo_highest_transaction(client_id):
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


def mongo_show_cards(client_id):
    for x in cl.aggregate([
        {"$match":{"_id": client_id}},
        { "$project": {
                "firstname" : 1,
                "lastname": 1,
                "cards": {"credit_card": 1, "debit_card": 1}
            }}]):
        print(x)
    return json.dumps(x, indent=2) 

def mongo_show_loans(client_id):
    for x in cl.aggregate([
        {"$match":{"_id": client_id}},
        { "$project": {
                "firstname" : 1,
                "lastname": 1,
                "loans": 1
            }}]):
        print(x)
    return json.dumps(x, indent=2)

def mongo_show_transactions(client_id, start_date, end_date):
    data = []
    for x in tr.find({"client_id": client_id, "date": {"$gte": start_date, "$lte": end_date}}):
        data.append(x)
    if not data:
        return 1
    return json.dumps(data, indent=2)


def mongo_send(client_id,account_number, _amount):
    amount = float(_amount)
   # print(cl.aggregate([{"$project": {"accounts": {"balance" : 1}}}]))
    cl.update({ "_id": client_id, "accounts.number": account_number}, {"$inc": { "accounts.$.balance": amount}, "$currentDate": {"accounts.$.lastUpdate": {"$type": "date"}}})
    
    return 1


def mongo_received(client_id,_amount):
    amount = float(_amount)
    
    return 1




def pymongo_find():
    data = []
    cl = db["transactions"]
    for x in cl.find():
        print(x)
        data.append(x)       
    return json.dumps(data, indent=2)

def join_cata():
    data = []
    cl = db["transactions"]
    for x in cl.aggregate([
        {
           "$lookup":
                {
                    "from": "client",
                    "let":{"id": "$client_id"},
                    "pipeline":[
                        {"$match":{"$expr": {"$eq": ["$$id", "$_id"]}}},
                        {"$project":{"_id":0,"firstname":1,"lastname":1}}
                    ],
                    "as": "cor_client"
                }
            }
    ]):
        print(x)
        data.append(x)
    return json.dumps(data, indent=2)

        
def join_roman():
    data = []
    cl = db["transactions"]
    cl.aggregate([
        {
           "$lookup":
                {
                    "from": "client",
                    "localField": "client_id",
                    "foreignField":"_id",
                    "as": "client"
                }
            },
            {
                "$project":
                {
                    "amount": 1,
                    "cor_client": {"firstname" : 1, "lastname": 1}
                }
            }
    ])
    for x in cl.find():
        print(x)
        data.append(x)
    return json.dumps(data, indent=2)