# Import the necessary libraries.
import pickle
import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt
from sklearn.metrics import mean_absolute_error

# Create a machine learning model.
class predict:  
    def __init__(self, features): 
        self.features = features
        print(self.features)

    def userInput(features):
        try:
            input = pd.DataFrame(features, ['suburb', 'density', 'type_of_property', 'rooms', 'bedroom', 
                                    'toilets', 'toilets_type', 'ensuite', 'local_authority', 'constituency', 'garage', 'swimming_pool',
                                    'fixtures_fittings', 'cottage', 'power', 'power_backup', 'water',
                                    'water_backup', 'gated_community', 'garden_area']).T

            print(input)          
            print(input.shape)
            preprocessed_input = predict.preprocess_text(input)
            # load the model from disk
            model = pickle.load(open("./machine/harare/HarareRentPredictionModel.pkl", 'rb'))


            print("Processed text:",preprocessed_input)
            print("Processed text values:",preprocessed_input.values)
            # Model Prediction
            model_predicted = model.predict(preprocessed_input.values)

            print('model_name',model.__class__.__name__)
            print('prediction is', model_predicted)
            
            
            print("Prediction is on index number is {}".format(np.argmax(model_predicted)))
            predIndex = np.argmax(model_predicted)
            for option in enumerate(model_predicted):
                print(f"prediction number: {option[0]},amount {option[1]:.6f}")
                if option[0] == predIndex:
                    output = option[1]
                    print(f"The final prediction is on : {option[0]},and the amount is : {option[1]:.6f}")
                    return output     
        except Exception as e:
                print("An error occurred:", e)
    
    def preprocess_text(input):
        data = pd.read_csv('./machine/harare/updated.csv', keep_default_na=False)

        # Option 1: Create a new DataFrame without the column
        data = data.drop('price', axis=1)

        input['rooms'] = input['rooms'].astype(int)
        data['rooms'] = data['price'].astype(int)

        input['bedroom'] = input['bedroom'].astype(int)
        data['bedroom'] = data['bedroom'].astype(int)

        input['garage'] = input['garage'].astype(int)
        data['garage'] = data['garage'].astype(int)

        input['cottage'] = input['cottage'].astype(int)
        data['cottage'] = data['cottage'].astype(int)

        data = pd.concat([data, input], ignore_index=True)  # Combine and reset index
        print(data.tail())

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