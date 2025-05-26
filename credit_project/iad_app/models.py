from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    annual_income = models.FloatField()

class Application(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_bank_accounts = models.IntegerField()
    num_credit_cards = models.IntegerField()
    interest_rate = models.FloatField()
    num_of_loans = models.IntegerField()
    num_of_delayed_payments = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class AnalysisResult(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    predicted_score = models.CharField(max_length=20)
    credit_score = models.PositiveIntegerField()
    suggested_rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
