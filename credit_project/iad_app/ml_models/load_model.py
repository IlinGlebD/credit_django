import joblib
import os
import numpy as np

# Путь к сохранённой 3-классовой модели
MODEL_PATH = os.path.join(os.path.dirname(__file__),
                          'credit_model_rf_randomforest.pkl')

# Загрузка модели
model = joblib.load(MODEL_PATH)

# Классы по индексам
CLASS_MAP = {0: "Низкий", 1: "Средний", 2: "Высокий"}


def predict_credit_score(input_data: dict) -> str:
    """
    input_data = {
        'Age': 30,
        'Annual_Income': 50000,
        'Num_Bank_Accounts': 3,
        'Num_Credit_Card': 2,
        'Interest_Rate': 15,
        'Num_of_Loan': 1,
        'Num_of_Delayed_Payment': 0
    }
    """
    # Упорядочим признаки в нужном порядке
    features = [
        input_data['age'],
        input_data['annual_income'],
        input_data['num_bank_accounts'],
        input_data['num_credit_cards'],
        input_data['interest_rate'],
        input_data['num_of_loans'],
        input_data['num_of_delayed_payments']
    ]

    # Преобразуем в формат, подходящий для sklearn
    X = np.array([features])

    # Предсказание
    prediction = model.predict(X)[0]

    # Возвращаем строковое значение
    return CLASS_MAP[prediction]
