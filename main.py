import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_data(filepath):
    data = pd.read_csv(filepath)
    data['Data'] = pd.to_datetime(data['Data'])
    data = data[::-1]  # reverse so the most recent is at index 0
    data.set_index('Data', inplace=True)
    return data

def EMA(p, N):
    a =  2 / (N + 1)
    fac = (1 - a) ** np.arange(N)
    return np.sum(fac * p[:N]) / np.sum(fac)

def MACD(data):
    return EMA(data, 12) - EMA(data, 26)

def SIGNAL(data):
    return EMA(data, 9)

def apply_to_slices(arr, fun, l):
    return np.array([fun(arr[i:i+l]) for i in range(len(arr) - l)])

def calc_macd_signal(data):
    macd = apply_to_slices(data, MACD, 26)
    signal = apply_to_slices(macd, SIGNAL, 26)
    return macd, signal

# def crossings(macd, signal):
#     diff = macd[:len(signal)] - signal
#     crossing_indices = np.where(np.diff(np.sign(diff)))[0]
#     crossing_dates = data.index[:len(signal)][crossing_indices]
#     crossing_values = macd[:len(signal)][crossing_indices]
#     return crossing_dates, crossing_values

def plot(data, macd, signal):
    plt.figure(figsize=(16, 8))

    # Subplot 1: Closing Price
    plt.subplot(3, 1, 1)
    plt.plot(data.index, data, label="Closing Price", color='blue')
    plt.ylabel('Stock Value')
    plt.title("Accesco Poland")
    plt.legend()

    # Subplot 2: MACD and Signal Line
    plt.subplot(3, 1, 2)
    plt.plot(data.index[:len(macd)], macd, label="MACD", color='green')
    plt.plot(data.index[:len(signal)], signal, label="Signal Line", color='red')

    # Find crossing points
    diff = macd[:len(signal)] - signal
    crossing_indices = np.where(np.diff(np.sign(diff)))[0] # change of sign

    bearish_crossings = []  # MACD crosses Signal Line from top to bottom
    bullish_crossings = []  # MACD crosses Signal Line from bottom to top

    for idx in crossing_indices:
        if diff[idx] > 0 and diff[idx + 1] < 0:  # Top to bottom
            bearish_crossings.append(idx)
        elif diff[idx] < 0 and diff[idx + 1] > 0:  # Bottom to top
            bullish_crossings.append(idx)

    # top to bottom
    bearish_dates = data.index[:len(signal)][bearish_crossings]
    bearish_values = macd[:len(signal)][bearish_crossings]
    plt.scatter(bearish_dates, bearish_values, color='red', marker='v', label="Bearish Cross", zorder=5)

    # bottom to top
    bullish_dates = data.index[:len(signal)][bullish_crossings]
    bullish_values = macd[:len(signal)][bullish_crossings]
    plt.scatter(bullish_dates, bullish_values, color='green', marker='^', label="Bullish Cross", zorder=5)
    plt.legend()

    # Subplot 3: MACD Histogram
    plt.subplot(3, 1, 3)
    hist = np.concatenate((macd[:len(signal)] - signal, np.zeros(len(macd) - len(signal))))
    plt.bar(data.index[:len(hist)], hist, label="MACD Histogram", color='purple', alpha=0.5)

    plt.xlabel('Date')
    plt.legend()

    # Adjust layout
    plt.tight_layout()
    plt.show()



data = load_data('acp_d.csv')
closing = data['Zamkniecie'][:200]
macd, signal = calc_macd_signal(closing.to_numpy())

plot(closing, macd, signal)
plt.show()
