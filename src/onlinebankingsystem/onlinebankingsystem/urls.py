"""onlinebankingsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from onlinebanking_app import views
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('mysql/highestTransaction/<int:account_id>/', views.highest, name='Highest Transaction Made'),
    path('mysql/showCards/<str:ssnclient>/', views.show_cards, name='Show Cards'),
    path('mysql/showTransactions/<str:account_number>/<str:start_date>/<str:end_date>/', views.show_transactions, name='Show Transactions for the specific period'),
    path('mysql/showLoans/<int:account_id>/', views.show_loans, name='Show loans and their state'),
    path('mysql/cashback/', views.cashback, name='Cashback'),

    path('mongo/login/', views.mongo_login, name="Login"),
    path('mongo/transactions/<int:client_id>/',views.mongo_show_transactions, name='Mongo'),
    path('mongo/show_cards/<int:_id>',views.mongo_show_cards, name='Show cards'),
    path('mongo/show_loans/<int:_id>',views.mongo_show_loans, name='Show loans'),
    path('mongo/highest/<int:client_id>', views.mongo_highest),
    path('mongo/send/', views.mongo_send),
    path('mongo/received/', views.mongo_received),

    path('neo4j/login/', views.neo4j_login),
    path('neo4j/highestTransaction/<int:client_id>/', views.neo4j_highest),
    path('neo4j/show_cards/<int:client_id>/', views.neo4j_show_cards),
    path('neo4j/show_loans/<int:client_id>/', views.neo4j_show_loans),
    path('neo4j/show_transactions/<int:client_id>/', views.neo4j_show_transactions),
    path('neo4j/send/', views.neo4j_send),
    path('neo4j/receive/', views.neo4j_receive),

]
