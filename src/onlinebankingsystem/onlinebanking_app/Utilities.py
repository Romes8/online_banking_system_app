from django.db import connection
import json


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
        cursor.callproc("highestTransaction", [param, ])
        result = cursor.stored_results()
        for row in result:
            for record in row.fetchall():
                mydict = {"accountNumber": record[0], "amount": float(record[1]), "typeOfTransaction": record[2], "status": record[3], "date": record[4]}
        return json.dumps(mydict, indent=2)
    finally:
        cursor.close()


def show_cards(param):
    cursor = connection.cursor()
    try:
        id = 0
        mydict = dict()
        cursor.callproc("Show_Cards", [param, ])
        for result in cursor.stored_results():
            for record in result.fetchall():
                id += 1
                mydict[id] = {"firstName": record[0], "lastName": record[1], "type": record[2], "number": record[3], "date": record[4], "type2": record[5]}

        return json.dumps(mydict, indent=2, sort_keys=False)
    finally:
        cursor.close()


def show_transactions(account_number, start_date, end_date):
    cursor = connection.cursor()
    try:
        mydict = dict()
        cursor.callproc("ShowTransactions", [account_number, start_date, end_date, ])
        for result in cursor.stored_results():
            for record in result.fetchall():
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
        cursor.callproc("loan_duration_left", [accountId])
        for result in cursor.stored_results():
            for record in result.fetchall():
                id += 1
                mydict[id] = {"typeOfLoan": record[0], "Months left": record[1]}
        return json.dumps(mydict, indent=2)
    finally:
        cursor.close()