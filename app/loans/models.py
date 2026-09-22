from django.db import models
from django.contrib.auth.models import User
# Branch перевод Фелиалы
class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название филиала")
    city = models.CharField(max_length=100, verbose_name="Город")
    address = models.CharField(max_length=200, verbose_name="Адрес")

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

class Tariff(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название тарифа")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Ставка (% в день)")
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Макс. сумма (руб.)")
    term_days = models.IntegerField(verbose_name="Срок (в днях)")

    def __str__(self):
        return f"{self.name} ({self.interest_rate}%)"

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

class Loan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('paid', 'Погашен'),
        ('overdue', 'Просрочен'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент")
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, verbose_name="Тариф")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, verbose_name="Филиал")

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма займа (руб.)")
    issue_date = models.DateField(auto_now_add=True, verbose_name="Дата выдачи")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="Статус")

    def __str__(self):
        return f"Займ #{self.id} - {self.client.username} ({self.amount} руб.)"

    class Meta:
        verbose_name = "Займ"
        verbose_name_plural = "Займы"

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, verbose_name="Заем")
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма платежа")
    payment_date = models.DateField(auto_now_add=True, verbose_name="Дата и время платежа")

    def __str__(self):
        return f"Платеж #{self.id} по займу #{self.loan.id} на {self.payment_amount} руб."

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"