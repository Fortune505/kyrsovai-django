from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker
from loans.models import Branch, Tariff, Loan, Payment


# BranchViewSet фелиалы
@pytest.mark.django_db
class TestBranchViewSet:
    def test_get_branches(self):
        client = APIClient()
        response = client.get('/api/branches/')

        assert response.status_code == 200

    def test_create_branch(self):
        client = APIClient()
        branch_data = {
            'name' : 'Филиал на улице Пушкина',
            'city' : 'Москва',
            'address' : 'ул. Пушкина, д. Калатушкина',
        }
        response = client.post('/api/branches/', branch_data)

        assert response.status_code == 201

        assert Branch.objects.filter(name='Филиал на улице Пушкина').exists()

    def test_delete_branch(self):
        client = APIClient()
        branch = baker.make(Branch)
        response = client.delete(f'/api/branches/{branch.id}/')

        assert response.status_code == 204

        assert not Branch.objects.filter(id=branch.id).exists()

    def test_update_branch(self):
        client = APIClient()
        branch = baker.make(Branch, name='Филиал Калун')
        response = client.patch(f'/api/branches/{branch.id}/', {'name' : 'Филиал Марунов'})

        assert response.status_code == 200

        branch.refresh_from_db()
        assert branch.name == 'Филиал Марунов'

#TestTariffViewSet тариыф
@pytest.mark.django_db
class TestTariffViewSet:
    def test_get_tariffs(self):
        client = APIClient()
        response = client.get('/api/tariffs/')

        assert response.status_code == 200

    def test_create_tariff(self):
        client = APIClient()
        tariff_data = {
            'name' : 'До зарплаты',
            'interest_rate' : 5.0,
            'max_amount' : 10000.0,
            'term_days' : 30,
        }
        response = client.post('/api/tariffs/', tariff_data)

        assert response.status_code == 201

        assert Tariff.objects.filter(name='До зарплаты').exists()

    def test_delete_tariff(self):
        client = APIClient()
        tariff = baker.make(Tariff)
        response = client.delete(f'/api/tariffs/{tariff.id}/')

        assert response.status_code == 204

        assert not Tariff.objects.filter(id=tariff.id).exists()

    def test_update_tariff(self):
        client = APIClient()
        tariff = baker.make(Tariff, name='До зарплаты')
        response = client.patch(f'/api/tariffs/{tariff.id}/', {'name' : 'До обеда'})

        assert response.status_code == 200

        tariff.refresh_from_db()
        assert tariff.name == 'До обеда'

# TestLoanViewSet кредиты
@pytest.mark.django_db
class TestLoanViewSet:
    def test_get_loans(self):
        client = APIClient()
        response = client.get('/api/loans/')

        assert response.status_code == 200

    def test_create_loan(self):
        client = APIClient()
        user = baker.make('User')
        tariff = baker.make(Tariff)
        branch = baker.make(Branch)

        loan_date = {
            'client' : user.id,
            'tariff' : tariff.id,
            'branch' : branch.id,
            'amount' : '5000.0',
            'status' : 'active',
        }

        response = client.post('/api/loans/', loan_date)
        assert response.status_code == 201
        assert Loan.objects.filter(amount='5000.0').exists()

    def test_delete_loan(self):
        client = APIClient()
        loan = baker.make(Loan)
        response = client.delete(f'/api/loans/{loan.id}/')

        assert response.status_code == 204

        assert not Loan.objects.filter(id=loan.id).exists()

    def test_update_loan(self):
        client = APIClient()
        loan = baker.make(Loan, status='active')
        response = client.patch(f'/api/loans/{loan.id}/', {'status' : 'paid'})

        assert response.status_code == 200

        loan.refresh_from_db()
        assert loan.status == 'paid'

# TestPaymentViewSet платежи
@pytest.mark.django_db  
class TestPaymentViewSet:
    def test_get_payments(self):
        client = APIClient()
        response = client.get('/api/payments/')

        assert response.status_code == 200

    def test_create_payment(self):
        client = APIClient()
        loan = baker.make(Loan)
        payment_data = {
            'loan' : loan.id,
            'payment_amount' : '5000.0',
        }
        response = client.post('/api/payments/', payment_data)

        assert response.status_code == 201

        assert Payment.objects.filter(payment_amount='5000.0').exists()

    def test_delete_payment(self):
        client = APIClient()
        payment = baker.make(Payment)
        response = client.delete(f'/api/payments/{payment.id}/')

        assert response.status_code == 204

        assert not Payment.objects.filter(id=payment.id).exists()

    def test_update_payment(self):
        client = APIClient()
        payment = baker.make(Payment, payment_amount='5000.0')
        response = client.patch(f'/api/payments/{payment.id}/', {'payment_amount' : '6000.0'})

        assert response.status_code == 200

        payment.refresh_from_db()
        assert float(payment.payment_amount) == 6000.0

# TestUserViewSet пользователи
@pytest.mark.django_db
class TestUserViewSet:
    def test_get_users(self):
        client = APIClient()
        response = client.get('/api/users/')

        assert response.status_code == 200

    def test_create_user(self):
        client = APIClient()
        user_data = {
            'username' : 'testuser',
            'email' : 'testuser@example.com',    
        }
        response = client.post('/api/users/', user_data)
        assert response.status_code == 201
        assert User.objects.filter(username='testuser').exists()

    def test_delete_user(self):
        client = APIClient()
        user = baker.make(User)
        response = client.delete(f'/api/users/{user.id}/')

        assert response.status_code == 204

        assert not User.objects.filter(id=user.id).exists()

    def test_update_user(self):
        client = APIClient()
        user = baker.make(User, username='testuser')
        response = client.patch(f'/api/users/{user.id}/', {'username' : 'updateduser'})

        assert response.status_code == 200

        user.refresh_from_db()
        assert user.username == 'updateduser'
