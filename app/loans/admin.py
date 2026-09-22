from django.contrib import admin
from .models import Branch, Tariff, Loan, Payment

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address')

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'interest_rate', 'max_amount', 'term_days')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'tariff', 'branch', 'amount', 'issue_date', 'status')
    list_filter = ('status', 'tariff', 'branch')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan', 'payment_amount', 'payment_date')