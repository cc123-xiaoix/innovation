import pandas as pd 
import numpy as np
import csv as csv
import matplotlib
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge, RidgeCV, ElasticNet, LassoCV, LassoLarsCV
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler


#1)获取数据集
data_or = pd.read_csv("haodf.csv", header=0)           
df = pd.get_dummies(data_or.iloc[:,[0,1,2,3,5,6,7]])
data =  df.loc[df.iloc[:,1]> 0, :]
data=data.loc[data.iloc[:,6]> 0, :]
X_train=data[["total_visit","served_patient","good_reputation","bad_reputation","administrative_office","doctor"]]
y=data["per_patient_satisfaction"]
'''
print(data.head())
print(X_train.head())
print(y.head())
'''
#2)标准化
transfer=StandardScaler()
X_train=transfer.fit_transform(X_train)
X_train=pd.DataFrame(X_train,columns=[["total_visit","served_patient","good_reputation","bad_reputation","administrative_office","doctor"]])
'''print(X_train)'''

def rmse_cv(model):
    rmse= np.sqrt(-cross_val_score(model, X_train, y, scoring="neg_mean_squared_error", cv = 3))
    return(rmse)

#调用LassoCV函数，并进行交叉验证，默认cv=3
model_lasso = LassoCV(alphas = [0.1,1,0.001, 0.0005]).fit(X_train, y)

#模型所选择的最优正则化参数alpha
print("Optimal regularization parameter: "+str(model_lasso.alpha_))

#各特征列的参数值或者说权重参数，为0代表该特征被模型剔除了
print("weight: "+str(model_lasso.coef_))

#输出看模型最终选择了几个特征向量，剔除了几个特征向量
coef = pd.Series(model_lasso.coef_, index = X_train.columns)
print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other " +  str(sum(coef == 0)) + " variables")

#输出所选择的最优正则化参数情况下的残差平均值，因为是3折，所以看平均值
print("Mean of residual error: "+str(rmse_cv(model_lasso).mean()))


#画出特征变量的重要程度，这里面选出前3个重要，后3个不重要的举例
imp_coef = pd.concat([coef.sort_values().head(3),
                     coef.sort_values().tail(3)])

matplotlib.rcParams['figure.figsize'] = (8.0, 10.0)
imp_coef.plot(kind = "barh")
plt.title("Coefficients in the Lasso Model")
plt.show()

