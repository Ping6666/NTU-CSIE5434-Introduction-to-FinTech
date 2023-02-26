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


def main():
    print('***Datasets***')
    ((((ccba_x_t, ccba_y_t, ccba_ak_t), (cdtx_x_t, cdtx_y_t, cdtx_ak_t),
       (dp_x_t, dp_y_t, dp_ak_t), (remit_x_t, remit_y_t, remit_ak_t)),
      ((ccba_x_all, _, ccba_ak_all), (cdtx_x_all, _, cdtx_ak_all),
       (dp_x_all, _, dp_ak_all), (remit_x_all, _, remit_ak_all))),
     ((rt_x_t, rt_y_t, rt_ak_t), (rt_x_all, _, rt_ak_all))) = d.do_workhouse()

    print('***Training***')
    ccba_ensemble = m.ensemble_workhouse()
    print('ccba_x_t', ccba_x_t.columns.tolist())
    ccba_model = ccba_ensemble.fit(ccba_x_t, ccba_y_t)

    cdtx_ensemble = m.ensemble_workhouse()
    print('cdtx_x_t', cdtx_x_t.columns.tolist())
    cdtx_model = cdtx_ensemble.fit(cdtx_x_t, cdtx_y_t)

    dp_ensemble = m.ensemble_workhouse()
    print('dp_x_t', dp_x_t.columns.tolist())
    dp_model = dp_ensemble.fit(dp_x_t, dp_y_t)

    remit_ensemble = m.ensemble_workhouse()
    print('remit_x_t', remit_x_t.columns.tolist())
    remit_model = remit_ensemble.fit(remit_x_t, remit_y_t)

    print('***Final Training***')
    # predict
    ccba_y_pred_t = ccba_model.predict(ccba_x_t)
    cdtx_y_pred_t = cdtx_model.predict(cdtx_x_t)
    dp_y_pred_t = dp_model.predict(dp_x_t)
    remit_y_pred_t = remit_model.predict(remit_x_t)

    # convert 2d-like list to 1d list (w/ seq. right)
    ccba_y_pred_t_adj = d.get_ak_adj_list(ccba_ak_t, ccba_y_pred_t, rt_ak_t)
    cdtx_y_pred_t_adj = d.get_ak_adj_list(cdtx_ak_t, cdtx_y_pred_t, rt_ak_t)
    dp_y_pred_t_adj = d.get_ak_adj_list(dp_ak_t, dp_y_pred_t, rt_ak_t)
    remit_y_pred_t_adj = d.get_ak_adj_list(remit_ak_t, remit_y_pred_t, rt_ak_t)

    # set to the dataset
    rt_x_t['ccba'] = ccba_y_pred_t_adj
    rt_x_t['cdtx0001'] = cdtx_y_pred_t_adj
    rt_x_t['dp'] = dp_y_pred_t_adj
    rt_x_t['remit1'] = remit_y_pred_t_adj

    c_ensemble = m.ensemble_workhouse()
    print('rt_x_t', rt_x_t.columns.tolist())
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
    # predict
    ccba_y_pred_all = ccba_model.predict(ccba_x_all)
    cdtx_y_pred_all = cdtx_model.predict(cdtx_x_all)
    dp_y_pred_all = dp_model.predict(dp_x_all)
    remit_y_pred_all = remit_model.predict(remit_x_all)

    # convert 2d-like list to 1d list (w/ seq. right)
    ccba_y_pred_all_adj = d.get_ak_adj_list(ccba_ak_all, ccba_y_pred_all,
                                            rt_ak_all)
    cdtx_y_pred_all_adj = d.get_ak_adj_list(cdtx_ak_all, cdtx_y_pred_all,
                                            rt_ak_all)
    dp_y_pred_all_adj = d.get_ak_adj_list(dp_ak_all, dp_y_pred_all, rt_ak_all)
    remit_y_pred_all_adj = d.get_ak_adj_list(remit_ak_all, remit_y_pred_all,
                                             rt_ak_all)

    # set to the dataset
    rt_x_all['ccba'] = ccba_y_pred_all_adj
    rt_x_all['cdtx0001'] = cdtx_y_pred_all_adj
    rt_x_all['dp'] = dp_y_pred_all_adj
    rt_x_all['remit1'] = remit_y_pred_all_adj

    print('***Final predict on test***')

    y_pred_all = c_model.predict(rt_x_all)
    printer_unique_counter(y_pred_all, 'distribution of predict on all:')

    print('***Predict on final test***')
    df_pred = d.get_answer_form(rt_ak_all, y_pred_all)
    df_submit = d.get_submit(df_pred, './pred.csv')

    printer_unique_counter(df_submit['probability'], 'distribution of submit:')

    print('GOOD')

    return


if __name__ == '__main__':
    main()
