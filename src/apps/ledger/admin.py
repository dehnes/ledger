from django.contrib import admin


from .models import (
    FinancialInstitute,
    Account,
    BankAccount,
    CreditCard,
    LedgerEntry,
    Transaction,
)


class LedgerEntryInline(admin.TabularInline):
    model = LedgerEntry
    extra = 2  # Shows 2 empty rows by default for new transactions
    fields = ("account", "amount")
    # We use raw_id_fields if you eventually have thousands of accounts
    raw_id_fields = ("account",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("valuta_date", "description", "get_total_amount")
    search_fields = ("description",)
    list_filter = ("valuta_date",)
    inlines = [LedgerEntryInline]

    def get_total_amount(self, obj):
        """Show the absolute sum of the 'positive' side for a quick overview"""
        from django.db.models import Sum

        # Sum only positive entries to show the 'value' of the transaction
        total = obj.entries.filter(amount__gt=0).aggregate(Sum("amount"))["amount__sum"]
        return total or 0

    get_total_amount.short_description = "Amount"


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
