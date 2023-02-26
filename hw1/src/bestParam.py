import numpy as np
import pandas as pd
import talib


def my_strategy(p_prices, c_price, oversold, overbought):
    # action and prices, parameters
    action: int = 0  # 1 (buy), -1 (sell), 0 (hold)
    check_over: bool = False
    # oversold, overbought = 10, 70

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
    if ((len(rsi_k) < 2) or (len(rsi_d) < 2)):
        return action

    # buy / sell signal checker
    if ((rsi_k[-2] < rsi_d[-2]) and (rsi_k[-1] > rsi_d[-1])):
        if ((not check_over) or (check_over and (oversold > rsi_d[-1]))):
            # buy signal
            action = 1
    elif ((rsi_k[-2] > rsi_d[-2]) and (rsi_k[-1] < rsi_d[-1])):
        if ((not check_over) or (check_over and (overbought < rsi_d[-1]))):
            # sell signal
            action = -1
    return action


def compute_rr(t_prices, _os, _ob):
    capital = 1000
    orig_capital = capital

    t_length = len(t_prices)

    sug_action = np.zeros((t_length, 1))  # suggested action
    r_action = np.zeros((t_length, 1))  # real action

    stock_hold = np.zeros((t_length, 1))  # stock holding
    t_capital = np.zeros((t_length, 1))  # total capital

    for t in range(t_length):
        c_price = t_prices[t]
        sug_action[t] = my_strategy(t_prices[0:t], c_price, _os, _ob)
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
    os_min, os_max = 0, 100  # oversold
    ob_min, ob_max = 0, 100  # overbought

    output_str = f"Test file: {csv_file}, time length: {len(t_prices)}\n" + \
        f"Test param | os: [{os_min}, {os_max}], ob: [{ob_min}, {ob_max}]\n" + \
        f"time lengths: {lengths}\n"
    print(output_str)

    # best parameters and return rate
    b_rr, b_os, b_ob = -1, 0, 100

    # find parameters
    t2 = 60
    for t1 in lengths:
        if t2 > t1:
            continue

        # reset
        b_rr, b_os, b_ob = -1, 0, 100

        # check all possible parameters
        c_t_prices = t_prices[-t1:][:t2]
        for _os in range(os_min, os_max + 1, 5):
            for _ob in range(ob_min, ob_max + 1, 5):
                _rr = compute_rr(c_t_prices, _os, _ob)
                c_result = f"t1: {t1}, t2: {t2}, os: {_os}, ob: {_ob}, rr: {_rr}"
                print(f"\r{c_result}", end='')

                if _rr > b_rr:
                    b_os = _os
                    b_ob = _ob
                    b_rr = _rr

        # store
        c_output_str = f"Best | t1: {t1}, t2: {t2}, os: {b_os}, ob: {b_ob}, rr: {b_rr}\n"
        print(f"\n{c_output_str}")
        output_str += c_output_str

    print("results")
    print(output_str)
'''
True

results
Test file: ../0050.TW.csv, time length: 3644
Test param | os: [0, 100], ob: [0, 100]
time lengths: [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1020, 1040, 1060, 1080, 1100, 1120, 1140, 1160, 1180, 1200, 1220, 1240, 1260, 1280, 1300, 1320, 1340, 1360, 1380, 1400, 1420, 1440, 1460, 1480, 1500, 1520, 1540, 1560, 1580, 1600, 1620, 1640, 1660, 1680, 1700, 1720, 1740, 1760, 1780, 1800, 1820, 1840, 1860, 1880, 1900, 1920, 1940, 1960, 1980, 2000, 2020, 2040, 2060, 2080, 2100, 2120, 2140, 2160, 2180, 2200, 2220, 2240, 2260, 2280, 2300, 2320, 2340, 2360, 2380, 2400, 2420, 2440, 2460, 2480, 2500, 2520, 2540, 2560, 2580, 2600, 2620, 2640, 2660, 2680, 2700, 2720, 2740, 2760, 2780, 2800, 2820, 2840, 2860, 2880, 2900, 2920, 2940, 2960, 2980, 3000, 3020, 3040, 3060, 3080, 3100, 3120, 3140, 3160, 3180, 3200, 3220, 3240, 3260, 3280, 3300, 3320, 3340, 3360, 3380, 3400, 3420, 3440, 3460, 3480, 3500, 3520, 3540, 3560, 3580, 3600, 3620, 3640, 3644]
Best | t1: 60, t2: 60, os: 0, ob: 0, rr: [-0.00599591]
Best | t1: 80, t2: 60, os: 45, ob: 20, rr: [0.01007897]
Best | t1: 100, t2: 60, os: 50, ob: 0, rr: [0.07897225]
Best | t1: 120, t2: 60, os: 30, ob: 15, rr: [0.05774376]
Best | t1: 140, t2: 60, os: 5, ob: 0, rr: [0.03193162]
Best | t1: 160, t2: 60, os: 0, ob: 30, rr: [0.01580403]
Best | t1: 180, t2: 60, os: 0, ob: 0, rr: [0.01738441]
Best | t1: 200, t2: 60, os: 5, ob: 0, rr: [0.01862259]
Best | t1: 220, t2: 60, os: 50, ob: 5, rr: [0.01863458]
Best | t1: 240, t2: 60, os: 5, ob: 40, rr: [0.06414825]
Best | t1: 260, t2: 60, os: 60, ob: 40, rr: [0.05938179]
Best | t1: 280, t2: 60, os: 30, ob: 20, rr: [0.06951533]
Best | t1: 300, t2: 60, os: 5, ob: 50, rr: [0.03120296]
Best | t1: 320, t2: 60, os: 5, ob: 5, rr: [0.05189029]
Best | t1: 340, t2: 60, os: 20, ob: 15, rr: [0.03385457]
Best | t1: 360, t2: 60, os: 5, ob: 50, rr: [0.05344853]
Best | t1: 380, t2: 60, os: 50, ob: 5, rr: [0.02140966]
Best | t1: 400, t2: 60, os: 55, ob: 5, rr: [0.03671946]
Best | t1: 420, t2: 60, os: 30, ob: 0, rr: [0.06934587]
Best | t1: 440, t2: 60, os: 10, ob: 60, rr: [0.06023487]
Best | t1: 460, t2: 60, os: 15, ob: 75, rr: [0.1928473]
Best | t1: 480, t2: 60, os: 30, ob: 80, rr: [0.25109358]
Best | t1: 500, t2: 60, os: 25, ob: 55, rr: [0.16061049]
Best | t1: 520, t2: 60, os: 0, ob: 50, rr: [0.10640351]
Best | t1: 540, t2: 60, os: 0, ob: 0, rr: [0.01994067]
Best | t1: 560, t2: 60, os: 40, ob: 35, rr: [0.02432294]
Best | t1: 580, t2: 60, os: 55, ob: 75, rr: [0.07548152]
Best | t1: 600, t2: 60, os: 15, ob: 80, rr: [0.1856018]
Best | t1: 620, t2: 60, os: 15, ob: 65, rr: [0.13834227]
Best | t1: 640, t2: 60, os: 5, ob: 60, rr: [0.10754012]
Best | t1: 660, t2: 60, os: 10, ob: 50, rr: [0.16529417]
Best | t1: 680, t2: 60, os: 20, ob: 0, rr: [0.06122904]
Best | t1: 700, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 720, t2: 60, os: 5, ob: 30, rr: [0.02262698]
Best | t1: 740, t2: 60, os: 20, ob: 55, rr: [0.05921569]
Best | t1: 760, t2: 60, os: 30, ob: 75, rr: [0.08894097]
Best | t1: 780, t2: 60, os: 50, ob: 75, rr: [0.1265977]
Best | t1: 800, t2: 60, os: 30, ob: 45, rr: [0.06571374]
Best | t1: 820, t2: 60, os: 25, ob: 45, rr: [0.02813751]
Best | t1: 840, t2: 60, os: 15, ob: 45, rr: [0.03457957]
Best | t1: 860, t2: 60, os: 0, ob: 45, rr: [0.03368679]
Best | t1: 880, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 900, t2: 60, os: 5, ob: 75, rr: [0.08667102]
Best | t1: 920, t2: 60, os: 40, ob: 75, rr: [0.09248165]
Best | t1: 940, t2: 60, os: 35, ob: 45, rr: [0.06091823]
Best | t1: 960, t2: 60, os: 0, ob: 45, rr: [0.02719239]
Best | t1: 980, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 1000, t2: 60, os: 0, ob: 0, rr: [0.03046362]
Best | t1: 1020, t2: 60, os: 0, ob: 35, rr: [0.05961267]
Best | t1: 1040, t2: 60, os: 0, ob: 35, rr: [0.01459428]
Best | t1: 1060, t2: 60, os: 70, ob: 40, rr: [0.04475629]
Best | t1: 1080, t2: 60, os: 10, ob: 55, rr: [0.03742335]
Best | t1: 1100, t2: 60, os: 15, ob: 45, rr: [0.02028275]
Best | t1: 1120, t2: 60, os: 30, ob: 0, rr: [0.02287301]
Best | t1: 1140, t2: 60, os: 10, ob: 0, rr: [0.01906836]
Best | t1: 1160, t2: 60, os: 15, ob: 0, rr: [0.02227392]
Best | t1: 1180, t2: 60, os: 35, ob: 5, rr: [0.0415725]
Best | t1: 1200, t2: 60, os: 30, ob: 0, rr: [0.01565098]
Best | t1: 1220, t2: 60, os: 0, ob: 50, rr: [0.00960378]
Best | t1: 1240, t2: 60, os: 20, ob: 5, rr: [-0.00085075]
Best | t1: 1260, t2: 60, os: 5, ob: 55, rr: [0.03339405]
Best | t1: 1280, t2: 60, os: 25, ob: 60, rr: [0.03726334]
Best | t1: 1300, t2: 60, os: 5, ob: 30, rr: [0.03966546]
Best | t1: 1320, t2: 60, os: 70, ob: 30, rr: [0.02222965]
Best | t1: 1340, t2: 60, os: 50, ob: 30, rr: [0.08797182]
Best | t1: 1360, t2: 60, os: 60, ob: 45, rr: [0.11896228]
Best | t1: 1380, t2: 60, os: 0, ob: 55, rr: [0.0440977]
Best | t1: 1400, t2: 60, os: 10, ob: 30, rr: [0.03736101]
Best | t1: 1420, t2: 60, os: 20, ob: 10, rr: [0.02838579]
Best | t1: 1440, t2: 60, os: 5, ob: 55, rr: [0.03319207]
Best | t1: 1460, t2: 60, os: 20, ob: 50, rr: [0.03323754]
Best | t1: 1480, t2: 60, os: 60, ob: 40, rr: [0.00620599]
Best | t1: 1500, t2: 60, os: 65, ob: 45, rr: [-0.00285621]
Best | t1: 1520, t2: 60, os: 65, ob: 45, rr: [0.05422395]
Best | t1: 1540, t2: 60, os: 20, ob: 40, rr: [0.04305106]
Best | t1: 1560, t2: 60, os: 30, ob: 55, rr: [0.06621014]
Best | t1: 1580, t2: 60, os: 15, ob: 15, rr: [0.07859927]
Best | t1: 1600, t2: 60, os: 10, ob: 50, rr: [0.10166663]
Best | t1: 1620, t2: 60, os: 55, ob: 0, rr: [0.04752363]
Best | t1: 1640, t2: 60, os: 75, ob: 5, rr: [0.01488513]
Best | t1: 1660, t2: 60, os: 60, ob: 35, rr: [0.11808042]
Best | t1: 1680, t2: 60, os: 5, ob: 65, rr: [0.03868309]
Best | t1: 1700, t2: 60, os: 5, ob: 40, rr: [0.01390469]
Best | t1: 1720, t2: 60, os: 0, ob: 15, rr: [7.44055851e-05]
Best | t1: 1740, t2: 60, os: 5, ob: 20, rr: [0.02819626]
Best | t1: 1760, t2: 60, os: 5, ob: 50, rr: [0.13325341]
Best | t1: 1780, t2: 60, os: 5, ob: 50, rr: [0.09686449]
Best | t1: 1800, t2: 60, os: 5, ob: 0, rr: [0.05482882]
Best | t1: 1820, t2: 60, os: 0, ob: 0, rr: [0.01043227]
Best | t1: 1840, t2: 60, os: 15, ob: 5, rr: [0.00845621]
Best | t1: 1860, t2: 60, os: 0, ob: 5, rr: [-0.01858463]
Best | t1: 1880, t2: 60, os: 30, ob: 45, rr: [0.03543917]
Best | t1: 1900, t2: 60, os: 25, ob: 40, rr: [0.02246381]
Best | t1: 1920, t2: 60, os: 20, ob: 65, rr: [0.06240605]
Best | t1: 1940, t2: 60, os: 5, ob: 65, rr: [0.04517606]
Best | t1: 1960, t2: 60, os: 5, ob: 0, rr: [0.02980323]
Best | t1: 1980, t2: 60, os: 10, ob: 30, rr: [0.04376489]
Best | t1: 2000, t2: 60, os: 10, ob: 30, rr: [0.02888744]
Best | t1: 2020, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 2040, t2: 60, os: 5, ob: 55, rr: [0.01951958]
Best | t1: 2060, t2: 60, os: 40, ob: 55, rr: [0.04055091]
Best | t1: 2080, t2: 60, os: 50, ob: 0, rr: [0.09098158]
Best | t1: 2100, t2: 60, os: 35, ob: 75, rr: [0.05551024]
Best | t1: 2120, t2: 60, os: 5, ob: 50, rr: [0.07587376]
Best | t1: 2140, t2: 60, os: 60, ob: 55, rr: [0.05322043]
Best | t1: 2160, t2: 60, os: 5, ob: 55, rr: [0.07693793]
Best | t1: 2180, t2: 60, os: 55, ob: 5, rr: [0.02497783]
Best | t1: 2200, t2: 60, os: 10, ob: 5, rr: [0.0426667]
Best | t1: 2220, t2: 60, os: 10, ob: 5, rr: [0.02843165]
Best | t1: 2240, t2: 60, os: 50, ob: 35, rr: [0.02181461]
Best | t1: 2260, t2: 60, os: 15, ob: 50, rr: [0.08410526]
Best | t1: 2280, t2: 60, os: 0, ob: 35, rr: [0.04826952]
Best | t1: 2300, t2: 60, os: 5, ob: 30, rr: [0.02256942]
Best | t1: 2320, t2: 60, os: 5, ob: 20, rr: [0.01516509]
Best | t1: 2340, t2: 60, os: 80, ob: 0, rr: [0.01376591]
Best | t1: 2360, t2: 60, os: 5, ob: 50, rr: [0.08550192]
Best | t1: 2380, t2: 60, os: 5, ob: 65, rr: [0.04578755]
Best | t1: 2400, t2: 60, os: 10, ob: 15, rr: [0.03254195]
Best | t1: 2420, t2: 60, os: 10, ob: 35, rr: [0.04881453]
Best | t1: 2440, t2: 60, os: 0, ob: 35, rr: [0.0084428]
Best | t1: 2460, t2: 60, os: 15, ob: 55, rr: [0.06368161]
Best | t1: 2480, t2: 60, os: 0, ob: 35, rr: [-0.00375236]
Best | t1: 2500, t2: 60, os: 15, ob: 0, rr: [-0.02513068]
Best | t1: 2520, t2: 60, os: 60, ob: 45, rr: [0.07602991]
Best | t1: 2540, t2: 60, os: 0, ob: 35, rr: [0.07171715]
Best | t1: 2560, t2: 60, os: 0, ob: 55, rr: [0.09475025]
Best | t1: 2580, t2: 60, os: 5, ob: 20, rr: [0.07731184]
Best | t1: 2600, t2: 60, os: 0, ob: 0, rr: [-0.00741845]
Best | t1: 2620, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 2640, t2: 60, os: 5, ob: 25, rr: [0.00127891]
Best | t1: 2660, t2: 60, os: 60, ob: 45, rr: [0.11980984]
Best | t1: 2680, t2: 60, os: 5, ob: 55, rr: [0.15425532]
Best | t1: 2700, t2: 60, os: 5, ob: 25, rr: [0.10052851]
Best | t1: 2720, t2: 60, os: 5, ob: 25, rr: [0.04160434]
Best | t1: 2740, t2: 60, os: 15, ob: 30, rr: [0.04510404]
Best | t1: 2760, t2: 60, os: 5, ob: 30, rr: [0.1069457]
Best | t1: 2780, t2: 60, os: 5, ob: 0, rr: [-0.05202355]
Best | t1: 2800, t2: 60, os: 0, ob: 0, rr: [-0.02290572]
Best | t1: 2820, t2: 60, os: 5, ob: 25, rr: [0.08384266]
Best | t1: 2840, t2: 60, os: 0, ob: 30, rr: [0.01061228]
Best | t1: 2860, t2: 60, os: 5, ob: 5, rr: [0.04400555]
Best | t1: 2880, t2: 60, os: 5, ob: 30, rr: [0.05814901]
Best | t1: 2900, t2: 60, os: 5, ob: 30, rr: [0.03332438]
Best | t1: 2920, t2: 60, os: 70, ob: 65, rr: [0.07097415]
Best | t1: 2940, t2: 60, os: 20, ob: 70, rr: [0.1115399]
Best | t1: 2960, t2: 60, os: 10, ob: 65, rr: [0.06991152]
Best | t1: 2980, t2: 60, os: 10, ob: 55, rr: [0.02395989]
Best | t1: 3000, t2: 60, os: 5, ob: 55, rr: [0.07054758]
Best | t1: 3020, t2: 60, os: 5, ob: 60, rr: [0.07149495]
Best | t1: 3040, t2: 60, os: 5, ob: 75, rr: [0.08506767]
Best | t1: 3060, t2: 60, os: 0, ob: 60, rr: [0.14362802]
Best | t1: 3080, t2: 60, os: 5, ob: 5, rr: [0.09579805]
Best | t1: 3100, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 3120, t2: 60, os: 15, ob: 0, rr: [0.04026044]
Best | t1: 3140, t2: 60, os: 10, ob: 40, rr: [0.06049628]
Best | t1: 3160, t2: 60, os: 25, ob: 45, rr: [0.02079282]
Best | t1: 3180, t2: 60, os: 25, ob: 0, rr: [0.06577534]
Best | t1: 3200, t2: 60, os: 25, ob: 40, rr: [0.07089364]
Best | t1: 3220, t2: 60, os: 10, ob: 40, rr: [0.01498451]
Best | t1: 3240, t2: 60, os: 35, ob: 45, rr: [0.03348332]
Best | t1: 3260, t2: 60, os: 30, ob: 45, rr: [0.14938284]
Best | t1: 3280, t2: 60, os: 50, ob: 40, rr: [0.11844388]
Best | t1: 3300, t2: 60, os: 15, ob: 55, rr: [0.13440375]
Best | t1: 3320, t2: 60, os: 5, ob: 60, rr: [0.0809365]
Best | t1: 3340, t2: 60, os: 5, ob: 0, rr: [0.20932205]
Best | t1: 3360, t2: 60, os: 40, ob: 0, rr: [0.25702226]
Best | t1: 3380, t2: 60, os: 15, ob: 45, rr: [0.22541607]
Best | t1: 3400, t2: 60, os: 15, ob: 60, rr: [0.1295582]
Best | t1: 3420, t2: 60, os: 10, ob: 40, rr: [0.04895604]
Best | t1: 3440, t2: 60, os: 10, ob: 25, rr: [0.21294274]
Best | t1: 3460, t2: 60, os: 5, ob: 0, rr: [0.16218156]
Best | t1: 3480, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 3500, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 3520, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 3540, t2: 60, os: 0, ob: 10, rr: [-0.00241593]
Best | t1: 3560, t2: 60, os: 0, ob: 10, rr: [-0.00241593]
Best | t1: 3580, t2: 60, os: 0, ob: 0, rr: [-0.02118571]
Best | t1: 3600, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 3620, t2: 60, os: 45, ob: 60, rr: [0.03326044]
Best | t1: 3640, t2: 60, os: 25, ob: 55, rr: [0.13856189]
Best | t1: 3644, t2: 60, os: 0, ob: 50, rr: [0.26270276]
'''
'''
False

results
Test file: ../0050.TW.csv, time length: 3644
Test param | os: [0, 100], ob: [0, 100]
time lengths: [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1020, 1040, 1060, 1080, 1100, 1120, 1140, 1160, 1180, 1200, 1220, 1240, 1260, 1280, 1300, 1320, 1340, 1360, 1380, 1400, 1420, 1440, 1460, 1480, 1500, 1520, 1540, 1560, 1580, 1600, 1620, 1640, 1660, 1680, 1700, 1720, 1740, 1760, 1780, 1800, 1820, 1840, 1860, 1880, 1900, 1920, 1940, 1960, 1980, 2000, 2020, 2040, 2060, 2080, 2100, 2120, 2140, 2160, 2180, 2200, 2220, 2240, 2260, 2280, 2300, 2320, 2340, 2360, 2380, 2400, 2420, 2440, 2460, 2480, 2500, 2520, 2540, 2560, 2580, 2600, 2620, 2640, 2660, 2680, 2700, 2720, 2740, 2760, 2780, 2800, 2820, 2840, 2860, 2880, 2900, 2920, 2940, 2960, 2980, 3000, 3020, 3040, 3060, 3080, 3100, 3120, 3140, 3160, 3180, 3200, 3220, 3240, 3260, 3280, 3300, 3320, 3340, 3360, 3380, 3400, 3420, 3440, 3460, 3480, 3500, 3520, 3540, 3560, 3580, 3600, 3620, 3640, 3644]
Best | t1: 60, t2: 60, os: 0, ob: 0, rr: [-0.06555641]
Best | t1: 80, t2: 60, os: 0, ob: 0, rr: [0.00268088]
Best | t1: 100, t2: 60, os: 0, ob: 0, rr: [0.07897225]
Best | t1: 120, t2: 60, os: 0, ob: 0, rr: [0.03583036]
Best | t1: 140, t2: 60, os: 0, ob: 0, rr: [-2.55600311e-05]
Best | t1: 160, t2: 60, os: 0, ob: 0, rr: [-0.06274102]
Best | t1: 180, t2: 60, os: 0, ob: 0, rr: [-0.05554624]
Best | t1: 200, t2: 60, os: 0, ob: 0, rr: [-0.06708512]
Best | t1: 220, t2: 60, os: 0, ob: 0, rr: [0.00447546]
Best | t1: 240, t2: 60, os: 0, ob: 0, rr: [0.02398442]
Best | t1: 260, t2: 60, os: 0, ob: 0, rr: [0.04163751]
Best | t1: 280, t2: 60, os: 0, ob: 0, rr: [0.06137245]
Best | t1: 300, t2: 60, os: 0, ob: 0, rr: [-0.00122073]
Best | t1: 320, t2: 60, os: 0, ob: 0, rr: [-0.00538739]
Best | t1: 340, t2: 60, os: 0, ob: 0, rr: [0.00950256]
Best | t1: 360, t2: 60, os: 0, ob: 0, rr: [0.03201668]
Best | t1: 380, t2: 60, os: 0, ob: 0, rr: [-0.02336872]
Best | t1: 400, t2: 60, os: 0, ob: 0, rr: [-0.0087301]
Best | t1: 420, t2: 60, os: 0, ob: 0, rr: [0.04375502]
Best | t1: 440, t2: 60, os: 0, ob: 0, rr: [0.02101979]
Best | t1: 460, t2: 60, os: 0, ob: 0, rr: [0.15876859]
Best | t1: 480, t2: 60, os: 0, ob: 0, rr: [0.0665521]
Best | t1: 500, t2: 60, os: 0, ob: 0, rr: [0.10919071]
Best | t1: 520, t2: 60, os: 0, ob: 0, rr: [0.06231547]
Best | t1: 540, t2: 60, os: 0, ob: 0, rr: [-0.00901741]
Best | t1: 560, t2: 60, os: 0, ob: 0, rr: [0.00329512]
Best | t1: 580, t2: 60, os: 0, ob: 0, rr: [0.02686567]
Best | t1: 600, t2: 60, os: 0, ob: 0, rr: [0.12230806]
Best | t1: 620, t2: 60, os: 0, ob: 0, rr: [0.05584154]
Best | t1: 640, t2: 60, os: 0, ob: 0, rr: [0.01658577]
Best | t1: 660, t2: 60, os: 0, ob: 0, rr: [0.10724861]
Best | t1: 680, t2: 60, os: 0, ob: 0, rr: [0.06122904]
Best | t1: 700, t2: 60, os: 0, ob: 0, rr: [-0.05541096]
Best | t1: 720, t2: 60, os: 0, ob: 0, rr: [-0.01631971]
Best | t1: 740, t2: 60, os: 0, ob: 0, rr: [0.01916373]
Best | t1: 760, t2: 60, os: 0, ob: 0, rr: [0.02181822]
Best | t1: 780, t2: 60, os: 0, ob: 0, rr: [0.05969849]
Best | t1: 800, t2: 60, os: 0, ob: 0, rr: [0.02707618]
Best | t1: 820, t2: 60, os: 0, ob: 0, rr: [-0.00844514]
Best | t1: 840, t2: 60, os: 0, ob: 0, rr: [-0.01042708]
Best | t1: 860, t2: 60, os: 0, ob: 0, rr: [0.00370791]
Best | t1: 880, t2: 60, os: 0, ob: 0, rr: [-0.00712483]
Best | t1: 900, t2: 60, os: 0, ob: 0, rr: [0.03714267]
Best | t1: 920, t2: 60, os: 0, ob: 0, rr: [0.05899799]
Best | t1: 940, t2: 60, os: 0, ob: 0, rr: [0.02527613]
Best | t1: 960, t2: 60, os: 0, ob: 0, rr: [-0.02244202]
Best | t1: 980, t2: 60, os: 0, ob: 0, rr: [-0.0504582]
Best | t1: 1000, t2: 60, os: 0, ob: 0, rr: [-0.05919742]
Best | t1: 1020, t2: 60, os: 0, ob: 0, rr: [-0.06638261]
Best | t1: 1040, t2: 60, os: 0, ob: 0, rr: [-0.07973672]
Best | t1: 1060, t2: 60, os: 0, ob: 0, rr: [0.03612103]
Best | t1: 1080, t2: 60, os: 0, ob: 0, rr: [-0.01895547]
Best | t1: 1100, t2: 60, os: 0, ob: 0, rr: [-0.02002894]
Best | t1: 1120, t2: 60, os: 0, ob: 0, rr: [0.02287301]
Best | t1: 1140, t2: 60, os: 0, ob: 0, rr: [0.01538062]
Best | t1: 1160, t2: 60, os: 0, ob: 0, rr: [0.02227392]
Best | t1: 1180, t2: 60, os: 0, ob: 0, rr: [0.03307794]
Best | t1: 1200, t2: 60, os: 0, ob: 0, rr: [0.01565098]
Best | t1: 1220, t2: 60, os: 0, ob: 0, rr: [-0.00445185]
Best | t1: 1240, t2: 60, os: 0, ob: 0, rr: [-0.00802577]
Best | t1: 1260, t2: 60, os: 0, ob: 0, rr: [0.01021437]
Best | t1: 1280, t2: 60, os: 0, ob: 0, rr: [0.0073651]
Best | t1: 1300, t2: 60, os: 0, ob: 0, rr: [0.01097362]
Best | t1: 1320, t2: 60, os: 0, ob: 0, rr: [0.01042019]
Best | t1: 1340, t2: 60, os: 0, ob: 0, rr: [0.07071302]
Best | t1: 1360, t2: 60, os: 0, ob: 0, rr: [0.09737296]
Best | t1: 1380, t2: 60, os: 0, ob: 0, rr: [0.0292493]
Best | t1: 1400, t2: 60, os: 0, ob: 0, rr: [-0.00553036]
Best | t1: 1420, t2: 60, os: 0, ob: 0, rr: [-0.00966138]
Best | t1: 1440, t2: 60, os: 0, ob: 0, rr: [-0.00187675]
Best | t1: 1460, t2: 60, os: 0, ob: 0, rr: [0.00361296]
Best | t1: 1480, t2: 60, os: 0, ob: 0, rr: [-0.03259772]
Best | t1: 1500, t2: 60, os: 0, ob: 0, rr: [-0.05062622]
Best | t1: 1520, t2: 60, os: 0, ob: 0, rr: [0.03166017]
Best | t1: 1540, t2: 60, os: 0, ob: 0, rr: [0.0348625]
Best | t1: 1560, t2: 60, os: 0, ob: 0, rr: [0.05701229]
Best | t1: 1580, t2: 60, os: 0, ob: 0, rr: [0.06143106]
Best | t1: 1600, t2: 60, os: 0, ob: 0, rr: [0.07640974]
Best | t1: 1620, t2: 60, os: 0, ob: 0, rr: [0.04752363]
Best | t1: 1640, t2: 60, os: 0, ob: 0, rr: [-0.00158511]
Best | t1: 1660, t2: 60, os: 0, ob: 0, rr: [0.08553371]
Best | t1: 1680, t2: 60, os: 0, ob: 0, rr: [0.02132974]
Best | t1: 1700, t2: 60, os: 0, ob: 0, rr: [-0.02275549]
Best | t1: 1720, t2: 60, os: 0, ob: 0, rr: [-0.07935544]
Best | t1: 1740, t2: 60, os: 0, ob: 0, rr: [-0.04173255]
Best | t1: 1760, t2: 60, os: 0, ob: 0, rr: [0.07098449]
Best | t1: 1780, t2: 60, os: 0, ob: 0, rr: [0.07129727]
Best | t1: 1800, t2: 60, os: 0, ob: 0, rr: [0.02479837]
Best | t1: 1820, t2: 60, os: 0, ob: 0, rr: [-0.00766853]
Best | t1: 1840, t2: 60, os: 0, ob: 0, rr: [-0.00660196]
Best | t1: 1860, t2: 60, os: 0, ob: 0, rr: [-0.04287332]
Best | t1: 1880, t2: 60, os: 0, ob: 0, rr: [0.00258834]
Best | t1: 1900, t2: 60, os: 0, ob: 0, rr: [-0.0136617]
Best | t1: 1920, t2: 60, os: 0, ob: 0, rr: [0.01794005]
Best | t1: 1940, t2: 60, os: 0, ob: 0, rr: [0.0410344]
Best | t1: 1960, t2: 60, os: 0, ob: 0, rr: [-0.0003451]
Best | t1: 1980, t2: 60, os: 0, ob: 0, rr: [0.00617039]
Best | t1: 2000, t2: 60, os: 0, ob: 0, rr: [0.01081573]
Best | t1: 2020, t2: 60, os: 0, ob: 0, rr: [-0.03035129]
Best | t1: 2040, t2: 60, os: 0, ob: 0, rr: [-0.04801911]
Best | t1: 2060, t2: 60, os: 0, ob: 0, rr: [0.02119083]
Best | t1: 2080, t2: 60, os: 0, ob: 0, rr: [0.09098158]
Best | t1: 2100, t2: 60, os: 0, ob: 0, rr: [0.00374264]
Best | t1: 2120, t2: 60, os: 0, ob: 0, rr: [0.02636342]
Best | t1: 2140, t2: 60, os: 0, ob: 0, rr: [0.00877777]
Best | t1: 2160, t2: 60, os: 0, ob: 0, rr: [0.01084393]
Best | t1: 2180, t2: 60, os: 0, ob: 0, rr: [0.01614033]
Best | t1: 2200, t2: 60, os: 0, ob: 0, rr: [0.03636383]
Best | t1: 2220, t2: 60, os: 0, ob: 0, rr: [0.02567196]
Best | t1: 2240, t2: 60, os: 0, ob: 0, rr: [0.00345941]
Best | t1: 2260, t2: 60, os: 0, ob: 0, rr: [0.03582956]
Best | t1: 2280, t2: 60, os: 0, ob: 0, rr: [0.0124193]
Best | t1: 2300, t2: 60, os: 0, ob: 0, rr: [-0.01881231]
Best | t1: 2320, t2: 60, os: 0, ob: 0, rr: [0.00461455]
Best | t1: 2340, t2: 60, os: 0, ob: 0, rr: [0.01376591]
Best | t1: 2360, t2: 60, os: 0, ob: 0, rr: [0.01573351]
Best | t1: 2380, t2: 60, os: 0, ob: 0, rr: [-0.01338322]
Best | t1: 2400, t2: 60, os: 0, ob: 0, rr: [-0.00916121]
Best | t1: 2420, t2: 60, os: 0, ob: 0, rr: [0.02903555]
Best | t1: 2440, t2: 60, os: 0, ob: 0, rr: [-0.00842292]
Best | t1: 2460, t2: 60, os: 0, ob: 0, rr: [0.03688619]
Best | t1: 2480, t2: 60, os: 0, ob: 0, rr: [-0.01805436]
Best | t1: 2500, t2: 60, os: 0, ob: 0, rr: [-0.03216712]
Best | t1: 2520, t2: 60, os: 0, ob: 0, rr: [0.0461276]
Best | t1: 2540, t2: 60, os: 0, ob: 0, rr: [0.02065394]
Best | t1: 2560, t2: 60, os: 0, ob: 0, rr: [0.05676813]
Best | t1: 2580, t2: 60, os: 0, ob: 0, rr: [0.03073762]
Best | t1: 2600, t2: 60, os: 0, ob: 0, rr: [-0.08398364]
Best | t1: 2620, t2: 60, os: 0, ob: 0, rr: [-0.0737125]
Best | t1: 2640, t2: 60, os: 0, ob: 0, rr: [-0.05313899]
Best | t1: 2660, t2: 60, os: 0, ob: 0, rr: [0.05618637]
Best | t1: 2680, t2: 60, os: 0, ob: 0, rr: [0.06601125]
Best | t1: 2700, t2: 60, os: 0, ob: 0, rr: [-0.02141332]
Best | t1: 2720, t2: 60, os: 0, ob: 0, rr: [-0.07697105]
Best | t1: 2740, t2: 60, os: 0, ob: 0, rr: [-0.01469297]
Best | t1: 2760, t2: 60, os: 0, ob: 0, rr: [0.05795853]
Best | t1: 2780, t2: 60, os: 0, ob: 0, rr: [-0.05843287]
Best | t1: 2800, t2: 60, os: 0, ob: 0, rr: [-0.02947835]
Best | t1: 2820, t2: 60, os: 0, ob: 0, rr: [-0.00233305]
Best | t1: 2840, t2: 60, os: 0, ob: 0, rr: [-0.06140467]
Best | t1: 2860, t2: 60, os: 0, ob: 0, rr: [0.00887443]
Best | t1: 2880, t2: 60, os: 0, ob: 0, rr: [0.0406005]
Best | t1: 2900, t2: 60, os: 0, ob: 0, rr: [-0.01711207]
Best | t1: 2920, t2: 60, os: 0, ob: 0, rr: [0.06839179]
Best | t1: 2940, t2: 60, os: 0, ob: 0, rr: [0.05506599]
Best | t1: 2960, t2: 60, os: 0, ob: 0, rr: [0.01995106]
Best | t1: 2980, t2: 60, os: 0, ob: 0, rr: [-0.01599824]
Best | t1: 3000, t2: 60, os: 0, ob: 0, rr: [0.02647496]
Best | t1: 3020, t2: 60, os: 0, ob: 0, rr: [0.03754713]
Best | t1: 3040, t2: 60, os: 0, ob: 0, rr: [0.01828773]
Best | t1: 3060, t2: 60, os: 0, ob: 0, rr: [0.04301954]
Best | t1: 3080, t2: 60, os: 0, ob: 0, rr: [0.040109]
Best | t1: 3100, t2: 60, os: 0, ob: 0, rr: [-0.07554448]
Best | t1: 3120, t2: 60, os: 0, ob: 0, rr: [0.0336994]
Best | t1: 3140, t2: 60, os: 0, ob: 0, rr: [0.02546615]
Best | t1: 3160, t2: 60, os: 0, ob: 0, rr: [-0.01371989]
Best | t1: 3180, t2: 60, os: 0, ob: 0, rr: [0.03944601]
Best | t1: 3200, t2: 60, os: 0, ob: 0, rr: [0.00573038]
Best | t1: 3220, t2: 60, os: 0, ob: 0, rr: [-0.01972435]
Best | t1: 3240, t2: 60, os: 0, ob: 0, rr: [0.02186999]
Best | t1: 3260, t2: 60, os: 0, ob: 0, rr: [0.11218778]
Best | t1: 3280, t2: 60, os: 0, ob: 0, rr: [0.09348356]
Best | t1: 3300, t2: 60, os: 0, ob: 0, rr: [0.00740851]
Best | t1: 3320, t2: 60, os: 0, ob: 0, rr: [-0.00851865]
Best | t1: 3340, t2: 60, os: 0, ob: 0, rr: [0.16277136]
Best | t1: 3360, t2: 60, os: 0, ob: 0, rr: [0.25702226]
Best | t1: 3380, t2: 60, os: 0, ob: 0, rr: [0.05212331]
Best | t1: 3400, t2: 60, os: 0, ob: 0, rr: [-0.28641496]
Best | t1: 3420, t2: 60, os: 0, ob: 0, rr: [-0.40972713]
Best | t1: 3440, t2: 60, os: 0, ob: 0, rr: [-0.02329278]
Best | t1: 3460, t2: 60, os: 0, ob: 0, rr: [0.16218156]
Best | t1: 3480, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 3500, t2: 60, os: 0, ob: 0, rr: [-0.37322585]
Best | t1: 3520, t2: 60, os: 0, ob: 0, rr: [0.]
Best | t1: 3540, t2: 60, os: 0, ob: 0, rr: [-0.04282404]
Best | t1: 3560, t2: 60, os: 0, ob: 0, rr: [-0.14712313]
Best | t1: 3580, t2: 60, os: 0, ob: 0, rr: [-0.14254706]
Best | t1: 3600, t2: 60, os: 0, ob: 0, rr: [-0.06640193]
Best | t1: 3620, t2: 60, os: 0, ob: 0, rr: [-0.07009916]
Best | t1: 3640, t2: 60, os: 0, ob: 0, rr: [-0.02284502]
Best | t1: 3644, t2: 60, os: 0, ob: 0, rr: [0.10335613]
'''
