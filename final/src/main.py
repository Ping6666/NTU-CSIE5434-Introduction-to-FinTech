from typing import Tuple

import numpy as np

from sklearn import metrics, preprocessing

import data as d
import model as m


def printer_unique_counter(n: np.ndarray, pre_str: str = None):
    unique, counts = np.unique(n, return_counts=True)
    print(len(unique), end=' ')
    if pre_str != None:
        print(pre_str, end=' ')
    print(dict(zip(unique, counts)))
    return


def printer_recall_precision(y_true, y_pred):
    ## Recall@N-1 Precision ##
    # argsort (descending order)
    y_pred_argsort = np.argsort(-1 * y_pred)

    arg_ids = []
    for i, t in enumerate(y_true):
        if t == 1:
            # if got sar_flag, save the arg_id
            arg_ids.append(i)

    print('sar_flag: ', arg_ids)

    rp_ids = []
    for i, pa in enumerate(y_pred_argsort):
        if pa in arg_ids:
            # if should report sar_flag, save the report seq.
            rp_ids.append(i + 1)

    print('pred sar_flag: ', rp_ids)

    assert len(arg_ids) == len(rp_ids), 'sar_flag poison'

    if len(rp_ids) >= 2:
        rp_id = np.argsort(rp_ids)[-2]
        rp = rp_ids[rp_id]
        print("Recall@N-1 Precision", ((len(arg_ids) - 1) / rp))
    else:
        print("Recall@N-1 Precision fail to compute")
    print()

    return


def printer_metrics(y_true, y_pred):
    import warnings
    warnings.filterwarnings('ignore')

    print("accuracy:", metrics.accuracy_score(y_true, y_pred))
    print("precision:", metrics.precision_score(y_true, y_pred))
    print("recall:", metrics.recall_score(y_true, y_pred))
    print("f1:", metrics.f1_score(y_true, y_pred))
    print("r2:", metrics.r2_score(y_true, y_pred))
    print()
    return


def min_max(_y_pred):
    # make sure output in between 0~1
    mm_scaler = preprocessing.MinMaxScaler()
    y_pred = mm_scaler.fit_transform(_y_pred.reshape(-1, 1))
    y_pred = y_pred.reshape(-1, )
    return y_pred


def training(xs, ys, aks):
    # checker
    assert len(xs) == 5, 'xs must be len 5 tuple'
    assert len(ys) == 5, 'ys must be len 5 tuple'
    assert len(aks) == 5, 'aks must be len 5 tuple'

    # input
    ccba_x, cdtx_x, dp_x, remit_x, rt_x = xs
    ccba_y, cdtx_y, dp_y, remit_y, rt_y = ys
    ccba_ak, cdtx_ak, dp_ak, remit_ak, rt_ak = aks

    print('***Training***')

    # ccba
    ccba_ensemble = m.model_workhouse()
    print('ccba_x', ccba_x.columns.tolist())
    ccba_model = ccba_ensemble.fit(ccba_x, ccba_y)

    # cdtx
    cdtx_ensemble = m.model_workhouse()
    print('cdtx_x', cdtx_x.columns.tolist())
    cdtx_model = cdtx_ensemble.fit(cdtx_x, cdtx_y)

    # dp
    dp_ensemble = m.model_workhouse()
    print('dp_x', dp_x.columns.tolist())
    dp_model = dp_ensemble.fit(dp_x, dp_y)

    # remit
    remit_ensemble = m.model_workhouse()
    print('remit_x', remit_x.columns.tolist())
    remit_model = remit_ensemble.fit(remit_x, remit_y)

    print('***Final Training***')
    # predict
    ccba_y_pred = ccba_model.predict(ccba_x)
    cdtx_y_pred = cdtx_model.predict(cdtx_x)
    dp_y_pred = dp_model.predict(dp_x)
    remit_y_pred = remit_model.predict(remit_x)

    # convert 2d-like list to 1d list (w/ seq. right)
    mode = 'train'
    ccba_y_pred_adj = d.get_ak_adj_list(mode, ccba_ak, ccba_y_pred, rt_ak)
    cdtx_y_pred_adj = d.get_ak_adj_list(mode, cdtx_ak, cdtx_y_pred, rt_ak)
    dp_y_pred_adj = d.get_ak_adj_list(mode, dp_ak, dp_y_pred, rt_ak)
    remit_y_pred_adj = d.get_ak_adj_list(mode, remit_ak, remit_y_pred, rt_ak)

    # set to the dataset
    rt_x['ccba'] = ccba_y_pred_adj
    rt_x['cdtx0001'] = cdtx_y_pred_adj
    rt_x['dp'] = dp_y_pred_adj
    rt_x['remit1'] = remit_y_pred_adj

    c_ensemble = m.model_workhouse()
    print('rt_x', rt_x.columns.tolist())
    c_model = c_ensemble.fit(rt_x, rt_y)

    print('***All Training Done!!!***')

    return ccba_model, cdtx_model, dp_model, remit_model, c_model


def prediction(name: str,
               threshold: float,
               models: Tuple,
               xs: Tuple,
               aks: Tuple[list],
               y=None):
    # checker
    assert len(models) == 5, 'models must be len 5 tuple'
    assert len(xs) == 5, 'xs must be len 5 tuple'
    assert len(aks) == 5, 'aks must be len 5 tuple'

    # input
    ccba_model, cdtx_model, dp_model, remit_model, c_model = models
    ccba_x, cdtx_x, dp_x, remit_x, rt_x = xs
    ccba_ak, cdtx_ak, dp_ak, remit_ak, ak_all = aks

    print(f'\n***Predict on {name}***')
    # predict
    ccba_y_pred = ccba_model.predict(ccba_x)
    cdtx_y_pred = cdtx_model.predict(cdtx_x)
    dp_y_pred = dp_model.predict(dp_x)
    remit_y_pred = remit_model.predict(remit_x)

    # convert 2d-like list to 1d list (w/ seq. right)
    mode = 'dev'
    ccba_y_pred_adj = d.get_ak_adj_list(mode, ccba_ak, ccba_y_pred, ak_all)
    cdtx_y_pred_adj = d.get_ak_adj_list(mode, cdtx_ak, cdtx_y_pred, ak_all)
    dp_y_pred_adj = d.get_ak_adj_list(mode, dp_ak, dp_y_pred, ak_all)
    remit_y_pred_adj = d.get_ak_adj_list(mode, remit_ak, remit_y_pred, ak_all)

    # set to the dataset
    rt_x['ccba'] = ccba_y_pred_adj
    rt_x['cdtx0001'] = cdtx_y_pred_adj
    rt_x['dp'] = dp_y_pred_adj
    rt_x['remit1'] = remit_y_pred_adj

    print(f'***Final predict on {name}***')
    _y_pred = c_model.predict(rt_x)
    y_pred = min_max(_y_pred)

    print(f'***Result of {name}***')
    if y is not None:
        printer_unique_counter(y, f'distribution of {name} data:')

    unique, counts = np.unique(y_pred, return_counts=True)
    print('unique:', len(unique))
    # printer_unique_counter(y_pred,
    #                        f'distribution of predict on {name} (regression):')

    y_pred_class = (y_pred >= threshold).astype(int)
    printer_unique_counter(
        y_pred_class,
        f'distribution of predict on {name} (classification, threshold: {threshold}):'
    )

    if y is not None:
        printer_metrics(y, y_pred_class)
        printer_recall_precision(y, y_pred_class)

    return y_pred


def main():
    threshold = 1.0  # 0.5, 1.0
    break_id = -1  # -1, 100, 200, 500, 1000

    print('***Datasets***')
    '''
    t: train (part of train)
    v: validation (part of train)
    all: train + public
    '''
    (
        (
            # train
            ((ccba_x_t, ccba_y_t, ccba_ak_t), (cdtx_x_t, cdtx_y_t, cdtx_ak_t),
             (dp_x_t, dp_y_t, dp_ak_t), (remit_x_t, remit_y_t, remit_ak_t)),
            # validation
            ((ccba_x_v, ccba_y_v, ccba_ak_v), (cdtx_x_v, cdtx_y_v, cdtx_ak_v),
             (dp_x_v, dp_y_v, dp_ak_v), (remit_x_v, remit_y_v, remit_ak_v)),
            # public
            ((ccba_x_p, ccba_y_p, ccba_ak_p), (cdtx_x_p, cdtx_y_p, cdtx_ak_p),
             (dp_x_p, dp_y_p, dp_ak_p), (remit_x_p, remit_y_p, remit_ak_p)),
            # all
            ((ccba_x_all, ccba_y_all, ccba_ak_all), (cdtx_x_all, cdtx_y_all,
                                                     cdtx_ak_all),
             (dp_x_all, dp_y_all, dp_ak_all), (remit_x_all, remit_y_all,
                                               remit_ak_all)),
        ),
        (
            # train
            (rt_x_t, rt_y_t, rt_ak_t),
            # validation
            (rt_x_v, rt_y_v, rt_ak_v),
            # public
            (rt_x_p, rt_y_p, rt_ak_p),
            # all
            (rt_x_all, rt_y_all, rt_ak_all),
        ),
    ) = d.do_workhouse(break_id=break_id)

    ## train ##

    ccba_model, cdtx_model, dp_model, remit_model, c_model = training(
        (ccba_x_t, cdtx_x_t, dp_x_t, remit_x_t, rt_x_t),
        (ccba_y_t, cdtx_y_t, dp_y_t, remit_y_t, rt_y_t),
        (ccba_ak_t, cdtx_ak_t, dp_ak_t, remit_ak_t, rt_ak_t),
    )

    ## predoction ##

    # train
    prediction(
        'train',
        threshold,
        (ccba_model, cdtx_model, dp_model, remit_model, c_model),
        (ccba_x_t, cdtx_x_t, dp_x_t, remit_x_t, rt_x_t),
        (ccba_ak_t, cdtx_ak_t, dp_ak_t, remit_ak_t, rt_ak_t),
        rt_y_t,
    )

    # validation
    prediction(
        'validation',
        threshold,
        (ccba_model, cdtx_model, dp_model, remit_model, c_model),
        (ccba_x_v, cdtx_x_v, dp_x_v, remit_x_v, rt_x_v),
        (ccba_ak_v, cdtx_ak_v, dp_ak_v, remit_ak_v, rt_ak_v),
        rt_y_v,
    )

    # validation
    prediction(
        'public',
        threshold,
        (ccba_model, cdtx_model, dp_model, remit_model, c_model),
        (ccba_x_p, cdtx_x_p, dp_x_p, remit_x_p, rt_x_p),
        (ccba_ak_p, cdtx_ak_p, dp_ak_p, remit_ak_p, rt_ak_p),
        rt_y_p,
    )

    # test
    y_pred_all = prediction(
        'test',
        threshold,
        (ccba_model, cdtx_model, dp_model, remit_model, c_model),
        (ccba_x_all, cdtx_x_all, dp_x_all, remit_x_all, rt_x_all),
        (ccba_ak_all, cdtx_ak_all, dp_ak_all, remit_ak_all, rt_ak_all),
        rt_y_all,
    )

    print('***Predict on final test***')
    df_pred = d.get_answer_form(rt_ak_all, y_pred_all)
    df_submit = d.get_submit(df_pred, './pred.csv')

    printer_unique_counter(df_submit['probability'], 'distribution of submit:')

    print('GOOD')

    return


if __name__ == '__main__':
    main()
