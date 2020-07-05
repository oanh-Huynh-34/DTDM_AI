import requests
from pandas.io.json import json_normalize
import pandas as pd
from firebase import firebase
from scipy import stats
import matplotlib.pyplot as plt
import json 
import pandas as pd
import numpy as np
from sklearn import linear_model
clf = linear_model.LinearRegression()
firebase=firebase.FirebaseApplication('https://do-an-cuoi-ky-n9.firebaseio.com/')
resultJsonTime=firebase.get('/DHT11/Time',None)
resultJsonHumidity=firebase.get('/DHT11/Humidity',None)
resultJsonTemperature=firebase.get('/DHT11/Temperature',None)
times=[]
for key, value in resultJsonTime.items():
    times.append(float(value))
humidity=[]
for key, value in resultJsonHumidity.items():
    humidity.append(float(value))
temperature=[]
for key, value in resultJsonTemperature.items():
    temperature.append(float(value))

#Lấy 1000 record cuối cùng
new_temperature=temperature[-2200:]
new_times=times[-2200:]
new_humidity=humidity[-2200:]
#Lấy vị trí của nhiệt độ sau khoản thới gian 1800 s =30 phút
def findIndex(newTime):
    for j in range(len(new_times)-1):
        if newTime==new_times[j]:
            return j
        if int(new_times[i])<=newTime and int(new_times[j+1])>=newTime:
            if(int(new_times[j+1])-newTime<newTime-int(new_times[j])): #and int(new_times[j+1])-newTime<=3):
                return j+1
            else:
                return j
    return None
#Dãy nhiệt độ thực tế sau 1800 s =30 phút   
tempx=[]
for i in range(len(new_times)):
    newTime=int(new_times[i])+5400
    c=findIndex(newTime)
    if(c is not None):
        tempx.append(new_temperature[c])
print(len(temperature))
#Hồi qui tuyến tính 80% 
size_train=int(len(tempx)*0.8)
df = pd.DataFrame({'temperature':new_temperature[:size_train], 'humidity':new_humidity[:size_train],'next_temp':tempx[:size_train]})
print(df)
#Hoi Qui
except_quality = df.drop("next_temp", axis=1)
X = except_quality
 
# Sử dụng quality làm biến mục tiêu
Y = df['next_temp']
 
# Tạo model
clf.fit(X, Y)
 
# Hệ số hồi quy
print(pd.DataFrame({"Name":except_quality.columns,
                    "Coefficients":clf.coef_}).sort_values(by='Coefficients') )
 
# Sai số
print(clf.intercept_)
#print(df)
def f(x,y):
    return (-0.350735*float(x)+0.238915*float(y)+27.140632706338145)
re=[]
for i in range(size_train, len(tempx)):
    re.append(f(new_temperature[i],new_humidity[i]))
#arr1 là chỉ kết quả dự báo, arr2 chỉ kết quả nhiệt độ thực tế
arr1 = np.array(re)
arr2=np.array(new_temperature[size_train:])
plt.scatter(new_temperature[size_train:len(tempx)],tempx[size_train:])
plt.scatter(new_temperature[size_train:len(tempx)],re,color='red')