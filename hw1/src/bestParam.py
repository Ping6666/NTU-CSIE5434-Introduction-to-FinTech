import numpy as np
import pandas as pd
import talib


def my_strategy(p_prices, c_price, days):
    # action and prices, parameters
    action: int = 0  # 1 (buy), -1 (sell), 0 (hold)
    check_over: bool = True
    # days = 5

    try:
        t_prices = np.append(p_prices, c_price)

        # technical analysis: RSI and K/D
        rsi = talib.RSI(t_prices)
        k, d = talib.STOCHF(t_prices, t_prices, t_prices)
        rsi_k = (rsi * k) / 100
        rsi_d = (rsi * d) / 100
    except:
        return action

    # length checker
    if ((len(rsi_k) < days + 1) or (len(rsi_d) < days + 1)):
        return action

    # buy / sell signal checker
    rsi_k_min, rsi_k_max = 101, -1
    for i in range(days):
        if rsi_k_min > rsi_k[-i - 1]:
            rsi_k_min = rsi_k[-i - 1]
        if rsi_k_max < rsi_k[-i - 1]:
            rsi_k_max = rsi_k[-i - 1]

    if rsi_k_min > rsi_k[-1]:
        # sell signal
        action = -1
    elif rsi_k_max < rsi_k[-1]:
        # buy signal
        action = 1

    # if ((rsi_k[-2] < rsi_d[-2]) and (rsi_k[-1] > rsi_d[-1])):
    #     if ((not check_over) or (check_over and (oversold > rsi_d[-1]))):
    #         # buy signal
    #         action = 1
    # elif ((rsi_k[-2] > rsi_d[-2]) and (rsi_k[-1] < rsi_d[-1])):
    #     if ((not check_over) or (check_over and (overbought < rsi_d[-1]))):
    #         # sell signal
    #         action = -1
    return action


def compute_rr(t_prices, _days):
    capital = 1000
    orig_capital = capital

    t_length = len(t_prices)

    sug_action = np.zeros((t_length, 1))  # suggested action
    r_action = np.zeros((t_length, 1))  # real action

    stock_hold = np.zeros((t_length, 1))  # stock holding
    t_capital = np.zeros((t_length, 1))  # total capital

    for t in range(t_length):
        c_price = t_prices[t]
        sug_action[t] = my_strategy(t_prices[0:t], c_price, _days)
        if t > 0:
            stock_hold[t] = stock_hold[t - 1]

        # do action
        if sug_action[t] == 1:
            if stock_hold[t] == 0:
                # buy
                stock_hold[t] = capital / c_price
                capital = 0
                r_action[t] = 1
        elif sug_action[t] == -1:
            if stock_hold[t] > 0:
                # sell
                capital = stock_hold[t] * c_price
                stock_hold[t] = 0
                r_action[t] = -1
        elif sug_action[t] == 0:
            r_action[t] = 0
        else:
            assert False

        # compute total capital
        t_capital[t] = capital + stock_hold[t] * c_price
    rr = (t_capital[-1] - orig_capital) / orig_capital
    return rr


if __name__ == '__main__':
    # file
    # csv_file = '../0050.TW-short.csv'
    csv_file = '../0050.TW.csv'
    df = pd.read_csv(csv_file)

    t_prices = df["Adj Close"].values
    _ll = len(t_prices)
    lengths = [i for i in range(20, -_ll % 20 + _ll, 20)] + [_ll]

    # parameters range
    days_min, days_max = 0, 10  # days

    output_str = f"Test file: {csv_file}, time length: {len(t_prices)}\n" + \
        f"Test param | days: [{days_min}, {days_max}]\n" + \
        f"time lengths: {lengths}\n"
    print(output_str)

    # best parameters and return rate
    b_rr, b_days = -1, 0

    # find parameters
    t2 = 60
    for t1 in lengths:
        if t2 > t1:
            continue

        # reset
        b_rr, b_days = -1, 0

        # check all possible parameters
        c_t_prices = t_prices[-t1:][:t2]
        for _d in range(days_min, days_max + 1):
            _rr = compute_rr(c_t_prices, _d)
            c_result = f"t1: {t1}, t2: {t2}, days: {_d}, rr: {_rr}"
            print(f"\r{c_result}", end='')

            if _rr > b_rr:
                b_days = _d
                b_rr = _rr

        # store
        c_output_str = f"Best | t1: {t1}, t2: {t2}, days: {b_days}, rr: {b_rr}\n"
        print(f"\n{c_output_str}")
        output_str += c_output_str

    print("results")
    print(output_str)
