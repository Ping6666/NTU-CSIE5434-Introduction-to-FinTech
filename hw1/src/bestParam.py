import numpy as np
import pandas as pd
import talib

t_shift = 100


def my_strategy(p_prices, c_price, tp_1, tp_2):
    # action and prices, parameters
    action: int = 0  # 1 (buy), -1 (sell), 0 (hold)
    # tp_1, tp_2 = 7, 11

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


def compute_rr(t_prices, tp_1, tp_2):
    capital = 1000
    orig_capital = capital

    t_length = len(t_prices) - t_shift

    sug_action = np.zeros((t_length, 1))  # suggested action
    r_action = np.zeros((t_length, 1))  # real action

    stock_hold = np.zeros((t_length, 1))  # stock holding
    t_capital = np.zeros((t_length, 1))  # total capital

    for t in range(t_length):
        c_price = t_prices[t + t_shift]
        sug_action[t] = my_strategy(t_prices[0:t + t_shift], c_price, tp_1,
                                    tp_2)
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
    csv_file = '../0050.TW.csv'
    df = pd.read_csv(csv_file)

    t_prices = df["Adj Close"].values
    _ll = len(t_prices)
    lengths = [i for i in range(20, -_ll % 20 + _ll, 20)] + [_ll]

    # parameters range
    tp_1_min, tp_1_max = 1, 40  # tp_1
    tp_2_min, tp_2_max = 1, 40  # tp_2

    output_str = f"Test file: {csv_file}, time length: {len(t_prices)}\n" + \
        f"Test param | tp_1: [{tp_1_min}, {tp_1_max}], tp_2: [{tp_2_min}, {tp_2_max}]\n" + \
        f"time lengths: {lengths}\n"
    print(output_str)

    # best parameters and return rate
    b_rr, b_tp_1, b_tp_2 = -1, 0, 0

    # find parameters
    t2 = 60 + t_shift  # 60 for test time interval
    for t1 in lengths:
        if t2 > t1:
            continue

        # reset
        b_rr, b_tp_1, b_tp_2 = -1, 0, 0

        # check all possible parameters
        c_t_prices = t_prices[-t1:][:t2]

        for _tp_1 in range(tp_1_min, tp_1_max + 1):
            for _tp_2 in range(tp_2_min, tp_2_max + 1):
                if _tp_2 <= _tp_1:
                    continue

                _rr = compute_rr(c_t_prices, _tp_1, _tp_2)
                c_result = f"t1: {t1}, t2: {t2}, tp_1: {_tp_1}, tp_2: {_tp_2}, rr: {_rr}"
                print(f"\r{c_result}", end='')

                if _rr > b_rr:
                    b_tp_1 = _tp_1
                    b_tp_2 = _tp_2
                    b_rr = _rr

        # store
        c_output_str = f"Best | t1: {t1}, t2: {t2}, tp_1: {b_tp_1}, tp_2: {b_tp_2}, rr: {b_rr}\n"
        print(f"\n{c_output_str}")
        output_str += c_output_str

    print("results")
    print(output_str)
'''
global check

results
Test file: ../0050.TW.csv, time length: 3145
Test param | tp_1: [1, 40], tp_2: [1, 40]
time lengths: [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1020, 1040, 1060, 1080, 1100, 1120, 1140, 1160, 1180, 1200, 1220, 1240, 1260, 1280, 1300, 1320, 1340, 1360, 1380, 1400, 1420, 1440, 1460, 1480, 1500, 1520, 1540, 1560, 1580, 1600, 1620, 1640, 1660, 1680, 1700, 1720, 1740, 1760, 1780, 1800, 1820, 1840, 1860, 1880, 1900, 1920, 1940, 1960, 1980, 2000, 2020, 2040, 2060, 2080, 2100, 2120, 2140, 2160, 2180, 2200, 2220, 2240, 2260, 2280, 2300, 2320, 2340, 2360, 2380, 2400, 2420, 2440, 2460, 2480, 2500, 2520, 2540, 2560, 2580, 2600, 2620, 2640, 2660, 2680, 2700, 2720, 2740, 2760, 2780, 2800, 2820, 2840, 2860, 2880, 2900, 2920, 2940, 2960, 2980, 3000, 3020, 3040, 3060, 3080, 3100, 3120, 3140, 3145]
Best | t1: 160, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 180, t2: 160, tp_1: 7, tp_2: 21, rr: [0.01842278]
Best | t1: 200, t2: 160, tp_1: 24, tp_2: 39, rr: [0.03922437]
Best | t1: 220, t2: 160, tp_1: 16, tp_2: 38, rr: [0.01266405]
Best | t1: 240, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 260, t2: 160, tp_1: 24, tp_2: 39, rr: [0.03426297]
Best | t1: 280, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 300, t2: 160, tp_1: 8, tp_2: 31, rr: [0.01898215]
Best | t1: 320, t2: 160, tp_1: 3, tp_2: 4, rr: [0.05721007]
Best | t1: 340, t2: 160, tp_1: 2, tp_2: 3, rr: [0.08885902]
Best | t1: 360, t2: 160, tp_1: 4, tp_2: 5, rr: [0.04068474]
Best | t1: 380, t2: 160, tp_1: 10, tp_2: 15, rr: [0.03028565]
Best | t1: 400, t2: 160, tp_1: 4, tp_2: 7, rr: [0.05185208]
Best | t1: 420, t2: 160, tp_1: 4, tp_2: 7, rr: [0.06903626]
Best | t1: 440, t2: 160, tp_1: 3, tp_2: 7, rr: [0.08672723]
Best | t1: 460, t2: 160, tp_1: 4, tp_2: 8, rr: [0.07172154]
Best | t1: 480, t2: 160, tp_1: 5, tp_2: 9, rr: [0.05542352]
Best | t1: 500, t2: 160, tp_1: 11, tp_2: 16, rr: [0.05147783]
Best | t1: 520, t2: 160, tp_1: 3, tp_2: 4, rr: [0.08844576]
Best | t1: 540, t2: 160, tp_1: 3, tp_2: 6, rr: [0.05903413]
Best | t1: 560, t2: 160, tp_1: 4, tp_2: 26, rr: [0.17685609]
Best | t1: 580, t2: 160, tp_1: 13, tp_2: 40, rr: [0.23874092]
Best | t1: 600, t2: 160, tp_1: 3, tp_2: 11, rr: [0.13603733]
Best | t1: 620, t2: 160, tp_1: 3, tp_2: 11, rr: [0.14481606]
Best | t1: 640, t2: 160, tp_1: 2, tp_2: 7, rr: [0.07591773]
Best | t1: 660, t2: 160, tp_1: 5, tp_2: 28, rr: [0.05659718]
Best | t1: 680, t2: 160, tp_1: 7, tp_2: 36, rr: [0.1640171]
Best | t1: 700, t2: 160, tp_1: 10, tp_2: 39, rr: [0.22650761]
Best | t1: 720, t2: 160, tp_1: 4, tp_2: 28, rr: [0.11944673]
Best | t1: 740, t2: 160, tp_1: 12, tp_2: 30, rr: [0.21818178]
Best | t1: 760, t2: 160, tp_1: 10, tp_2: 37, rr: [0.13535358]
Best | t1: 780, t2: 160, tp_1: 14, tp_2: 28, rr: [0.09023565]
Best | t1: 800, t2: 160, tp_1: 3, tp_2: 26, rr: [0.03273065]
Best | t1: 820, t2: 160, tp_1: 3, tp_2: 36, rr: [0.05107471]
Best | t1: 840, t2: 160, tp_1: 2, tp_2: 28, rr: [0.10466061]
Best | t1: 860, t2: 160, tp_1: 2, tp_2: 3, rr: [0.08274391]
Best | t1: 880, t2: 160, tp_1: 10, tp_2: 39, rr: [0.11362253]
Best | t1: 900, t2: 160, tp_1: 11, tp_2: 29, rr: [0.06963965]
Best | t1: 920, t2: 160, tp_1: 10, tp_2: 36, rr: [0.07446849]
Best | t1: 940, t2: 160, tp_1: 6, tp_2: 14, rr: [0.06255495]
Best | t1: 960, t2: 160, tp_1: 10, tp_2: 35, rr: [0.04680578]
Best | t1: 980, t2: 160, tp_1: 5, tp_2: 13, rr: [0.04349601]
Best | t1: 1000, t2: 160, tp_1: 11, tp_2: 35, rr: [0.08076167]
Best | t1: 1020, t2: 160, tp_1: 14, tp_2: 40, rr: [0.11748814]
Best | t1: 1040, t2: 160, tp_1: 14, tp_2: 35, rr: [0.02153408]
Best | t1: 1060, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1080, t2: 160, tp_1: 3, tp_2: 4, rr: [0.00705801]
Best | t1: 1100, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1120, t2: 160, tp_1: 3, tp_2: 8, rr: [0.01897042]
Best | t1: 1140, t2: 160, tp_1: 3, tp_2: 8, rr: [0.0161342]
Best | t1: 1160, t2: 160, tp_1: 2, tp_2: 10, rr: [0.05773889]
Best | t1: 1180, t2: 160, tp_1: 6, tp_2: 34, rr: [0.02957593]
Best | t1: 1200, t2: 160, tp_1: 2, tp_2: 3, rr: [0.0279956]
Best | t1: 1220, t2: 160, tp_1: 2, tp_2: 3, rr: [0.01516186]
Best | t1: 1240, t2: 160, tp_1: 2, tp_2: 3, rr: [0.03080468]
Best | t1: 1260, t2: 160, tp_1: 3, tp_2: 6, rr: [0.0080694]
Best | t1: 1280, t2: 160, tp_1: 3, tp_2: 6, rr: [0.11693165]
Best | t1: 1300, t2: 160, tp_1: 4, tp_2: 8, rr: [0.05891691]
Best | t1: 1320, t2: 160, tp_1: 2, tp_2: 3, rr: [0.0365616]
Best | t1: 1340, t2: 160, tp_1: 9, tp_2: 23, rr: [0.03052639]
Best | t1: 1360, t2: 160, tp_1: 11, tp_2: 16, rr: [0.0310549]
Best | t1: 1380, t2: 160, tp_1: 8, tp_2: 15, rr: [0.02313676]
Best | t1: 1400, t2: 160, tp_1: 21, tp_2: 34, rr: [0.02177971]
Best | t1: 1420, t2: 160, tp_1: 2, tp_2: 5, rr: [0.05686091]
Best | t1: 1440, t2: 160, tp_1: 2, tp_2: 5, rr: [0.08461226]
Best | t1: 1460, t2: 160, tp_1: 36, tp_2: 40, rr: [0.10612249]
Best | t1: 1480, t2: 160, tp_1: 2, tp_2: 5, rr: [0.04446719]
Best | t1: 1500, t2: 160, tp_1: 5, tp_2: 7, rr: [0.0181391]
Best | t1: 1520, t2: 160, tp_1: 3, tp_2: 4, rr: [0.03217831]
Best | t1: 1540, t2: 160, tp_1: 3, tp_2: 5, rr: [0.02078964]
Best | t1: 1560, t2: 160, tp_1: 8, tp_2: 30, rr: [0.00344047]
Best | t1: 1580, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1600, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1620, t2: 160, tp_1: 2, tp_2: 3, rr: [0.030353]
Best | t1: 1640, t2: 160, tp_1: 2, tp_2: 3, rr: [0.07425849]
Best | t1: 1660, t2: 160, tp_1: 2, tp_2: 3, rr: [0.09094217]
Best | t1: 1680, t2: 160, tp_1: 2, tp_2: 4, rr: [0.13851922]
Best | t1: 1700, t2: 160, tp_1: 2, tp_2: 7, rr: [0.08153737]
Best | t1: 1720, t2: 160, tp_1: 6, tp_2: 12, rr: [0.07128513]
Best | t1: 1740, t2: 160, tp_1: 2, tp_2: 31, rr: [0.03351644]
Best | t1: 1760, t2: 160, tp_1: 12, tp_2: 14, rr: [0.13175086]
Best | t1: 1780, t2: 160, tp_1: 7, tp_2: 36, rr: [0.10001925]
Best | t1: 1800, t2: 160, tp_1: 4, tp_2: 7, rr: [0.00727867]
Best | t1: 1820, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1840, t2: 160, tp_1: 12, tp_2: 25, rr: [0.00910875]
Best | t1: 1860, t2: 160, tp_1: 9, tp_2: 29, rr: [0.07162757]
Best | t1: 1880, t2: 160, tp_1: 10, tp_2: 23, rr: [0.07810849]
Best | t1: 1900, t2: 160, tp_1: 7, tp_2: 28, rr: [0.02558138]
Best | t1: 1920, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 1940, t2: 160, tp_1: 2, tp_2: 4, rr: [0.04244244]
Best | t1: 1960, t2: 160, tp_1: 2, tp_2: 3, rr: [0.01622027]
Best | t1: 1980, t2: 160, tp_1: 2, tp_2: 3, rr: [0.03173649]
Best | t1: 2000, t2: 160, tp_1: 2, tp_2: 3, rr: [0.04467732]
Best | t1: 2020, t2: 160, tp_1: 2, tp_2: 3, rr: [0.10580729]
Best | t1: 2040, t2: 160, tp_1: 2, tp_2: 3, rr: [0.08151747]
Best | t1: 2060, t2: 160, tp_1: 2, tp_2: 3, rr: [0.0535854]
Best | t1: 2080, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2100, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2120, t2: 160, tp_1: 4, tp_2: 38, rr: [0.02069753]
Best | t1: 2140, t2: 160, tp_1: 5, tp_2: 10, rr: [0.04087808]
Best | t1: 2160, t2: 160, tp_1: 6, tp_2: 8, rr: [0.09212365]
Best | t1: 2180, t2: 160, tp_1: 39, tp_2: 40, rr: [0.11037641]
Best | t1: 2200, t2: 160, tp_1: 27, tp_2: 40, rr: [0.06346618]
Best | t1: 2220, t2: 160, tp_1: 37, tp_2: 39, rr: [0.09262439]
Best | t1: 2240, t2: 160, tp_1: 10, tp_2: 22, rr: [0.02708341]
Best | t1: 2260, t2: 160, tp_1: 3, tp_2: 4, rr: [0.0343131]
Best | t1: 2280, t2: 160, tp_1: 3, tp_2: 4, rr: [0.04061602]
Best | t1: 2300, t2: 160, tp_1: 2, tp_2: 7, rr: [0.04243568]
Best | t1: 2320, t2: 160, tp_1: 6, tp_2: 34, rr: [0.01791544]
Best | t1: 2340, t2: 160, tp_1: 24, tp_2: 30, rr: [0.01863777]
Best | t1: 2360, t2: 160, tp_1: 39, tp_2: 40, rr: [0.03043869]
Best | t1: 2380, t2: 160, tp_1: 6, tp_2: 7, rr: [0.04559195]
Best | t1: 2400, t2: 160, tp_1: 7, tp_2: 10, rr: [0.0505111]
Best | t1: 2420, t2: 160, tp_1: 4, tp_2: 16, rr: [0.04599854]
Best | t1: 2440, t2: 160, tp_1: 5, tp_2: 15, rr: [0.06879389]
Best | t1: 2460, t2: 160, tp_1: 4, tp_2: 15, rr: [0.02840672]
Best | t1: 2480, t2: 160, tp_1: 19, tp_2: 40, rr: [0.04328218]
Best | t1: 2500, t2: 160, tp_1: 3, tp_2: 7, rr: [0.01529616]
Best | t1: 2520, t2: 160, tp_1: 4, tp_2: 5, rr: [0.04758422]
Best | t1: 2540, t2: 160, tp_1: 3, tp_2: 6, rr: [0.08159891]
Best | t1: 2560, t2: 160, tp_1: 6, tp_2: 11, rr: [0.06477865]
Best | t1: 2580, t2: 160, tp_1: 2, tp_2: 3, rr: [0.10690457]
Best | t1: 2600, t2: 160, tp_1: 5, tp_2: 12, rr: [0.04184878]
Best | t1: 2620, t2: 160, tp_1: 32, tp_2: 36, rr: [0.10276445]
Best | t1: 2640, t2: 160, tp_1: 4, tp_2: 11, rr: [0.06917069]
Best | t1: 2660, t2: 160, tp_1: 2, tp_2: 3, rr: [0.05823557]
Best | t1: 2680, t2: 160, tp_1: 20, tp_2: 31, rr: [0.00506073]
Best | t1: 2700, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2720, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2740, t2: 160, tp_1: 9, tp_2: 18, rr: [0.07725205]
Best | t1: 2760, t2: 160, tp_1: 7, tp_2: 37, rr: [0.1190877]
Best | t1: 2780, t2: 160, tp_1: 23, tp_2: 27, rr: [0.07543761]
Best | t1: 2800, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2820, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2840, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2860, t2: 160, tp_1: 1, tp_2: 2, rr: [0.]
Best | t1: 2880, t2: 160, tp_1: 2, tp_2: 6, rr: [0.05184816]
Best | t1: 2900, t2: 160, tp_1: 3, tp_2: 35, rr: [0.00817475]
Best | t1: 2920, t2: 160, tp_1: 3, tp_2: 8, rr: [0.01849749]
Best | t1: 2940, t2: 160, tp_1: 3, tp_2: 30, rr: [0.00841972]
Best | t1: 2960, t2: 160, tp_1: 5, tp_2: 9, rr: [0.0456246]
Best | t1: 2980, t2: 160, tp_1: 2, tp_2: 5, rr: [0.10575472]
Best | t1: 3000, t2: 160, tp_1: 2, tp_2: 3, rr: [0.08827351]
Best | t1: 3020, t2: 160, tp_1: 2, tp_2: 5, rr: [0.11097098]
Best | t1: 3040, t2: 160, tp_1: 2, tp_2: 5, rr: [0.08745184]
Best | t1: 3060, t2: 160, tp_1: 12, tp_2: 29, rr: [0.0331837]
Best | t1: 3080, t2: 160, tp_1: 12, tp_2: 27, rr: [0.03477246]
Best | t1: 3100, t2: 160, tp_1: 10, tp_2: 34, rr: [0.05206189]
Best | t1: 3120, t2: 160, tp_1: 4, tp_2: 19, rr: [0.08072018]
Best | t1: 3140, t2: 160, tp_1: 4, tp_2: 39, rr: [0.12095175]
Best | t1: 3145, t2: 160, tp_1: 4, tp_2: 23, rr: [0.08244616]
'''
