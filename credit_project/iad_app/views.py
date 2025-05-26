from django.shortcuts import render
from .form import CreditForm, FilterForm
from .ml_models.load_model import predict_credit_score
from .models import Client, Application, AnalysisResult


def credit_view(request):
    if request.method == 'POST':
        form = CreditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # 1. Создаём или получаем клиента
            client, created = Client.objects.get_or_create(
                name=data['name'],
                defaults={
                    'age': data['age'],
                    'annual_income': data['annual_income']
                }
            )

            # 2. Создаём заявку
            application = Application.objects.create(
                client=client,
                num_bank_accounts=data['num_bank_accounts'],
                num_credit_cards=data['num_credit_cards'],
                interest_rate=data['interest_rate'],
                num_of_loans=data['num_of_loans'],
                num_of_delayed_payments=data['num_of_delayed_payments']
            )

            # 3. Получаем прогноз, балл, ставку
            predicted_score, score, rate = predict_credit_score(data)

            # 4. Сохраняем результат
            AnalysisResult.objects.create(
                application=application,
                predicted_score=predicted_score,
                credit_score=score,
                suggested_rate=rate
            )

            return render(request, 'credit_result.html', {
                'result': predicted_score,
                'score': score,
                'suggested_rate': rate,
                'data': data,
            })

    else:
        form = CreditForm()

    return render(request, 'credit_form.html', {'form': form})


def history_view(request):
    form = FilterForm(request.GET or None)

    applications = Application.objects.select_related('client', 'analysisresult').order_by('-created_at')

    if form.is_valid():
        name = form.cleaned_data.get('name')
        prediction = form.cleaned_data.get('prediction')

        if name:
            applications = applications.filter(client__name__icontains=name)
        if prediction:
            applications = applications.filter(analysisresult__predicted_score=prediction)

    return render(request, 'credit_history.html', {
        'applications': applications,
        'form': form
    })
