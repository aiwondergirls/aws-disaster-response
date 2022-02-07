import pandas as pd
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder
import pickle 
from sklearn.preprocessing import MinMaxScaler

def predictAffected(df1):
    # load the model from disk
    bst = XGBRegressor()  # init model
    bst.load_model('./affected_model/models/finalxgboost2.model')  # load data     
    X_test = df1
    scaler = MinMaxScaler()
    X_test_scaled = scaler.fit_transform(X_test)
    pred = bst.predict(X_test_scaled)
    return pred
   
"""def predict():
    bst = XGBRegressor()  # init model
    bst.load_model('./affected_model/models/wids1.model')  # load data
    df_test = pd.read_csv('./affected_model/data/test.csv')
    X_test = df_test.drop('Year_Factor', axis=1)
    X_test = X_test.drop('id', axis=1)
        
    for col in ['year_built', 'energy_star_rating', 'direction_max_wind_speed', 'direction_peak_wind_speed', 'max_wind_speed', 'days_with_fog']:
        X_test[col] = X_test[col].fillna(df_test[col].median())

    # Encode categorial features
    labelencoder = LabelEncoder()
    X_test['State_Factor_Cat'] = labelencoder.fit_transform(X_test['State_Factor'])
    X_test['building_class_Cat'] = labelencoder.fit_transform(X_test['building_class'])
    X_test['facility_type_Cat'] = labelencoder.fit_transform(X_test['facility_type'])

    X_test = X_test.drop('State_Factor', axis=1)
    X_test = X_test.drop('building_class', axis=1)
    X_test = X_test.drop('facility_type', axis=1)
    pred = bst.predict(X_test)
    return pred"""

