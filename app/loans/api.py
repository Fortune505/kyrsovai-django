from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from loans.models import Branch, Tariff, Loan, Payment, BranchPicture
from loans.serializers import UserSerializer, BranchSerializer, TariffSerializer, LoanSerializer, PaymentSerializer, BranchPictureSerializer

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

class BranchPictureViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = BranchPicture.objects.all()
    serializer_class = BranchPictureSerializer

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

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            return qs.none()

        if user.is_superuser or user.is_staff:
            user_param = self.request.query_params.get('user')
            if user_param:
                qs = qs.filter(client_id=user_param)
            return qs

        return qs.filter(client=user)

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

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.is_superuser or user.is_staff:
            return qs
        return qs.filter(loan__client=user)

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

    @action(detail=False, methods=['get'])
    def current(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'is_authenticated': False})
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_authenticated': True,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        })

    @action(detail=False, methods=['post'])
    def login_user(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'success': True, 'username': user.username, 'is_superuser': user.is_superuser, 'is_staff': user.is_staff})
        return Response({'success': False, 'error': 'Неверный логин или пароль'}, status=400)

    @action(detail=False, methods=['post'])
    def register_user(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        if User.objects.filter(username=username).exists():
            return Response({'success': False, 'error': 'Пользователь с таким логином уже существует'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return Response({'success': True, 'username': user.username, 'is_superuser': False, 'is_staff': False})

    @action(detail=False, methods=['post'])
    def logout_user(self, request):
        logout(request)
        return Response({'success': True})






