# Import the necessary libraries.
import pickle

import pandas as pd 
import numpy as np 

import sklearn 
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from xgboost import XGBClassifier


from sklearn import preprocessing
import sklearn.model_selection as ms
import sklearn.metrics as sklm
from sklearn.model_selection import train_test_split


# Create a machine learning model.
# Create a machine learning model.
class rentalPrediction:
    def __init__(self, features): 
        self.features = features

    def predict(features):
        # Read the dataset
        data = pd.read_csv('./model/updated.csv')
        print(data.head())

        from sklearn.preprocessing import LabelEncoder
        LabelEncoding= LabelEncoder()
        for col in data.select_dtypes(include=['object']).columns:
            data[col]= LabelEncoding.fit_transform(data[col])

        # Import sklearn modules required for encoding categorical variable, and splitting train and test data
        from sklearn import preprocessing
        import sklearn.model_selection as ms
        import sklearn.metrics as sklm
        from sklearn.model_selection import train_test_split

        x = data.values[:,0:20]
        x

        y = data.values[:,-1]
        y

        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler

        Feature_Scaling = StandardScaler()

        x_scaled = Feature_Scaling.fit_transform(x)
        x_scaled

        x_train,x_test,y_train,y_test=train_test_split (x_scaled,y,test_size=0.2,random_state=32)

        model = tf.keras.models.Sequential()## create a model 
        model.add(tf.keras.layers.Dense(8,input_dim=20,activation='relu'))## create a hidden layer with 50 neurons with 11 features
        model.add(tf.keras.layers.Dense(8,activation='relu'))
        model.add(tf.keras.layers.Dense(8,activation='relu'))
        model.add(tf.keras.layers.Dense(1,activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        checkpoint = tf.keras.callbacks.ModelCheckpoint("Policy rooms Predictor.h5", 
                                                monitor='val_acc', 
                                                verbose=1, 
                                                save_best_only=True, 
                                                save_weights_only=False,
                                                mode='auto',
                                                save_freq=1)
        
        tensorboard = tf.keras.callbacks.TensorBoard(log_dir='tb_logs', 
                                             histogram_freq=1,
                                             write_graph=True, 
                                             write_images=True)
        
        history=model.fit(x_train,y_train,
                  epochs=8,
                  batch_size=5,
                  verbose=1,
                  validation_split=0.1)
        
        model.evaluate(x_train,y_train)
        predictions = model.predict(x_test)
        p = np.argmax(predictions, axis=1)
        p

        from sklearn import metrics
        from sklearn.metrics import classification_report
        print(classification_report(y_test,p))
        print("Accuracy:",metrics.accuracy_score(y_test, p))

        from sklearn.ensemble import  RandomForestRegressor
        from sklearn.ensemble import  BaggingRegressor 
        from sklearn.ensemble import  AdaBoostRegressor
        from sklearn.ensemble import  GradientBoostingRegressor

        RFRModel = RandomForestRegressor(max_leaf_nodes=20, random_state=1)
        RFRModel.fit(x_train, y_train)
        RandomForestRegressor(max_leaf_nodes=20, random_state=1)
        RFRModel_predicted = RFRModel.predict(x_test)
        RFRModel_score = RFRModel.score(x_test, y_test)
        RFRModel_score

        # Creating Model
        BGR_model = BaggingRegressor()

        # Model Fitting
        BGR_model.fit(x_train, y_train)

        # Model Prediction
        BGR_model_predicted = BGR_model.predict(x_test)

        # Model Score
        BGR_model_score = BGR_model.score(x_test, y_test)

        # find Mean Absolute Error
        mae = mean_absolute_error(y_test, BGR_model_predicted)        


features =  ['Zengeza 4' ,1, 'type_of_property', 'price', 'rooms', 'bedroom','toilets', 'ensuite',
                 'toilets_type', 'garage', 'swimming_pool', 'fixtures_fittings', 'cottage', 'power', 'power_backup',
                   'water', 'water_backup', 'gated_community', 'garden_area']   

rent = rentalPrediction.predict(features)