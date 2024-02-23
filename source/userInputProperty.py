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
            columns = ['suburb','density','price','constituency','local_authority']
            model_predicted = model.predict(preprocessed_input[columns])[0]

            print('model_name',model.__class__.__name__)
            print('prediction is', model_predicted)

            output = model_predicted
            return output     
                
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
        for col in data.select_dtypes(include=['object']).columns:
            data[col]= LabelEncoder.fit_transform(data[col])
        
        preprocessed_text = data.tail(1)
        print(preprocessed_text)
        print("User input size: ", preprocessed_text.shape)
        return preprocessed_text