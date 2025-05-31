import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import numpy as np
import re

# Загрузка данных
df = pd.read_csv('credit_project/iad_app/ml_models/train.csv')

# Оставляем только три класса
df = df[df['Credit_Score'].isin(['Good', 'Standard', 'Poor'])]

# Заменим строки-пробелы на NaN
df = df.replace(' ', pd.NA)


# Очистка числовых столбцов с мусорными символами
def clean_numeric_column(series):
    return pd.to_numeric(series.astype(str).str.replace(r'[^0-9.\-]', '',
                                                        regex=True), errors='coerce')


columns_to_clean = [
    'Age', 'Annual_Income', 'Num_of_Loan', 'Num_of_Delayed_Payment',
    'Changed_Credit_Limit', 'Outstanding_Debt', 'Amount_invested_monthly',
    'Monthly_Balance', 'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate'
]

for col in columns_to_clean:
    df[col] = clean_numeric_column(df[col])

# Удаляем некорректный возраст
df['Age'] = df['Age'].apply(lambda x: x if 0 < x < 100 else np.nan)


# Преобразование кредитной истории в месяцы
def convert_credit_history(s):
    if pd.isna(s):
        return np.nan
    match = re.match(r'(\d+)\s+Years.*?(\d+)\s+Months', str(s))
    if match:
        return int(match.group(1)) * 12 + int(match.group(2))
    return np.nan


df['Credit_History_Months'] = df['Credit_History_Age'].apply(convert_credit_history)

# Удаление мусора в других столбцах
df['Credit_Mix'] = df['Credit_Mix'].replace('_', pd.NA)
df['Occupation'] = df['Occupation'].replace('_______', pd.NA)
df['SSN'] = df['SSN'].where(df['SSN'].str.match(r'^\d{3}-\d{2}-\d{4}$'))

# Удаление строк с критически важными пропусками
df = df.dropna(subset=[
    'Age', 'Annual_Income', 'Num_Bank_Accounts', 'Num_Credit_Card',
    'Interest_Rate', 'Num_of_Loan', 'Num_of_Delayed_Payment'
])

# Приведение метки к числу
df['Credit_Score_Label'] = df['Credit_Score'].map({'Poor': 0, 'Standard': 1,
                                                   'Good': 2})
df = df.dropna(subset=['Credit_Score_Label'])

# Признаки и целевая переменная
features = [
    'Age', 'Annual_Income', 'Num_Bank_Accounts', 'Num_Credit_Card',
    'Interest_Rate', 'Num_of_Loan', 'Num_of_Delayed_Payment'
]
X = df[features]
y = df['Credit_Score_Label']

# Разделение
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42)

# Обучение модели
model = RandomForestClassifier(class_weight='balanced', n_estimators=100,
                               random_state=42)
model.fit(X_train, y_train)

# Оценка
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=['Низкий', 'Средний',
                                                          'Высокий']))

# Сохранение модели
joblib.dump(model, 'credit_model_rf_randomforest.pkl')
print("Модель RandomForest сохранена как credit_model_rf_randomforest.pkl")
