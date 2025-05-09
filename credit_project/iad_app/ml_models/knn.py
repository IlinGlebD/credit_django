import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
import joblib

# Загрузка данных
df = pd.read_csv('iad_app/ml_models/train.csv')

# Оставляем все три класса
df = df[df['Credit_Score'].isin(['Good', 'Standard', 'Poor'])]

# Удаляем пробелы и пропуски
df = df.replace(' ', pd.NA)
df = df.dropna(subset=['Age', 'Annual_Income', 'Num_Bank_Accounts',
                       'Num_Credit_Card', 'Interest_Rate',
                       'Num_of_Loan', 'Num_of_Delayed_Payment',
                       'Credit_Score'])

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
df = df.dropna(subset=['Age', 'Annual_Income', 'Num_of_Loan',
                       'Num_of_Delayed_Payment'])

# Кодирование классов: Poor = 0, Standard = 1, Good = 2
df['Credit_Score_Label'] = df['Credit_Score'].map({'Poor': 0, 'Standard': 1,
                                                   'Good': 2})

# Выбор признаков
features = ['Age', 'Annual_Income', 'Num_Bank_Accounts', 
            'Num_Credit_Card', 'Interest_Rate', 
            'Num_of_Loan', 'Num_of_Delayed_Payment']
X = df[features]
y = df['Credit_Score_Label']

# Разделение на train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42)

# Обучение KNN-модели
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

# Оценка
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=['Poor', 'Standard',
                                                          'Good']))

# Сохранение
joblib.dump(model, 'credit_model_knn_3class.pkl')
print("Модель KNN (3 класса) сохранена как credit_model_knn_3class.pkl")
