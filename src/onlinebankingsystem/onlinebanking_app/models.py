# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountCustomers(models.Model):
    account = models.ForeignKey('Accounts', models.DO_NOTHING, primary_key=True)
    client = models.ForeignKey('Clients', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_customers'
        unique_together = (('account', 'client'),)


class AccountType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=40)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=3)
    fee = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'account_type'


class Accounts(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    accountnumber = models.CharField(db_column='accountNumber', unique=True, max_length=50)  # Field name made lowercase.
    typeofaccount = models.ForeignKey(AccountType, models.DO_NOTHING, db_column='typeOfAccount')  # Field name made lowercase.
    balance = models.DecimalField(max_digits=19, decimal_places=2)
    bank = models.ForeignKey('Bank', models.DO_NOTHING)
    dateopened = models.DateField(db_column='dateOpened')  # Field name made lowercase.
    lastupdated = models.DateField(db_column='lastUpdated')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accounts'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bank(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bank'


class BankEmployees(models.Model):
    bankid = models.ForeignKey(Bank, models.DO_NOTHING, db_column='BankID', primary_key=True)  # Field name made lowercase.
    employeesid = models.ForeignKey('Employees', models.DO_NOTHING, db_column='EmployeesID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bank_employees'
        unique_together = (('bankid', 'employeesid'),)


class Clients(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=45)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=45)  # Field name made lowercase.
    ssn = models.CharField(db_column='SSN', unique=True, max_length=11)  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='dateOfBirth')  # Field name made lowercase.
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=10)  # Field name made lowercase.
    email = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'clients'


class CreditCardTypes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=20)
    min_limit = models.DecimalField(max_digits=10, decimal_places=2)
    max_limit = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'credit_card_types'


class CreditCards(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    typeofcard = models.ForeignKey(CreditCardTypes, models.DO_NOTHING, db_column='typeOfCard')  # Field name made lowercase.
    number = models.CharField(unique=True, max_length=20)
    cvc = models.CharField(max_length=3)
    expiry_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'credit_cards'


class DebitCardTypes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=20)
    fee = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'debit_card_types'


class DebitCards(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    typeofcard = models.ForeignKey(DebitCardTypes, models.DO_NOTHING, db_column='typeOfCard')  # Field name made lowercase.
    number = models.CharField(unique=True, max_length=20)
    cvc = models.CharField(max_length=3)
    expiry_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'debit_cards'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employees(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=45)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=45)  # Field name made lowercase.
    ssn = models.CharField(max_length=45)
    dateofbirth = models.DateField(db_column='dateOfBirth')  # Field name made lowercase.
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    salary = models.DecimalField(max_digits=19, decimal_places=2)
    position = models.CharField(max_length=25)
    email = models.CharField(unique=True, max_length=50)
    bankid = models.ForeignKey(Bank, models.DO_NOTHING, db_column='BankID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employees'


class LoanTypes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=20)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'loan_types'


class Loans(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    typeofloan = models.ForeignKey(LoanTypes, models.DO_NOTHING, db_column='typeOfLoan')  # Field name made lowercase.
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateField()
    period = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'loans'


class Login(models.Model):
    id = models.ForeignKey(Clients, models.DO_NOTHING, db_column='ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(unique=True, max_length=25)
    password = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'login'


class TransactionTypes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'transaction_types'


class Transactions(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    typeoftransaction = models.ForeignKey(TransactionTypes, models.DO_NOTHING, db_column='typeOfTransaction')  # Field name made lowercase.
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'transactions'
