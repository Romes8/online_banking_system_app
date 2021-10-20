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


def highest(request, account_id):
    action = Utilities.highest_transaction(account_id)
    print("test")
    return HttpResponse(action, content_type = "application/json")


def show_transactions(request, account_number, start_date, end_date):
    action = Utilities.show_transactions(account_number, start_date, end_date)
    return HttpResponse(action, content_type = "application/json")


def show_loans(request, account_id):
    action = Utilities.check_loans(account_id)
    return HttpResponse(action, content_type = "application/json")

def cashback(request):
    action = Utilities.cashback()
    return HttpResponse(action, content_type = "application/json")