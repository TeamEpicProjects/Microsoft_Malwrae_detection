import numpy as np
import pandas as pd
import missingno as msno
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

df=pd.read_csv('Malware_Classification.csv')
del df['md5']
del df['Unnamed: 57']
df=df[~(df.Machine=='3ab1aa9785d0681434766bb0ffc4a13c')]

X=df.drop('legitimate',axis=1)
Y=df.legitimate



scale=StandardScaler()
logreg=LogisticRegression()

impute=SimpleImputer()

ct=make_column_transformer((impute,['MajorLinkerVersion']),
                           (scale,X.columns),remainder='passthrough')



pipe=make_pipeline(ct,logreg)
pipe.fit(X,Y)
df=pipe.fit_transform(df)
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3)
Y_pred=pipe.predict(X_test)

print(classification_report(Y_pred,Y_test))