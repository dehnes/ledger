from rest_framework import viewsets, permissions
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """

    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # The user sees accounts THEY created (Manager role)
        # regardless of who the "People" owners are.
        return Account.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically link the newly created account to the logged-in user.
        """
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Handles viewing and creating transactions.
    """

    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # We only want to see transactions where the user
        # owns at least one of the involved accounts.
        return (
            Transaction.objects.filter(entries__account__user=self.request.user)
            .distinct()
            .order_by("-valuta_date")
        )
