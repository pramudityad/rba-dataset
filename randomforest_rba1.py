import pandas as pd
import ipaddress

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder

# Prepare the data
data = {
    'ip_address': ['192.168.0.1', '10.0.0.1', '172.16.0.1', '192.168.0.2', '10.0.0.2', '172.16.0.2', '192.168.0.3', '10.0.0.3', '172.16.0.3', '192.168.0.4'],
    'timestamp': ['2023-05-01 09:30:00', '2023-05-02 15:45:00', '2023-05-03 11:20:00', '2023-05-04 08:10:00', '2023-05-05 13:25:00', '2023-05-06 10:05:00', '2023-05-07 17:40:00', '2023-05-08 14:15:00', '2023-05-09 09:50:00', '2023-05-10 16:30:00'],
    'user_agent': ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                   'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                   'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
                   'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
                   ],
    'username': ['user1', '3452', 'user3', 'nano1231', 'user2', 'user3', 'asjdqwo', 'osfouweb', '18726891', 'user1'],
    'access_token': ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
                     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkRvZSBNYXJrIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjJ9._vWrkmT3Dn29zO5Wq5J9gWUEjV8_eycAbj-xGdpO3Fc',
                     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IldvbGZCb3giLCJpYXQiOjE1MTYyMzkwMjIsImV4cCI6MTUxNjIzOTAyMn0.0-1MqoQXCrkAB6S8cNExx0ULPOWgMi4rhvTXeJu3pSo',
                     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
                     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkRvZSBNYXJrIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjJ9._vWrkmT3Dn29zO5Wq5J9gWUEjV8_eycAbj-xGdpO3Fc',
                     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IldvbGZCb3giLCJpYXQiOjE1MTYyMzkwMjIsImV4cCI6MTUxNjIzOTAyMn0.0-1MqoQXCrkAB6S8cNExx0ULPOWgMi4rhvTXeJu3pSo',
                     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
                     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkRvZSBNYXJrIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjJ9._vWrkmT3Dn29zO5Wq5J9gWUEjV8_eycAbj-xGdpO3Fc',
                     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IldvbGZCb3giLCJpYXQiOjE1MTYyMzkwMjIsImV4cCI6MTUxNjIzOTAyMn0.0-1MqoQXCrkAB6S8cNExx0ULPOWgMi4rhvTXeJu3pSo',
                     'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
                   ],
    'login_successful': [True, False, True, True, True, False, False, True, False, True]
}

df = pd.DataFrame(data)

# Preprocess the data
def preprocess_data(df):
    df_encoded = encode_ip_addresses(df['ip_address'])
    df_encoded.columns = ['ip_' + str(col) for col in df_encoded.columns]
    df = pd.concat([df.drop(columns='ip_address'), df_encoded], axis=1)
    df = preprocess_user_agent(df, 'user_agent')
    df = preprocess_timestamp(df, 'timestamp')
    # df = preprocess_access_token(df, 'access_token')
    # Perform additional preprocessing steps if necessary
    return df

# Encode IP addresses using one-hot encoding
def encode_ip_addresses(ip_addresses):
    encoded_ips = []
    max_prefixlen = 0

    # Find the maximum prefix length among the IP addresses
    for ip in ip_addresses:
        ip_obj = ipaddress.ip_address(ip)
        max_prefixlen = max(max_prefixlen, ip_obj.max_prefixlen)

    # Perform one-hot encoding for each IP address
    for ip in ip_addresses:
        ip_obj = ipaddress.ip_address(ip)
        ip_binary = bin(int(ip_obj))[2:].zfill(max_prefixlen)
        encoded_ip = [int(bit) for bit in ip_binary]
        encoded_ips.append(encoded_ip)

    encoded_df = pd.DataFrame(encoded_ips)
    return encoded_df

def preprocess_access_token(df, access_token_column):
    # Extract relevant features from the access token
    df['token_length'] = df[access_token_column].apply(lambda x: len(x))
    # Add more relevant features based on the specific JWT structure or requirements

    # Drop the original access token column
    df.drop(columns=[access_token_column], inplace=True)

    return df


# Preprocess the user agent column
def preprocess_user_agent(df, user_agent_column):
    df['device_type'] = df[user_agent_column].apply(lambda x: x.split('(')[1].split(';')[0])
    df['operating_system'] = df[user_agent_column].apply(lambda x: x.split('(')[1].split(';')[1])
    df['browser'] = df[user_agent_column].apply(lambda x: x.split('(')[1].split(';')[2].split(')')[0] if len(x.split('(')) > 1 and len(x.split(';')) > 2 else '')
    df.drop(columns=[user_agent_column], inplace=True)
    return df

# Preprocess the timestamp column
def preprocess_timestamp(df, timestamp_column):
    df[timestamp_column] = pd.to_datetime(df[timestamp_column])
    df['hour'] = df[timestamp_column].dt.hour
    df['day_of_week'] = df[timestamp_column].dt.dayofweek
    df['month'] = df[timestamp_column].dt.month
    df.drop(columns=[timestamp_column], inplace=True)
    return df

# df = preprocess_data(df)

# Prepare the features and target
features = df.drop(columns='login_successful')
target = df['login_successful']

# One-hot encode the categorical features
features_encoded = pd.get_dummies(features)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features_encoded, target, test_size=0.7, random_state=42)

# Initialize and train the Random Forest classifier
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Evaluate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)
