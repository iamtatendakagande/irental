# Import the necessary libraries.
import pickle
from tensorflow.keras.models import load_model 
import pandas as pd

# Create a machine learning model.
class predict:  
    def _init_(self, features): 
        self.features = features
        print(self.features)

    def userInput(input):
        try:
            preprocessed_input = predict.preprocess_text(input)
            model = load_model("./machine/pickled/HarareRentNeuralNetworkModel.keras")
            print("Processed text:",preprocessed_input)
            output = model.predict(preprocessed_input)[0,0]
            return output     
        except Exception as e:
                print("An error occurred:", e)
    
    def preprocess_text(input):
        data = pd.read_csv('./machine/data/harare-metropolian-updated.csv', keep_default_na=False)
        data = data.astype({'rooms': 'int','bedroom': 'int', 'toilets':'int', 'ensuite':'int', 'carport':'int', 'cottage':'int'})
        input = input.astype({'rooms': 'int','bedroom': 'int', 'toilets':'int', 'ensuite':'int', 'carport':'int', 'cottage':'int'})

        data = pd.concat([data, input], ignore_index=True)  # Combine and reset index
        
        print(data.info())
        print(data.tail(1).T)

        categorical_features = data.select_dtypes('object').columns
        print(categorical_features)

        data = data.astype(str)

        # Encoding ...
        from sklearn import preprocessing
        LabelEncoder = preprocessing.LabelEncoder()
        for col in data[categorical_features]:
            data[col]= LabelEncoder.fit_transform(data[col])

        preprocessed_text = data.tail(1)
        #print(preprocessed_text)

        # features of new house
        single_house = preprocessed_text.drop('price',axis=1).iloc[0]
        print(f'Features of new house:\n{single_house}')

        # load the scaler from disk
        scaler  = pickle.load(open("./machine/pickled/HarareRentNeuralNetworkModelScaler.pkl", 'rb'))
        # reshape the numpy array and scale the features
        single_house = scaler.transform(single_house.values.reshape(-1, 20))
        print("User input size: ", single_house.shape)
        return single_house