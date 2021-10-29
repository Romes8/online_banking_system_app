from django.shortcuts import render
from django.http import HttpResponse
from onlinebanking_app import Utilities

# Create your views here.
def index(request):
    action = Utilities.cashback()
    return HttpResponse("Cashback done")


def show_cards(request, ssnclient):
    action = Utilities.show_cards(ssnclient)
    print(action)
    print("test")
    return HttpResponse(action, content_type = 'application/json')

def mongo_show_cards(request, _id):
    action = Utilities.mongo_show_cards(_id)
    return HttpResponse(action, content_type = 'application/json')


def highest(request, account_id):
    action = Utilities.highest_transaction(account_id)
    print("test")
    return HttpResponse(action, content_type = "application/json")

def mongo_highest(request, client_id):
    action = Utilities.mongo_highest_transaction(client_id)
    return HttpResponse(action, content_type = "application/json")


def show_transactions(request, account_number, start_date, end_date):
    action = Utilities.show_transactions(account_number, start_date, end_date)
    return HttpResponse(action, content_type = "application/json")

def mongo_show_transactions(request, client_id, start_date, end_date):
    action = Utilities.mongo_show_transactions(client_id, start_date, end_date)
    if action == 1:
        return HttpResponse("No transactions made in this period or this client does't exist")
    return HttpResponse(action, content_type = "application/json")

def show_loans(request, account_id):
    action = Utilities.check_loans(account_id)
    return HttpResponse(action, content_type = "application/json")

def mongo_show_loans(request, _id):
    action = Utilities.mongo_show_loans(_id)
    return HttpResponse(action, content_type = 'application/json')

def cashback(request):
    action = Utilities.cashback()
    return HttpResponse(action, content_type = "application/json")

def mongo_send(request, client_id, account_number, amount):
    action = Utilities.mongo_send(client_id, account_number, amount)
    return HttpResponse(action, content_type = "application/json")

def mongo_received(request,client_id, account_number, amount):
    action = Utilities.mongo_received(client_id, account_number, amount)
    return HttpResponse(action, content_type = "application/json")


def mongodb(request):
    Utilities.pymongo_find()
    action = Utilities.join_cata()
    return HttpResponse(action, content_type = "application/json")

    