import numpy as np
import pandas as pd
import talib

t_shift = 10


def my_strategy(p_prices, c_price, tp_1_1, tp_2_1, tp_1_2, tp_2_2):
    # action and prices, parameters
    action: int = 0  # 1 (buy), -1 (sell), 0 (hold)
    tp_1_bull, tp_2_bull = tp_1_1, tp_2_1
    tp_1_bear, tp_2_bear = tp_1_2, tp_2_2

    try:
        t_prices = np.append(p_prices, c_price)

        # technical analysis: RSI and K/D
        ma_10 = talib.MA(t_prices, timeperiod=60)
    except:
        return action

    if ma_10[-1] > c_price:
        # bear
        tp_1 = tp_1_bear
        tp_2 = tp_2_bear
    else:
        # bull
        tp_1 = tp_1_bull
        tp_2 = tp_2_bull

    try:
        rsi_1 = talib.RSI(t_prices, timeperiod=tp_1)
        rsi_2 = talib.RSI(t_prices, timeperiod=tp_2)
    except:
        return action

    # length checker
    if ((len(rsi_1) < 2) or (len(rsi_2) < 2)):
        return action

    # buy / sell signal checker
    if ((rsi_1[-2] < rsi_2[-2]) and (rsi_1[-1] > rsi_2[-1])):
        if rsi_1[-1] < 30:
            # buy signal
            action = 1
    elif ((rsi_1[-2] > rsi_2[-2]) and (rsi_1[-1] < rsi_2[-1])):
        if rsi_1[-1] > 70:
            # sell signal
            action = -1
    return action


def compute_rr(t_prices, tp_1_1, tp_2_1, tp_1_2, tp_2_2):
    capital = 1000
    orig_capital = capital

    t_length = len(t_prices) - t_shift

    sug_action = np.zeros((t_length, 1))  # suggested action
    r_action = np.zeros((t_length, 1))  # real action

    stock_hold = np.zeros((t_length, 1))  # stock holding
    t_capital = np.zeros((t_length, 1))  # total capital

    for t in range(t_length):
        c_price = t_prices[t + t_shift]
        sug_action[t] = my_strategy(t_prices[0:t + t_shift], c_price, tp_1_1,
                                    tp_2_1, tp_1_2, tp_2_2)
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
    tp_1_min, tp_1_max = 1, 20  # tp_1
    tp_2_min, tp_2_max = 1, 20  # tp_2

    output_str = f"Test file: {csv_file}, time length: {len(t_prices)}\n" + \
        f"Test param | tp_1: [{tp_1_min}, {tp_1_max}], tp_2: [{tp_2_min}, {tp_2_max}]\n" + \
        f"time lengths: {lengths}\n"
    print(output_str)

    # best parameters and return rate
    b_rr, b_tp_1_1, b_tp_2_1, b_tp_1_2, b_tp_2_2 = -1, 0, 0, 0, 0

    # find parameters
    t2 = 60 + t_shift
    for t1 in lengths:
        if t2 > t1:
            continue

        # reset
        b_rr, b_tp_1_1, b_tp_2_1, b_tp_1_2, b_tp_2_2 = -1, 0, 0, 0, 0

        # check all possible parameters
        c_t_prices = t_prices[-t1:][:t2]
        for _tp_1_1 in range(tp_1_min, tp_1_max + 1):
            for _tp_2_1 in range(tp_2_min, tp_2_max + 1):
                if _tp_2_1 <= _tp_1_1:
                    continue

                for _tp_1_2 in range(tp_1_min, tp_1_max + 1):
                    for _tp_2_2 in range(tp_2_min, tp_2_max + 1):
                        if _tp_2_2 <= _tp_1_2:
                            continue

                        # _tp_1_1, _tp_2_1, _tp_1_2, _tp_2_2 = 5, 15, 3, 4
                        _rr = compute_rr(c_t_prices, _tp_1_1, _tp_2_1, _tp_1_2,
                                         _tp_2_2)
                        c_result = f"t1: {t1}, t2: {t2}, tp_1: {_tp_1_1}, tp_2: {_tp_2_1}, tp_1: {_tp_1_2}, tp_2: {_tp_2_2}, rr: {_rr}"
                        print(f"\r{c_result}", end='')

                        if _rr > b_rr:
                            b_tp_1_1 = _tp_1_1
                            b_tp_2_1 = _tp_2_1
                            b_tp_1_2 = _tp_1_2
                            b_tp_2_2 = _tp_2_2
                            b_rr = _rr

        # store
        c_output_str = f"Best | t1: {t1}, t2: {t2}, tp_1: {b_tp_1_1}, tp_2: {b_tp_2_1}, tp_1: {b_tp_1_2}, tp_2: {b_tp_2_2}, rr: {b_rr}\n"
        print(f"\n{c_output_str}")
        output_str += c_output_str

    print("results")
    print(output_str)
