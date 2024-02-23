# Import the necessary libraries.
import pickle
import pandas as pd 
from sklearn.preprocessing import LabelEncoder


# Read the dataset
data = pd.read_csv('../dataset/property.csv')
data = data[['suburb','density','price','rooms','constituency','local_authority']]

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
LabelEncoding = LabelEncoder()
for col in data.select_dtypes(include=['object']).columns:
    data[col]= LabelEncoding.fit_transform(data[col])

training_features = list(numeric_features) + list(categorical_features)

# Remove 'Price' Feature from list
training_features = ['price','suburb','local_authority','constituency','density']
# show the final list
print(training_features)

from sklearn.preprocessing import MinMaxScaler

# Let's Normalize the data for training and testing
minMaxNorm = MinMaxScaler()
minMaxNorm.fit(data[training_features])

#Create `X` data and assignning from `training feature` columns from `data` and make it normalized
X = minMaxNorm.transform(data[training_features]) 

#output = ['type_of_property','rooms','bedroom','toilets','fixtures_fittings','power','water']
Y = data['rooms']  
Y

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from xgboost import XGBRegressor

train_X, test_X, train_Y, test_Y = train_test_split(X, Y, random_state = 0)
print("Total size: ", data.shape[0])
print("Train size: ", train_X.shape, train_Y.shape)
print("Test size: ", test_X.shape, test_Y.shape)

XGBR_model = XGBRegressor()
XGBR_model.fit(train_X, train_Y)

#Pickel Model
with open("./machine/harare/HararePropertyPredictionModel.pkl", "wb") as f:
    pickle.dump(XGBR_model, f)

XGBR_model_score = XGBR_model.score(test_X, test_Y)

print('model_name',XGBR_model.__class__.__name__)
print("Best score: ", XGBR_model_score)