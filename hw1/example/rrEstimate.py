# How to invoke this program:
# 	python rrEstimate.py SPY.csv
import sys
import numpy as np
import pandas as pd
from myStrategy import myStrategy


# Estimate return rate over a given price vector
def rrEstimate(priceVec):
    # Initial available capital
    capital = 1000
    # original capital
    capitalOrig = capital
    # day size
    dataCount = len(priceVec)

    # suggested actions
    suggestedAction = np.zeros((dataCount, 1))
    # stock holdings
    stockHolding = np.zeros((dataCount, 1))
    # total asset
    total = np.zeros((dataCount, 1))

    # Real action, which might be different from suggested action.
    # For instance, when the suggested action is 1 (buy) but you don't have any capital,
    # then the real action is 0 (hold, or do nothing).
    realAction = np.zeros((dataCount, 1))

    # Run through each day
    for ic in range(dataCount):
        # current price
        currentPrice = priceVec[ic]
        # Obtain the suggested action
        suggestedAction[ic] = myStrategy(priceVec[0:ic], currentPrice)

        # get real action by suggested action
        if ic > 0:
            # The stock holding from the previous day
            stockHolding[ic] = stockHolding[ic - 1]
        if suggestedAction[ic] == 1:
            # Suggested action is "buy"

            if stockHolding[ic] == 0:
                # "buy" only if you don't have stock holding

                # Buy stock using cash
                stockHolding[ic] = capital / currentPrice

                # Cash
                capital = 0

                realAction[ic] = 1
        elif suggestedAction[ic] == -1:
            # Suggested action is "sell"

            if stockHolding[ic] > 0:
                # "sell" only if you have stock holding

                # Sell stock to have cash
                capital = stockHolding[ic] * currentPrice

                # Stocking holding
                stockHolding[ic] = 0

                realAction[ic] = -1
        elif suggestedAction[ic] == 0:
            # No action
            realAction[ic] = 0
        else:
            assert False
        # Total asset, including stock holding and cash
        total[ic] = capital + stockHolding[ic] * currentPrice
    # Return rate of this run
    returnRate = (total[-1] - capitalOrig) / capitalOrig
    return returnRate


if __name__ == "__main__":
    # input file
    file = sys.argv[1]
    df = pd.read_csv(file)

    # Get adj close as the price vector
    priceVec = df["Adj Close"].values

    # Compute return rate
    rr = rrEstimate(priceVec)
    print("rr=%f%%" % (rr * 100))
