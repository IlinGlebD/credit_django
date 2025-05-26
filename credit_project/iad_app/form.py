from django import forms

class CreditForm(forms.Form):
    name = forms.CharField(label="ФИО", max_length=250, required=True)
    age = forms.IntegerField(label="Возраст",  required=True)
    annual_income = forms.FloatField(label="Годовой доход", required=True)
    num_bank_accounts = forms.IntegerField(label="Количество банковских счетов",
                                           required=True)
    num_credit_cards = forms.IntegerField(label="Количество кредитных карт",
                                          required=True)
    interest_rate = forms.FloatField(label="Процентная ставка",
                                     required=True)
    num_of_loans = forms.IntegerField(label="Количество кредитов",
                                      required=True)
    num_of_delayed_payments = forms.IntegerField(label="Задержки платежей",
                                                 required=True)


class FilterForm(forms.Form):
    name = forms.CharField(label="Имя клиента", required=False)

    prediction = forms.ChoiceField(
        label="Кредитный рейтинг",
        choices=[
            ('', '--- все ---'),
            ('Высокий', 'Высокий'),
            ('Средний', 'Средний'),
            ('Низкий', 'Низкий')
        ],
        required=False
    )
