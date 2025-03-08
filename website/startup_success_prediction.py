import numpy as np
import pandas as pd


file=pd.read_csv('startup_fail_success.csv')

file.head()

y=file.Result

x=file.drop('Result',axis='columns')

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3,random_state=10)

from sklearn.linear_model import LogisticRegression
model=LogisticRegression()

dummies=pd.get_dummies(file['State'])

x=x.drop('State',axis='columns')

x=pd.concat([x,dummies],axis='columns')

x.head()

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)

model.fit(x_train,y_train)

model.score(x_test,y_test)

model.predict([[165350,146897,443898,2269,0,0,1]])
x.head()

def predict_output(State,RnD,Administration,Marketing,Profit):    
    loc_index = np.where(x.columns==State)[0][0]

    m = np.zeros(len(x.columns))
    m[0] = RnD
    m[1] = Marketing
    m[2] = Profit
    m[3]= Administration
    if loc_index >= 0:
        m[loc_index] = 1

    return model.predict([m])[0]

print(predict_output("Bangalore",142107,1391,36,187))

