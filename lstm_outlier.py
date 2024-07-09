import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt
import tensorflow as tf
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import seaborn as sns

def find_outlier(data, sequence_length=10, load=False, epochs=50, data_target=str, data_time=str, data_val=str):
    data = pd.get_dummies(data, columns=[data_target])

    timestamps = data[data_time]  # 나중에 시각화를 위해 저장
    data = data.drop(columns=[data_time])

    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    X = create_sequences(data_scaled, sequence_length)
    
    if load==True:
        model = tf.keras.models.load_model("./model/lstm_outlier.keras")
    else:
        model = Sequential()
        model.add(LSTM(64, input_shape=(sequence_length, data_scaled.shape[1]), return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(32, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(data_scaled.shape[1]))

        model.compile(optimizer='adam', loss='mse')
        model.fit(X, X[:, -1, :], epochs=epochs, batch_size=32, validation_split=0.2)
        
        model.save('./model/lstm_outlier.keras')
        
    # err calc
    X_pred = model.predict(X)
    reconstruction_error = np.mean(np.square(X[:, -1, :] - X_pred), axis=1)
    
    # 임계값 설정 및 이상 탐지 - 5%
    threshold = np.percentile(reconstruction_error, 95)
    outlier = reconstruction_error > threshold

    # 이상 데이터 출력
    anomaly_data = data.iloc[sequence_length:][outlier]
    anomaly_data = pd.DataFrame(anomaly_data)
    test_data = anomaly_data.tail(100).transpose()
    df = pd.DataFrame(test_data[1:])
    styled_df = df.style.applymap(colorize)
    st.title('Device Status Table')
    st.table(styled_df)
    
    
def colorize(val):
    color = 'red' if val else 'green'
    return f'background-color: {color}'

def create_sequences(data, sequence_length):
    sequences = []
    for i in range(len(data) - sequence_length):
        sequences.append(data[i:i + sequence_length])
    return np.array(sequences)


def boolstr_to_floatstr(v):
    if v == 'True':
        return '1'
    elif v == 'False':
        return '0'
    else:
        return v