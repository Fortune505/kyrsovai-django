from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Branch, Tariff, Loan, Payment, BranchPicture

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False)

    def get_role(self, obj):
        if obj.is_superuser:
            return 'Администратор'
        if obj.is_staff:
            return 'Менеджер'
        return 'Клиент'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_staff', 'is_superuser', 'password']

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class BranchPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchPicture
        fields = '__all__'

class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.username', read_only=True)
    tariff_name = serializers.CharField(source='tariff.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['client']=self.context['request'].user
        return super().create(validated_data)
    class Meta:
        model = Loan
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

