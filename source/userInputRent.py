# Import the necessary libraries.
import pickle
import pandas as pd

# Create a machine learning model.
class predict:  
    def _init_(self, features): 
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
            model = pickle.load(open("./machine/harare/HarareNeuralNetworkModel.pkl", 'rb'))

            print("Processed text:",preprocessed_input)
            print("Processed text values:",preprocessed_input.values)
            
            # features of new house
            single_house = preprocessed_input
            print(f'Features of new house:\n{single_house}')

            # run the model and get the price prediction
            print('\nPrediction Price:',model.predict(single_house)[0,0])
            output = model.predict(single_house)[0,0]
            return output     
        except Exception as e:
                print("An error occurred:", e)
    
    def preprocess_text(input):
        data = pd.read_csv('./machine/dataset/updated.csv', keep_default_na=False)
        data = data.drop('price', axis=1)
        data = data.astype(str)

        data = data.astype({'rooms': 'int','bedroom': 'int', 'toilets':'int', 'ensuite':'int', 'garage':'int', 'cottage':'int'})
        input = input.astype({'rooms': 'int','bedroom': 'int', 'toilets':'int', 'ensuite':'int', 'garage':'int', 'cottage':'int'})

        data = pd.concat([data, input], ignore_index=True)  # Combine and reset index
        
        print(data.info())
        print(data.tail())
        print(data.sample(20))

        categorical_features = data.select_dtypes('object').columns
        print(categorical_features)

        print( data[categorical_features])

        # Encoding ...
        from sklearn import preprocessing
        LabelEncoder = preprocessing.LabelEncoder()
        for col in data[categorical_features]:
            data[col]= LabelEncoder.fit_transform(data[col])

        preprocessed_text = data.tail(1)
        print(preprocessed_text)
        print("User input size: ", preprocessed_text.shape)
        return preprocessed_text