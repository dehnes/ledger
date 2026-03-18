from django.contrib import admin
from .models import Person
from apps.ledger.models import Account


# This allows you to see a person's accounts while looking at the person
class AccountInline(admin.TabularInline):
    model = Account.owners.through  # Link to the ManyToMany relationship
    extra = 0
    verbose_name = "Account Ownership"
    verbose_name_plural = "Accounts Owned"


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "user", "get_account_count")
    search_fields = ("first_name", "last_name", "user__email")
    list_filter = ("user__is_active",)

    # Allows you to edit which accounts they own without leaving the page
    # Note: Requires Account to be imported or handled via 'through'
    # inlines = [AccountInline]

    def get_account_count(self, obj):
        return obj.accounts.count()

    get_account_count.short_description = "Accounts"
