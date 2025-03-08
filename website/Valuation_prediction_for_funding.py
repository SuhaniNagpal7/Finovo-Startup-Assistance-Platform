import pandas as pd
import numpy as np
from google.colab import files

data=files.upload()

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

import tensorflow as tf

from sklearn.metrics import r2_score
data=pd.read_csv('startup_funding.csv')

def preprocess_inputs(df):
    df = df.copy()

    # Drop ID and high-cardinality columns
    df = df.drop(['Sr No', 'Startup Name', 'SubVertical', 'Investors Name'], axis=1)

    # Clean \\xc2\\xa0 examples
    df = df.applymap(lambda x: x.replace(r'\\xc2\\xa0', '') if type(x) == str else x)

    # Clean target column
    df['Amount in USD'] = df['Amount in USD'].apply(lambda x: x.replace(',', '') if str(x) != 'nan' else x)
    df['Amount in USD'] = df['Amount in USD'].replace({
        'undisclosed': np.NaN,
        'unknown': np.NaN,
        'Undisclosed': np.NaN,
        'N/A': np.NaN,
        '14342000+': '14342000'
    })

    # Drop missing target rows
    missing_target_rows = df[df['Amount in USD'].isna()].index
    df = df.drop(missing_target_rows, axis=0).reset_index(drop=True)
    df = df.drop('Remarks', axis=1)

    # Fill categorical missing values with most frequent occurrence
    for column in ['Industry Vertical', 'City  Location', 'InvestmentnType']:
        df[column] = df[column].fillna(df[column].mode()[0])

    # Clean date column
    df['Date dd/mm/yyyy'] = df['Date dd/mm/yyyy'].replace({
        '05/072018': '05/07/2018',
        '01/07/015': '01/07/2015',
        '22/01//2015': '22/01/2015'
    })

    # Extract date features
    df['Date dd/mm/yyyy'] = pd.to_datetime(df['Date dd/mm/yyyy'])
    df['Year'] = df['Date dd/mm/yyyy'].apply(lambda x: x.year)
    df['Month'] = df['Date dd/mm/yyyy'].apply(lambda x: x.month)
    df['Day'] = df['Date dd/mm/yyyy'].apply(lambda x: x.day)
    df = df.drop('Date dd/mm/yyyy', axis=1)
    df['Amount in USD'] = df['Amount in USD'].astype(np.float)

    # Split df into X and y
    y = df['Amount in USD']
    X = df.drop('Amount in USD', axis=1)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, shuffle=True, random_state=1)

    return X_train, X_test, y_train, y_test

df_final=pd.DataFrame(data)

def build_model():
    inputs = tf.keras.Input(shape=(532,))
    x = tf.keras.layers.Dense(128, activation='relu')(inputs)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    outputs = tf.keras.layers.Dense(1, activation='linear')(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    
    model.compile(
        optimizer='adam',
        loss='mse'
    )
    
    return model
def prediction1(ed):
    nominal_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('nominal', nominal_transformer, ['Industry Vertical', 'City  Location', 'InvestmentnType'])
    ], remainder='passthrough')

    regressor = tf.keras.wrappers.scikit_learn.KerasRegressor(build_model)

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('scaler', StandardScaler()),
        ('regressor', regressor)
    ])

    X_train, X_test, y_train, y_test = preprocess_inputs(df_final)

    model.fit(
        X_train,
        y_train,
        regressor__validation_split=0.2,
        regressor__batch_size=32,
        regressor__epochs=100,
        regressor__callbacks=[
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=3,
                restore_best_weights=True
            )
        ]
    )

    model.score(X_test, y_test)

    X_test

    model.predict(X_test)

    X_test

    X_test

    v = np.array(ed)

    X_test.shape

    v.shape

    g = pd.DataFrame(v)

    X_test.shape

    X_test[:1]
    model.predict(X_test[:1])
