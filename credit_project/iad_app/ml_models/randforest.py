import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Загрузка данных
df = pd.read_csv('credit_project/iad_app/ml_models/train.csv')

# Оставляем 3 класса
df = df[df['Credit_Score'].isin(['Good', 'Standard', 'Poor'])]
df = df.replace(' ', pd.NA)
df = df.dropna(subset=['Age', 'Annual_Income', 'Num_Bank_Accounts',
                       'Num_Credit_Card', 'Interest_Rate',
                       'Num_of_Loan', 'Num_of_Delayed_Payment'])

# Приведение чисел к float
def to_float(x):
    try:
        return float(x)
    except:
        return None


df['Age'] = df['Age'].apply(to_float)
df['Annual_Income'] = df['Annual_Income'].apply(to_float)
df['Num_of_Loan'] = df['Num_of_Loan'].apply(to_float)
df['Num_of_Delayed_Payment'] = df['Num_of_Delayed_Payment'].apply(to_float)
df = df.dropna()

# Кодировка классов
df['Credit_Score_Label'] = df['Credit_Score'].map({'Poor': 0, 'Standard': 1,
                                                   'Good': 2})

# Признаки и целевая переменная
features = ['Age', 'Annual_Income', 'Num_Bank_Accounts',
            'Num_Credit_Card', 'Interest_Rate',
            'Num_of_Loan', 'Num_of_Delayed_Payment']
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
print("Модель RandomForest сохранена как credit_model_rf_3class.pkl")
