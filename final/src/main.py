import numpy as np
import pandas as pd

from sklearn import metrics, ensemble

import data as d
import model as m


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


def train(c_ensemble, x, y):

    return


def main():
    (((ccba_x_t, ccba_y_t, ccba_ak_t), (cdtx_x_t, cdtx_y_t, cdtx_ak_t),
      (dp_x_t, dp_y_t, dp_ak_t), (remit_x_t, remit_y_t, remit_ak_t)),
     ((ccba_x_all, _, ccba_ak_all), (cdtx_x_all, _, cdtx_ak_all),
      (dp_x_all, _, dp_ak_all), (remit_x_all, _,
                                 remit_ak_all))) = d.df_workhouse()

    print('***Training***')
    ccba_ensemble = m.ensemble_workhouse()
    ccba_model = ccba_ensemble.fit(ccba_x_t, ccba_y_t)

    cdtx_ensemble = m.ensemble_workhouse()
    cdtx_model = cdtx_ensemble.fit(cdtx_x_t, cdtx_y_t)

    dp_ensemble = m.ensemble_workhouse()
    dp_model = dp_ensemble.fit(dp_x_t, dp_y_t)

    remit_ensemble = m.ensemble_workhouse()
    remit_model = remit_ensemble.fit(remit_x_t, remit_y_t)

    print('GOOD')
    exit(0)

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
