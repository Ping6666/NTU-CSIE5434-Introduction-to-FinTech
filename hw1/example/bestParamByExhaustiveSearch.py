import sys
import numpy as np
import pandas as pd


# Decision of the current day by the current price, with 3 modifiable parameters
def myStrategy(pastPriceVec, currentPrice, windowSize, alpha, beta):
    import numpy as np

    ## action ##
    # 1(buy), -1(sell), 0(hold), with 0 as the default action
    action = 0
    dataLen = len(pastPriceVec)
    if dataLen == 0:
        return action

    # Compute ma
    if dataLen < windowSize:
        # If given price vector is small than windowSize, compute MA by taking the average
        ma = np.mean(pastPriceVec)
    else:
        # Compute the normal MA using windowSize
        windowedData = pastPriceVec[-windowSize:]
        ma = np.mean(windowedData)

    # Determine action
    if (currentPrice - ma) > alpha:
        # If price-ma > alpha ==> buy
        action = 1
    elif (currentPrice - ma) < -beta:
        # If price-ma < -beta ==> sell
        action = -1
    return action


# Compute return rate over a given price vector, with 3 modifiable parameters
def computeReturnRate(priceVec, windowSize, alpha, beta):
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

    ## Real action ##
    # which might be different from suggested action.
    # For instance, when the suggested action is 1 (buy) but you don't have any capital,
    # then the real action is 0 (hold, or do nothing).
    realAction = np.zeros((dataCount, 1))

    # Run through each day
    for ic in range(dataCount):
        # current price
        currentPrice = priceVec[ic]
        # Obtain the suggested action
        suggestedAction[ic] = myStrategy(
            priceVec[0:ic], currentPrice, windowSize, alpha, beta
        )

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
    # Initial best return rate
    returnRateBest = -1.00
    # read stock file
    df = pd.read_csv(sys.argv[1])
    # get adj close as the price vector
    adjClose = df["Adj Close"].values

    # Range of windowSize to explore
    windowSizeMin = 11
    windowSizeMax = 20

    # Range of alpha to explore
    alphaMin = -5
    alphaMax = 5

    # Range of beta to explore
    betaMin = -5
    betaMax = 5

    # Start exhaustive search
    for windowSize in range(windowSizeMin, windowSizeMax + 1):
        print("windowSize=%d" % (windowSize))

        for alpha in range(alphaMin, alphaMax + 1):
            print("\talpha=%d" % (alpha))

            for beta in range(betaMin, betaMax + 1):
                print("\t\tbeta=%d" % (beta), end="")

                # Start the whole run with the given parameters
                returnRate = computeReturnRate(adjClose, windowSize, alpha, beta)
                print(" ==> returnRate=%f " % (returnRate))

                if returnRate > returnRateBest:
                    # Keep the best parameters
                    windowSizeBest = windowSize
                    alphaBest = alpha
                    betaBest = beta
                    returnRateBest = returnRate
    # Print the best result
    print(
        "Best settings: windowSize=%d, alpha=%d, beta=%d ==> returnRate=%f"
        % (windowSizeBest, alphaBest, betaBest, returnRateBest)
    )
