from django.contrib import admin


from .models import FinancialInstitute, Account, BankAccount, CreditCard


@admin.register(FinancialInstitute)
class FinancialInstituteAdmin(admin.ModelAdmin):
    list_display = ("name", "bic", "country")
    search_fields = ("name", "bic")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "account_type", "parent")
    list_filter = ("account_type", "user")
    search_fields = ("name",)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "institute", "iban")


admin.site.register(CreditCard)
