# load saved model
import pickle

with open('rfc_model_pkl' , 'rb') as f:
   rfc_pretrained = pickle.load(f)

import pandas as pd
import ipaddress
from sklearn.model_selection import train_test_split

# Create a DataFrame
df = pd.read_csv('rba-dataset-feature.csv')

# Encode IP addresses as integers
df['ip_address_encoded'] = df['ip_address'].apply(lambda x: int(ipaddress.IPv4Address(x)))

# Perform one-hot encoding for categorical features
df = pd.get_dummies(df, columns=['country', 'os_detail'], prefix=['country', 'os'])

# Separate the features (X) and the target (y)
X = df.drop(columns=['is_login_success', 'ip_address'])
#X = df_encoded.drop(columns=['is_login_success'])

y = df['is_login_success']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=42)
Z = pd.concat([X_test, y_test], axis=1)

test_data = Z.drop(['is_login_success'], axis=1)
test_data2 = test_data.tail(3).to_csv('test_data2.csv', index=False)
#print(test_data.tail(3))
#print(rfc_pretrained.predict(test_data.tail(3)))