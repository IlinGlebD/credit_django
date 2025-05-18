import os
import joblib
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import shutil

def generate_model_report_image():
    # Данные
    df = pd.read_csv('../credit_project/iad_app/ml_models/train.csv')
    df = df[df['Credit_Score'].isin(['Good', 'Standard', 'Poor'])]
    df = df.replace(' ', pd.NA)
    df = df.dropna(subset=[
        'Age', 'Annual_Income', 'Num_Bank_Accounts', 'Num_Credit_Card',
        'Interest_Rate', 'Num_of_Loan', 'Num_of_Delayed_Payment'
    ])

    def to_float(x):  # очистка
        try: return float(x)
        except: return None

    df['Age'] = df['Age'].apply(to_float)
    df['Annual_Income'] = df['Annual_Income'].apply(to_float)
    df['Num_of_Loan'] = df['Num_of_Loan'].apply(to_float)
    df['Num_of_Delayed_Payment'] = df['Num_of_Delayed_Payment'].apply(to_float)
    df = df.dropna()

    df['Credit_Score_Label'] = df['Credit_Score'].map({'Poor': 0, 'Standard': 1,
                                                       'Good': 2})

    features = ['Age', 'Annual_Income', 'Num_Bank_Accounts',
                'Num_Credit_Card', 'Interest_Rate',
                'Num_of_Loan', 'Num_of_Delayed_Payment']

    X = df[features]
    y = df['Credit_Score_Label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        random_state=42)

    model = joblib.load(os.path.join(os.path.dirname(__file__),
                                     'credit_model_rf_randomforest.pkl'))

    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True)

    # Визуализация важности признаков
    importances = model.feature_importances_
    plt.figure(figsize=(8, 5))
    plt.barh(features, importances)
    plt.xlabel("Важность признака")
    plt.tight_layout()

    # Сохраняем временно
    local_path = os.path.join(os.path.dirname(__file__), 'model_visual.png')
    plt.savefig(local_path)
    plt.close()

    static_dir = os.path.join('iad_app', 'static')
    os.makedirs(static_dir, exist_ok=True)

    # Копируем в static/
    static_path = os.path.join('iad_app', 'static', 'model_visual.png')
    shutil.copy(local_path, static_path)

    return report, 'model_visual.png'
