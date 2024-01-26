# Import the necessary libraries.
import pickle
import pandas as pd 
import numpy as np 
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer  # For numerical representation

# Create a machine learning model.
class rentalPrediction:
    def __init__(self, features): 
        self.features = features
        print(self.features)

    def userInput(features):
        try:
            input = pd.DataFrame(features, ['suburb', 'density', 'type_of_property', 'rooms', 'bedroom', 'toilets', 'ensuite', 'toilets_type',
                                    'local_authority', 'ward', 'garage', 'swimming_pool',
                                    'fixtures_fittings', 'cottage', 'power', 'power_backup', 'water',
                                    'water_backup', 'gated_community', 'garden_area']).T

            print(input)          
            print(input.shape)
            preprocessed_input = rentalPrediction.preprocess_text(input)
            price = rentalPrediction.predict(preprocessed_input)
            return price
        except Exception as e:
                print("An error occurred:", e)

    def preprocess_text(input):
        LabelEncoding = LabelEncoder()
        for col in input.select_dtypes(include=['object']).columns:
            input[col]= LabelEncoding.fit_transform(input[col])
        preprocessed_text = input
        print(preprocessed_text)
        return preprocessed_text
     
    def predict(preprocessed_input):
        # Read the dataset
        data = pd.read_csv('./machine/updated.csv')
        
        print(data.head())
        print(data.tail())
        print(data.shape)

        data.info()
        data.describe()
        data.price.describe([.2, .4, .6, .8])

        numeric_features = data.select_dtypes(['int', 'float']).columns
        numeric_features , len(numeric_features)

        categorical_features = data.select_dtypes('object').columns
        categorical_features, len(categorical_features)

        print("Number of `Numerical` Features are:", len(numeric_features))
        print("Number of `Categorical` Features are:", len(categorical_features))

        data.isna().sum().sort_values(ascending=False)
        (data.isna().sum() * 100 / data.isna().count()).sort_values(ascending=False)
        # Now, is there any missing values are there?
        data.isna().any()

        print("Total Records :", len(data))
        for col in categorical_features:
            print("Total Unique Records of "+ col + " =",  len(data[col].unique()))

        corr_ = data[numeric_features].corr()
        corr_

        # Encoding ...
        LabelEncoding= LabelEncoder()
        for col in data.select_dtypes(include=['object']).columns:
            data[col]= LabelEncoding.fit_transform(data[col])

        training_features = list(numeric_features) + list(categorical_features)

        # Remove 'Price' Feature from list
        training_features.remove('price')

        # show the final list
        print(training_features)

        from sklearn.preprocessing import MinMaxScaler

        # Let's Normalize the data for training and testing
        minMaxNorm = MinMaxScaler()
        minMaxNorm.fit(data[training_features])

        #Create `X` data and assignning from `training feature` columns from `data` and make it normalized
        X = minMaxNorm.transform(data[training_features]) 

        Y = data['price']  
        Y
        test_X = preprocessed_input
        print(test_X)

        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import  AdaBoostRegressor
        from sklearn.metrics import mean_absolute_error

        train_X, test_X, train_Y, test_Y = train_test_split(X, Y, random_state = 0)
        print("Total size: ", data.shape[0])
        print("Train size: ", train_X.shape, train_Y.shape)
        print("Test size: ", test_X.shape, test_Y.shape)

        print("User input size: ", preprocessed_input.shape)
        # Creating Model
        ADB_model = AdaBoostRegressor()
        # Model Fitting
        ADB_model.fit(train_X, train_Y)
        # Model Score
        ADB_model_score = ADB_model.score(test_X, test_Y)

        # Model Prediction
        ADB_model_predicted = ADB_model.predict(test_X)
        #ADB_model_predicted = ADB_model.predict(preprocessed_input)


        # find Mean Absolute Error
        mae = mean_absolute_error(test_Y, ADB_model_predicted)

        print('model_name',ADB_model.__class__.__name__)
        print('prediction_score', ADB_model_score)
        print('mean_absolute_error', mae)

        print('prediction is', ADB_model_predicted)
        return ADB_model_predicted