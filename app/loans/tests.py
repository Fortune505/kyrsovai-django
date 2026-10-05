from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker
from loans.models import Branch, Tariff, Loan, Payment


# BranchViewSet
class TestBranchViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_branches(self):
        branches = baker.make(Branch, 10)
        r = self.client.get('/api/branches/')
        data = r.json()
        assert r.status_code == 200
        assert len(data) == 10

    def test_create_branch(self):
        branch_data = {
            "name": "Филиал на улице Пушкина",
            "city": "Москва",
            "address": "ул. Пушкина, д. Калатушкина"
        }
        r =self.client.post('/api/branches/', branch_data)
        assert r.status_code == 201
        assert Branch.objects.filter(name="Филиал на улице Пушкина").exists()

    def test_delete_branch(self):
        branches = baker.make(Branch, 10)
        branch: Branch = branches[2]
        r = self.client.delete(f'/api/branches/{branch.id}/')
        assert r.status_code == 204
        assert not Branch.objects.filter(id=branch.id).exists()

    def test_update_branch(self):
        branches = baker.make(Branch, 10)
        branch: Branch = branches[2]
        r = self.client.get(f'/api/branches/{branch.id}/')
        data = r.json()
        assert data['name'] == branch.name

        r = self.client.put(f'/api/branches/{branch.id}/', {
            "name": "Филиал Марунов",
            "city": branch.city,
            "address": branch.address
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/branches/{branch.id}/')
        data = r.json()
        assert data['name'] == "Филиал Марунов"

        branch.refresh_from_db()
        assert data['name'] == branch.name

# TariffViewSet
class TestTariffViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_tariffs(self):
        tariffs = baker.make(Tariff, 10)
        r = self.client.get('/api/tariffs/')
        data = r.json()
        assert r.status_code == 200
        assert len(data) == 10

    def test_create_tariff(self):
        tariff_data = {
            "name": "До зарплаты",
            "interest_rate": "1.50",
            "max_amount": "10000.00",
            "term_days": 30
        }
        r = self.client.post('/api/tariffs/', tariff_data)
        assert r.status_code == 201
        assert Tariff.objects.filter(name="До зарплаты").exists()

    def test_delete_tariff(self):
        tariffs = baker.make(Tariff, 10)
        tariff: Tariff = tariffs[2]
        r = self.client.delete(f'/api/tariffs/{tariff.id}/')
        assert r.status_code == 204
        assert not Tariff.objects.filter(id=tariff.id).exists()

    def test_update_tariff(self):
        tariffs = baker.make(Tariff, 10)
        tariff: Tariff = tariffs[2]
        r = self.client.get(f'/api/tariffs/{tariff.id}/')
        data = r.json()
        assert data['name'] == tariff.name

        r = self.client.put(f'/api/tariffs/{tariff.id}/', {
            "name": "До обеда",
            "interest_rate": str(tariff.interest_rate),
            "max_amount": str(tariff.max_amount),
            "term_days": tariff.term_days
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/tariffs/{tariff.id}/')
        data = r.json()
        assert data['name'] == "До обеда"

        tariff.refresh_from_db()
        assert data['name'] == tariff.name

#LoanViewSet
class TestLoanViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_loans(self):
        loans = baker.make(Loan, 10)
        r = self.client.get('/api/loans/')
        data = r.json()
        assert r.status_code == 200
        assert len(data) == 10

    def test_create_loan(self):
        user = baker.make(User)
        branch = baker.make(Branch)
        tariff = baker.make(Tariff)
        loan_data = {
            "client": user.id,
            "tariff": tariff.id,
            "branch": branch.id,
            "amount": "5000.00",
            "status": "active"
        }
        r = self.client.post('/api/loans/', loan_data)
        assert r.status_code == 201
        assert Loan.objects.filter(amount="5000.00").exists()

    def test_delete_loan(self):
        loans = baker.make(Loan, 10)
        loan: Loan = loans[2]
        r = self.client.delete(f'/api/loans/{loan.id}/')
        assert r.status_code == 204
        assert not Loan.objects.filter(id=loan.id).exists()

    def test_update_loan(self):
        loans = baker.make(Loan, 10)
        loan: Loan = loans[2]
        r = self.client.patch(f'/api/loans/{loan.id}/', {
            "status": 'paid'
        })
        assert r.status_code == 200
        loan.refresh_from_db()
        assert loan.status == 'paid'
        
# PaymentViewSet
class TestPaymentViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_payments(self):
        payments = baker.make(Payment, 10)
        r = self.client.get('/api/payments/')
        data = r.json()
        assert r.status_code == 200
        assert len(data) == 10

    def test_create_payment(self):
        loan = baker.make(Loan)
        payment_data = {
            "loan": loan.id,
            "payment_amount": "1000.00"
        }
        r = self.client.post('/api/payments/', payment_data)
        assert r.status_code == 201
        assert Payment.objects.filter(payment_amount="1000.00").exists()

    def test_delete_payment(self):
        payments = baker.make(Payment, 10)
        payment: Payment = payments[2]
        r = self.client.delete(f'/api/payments/{payment.id}/')
        assert r.status_code == 204
        assert not Payment.objects.filter(id=payment.id).exists()

    def test_update_payment(self):
        payments = baker.make(Payment, 10)
        payment: Payment = payments[2]
        r = self.client.put(f'/api/payments/{payment.id}/', {
            "loan": payment.loan.id,
            "payment_amount": "2000.00"
        })
        assert r.status_code == 200
        payment.refresh_from_db()
        assert str(payment.payment_amount) == "2000.00"

# UserViewSet
class TestUserViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_users(self):
        users = baker.make(User, 10)
        r = self.client.get('/api/users/')
        data = r.json()
        assert r.status_code == 200
        assert len(data) >= 10

    def test_create_user(self):
        user_data = {
            "username": "unique_borrower_test",
            "email": "borrower@example.com"
        }
        r = self.client.post('/api/users/', user_data)
        assert r.status_code == 201
        assert User.objects.filter(username="unique_borrower_test").exists()

    def test_delete_user(self):
        users = baker.make(User, 10)
        user: User = users[2]
        r = self.client.delete(f'/api/users/{user.id}/')
        assert r.status_code == 204
        assert not User.objects.filter(id=user.id).exists()

    def test_update_user(self):
        users = baker.make(User, 10)
        user: User = users[2]
        r = self.client.put(f'/api/users/{user.id}/', {
            "username": "updated_borrower_test",
            "email": user.email
        })
        assert r.status_code == 200
        user.refresh_from_db()
        assert user.username == "updated_borrower_test"