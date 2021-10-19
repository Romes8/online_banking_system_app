from django.contrib import admin

# Register your models here.
#imports from databse - all tables 

from .models import Accounts
from .models import AccountCustomers
from .models import AccountType
from .models import Bank
from .models import BankEmployees
from .models import Clients
from .models import CreditCardTypes
from .models import CreditCards
from .models import DebitCardTypes
from .models import DebitCards
from .models import Employees
from .models import LoanTypes
from .models import Loans
from .models import Login
from .models import TransactionTypes
from .models import Transactions


#register tables on admin site
admin.site.register(Accounts)
admin.site.register(AccountCustomers)
admin.site.register(AccountType)
admin.site.register(Bank)
admin.site.register(BankEmployees)
admin.site.register(Clients)
admin.site.register(CreditCardTypes)
admin.site.register(CreditCards)
admin.site.register(DebitCardTypes)
admin.site.register(DebitCards)
admin.site.register(Employees)
admin.site.register(LoanTypes)
admin.site.register(Loans)
admin.site.register(Login)
admin.site.register(TransactionTypes)
admin.site.register(Transactions)

