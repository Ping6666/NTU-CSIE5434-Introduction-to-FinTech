# Fintech HW1

## conda env

```
conda env -n fintech python=3.9.13
pip install numpy==1.23.1 pandas==1.5.0
conda install -c conda-forge ta-lib
```

## Question

In this homework, you need to design a trading strategy to maximize the return of stock trading over a future period of time.

- Target stock: 0050.TW
    - from [Yahoo Finance](https://finance.yahoo.com/quote/0050.TW/history?p=0050.TW)
    - We shall use the price of **Adj Close** for trading.
- Your trading strategy
    - Your trading strategy can only take the currently available historical data for reaching a decision of **buy** or **sell**.
    - Your strategy should based on technical indicators (MA, RSI, etc) for maximizing the return. (You can define your own technical indicators if necessary.)
    - Your strategy will be used to determine the return over the evaluation period from 2022/10/24 to 2022/12/23.
    - Here is a file list of example code for you to start with. [example code](./example/readme.txt)
- Submission
    - You only need to submit the function `myStrategy.py`.

### Constraint

#### TA judge system

```
OS:     Linux (Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-193-generic x86_64))
CPU:    Intel® Xeon® Silver 4116 CPU @ 2.10GHz
GPU:    Quadro GV100

python:         3.9.13
numpy:          1.23.1
pandas:         1.5.0
torch:          1.12.1
scipy:          1.9.1
talib:          0.4.19
scikit-learn:   1.1.2
```

#### Other Notes

- Each call to `myStrategy()` should last no more than **10 sec**, otherwise it will be killed and the output of the function is 0 by default. This function will be called by TA's program during each day of the evaluation period.
- You can try other complicated TIs (such as deep neural networks), but you should keep in mind that complicated models do not necessarily perform well for test data. You always need to strike a balance between model complexity and available data amount.
- Evaluation criteria:
    - 50%: Ranking in return rate
    - 50%: A PDF report describing your work on this HW.
        - 15%: The TIs you adopt and how do you use them.
        - 17%: What are the modified parameters of your strategy, and how do you fine tune the parameters.
        - 18%: Any other things you have done to optimize your strategy.

## my result

return rate (RR): 16.12%
