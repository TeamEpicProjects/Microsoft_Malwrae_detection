import json
import pandas as pd
import numpy as np
import missingno as msno
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

df=pd.read_csv('Malware_Classification.csv')

plt.figure(figsize=(36,36))

new_df=df.drop("legitimate",axis=1)

#pearson correlation coeff
cor=new_df.corr()


def correlation(dataset,threshold):
    col_corr=set()
    corr_matrix=dataset.corr(method='spearman')
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if(abs(corr_matrix.iloc[i,j]>threshold)):
                col_name=corr_matrix.columns[i]
                col_corr.add(col_name)
    return col_corr

high_corr_features=correlation(new_df,0.7)

#print((high_corr_features))

high_corr_pearson=['SectionMaxVirtualsize', 'SectionMaxRawsize', 'SizeOfStackCommit', 'MinorImageVersion', 'SectionsMinVirtualsize', 'SizeOfHeapCommit', 'ResourcesMinSize', 'SectionsMinEntropy', 'NumberOfRvaAndSizes', 'ResourcesMaxEntropy', 'ImportsNbDLL', 'ResourcesMaxSize', 'SizeOfHeapReserve']
high_corr_spearman=['SectionsMinRawsize', 'ResourcesMaxEntropy', 'SectionsMinEntropy', 'SectionsMeanVirtualsize', 'SectionMaxVirtualsize', 'SectionAlignment', 'SizeOfHeapCommit', 'ImportsNb', 'MajorSubsystemVersion', 'BaseOfData', 'SectionsMeanRawsize', 'SizeOfImage', 'SectionMaxRawsize', 'MinorSubsystemVersion', 'AddressOfEntryPoint', 'ExportNb', 'ResourcesMaxSize', 'ResourcesMinSize']


#dropped the high correlated values.
new_df=new_df.drop(high_corr_spearman,axis=1)

del new_df['Unnamed: 57']

def covariance(dataset,threshold):
    col_cov=set()
    cov_matrix=dataset.cov()
    for i in range(len(cov_matrix.columns)):
        for j in range(i):
            if(abs(cov_matrix.iloc[i,j]>threshold)):
                col_name=cov_matrix.columns[i]
                col_cov.add(col_name)
    return col_cov


high_cov_val=covariance(new_df,6.888356e+15)

new_df=new_df.drop(high_cov_val,axis=1)

#label_encoding

new_df.Machine=new_df.Machine.apply(lambda x:str(x))

new_df=new_df[~(new_df.Machine==512)&~(new_df.Machine=='450')&
              ~(new_df.Machine=='43620')&~(new_df.Machine=='452')&
              ~(new_df.Machine=='422')&~(new_df.Machine=='3ab1aa9785d0681434766bb0ffc4a13c')&
              ~(new_df.Machine=='512')]


#removing the values with low count from the column
new_df=new_df[(new_df.SizeOfOptionalHeader==224)|(new_df.SizeOfOptionalHeader==240)]




lbl_encode=LabelEncoder()



new_df['Machine_label_encode']=lbl_encode.fit_transform(new_df.Machine)

new_df['SizeOfOptionalHeader_label']=lbl_encode.fit_transform(new_df.SizeOfOptionalHeader)

#one_hot_encoding

add_columns=pd.get_dummies(new_df.Machine)


new_df.drop(['Machine'],axis=1,inplace=True)

new_df=new_df.join(add_columns)


add_columns_n=pd.get_dummies(new_df.SizeOfOptionalHeader)

new_df.drop(['SizeOfOptionalHeader'],axis=1,inplace=True)

new_df=new_df.join(add_columns_n)


del df['Unnamed: 57']

#imputation based on class label

leg_values=df['legitimate'].values



legitimate_1=df[df.legitimate==1]
legitimate_0=df[df.legitimate==0]


mean_leg_1=legitimate_1.MajorLinkerVersion.mean()
mean_leg_0=legitimate_0.MajorLinkerVersion.mean()

for i in leg_values:
    if i==1:
        df['MajorLinkerVersion']=df['MajorLinkerVersion'].fillna(mean_leg_1)
    else:
        df['MajorLinkerVersion']=df['MajorLinkerVersion'].fillna(mean_leg_0)




mask=df.isna()
total=mask.sum()
percent=100*mask.mean()
missing_data=pd.concat([total,percent],axis=1,join='outer',keys=['count missing','percentage_missing'])
missing_data.sort_values(by='percentage_missing',ascending=False,inplace=True)

print(missing_data)