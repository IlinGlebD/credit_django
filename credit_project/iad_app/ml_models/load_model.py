import joblib
import os
import numpy as np

# Путь к модели
MODEL_PATH = os.path.join(os.path.dirname(__file__),
                          'credit_model_rf_randomforest.pkl')
model = joblib.load(MODEL_PATH)

CLASS_MAP = {0: "Низкий", 1: "Средний", 2: "Высокий"}


def predict_credit_score(input_data: dict) -> tuple[str, int, float]:
    """
    Возвращает:
    - рейтинг: 'Низкий' / 'Средний' / 'Высокий'
    - балл: 1–999
    - рекомендованная ставка (%)
    """

    # Порядок признаков
    features = [
        input_data['age'],
        input_data['annual_income'],
        input_data['num_bank_accounts'],
        input_data['num_credit_cards'],
        input_data['interest_rate'],
        input_data['num_of_loans'],
        input_data['num_of_delayed_payments']
    ]
    X = np.array([features])

    # Предсказание
    proba = model.predict_proba(X)[0]  # [p_низкий, p_средний, p_высокий]

    # Жёсткая интерпретация
    if proba[0] >= 0.5:
        predicted_class = 0
    elif proba[2] >= 0.6:
        predicted_class = 2
    else:
        predicted_class = 1

    # Балл по классам
    ranges = {
        0: (1, 399),
        1: (400, 599),
        2: (600, 999)
    }
    min_score, max_score = ranges[predicted_class]
    confidence = proba[predicted_class]
    score = round(min_score + (max_score - min_score) * confidence)
    score = max(1, min(score, 999))

    # Рекомендованная ставка
    if score >= 800:
        rate = 8.5
    elif score >= 600:
        rate = 12.5
    elif score >= 400:
        rate = 17.5
    else:
        rate = 22.5

    return CLASS_MAP[predicted_class], score, rate
