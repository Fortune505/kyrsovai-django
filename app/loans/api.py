from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from django.contrib.auth.models import User
from loans.models import Branch, Tariff, Loan, Payment
from loans.serializers import UserSerializer, BranchSerializer, TariffSerializer, LoanSerializer, PaymentSerializer

class BranchViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class TariffViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer

class LoanViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer






