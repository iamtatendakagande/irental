# Import the necessary libraries.
import pickle
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt
from sklearn.metrics import mean_absolute_error

# Create a machine learning model.
class predicted:  
    def __init__(self, features): 
        self.features = features
        print(self.features)

    def userInputed(features):
        try:
            input = pd.DataFrame(features, ['suburb','density','price','constituency','local_authority']).T

            print(input)          
            print(input.shape)
            preprocessed_input = predicted.preprocessed_text(input)
            # load the model from disk
            model = pickle.load(open("./machine/harare/HararePropertyPredictionModel.pkl", 'rb'))


            print("Processed text:",preprocessed_input)
            print("Processed text values:",preprocessed_input.values)
            # Model Prediction
            model_predicted = model.predict(preprocessed_input)

            print('model_name',model.__class__.__name__)
            print('prediction is', model_predicted)
                       
        except Exception as e:
                print("An error occurred:", e)
    
    def preprocessed_text(input):
        data = pd.read_csv('./machine/harare/property.csv', keep_default_na=False)
        data = data.drop('rooms', axis=1)

        input['price'] = input['price'].astype(int)  # Convert to integer
        data['price'] = data['price'].astype(int)  # Convert to integer

        data = pd.concat([data, input], ignore_index=True)  # Combine and reset index
        
        print(data.tail())
        print(data.info())
        print(data.sample(20))

        # Encoding ...
        from sklearn import preprocessing
        LabelEncoder = preprocessing.LabelEncoder()

        # Identify categorical columns
        categorical_cols = data.select_dtypes(include=['object']).columns

        # Apply LabelEncoder to categorical columns only
        data[categorical_cols] = data[categorical_cols].apply(LabelEncoder.fit_transform)

        print(data)
        
        preprocessed_text = data.tail(1)
        print(preprocessed_text)
        print("User input size: ", preprocessed_text.shape)
        return preprocessed_text