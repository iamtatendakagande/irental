# Import the necessary libraries.
import pickle
import pandas as pd 
from sklearn.preprocessing import LabelEncoder


# Read the dataset
data = pd.read_csv('./machine/melbourne/melbourne.csv')

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

# Encoding ...
LabelEncoding = LabelEncoder()
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

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import  RandomForestRegressor
from sklearn.ensemble import  BaggingRegressor 
from sklearn.ensemble import  AdaBoostRegressor
from sklearn.ensemble import  GradientBoostingRegressor
from xgboost import XGBRegressor

from sklearn.metrics import mean_absolute_error


train_X, test_X, train_Y, test_Y = train_test_split(X, Y, random_state = 0)
print("Total size: ", data.shape[0])
print("Train size: ", train_X.shape, train_Y.shape)
print("Test size: ", test_X.shape, test_Y.shape)

xgbr_model = XGBRegressor() # {'objective': 'reg:squarederror' }

params = {
    'n_estimators': [110, 120, 130, 140], 
    'learning_rate': [ 0.05, 0.075, 0.1],
    'max_depth': [ 7, 9],
    'reg_lambda': [0.3, 0.5]
}

model = GridSearchCV(estimator=xgbr_model, param_grid=params, cv=5, n_jobs=-1)

model.fit(train_X, train_Y)

model_score = model.best_score_

model_pred = model.predict(test_X)

mae = mean_absolute_error(test_Y, model_pred)

print("Best score: %0.3f" % model.best_score_)
print("Best parameters set:", model.best_params_)

print("mean_absolute_error :", mae)


#Pickel Model
with open("./machine/melbourne/MelborneRentPredictionModel.pkl", "wb") as f:
    pickle.dump(model, f)

# Model Score
ADB_model_score = model.score(test_X, test_Y)
print('prediction_score', ADB_model_score)