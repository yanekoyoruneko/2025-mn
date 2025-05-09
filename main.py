import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#FILENAME = 'wig20_d.csv'
FILENAME = 'acp_d.csv'
S_TIME = 1000
TIME = 1001

print(FILENAME)

def load_data(filepath):
    data = pd.read_csv(filepath)
    data['Data'] = pd.to_datetime(data['Data'])
    data.set_index('Data', inplace=True)
    # data = data.loc["2023-09-01":"2024-04-01"]
    data = data[::-1]  # reverse so the most recent is at index 0
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

def crossings(macd, signal):
    diff = macd[:len(signal)] - signal
    crossing_indices = np.where(np.diff(np.sign(diff)))[0] # change of sign

    bearish_crossings = []  # MACD crosses Signal Line from top to bottom
    bullish_crossings = []  # MACD crosses Signal Line from bottom to top
    combined = []

    for idx in crossing_indices:
        if diff[idx] > 0 and diff[idx + 1] < 0:  # Top to bottom
            bearish_crossings.append(idx)
            combined.append((idx, "TOP"))
        elif diff[idx] < 0 and diff[idx + 1] > 0:  # Bottom to top
            bullish_crossings.append(idx)
            combined.append((idx, "BOT"))
    return bullish_crossings, bearish_crossings, combined


def plot(data, macd, signal):
    plt.figure(figsize=(16, 8))

    # Subplot 1: Closing Price
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data, label="Closing Price", color='blue')
    plt.ylabel('Stock Value')
    plt.title(FILENAME)
    plt.legend()

    # Subplot 2: MACD and Signal Line
    plt.subplot(2, 1, 2)
    plt.plot(data.index[:len(macd)], macd, label="MACD", color='green')
    plt.plot(data.index[:len(signal)], signal, label="Signal Line", color='red')

    # Find crossing points
    bearish_crossings, bullish_crossings, combined = crossings(macd, signal)

    # top to bottom
    bearish_dates = data.index[:len(signal)][bearish_crossings]
    bearish_values = macd[:len(signal)][bearish_crossings]
    plt.scatter(bearish_dates, bearish_values, color='red', marker='v', label="Bearish Cross", zorder=5)

    # bottom to top
    bullish_dates = data.index[:len(signal)][bullish_crossings]
    bullish_values = macd[:len(signal)][bullish_crossings]
    plt.scatter(bullish_dates, bullish_values, color='green', marker='^', label="Bullish Cross", zorder=5)
    plt.legend()

    # # Subplot 3: MACD Histogram
    # plt.subplot(3, 1, 3)
    # hist = np.concatenate((macd[:len(signal)] - signal, np.zeros(len(macd) - len(signal))))
    # print(hist)
    # plt.bar(data.index[:len(hist)], hist, label="MACD Histogram", color='purple', alpha=0.5)

    plt.xlabel('Date')
    plt.legend()
    plt.savefig(FILENAME + str(TIME) + "-macd.png")

    # Adjust layout
    plt.tight_layout()


# data = load_data(FILENAME)[:TIME]
data = load_data(FILENAME)[:1000]
closing = data['Zamkniecie']
macd, signal = calc_macd_signal(closing.to_numpy())
bearish_crossings, bullish_crossings, combined = crossings(macd, signal)

def simulate(closing, date, capital=1000):
    money = 0
    portfolio_value = [capital * closing.iloc[-1]]  # Start with initial capital
    capital_value = [capital]
    p_timestamps = [date[-1]]  # Start with the first timestamp
    c_timestamps = [date[-1]]  # Start with the first timestamp

    print("TYPE", "DATE", "CAPITAL", "MONEY", "CLOSING", "TOTAL", sep='\t')
    print("START", date[-1], capital, portfolio_value[0], closing.iloc[-1], sep='\t')

    for crossing in reversed(combined):
        idx, direction = crossing
        if direction == "TOP" and money > 0:
            capital = money / closing.iloc[idx]
            money = 0
            total_value = money if money > 0 else capital * closing.iloc[idx]
            capital_value.append(capital)
            c_timestamps.append(date[idx])
            # portfolio_value.append(total_value)
            # timestamps.append(date[idx])
            print("BUY", date[idx], total_value, sep='\t\t')
        elif direction == "BOT" and capital > 0:
            money = capital * closing.iloc[idx]
            capital = 0
            total_value = money if money > 0 else capital * closing.iloc[idx]
            portfolio_value.append(total_value)
            p_timestamps.append(date[idx])
            print("SELL", date[idx], total_value, (total_value / portfolio_value[-2])*100, sep='\t\t')

    # Plot the portfolio value over time
    plt.figure(figsize=(10, 5))
    plt.title("Portfolio Value Over Time")
    plt.plot(p_timestamps, portfolio_value, label="Total Capital", marker="o", linestyle="-")
    plt.xlabel("Date")
    plt.ylabel("Total Capital")
    plt.legend()
    plt.grid()
    # for i, value in enumerate(portfolio_value):
    #     plt.annotate(f'{value:.2f}',
    #                  (timestamps[i], portfolio_value[i]),
    #                  textcoords="offset points",
    #                  xytext=(0, 10),
    #                  ha='center', fontsize=8, color='green')
    plt.savefig(FILENAME + str(TIME) + "-capital.png")
    plt.show()

plot(closing, macd, signal)
simulate(closing, data.index)
