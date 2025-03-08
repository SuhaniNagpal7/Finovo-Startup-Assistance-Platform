# -*- coding: utf-8 -*-
"""score_growth_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zzvicnxtdCUca-78DxcJ20JEvdWhJTTW
"""

import pandas as pd
from google.colab import files
file=files.upload()

file=pd.read_csv('best.csv')

file=file.dropna()

df=file
df['quantity_score']=df['quantity_score']/7
df['quality_score']=df['quality_score']/4
df['business_score']=df['business_score']/4

df[:1]

y=df['Growth Factor']

x=df.drop(['Growth Factor'],axis=1)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)

country_dummies=pd.get_dummies(df['country'])

x_final=pd.concat([x,country_dummies],axis=1)

x_final=x_final.drop('country',axis=1)

x_train,x_test,y_train,y_test=train_test_split(x_final,y,test_size=0.3)



from sklearn.linear_model import LogisticRegression
model=LogisticRegression()
model.fit(x_train,y_train)

model.score(x_test,y_test)

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score

def find_best_model_using_gridsearchcv(x_final,y):
    algos = {
        'linear_regression' : {
            'model': LinearRegression(),
            'params': {
                'fit_intercept': [True, False]
            }
        },
        'lasso': {
            'model': Lasso(),
            'params': {
                'alpha': [1,2],
                'selection': ['random', 'cyclic']
            }
        },
        'decision_tree': {
            'model': DecisionTreeRegressor(),
            'params': {
                'criterion' : ['mse','friedman_mse'],
                'splitter': ['best','random']
            }
        }
    }
    scores = []
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    for algo_name, config in algos.items():
        gs =  GridSearchCV(config['model'], config['params'], cv=cv, return_train_score=False)
        gs.fit(x_final,y)
        scores.append({
            'model': algo_name,
            'best_score': gs.best_score_,
            'best_params': gs.best_params_
        })

    return pd.DataFrame(scores,columns=['model','best_score','best_params'])


find_best_model_using_gridsearchcv(x_final,y)

from sklearn.ensemble import RandomForestClassifier
model1=RandomForestClassifier()
model1.fit(x_train,y_train)

model1.score(x_test,y_test)

import numpy as np
def predict_price(country,quantity_score,quality_score,business_score):    
    loc_index = np.where(x_final.columns==country)[0][0]

    m = np.zeros(len(x_final.columns))
    m[0] = quantity_score
    m[1] = quality_score
    m[2] = business_score
    if loc_index >= 0:
        m[loc_index] = 1

    return model.predict([m])[0]





