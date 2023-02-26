import numpy as np
import pandas as pd
import talib

t_shift = 60


def my_strategy(p_prices, c_price, tp_1_1, tp_2_1, tp_1_2, tp_2_2):
    # action and prices, parameters
    action: int = 0  # 1 (buy), -1 (sell), 0 (hold)
    tp_1_bull, tp_2_bull = tp_1_1, tp_2_1
    tp_1_bear, tp_2_bear = tp_1_2, tp_2_2

    try:
        t_prices = np.append(p_prices, c_price)

        # technical analysis: RSI and K/D
        ma_60 = talib.MA(t_prices, timeperiod=60)
    except:
        return action

    if ma_60[-1] > c_price:
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
        # for _tp_1_1 in range(tp_1_min, tp_1_max + 1):
        #     for _tp_2_1 in range(tp_2_min, tp_2_max + 1):
        #         if _tp_2_1 <= _tp_1_1:
        #             continue

        # for _tp_1_2 in range(tp_1_min, tp_1_max + 1):
        #     for _tp_2_2 in range(tp_2_min, tp_2_max + 1):
        #         if _tp_2_2 <= _tp_1_2:
        #             continue
        _tp_1_1, _tp_2_1, _tp_1_2, _tp_2_2 = 5, 15, 3, 4
        _rr = compute_rr(c_t_prices, _tp_1_1, _tp_2_1, _tp_1_2, _tp_2_2)
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
'''
local check on ma60: _tp_1_1, _tp_2_1, _tp_1_2, _tp_2_2 = 3, 10, 2, 3
local check on ma60: _tp_1_1, _tp_2_1, _tp_1_2, _tp_2_2 = 5, 15, 2, 3
'''
'''
global check on ma60

results
Test file: ../0050.TW.csv, time length: 3145
Test param | tp_1: [1, 20], tp_2: [1, 20]
time lengths: [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1020, 1040, 1060, 1080, 1100, 1120, 1140, 1160, 1180, 1200, 1220, 1240, 1260, 1280, 1300, 1320, 1340, 1360, 1380, 1400, 1420, 1440, 1460, 1480, 1500, 1520, 1540, 1560, 1580, 1600, 1620, 1640, 1660, 1680, 1700, 1720, 1740, 1760, 1780, 1800, 1820, 1840, 1860, 1880, 1900, 1920, 1940, 1960, 1980, 2000, 2020, 2040, 2060, 2080, 2100, 2120, 2140, 2160, 2180, 2200, 2220, 2240, 2260, 2280, 2300, 2320, 2340, 2360, 2380, 2400, 2420, 2440, 2460, 2480, 2500, 2520, 2540, 2560, 2580, 2600, 2620, 2640, 2660, 2680, 2700, 2720, 2740, 2760, 2780, 2800, 2820, 2840, 2860, 2880, 2900, 2920, 2940, 2960, 2980, 3000, 3020, 3040, 3060, 3080, 3100, 3120, 3140, 3145]
Best | t1: 120, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 140, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 160, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 5, rr: [0.06216218]
Best | t1: 180, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 5, rr: [0.05135132]
Best | t1: 200, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 220, t2: 120, tp_1: 1, tp_2: 2, tp_1: 4, tp_2: 7, rr: [0.06089093]
Best | t1: 240, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.00550751]
Best | t1: 260, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.0422642]
Best | t1: 280, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 300, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 320, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 340, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 360, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.00667168]
Best | t1: 380, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.0159378]
Best | t1: 400, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.04040039]
Best | t1: 420, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.07367197]
Best | t1: 440, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.08375342]
Best | t1: 460, t2: 120, tp_1: 2, tp_2: 3, tp_1: 3, tp_2: 4, rr: [0.06708034]
Best | t1: 480, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 500, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 520, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 540, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 560, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.17601543]
Best | t1: 580, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.11605416]
Best | t1: 600, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.02659574]
Best | t1: 620, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 640, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 660, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 680, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 700, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 720, t2: 120, tp_1: 1, tp_2: 2, tp_1: 13, tp_2: 14, rr: [0.13918923]
Best | t1: 740, t2: 120, tp_1: 1, tp_2: 2, tp_1: 13, tp_2: 14, rr: [0.09391888]
Best | t1: 760, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 780, t2: 120, tp_1: 1, tp_2: 2, tp_1: 4, tp_2: 5, rr: [0.02428262]
Best | t1: 800, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 820, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 840, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 860, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 880, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 900, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 8, rr: [0.04201681]
Best | t1: 920, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 8, rr: [0.06981257]
Best | t1: 940, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 8, rr: [0.02003884]
Best | t1: 960, t2: 120, tp_1: 2, tp_2: 3, tp_1: 1, tp_2: 2, rr: [0.076482]
Best | t1: 980, t2: 120, tp_1: 2, tp_2: 3, tp_1: 1, tp_2: 2, rr: [0.08667102]
Best | t1: 1000, t2: 120, tp_1: 2, tp_2: 3, tp_1: 1, tp_2: 2, rr: [0.0256073]
Best | t1: 1020, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1040, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1060, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1080, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.02706275]
Best | t1: 1100, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1120, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1140, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1160, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.04861119]
Best | t1: 1180, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.02904044]
Best | t1: 1200, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.03219701]
Best | t1: 1220, t2: 120, tp_1: 1, tp_2: 2, tp_1: 4, tp_2: 5, rr: [0.00313676]
Best | t1: 1240, t2: 120, tp_1: 1, tp_2: 2, tp_1: 4, tp_2: 5, rr: [0.05207028]
Best | t1: 1260, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1280, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1300, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1320, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1340, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1360, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1380, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1400, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1420, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1440, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.06029103]
Best | t1: 1460, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.03326405]
Best | t1: 1480, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.0451977]
Best | t1: 1500, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.02189258]
Best | t1: 1520, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.02754233]
Best | t1: 1540, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1560, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1580, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1600, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1620, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1640, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1660, t2: 120, tp_1: 1, tp_2: 2, tp_1: 4, tp_2: 5, rr: [0.0816667]
Best | t1: 1680, t2: 120, tp_1: 1, tp_2: 2, tp_1: 4, tp_2: 5, rr: [0.06750005]
Best | t1: 1700, t2: 120, tp_1: 1, tp_2: 2, tp_1: 4, tp_2: 5, rr: [1.13686838e-16]
Best | t1: 1720, t2: 120, tp_1: 4, tp_2: 6, tp_1: 6, tp_2: 7, rr: [0.13035863]
Best | t1: 1740, t2: 120, tp_1: 1, tp_2: 2, tp_1: 6, tp_2: 7, rr: [0.10673662]
Best | t1: 1760, t2: 120, tp_1: 1, tp_2: 2, tp_1: 6, tp_2: 7, rr: [0.0419947]
Best | t1: 1780, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1800, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1820, t2: 120, tp_1: 2, tp_2: 3, tp_1: 1, tp_2: 2, rr: [0.00552927]
Best | t1: 1840, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.03147135]
Best | t1: 1860, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1880, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1900, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1920, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1940, t2: 120, tp_1: 2, tp_2: 3, tp_1: 1, tp_2: 2, rr: [0.05141195]
Best | t1: 1960, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1980, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.10753535]
Best | t1: 2000, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.08320249]
Best | t1: 2020, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.02982727]
Best | t1: 2040, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2060, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2080, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2100, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2120, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2140, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2160, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2180, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2200, t2: 120, tp_1: 5, tp_2: 6, tp_1: 2, tp_2: 3, rr: [0.10089289]
Best | t1: 2220, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.07321425]
Best | t1: 2240, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.03482145]
Best | t1: 2260, t2: 120, tp_1: 2, tp_2: 5, tp_1: 3, tp_2: 4, rr: [0.05008943]
Best | t1: 2280, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.03488365]
Best | t1: 2300, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.01967796]
Best | t1: 2320, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.05272731]
Best | t1: 2340, t2: 120, tp_1: 4, tp_2: 6, tp_1: 3, tp_2: 4, rr: [0.05]
Best | t1: 2360, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.01545451]
Best | t1: 2380, t2: 120, tp_1: 2, tp_2: 3, tp_1: 1, tp_2: 2, rr: [0.00267622]
Best | t1: 2400, t2: 120, tp_1: 5, tp_2: 15, tp_1: 2, tp_2: 3, rr: [0.08550192]
Best | t1: 2420, t2: 120, tp_1: 5, tp_2: 15, tp_1: 2, tp_2: 3, rr: [0.0755065]
Best | t1: 2440, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.06537752]
Best | t1: 2460, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2480, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2500, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2520, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.07599998]
Best | t1: 2540, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.07099998]
Best | t1: 2560, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.01400002]
Best | t1: 2580, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2600, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2620, t2: 120, tp_1: 1, tp_2: 2, tp_1: 6, tp_2: 7, rr: [0.058058]
Best | t1: 2640, t2: 120, tp_1: 2, tp_2: 3, tp_1: 6, tp_2: 7, rr: [0.02702699]
Best | t1: 2660, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2680, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2700, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2720, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.14989511]
Best | t1: 2740, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.14779872]
Best | t1: 2760, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.06184488]
Best | t1: 2780, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2800, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2820, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.0252427]
Best | t1: 2840, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.03689324]
Best | t1: 2860, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2880, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2900, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2920, t2: 120, tp_1: 2, tp_2: 4, tp_1: 1, tp_2: 2, rr: [0.00248134]
Best | t1: 2940, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 4, rr: [0.04629629]
Best | t1: 2960, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2980, t2: 120, tp_1: 1, tp_2: 2, tp_1: 2, tp_2: 3, rr: [0.00925924]
Best | t1: 3000, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 3020, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 3040, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 3060, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 3080, t2: 120, tp_1: 1, tp_2: 2, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 3100, t2: 120, tp_1: 3, tp_2: 10, tp_1: 2, tp_2: 3, rr: [0.11941806]
Best | t1: 3120, t2: 120, tp_1: 2, tp_2: 3, tp_1: 3, tp_2: 5, rr: [0.1171938]
Best | t1: 3140, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 5, rr: [0.05535278]
Best | t1: 3145, t2: 120, tp_1: 1, tp_2: 2, tp_1: 3, tp_2: 4, rr: [0.04825631]
'''
