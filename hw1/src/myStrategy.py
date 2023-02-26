def myStrategy(p_prices, c_price):
    import numpy as np
    import talib

    # action and prices, parameters
    action: int = 0  # 1 (buy), -1 (sell), 0 (hold)
    tp_1, tp_2 = 7, 11

    try:
        t_prices = np.append(p_prices, c_price)

        # technical analysis: RSI and K/D
        rsi_1 = talib.RSI(t_prices, timeperiod=tp_1)
        rsi_2 = talib.RSI(t_prices, timeperiod=tp_2)
    except:
        return action

    # length checker
    if ((len(rsi_1) < 2) or (len(rsi_2) < 2)):
        return action

    # buy / sell signal checker
    if ((rsi_1[-2] < rsi_2[-2]) and (rsi_1[-1] > rsi_2[-1])):
        # buy signal
        action = 1
    elif ((rsi_1[-2] > rsi_2[-2]) and (rsi_1[-1] < rsi_2[-1])):
        # sell signal
        action = -1
    return action


if __name__ == '__main__':
    import pandas as pd

    csv_file = '../0050.TW.csv'
    try:
        df = pd.read_csv(csv_file)
    except:
        exit(0)

    t_prices = df["Adj Close"].values
    t_length = len(t_prices)
    # t_length = 20

    for t in range(t_length):
        action = myStrategy(t_prices[0:t], t_prices[t])
        print(action)
