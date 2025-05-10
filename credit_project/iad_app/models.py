from django.db import models


# Клиент
class Client(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    annual_income = models.FloatField()

    def __str__(self):
        return self.name

# 2. Заявка на анализ кредитоспособности
class Application(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_bank_accounts = models.IntegerField()
    num_credit_cards = models.IntegerField()
    interest_rate = models.FloatField()
    num_of_loans = models.IntegerField()
    num_of_delayed_payments = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка #{self.id} от {self.client.name}"

# 3. Результат анализа
class AnalysisResult(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    predicted_score = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Результат: {self.predicted_score}"

class CreditApplication(models.Model):
    name = models.CharField(max_length=100)
    age = models.FloatField()
    annual_income = models.FloatField()
    num_bank_accounts = models.IntegerField()
    num_credit_cards = models.IntegerField()
    interest_rate = models.FloatField()
    num_of_loans = models.IntegerField()
    num_of_delayed_payments = models.IntegerField()
    prediction = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.created_at.strftime('%d.%m.%Y %H:%M')}: {self.prediction}"
