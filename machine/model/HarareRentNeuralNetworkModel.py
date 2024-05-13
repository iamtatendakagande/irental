# Import the necessary libraries.
import pickle
# data analysis and wrangling
import pandas as pd
import numpy as np

# scaling and train test split
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# creating a model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# evaluation on test data
from sklearn.metrics import mean_squared_error,mean_absolute_error,explained_variance_score

# Read the dataset
data = pd.read_csv('./machine/data/harare-metropolian-updated.csv')
print(data.head())

from sklearn.preprocessing import LabelEncoder
LabelEncoding= LabelEncoder()
for col in data.select_dtypes(include=['object']).columns:
    data[col]= LabelEncoding.fit_transform(data[col])

# Features
X = data.drop('price',axis=1)

# Label
y = data['price']

# Split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=101)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

scaler = MinMaxScaler()

# fit and transfrom
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# everything has been scaled between 1 and 0
print('Max: ',X_train.max())
print('Min: ', X_train.min())    

model = Sequential()
# input layer
model.add(Dense(20,activation='relu'))
# hidden layers
model.add(Dense(20,activation='relu'))
model.add(Dense(15,activation='relu'))
model.add(Dense(10,activation='relu'))
model.add(Dense(5,activation='relu'))

# output layer
model.add(Dense(1))

model.compile(optimizer='adam',loss='mean_squared_error', metrics=['mae'])

#model training
model.fit(x=X_train, y=y_train.values,
          validation_data=(X_test,y_test.values),
          batch_size=64,epochs=400)
#Pickel Model
with open("./machine/data/HarareRentNeuralNetworkModel.pkl", "wb") as f:
    pickle.dump(model, f)

# save the scaler
with open("./machine/data/HarareRentNeuralNetworkModelScaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

# predictions on the test set
predictions = model.predict(X_test)

print('MAE: ',mean_absolute_error(y_test,predictions))
print('MSE: ',mean_squared_error(y_test,predictions))
print('RMSE: ',np.sqrt(mean_squared_error(y_test,predictions)))
print('Variance Regression Score: ',explained_variance_score(y_test,predictions))