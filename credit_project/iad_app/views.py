from django.shortcuts import render, redirect
from .form import CreditForm
from .ml_models.load_model import predict_credit_score
from .models import CreditApplication
from .form import FilterForm
from .ml_models.model_info import generate_model_report_image

def credit_view(request):
    if request.method == 'POST':
        form = CreditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            result = predict_credit_score(data)
            # сохраняем заявку
            CreditApplication.objects.create(
                name=data['name'],
                age=data['age'],
                annual_income=data['annual_income'],
                num_bank_accounts=data['num_bank_accounts'],
                num_credit_cards=data['num_credit_cards'],
                interest_rate=data['interest_rate'],
                num_of_loans=data['num_of_loans'],
                num_of_delayed_payments=data['num_of_delayed_payments'],
                prediction=result
            )
            report, image_filename = generate_model_report_image()
          
            return render(request, 'credit_result.html', {
                'result': result,
                'data': data,
                'report': report,
                'image': image_filename
            })
    else:
        form = CreditForm()

    return render(request, 'credit_form.html', {'form': form})


def history_view(request):
    form = FilterForm(request.GET or None)
    applications = CreditApplication.objects.all().order_by('-created_at')

    if form.is_valid():
        name = form.cleaned_data.get('name')
        prediction = form.cleaned_data.get('prediction')

        if name:
            applications = applications.filter(name__icontains=name)
        if prediction:
            applications = applications.filter(prediction=prediction)

    return render(request, 'credit_history.html', {
        'applications': applications,
        'form': form
    })
