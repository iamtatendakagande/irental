# Import the necessary libraries.
import pickle
import pandas as pd 
from sklearn.preprocessing import LabelEncoder

# Read the dataset
data = pd.read_csv('./machine/data/harare-metropolian-updated.csv')

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
training_features.remove('price')

# show the final list
print(training_features)

from sklearn.preprocessing import MinMaxScaler
# Let's Normalize the data for training and testing
minMaxNorm = MinMaxScaler()
minMaxNorm.fit(data[training_features])
#Create `X` data and assignning from `training feature` columns from `data` and make it normalized
scaled = minMaxNorm.transform(data[training_features]) 
Y = data['price']  
Y
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Create PCA object
pca = PCA()

# Fit PCA to the scaled features
pca.fit(scaled)


# Transform the data using the fitted PCA model
X = pca.transform(data[training_features])
X

from sklearn.model_selection import train_test_split
from sklearn.ensemble import  GradientBoostingRegressor

train_X, test_X, train_Y, test_Y = train_test_split(X, Y, random_state = 0)
print("Total size: ", data.shape[0])
print("Train size: ", train_X.shape, train_Y.shape)
print("Test size: ", test_X.shape, test_Y.shape)


scaler = MinMaxScaler()
# fit and transfrom
X_train = scaler.fit_transform(train_X)
X_test = scaler.transform(test_X)

# Creating Model
model = GradientBoostingRegressor(n_estimators=150, random_state=1)
# Model Fitting
model.fit(train_X, train_Y)

#Pickel Model
with open("./machine/pickled/HarareRentPredictionModel.pkl", "wb") as f:
    pickle.dump(model, f)

# save the scaler
with open("./machine/pickled/HarareRentPredictionModelScaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

model_predicted = model.predict(test_X)
model_score = model.score(test_X, test_Y)
# Model Score
GBR_model_score = model.score(test_X, test_Y)
print('prediction_score', GBR_model_score)
print('model_name', model.__class__.__name__)
model_score = model.score(test_X, test_Y)
print('prediction_score', model_score)

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

mae = mean_absolute_error(test_Y, model_predicted)
print('mean_absolute_error', mae)

mse = mean_squared_error(test_Y, model_predicted)
print("Mean Squared Error:", mse)