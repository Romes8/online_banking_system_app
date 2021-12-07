from neomodel import StructuredNode,IntegerProperty, StructuredRel, RelationshipFrom, DateProperty, StringProperty, StringProperty, FloatProperty, UniqueIdProperty, RelationshipTo

class AccountRel(StructuredRel):
    date = DateProperty()

class Transaction(StructuredNode):
    status = StringProperty()
    amount = FloatProperty()
    date = DateProperty()
    accounts = RelationshipTo('Account', 'MADE_BY')

class Account(StructuredNode):
    id = UniqueIdProperty()
    number = StringProperty()
    balance = FloatProperty()
    type = StringProperty()
    dateopened = StringProperty()
    lastupdated = StringProperty()

    #relationships
    transactions = RelationshipFrom(Transaction, 'MADE_BY', model=AccountRel)

class Bank(StructuredNode):
    id = UniqueIdProperty()
    name = StringProperty()
    address = StringProperty()
    phonenumber = StringProperty()

class Loan(StructuredNode):
    id = UniqueIdProperty()
    type = StringProperty()
    amount = FloatProperty()
    monthlyfee = FloatProperty()
    datestart = StringProperty()
    dateend = StringProperty()

class CreditCard(StructuredNode):
    id = UniqueIdProperty()
    type = StringProperty()
    number = StringProperty()
    cvc = StringProperty()
    fee = FloatProperty()
    expiredate = StringProperty()

class DebitCard(StructuredNode):
    id = UniqueIdProperty()
    type = StringProperty()
    number = StringProperty()
    cvc = StringProperty()
    expiredate = StringProperty()

class Client(StructuredNode):
    id = IntegerProperty()
    firstname = StringProperty()
    lastname = StringProperty()
    ssn = StringProperty()
    phonenumber = StringProperty()
    dateofbirth = StringProperty()
    email = StringProperty()
    address = StringProperty()
    city = StringProperty()
    username = StringProperty()
    password = StringProperty()

    #relationships
    account = RelationshipTo(Account, 'HAS')
    debitcard = RelationshipTo(DebitCard, 'HAS')
    creditcard = RelationshipTo(CreditCard, 'HAS')
    loan = RelationshipTo(Loan, 'HAS')
    bank = RelationshipTo(Bank, 'REGISTERED_TO')



