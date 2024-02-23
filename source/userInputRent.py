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
            input = pd.DataFrame({'suburb': features[0], 'density': features[1], 'type_of_property': features[2], 'rooms': features[3], 'bedroom': features[4], 
                                    'toilets': features[5], 'toilets_type': features[6], 'ensuite': features[7], 'local_authority': features[8], 'constituency': features[9], 'garage': features[10], 'swimming_pool': features[11],
                                    'fixtures_fittings': features[12], 'cottage': features[13], 'power': features[14], 'power_backup': features[15], 'water': features[16],
                                    'water_backup': features[17], 'gated_community': features[18], 'garden_area': features[19]}, index=[0])
            #input.to_csv('./machine/dataset/output.csv', index=False)
    
            print(input)          
            print(input.shape)
            preprocessed_input = predict.preprocess_text(input)
            # load the model from disk
            model = pickle.load(open("./machine/harare/HarareNeuralNetworkModel.pkl", 'rb'))
            print("Processed text:",preprocessed_input)
            
            output = model.predict(preprocessed_input)[0,0]
            return output     
        except Exception as e:
                print("An error occurred:", e)
    
    def preprocess_text(input):
        data = pd.read_csv('./machine/dataset/updated.csv', keep_default_na=False)

        #input = pd.read_csv('./machine/dataset/output.csv', keep_default_na=False)
        #data = data.drop('price', axis=1)
        
        data = data.astype(str)

        data = data.astype({'rooms': 'int','bedroom': 'int', 'toilets':'int', 'ensuite':'int', 'garage':'int', 'cottage':'int'})
        input = input.astype({'rooms': 'int','bedroom': 'int', 'toilets':'int', 'ensuite':'int', 'garage':'int', 'cottage':'int'})

        data = pd.concat([data, input], ignore_index=True)  # Combine and reset index
        
        print(data.info())
        print(data.tail())
        print(data.sample(20))

        categorical_features = data.select_dtypes('object').columns
        print(categorical_features)

        # Encoding ...
        from sklearn import preprocessing
        LabelEncoder = preprocessing.LabelEncoder()
        for col in data[categorical_features]:
            data[col]= LabelEncoder.fit_transform(data[col])

        preprocessed_text = data.tail(1)
        print(preprocessed_text)

        # features of new house
        single_house = preprocessed_text.drop('price',axis=1).iloc[0]
        print(f'Features of new house:\n{single_house}')

        # load the scaler from disk
        scaler  = pickle.load(open("./machine/harare/HarareNeuralNetworkscaler.pkl", 'rb'))
        # reshape the numpy array and scale the features
        single_house = scaler.transform(single_house.values.reshape(-1, 20))
        print("User input size: ", single_house.shape)
        return single_house