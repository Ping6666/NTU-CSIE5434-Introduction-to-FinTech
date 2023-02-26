import numpy as np
import pandas as pd

from sklearn import metrics, ensemble

import data as d


def ensemble_workhouse():
    # NOT GOOD ??? #
    # c_ensemble = ensemble.AdaBoostRegressor(n_estimators=200, learning_rate=1)

    # NOT GOOD ??? #
    # but output with -1 or 1
    # c_ensemble = ensemble.IsolationForest(n_estimators=200)

    # NOT GOOD ??? #
    # but output between -1 or 1
    # c_ensemble = ensemble.HistGradientBoostingRegressor(learning_rate=1)

    # VERY GOOD ??? #
    # given (train_y_pred >= 0.1).astype(int)
    # accuracy: 1.0
    # precision: 1.0
    # recall: 1.0
    # f1: 1.0
    # r2: 1.0
    # c_ensemble = ensemble.ExtraTreesRegressor(n_estimators=200)

    # GOOD ??? #
    # given (train_y_pred >= 0.1).astype(int)
    # accuracy: 0.9961934242449594
    # precision: 0.72
    # recall: 1.0
    # f1: 0.8372093023255813
    # r2: 0.6072669069880966
    c_ensemble = ensemble.RandomForestRegressor(n_estimators=200)

    # GOOD ??? #
    # given (train_y_pred >= 0.1).astype(int)
    # accuracy: 0.9961097632393542
    # precision: 0.7155963302752294
    # recall: 1.0
    # f1: 0.8342245989304813
    # r2: 0.5986354104383844
    # c_ensemble = ensemble.BaggingRegressor(n_estimators=200)

    # GOOD ??? #
    # but output between -1 or 1
    # c_ensemble = ensemble.GradientBoostingRegressor(n_estimators=200,
    #                                                 learning_rate=1)
    return c_ensemble


def printer_unique_counter(n: np.ndarray, pre_str: str = None):
    unique, counts = np.unique(n, return_counts=True)
    if pre_str != None:
        print(pre_str, end=' ')
    print(dict(zip(unique, counts)))
    return


def printer_metrics(y_true, y_pred):
    print("accuracy:", metrics.accuracy_score(y_true, y_pred))
    print("precision:", metrics.precision_score(y_true, y_pred))
    print("recall:", metrics.recall_score(y_true, y_pred))
    print("f1:", metrics.f1_score(y_true, y_pred))
    print("r2:", metrics.r2_score(y_true, y_pred))
    print()
    return


def main():
    (rt_x_t, rt_y_t, _), (rt_x_all, _, rt_ak_all) = d.df_workhouse()

    print('***Training***')
    c_ensemble = ensemble_workhouse()
    c_model = c_ensemble.fit(rt_x_t, rt_y_t)

    print('***Predict on train***')
    printer_unique_counter(rt_y_t, 'distribution of train data:')

    y_pred_t = c_model.predict(rt_x_t)
    printer_unique_counter(y_pred_t,
                           'distribution of predict on train (regression):')

    y_pred_t = (y_pred_t >= 0.5).astype(int)
    printer_unique_counter(
        y_pred_t, 'distribution of predict on train (classification):')

    printer_metrics(rt_y_t, y_pred_t)

    print('***Predict on test***')
    y_pred_all = c_model.predict(rt_x_all)
    printer_unique_counter(y_pred_all, 'distribution of predict on all:')

    print('***Predict on final test***')
    df_pred = d.get_answer_form(rt_ak_all, y_pred_all)
    df_submit = d.get_submit(df_pred, './pred.csv')

    printer_unique_counter(df_submit['probability'], 'distribution of submit:')
    return


if __name__ == '__main__':
    main()
