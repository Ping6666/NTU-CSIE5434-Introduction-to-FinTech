from typing import Tuple

import numpy as np
import pandas as pd

from tqdm import tqdm


def read_csv_dataset(base_dir):
    #
    '''
    name: public_train_x_ccba_full_hashed.csv
    col: cust_id, lupay, byymm, cycam, usgam, clamt, csamt, inamt, cucsm, cucah
    '''
    df_ccba_tp = pd.DataFrame(
        pd.read_csv(
            base_dir + 'public_train_x_ccba_full_hashed.csv',
            dtype={
                'cust_id': str,  # 顧客編號
                'lupay': float,  # 上月繳款總額 數值型 經過神秘轉換
                'byymm': int,  # 帳務年月 類別型 經過神秘轉換，數字序列有前後順序意義
                'cycam': float,  # 信用額度 數值型 經過神秘轉換
                'usgam': float,  # 已使用額度 數值型 經過神秘轉換
                'clamt': float,  # 本月分期預借現金金額 數值型 經過神秘轉換
                'csamt': float,  # 本月預借現金金額 數值型 經過神秘轉換
                'inamt': float,  # 本月分期消費金額 數值型 經過神秘轉換
                'cucsm': float,  # 本月消費金額 數值型 經過神秘轉換
                'cucah': float,  # 本月借現金額 數值型 經過神秘轉換
            }))
    print('df_ccba_tp', df_ccba_tp.isna().sum())
    print()

    #
    '''
    name: public_train_x_cdtx0001_full_hashed.csv
    col: cust_id, date, country, cur_type, amt
    '''
    df_cdtx0001_tp = pd.DataFrame(
        pd.read_csv(
            base_dir + 'public_train_x_cdtx0001_full_hashed.csv',
            dtype={
                'cust_id': str,  # 顧客編號
                'date': int,  # 消費日期 類別型 經過神秘轉換，數字序列有前後順序意義
                'country': int,  # 消費地國別 類別型 經過神秘轉換，(130 = 台灣)
                'cur_type': int,  # 消費地幣別 類別型 經過神秘轉換，(47 = 台幣)
                'amt': float,  # 交易金額-台幣 數值型 經過神秘轉換
            }))
    print('df_cdtx0001_tp', df_cdtx0001_tp.isna().sum())
    print()

    #
    '''
    name: public_train_x_custinfo_full_hashed.csv
    col: alert_key, cust_id, risk_rank, occupation_code, total_asset, AGE
    '''
    df_custinfo_tp = pd.DataFrame(
        pd.read_csv(
            base_dir + 'public_train_x_custinfo_full_hashed.csv',
            dtype={
                'alert_key': str,  #alert 主鍵
                'cust_id': str,  # 顧客編號
                'risk_rank': int,  # 風險等級 類別型
                'occupation_code': float,  # 職業 類別型
                'total_asset': float,  # 行內總資產 數值型 經過神秘轉換
                'AGE': int,  # 年齡 類別型
            }))
    df_custinfo_tp['occupation_code'].fillna(value=-1.0, inplace=True)
    print('df_custinfo_tp', df_custinfo_tp.isna().sum())
    print()

    #
    '''
    name: public_train_x_dp_full_hashed.csv
    col: cust_id, debit_credit, tx_date, tx_time, tx_type, tx_amt, exchg_rate, info_asset_code, fiscTxId, txbranch, cross_bank, ATM
    '''
    df_dp_tp = pd.DataFrame(
        pd.read_csv(
            base_dir + 'public_train_x_dp_full_hashed.csv',
            dtype={
                'cust_id': str,  # 顧客編號
                'debit_credit': str,  # 借貸別 類別型
                'tx_date': int,  # 交易日期 類別型 經過神秘轉換，數字序列有前後順序意義
                'tx_time': int,  # 交易時間 類別型 經過神秘轉換，數字序列有前後順序意義
                'tx_type': int,  # 交易類別 類別型
                'tx_amt': float,  # 交易金額 數值型 經過神秘轉換
                'exchg_rate': float,  # 匯率 數值型
                'info_asset_code':
                int,  # 資訊資產代號 類別型 經過神秘轉換，tx_type = 1且info_asset_code = 12時，該交易為臨櫃現金交易
                'fiscTxId': float,  # 交易代碼 類別型 經過神秘轉換
                'txbranch': float,  # 分行代碼 類別型 若為跨行交易，則僅代表交易對手銀行代碼，無分行資訊
                'cross_bank': int,  # 是否為跨行交易 類別型 (0=非跨行；1=跨行)
                'ATM': int,  # 是否為實體ATM交易 類別型 (0=非實體ATM交易；1=實體ATM交易)
            }))

    def debit_credit_to_numeric(x):
        if x == 'CR':
            return 1
        elif x == 'DB':
            return 2
        raise ValueError

    df_dp_tp['debit_credit'] = df_dp_tp['debit_credit'].apply(
        debit_credit_to_numeric)
    # df_dp_tp = df_dp_tp.drop(['debit_credit'], axis=1)

    df_dp_tp['tx_amt'].fillna(value=-1.0, inplace=True)
    df_dp_tp['fiscTxId'].fillna(value=-1.0, inplace=True)
    df_dp_tp['txbranch'].fillna(value=-1.0, inplace=True)
    print('df_dp_tp', df_dp_tp.isna().sum())
    print()

    #
    '''
    name: public_train_x_remit1_full_hashed.csv
    col: cust_id, trans_date, trans_no, trade_amount_usd
    '''
    df_remit1_tp = pd.DataFrame(
        pd.read_csv(
            base_dir + 'public_train_x_remit1_full_hashed.csv',
            dtype={
                'cust_id': str,  # 顧客編號		
                'trans_date': int,  # 外匯交易日(帳務日) 類別型 經過神秘轉換，數字序列有前後順序意義
                'trans_no': int,  # 交易編號 類別型 經過神秘轉換，代表不同的匯出方式
                'trade_amount_usd': float,  # 交易金額(折合美金) 數值型 經過神秘轉換
            }))
    print('df_remit1_tp', df_remit1_tp.isna().sum())
    print()

    return df_ccba_tp, df_cdtx0001_tp, df_custinfo_tp, df_dp_tp, df_remit1_tp


def read_csv_x(base_dir, mode):
    #
    '''
    name: train_x_alert_date.csv, public_x_alert_date.csv
    col: cust_id, trans_date, trans_no, trade_amount_usd
    '''
    df_alert_date = None
    if mode == 'train':
        df_alert_date = pd.DataFrame(
            pd.read_csv(
                base_dir + 'train_x_alert_date.csv',
                dtype={
                    'alert_key': str,  # alert主鍵
                    'date': int,  # alert主鍵發生日期 類別型 經過神秘轉換，數字序列有前後順序意義
                }))
    elif mode == 'public':
        df_alert_date = pd.DataFrame(
            pd.read_csv(
                base_dir + 'public_x_alert_date.csv',
                dtype={
                    'alert_key': str,  # alert主鍵
                    'date': int,  # alert主鍵發生日期 類別型 經過神秘轉換，數字序列有前後順序意義
                }))
    else:
        raise ValueError

    return df_alert_date


def read_csv_y(base_dir, mode='train'):
    #
    '''
    name: train_y_answer.csv
    col: alert_key, sar_flag
    '''
    df_answer = None
    if mode == 'train':
        df_answer = pd.DataFrame(
            pd.read_csv(
                base_dir + 'train_y_answer.csv',
                dtype={
                    'alert_key': str,  # alert主鍵
                    'sar_flag': int,  # alert主鍵報SAR與否 類別型 (0=未報SAR；1=有報SAR)
                }))
    else:
        raise ValueError

    return df_answer


def read_csv_submit_list(base_dir):
    #
    '''
    name: all_x_alert.csv
    col: alert_key, probability
    '''
    df_submit = None
    df_submit = pd.DataFrame(
        pd.read_csv(
            base_dir + 'all_x_alert.csv',
            dtype={
                'alert_key': str,  # alert主鍵
                'probability': float,
            }))
    submit_list = df_submit['alert_key'].to_list()

    return submit_list


def get_ccba_y(df_x: pd.DataFrame,
               dfs: Tuple[pd.DataFrame],
               df_y: pd.DataFrame = None,
               break_id: int = -1):
    df_ccba: pd.DataFrame
    df_cdtx0001: pd.DataFrame
    df_custinfo: pd.DataFrame
    df_dp: pd.DataFrame
    df_remit1: pd.DataFrame
    df_ccba, df_cdtx0001, df_custinfo, df_dp, df_remit1 = dfs

    ccbas = []
    total_length = 0
    for i, c_row in tqdm(df_x.iterrows(), desc="get_ccba",
                         total=df_x.shape[0]):
        if i == break_id:
            break

        # take out value
        c_ak = c_row['alert_key']
        c_date = c_row['date']

        # custinfo
        c_cust_id = df_custinfo[(df_custinfo['alert_key'] == c_ak)]
        c_cust_id = c_cust_id['cust_id'].values[0]

        # ccba
        ## use copy() prevent SettingWithCopyWarning
        c_ccba = df_ccba[((df_ccba['cust_id'] == c_cust_id) &
                          (df_ccba['byymm'] <= c_date) &
                          (df_ccba['byymm'] > c_date - 30))].copy()
        c_ccba['alert_key'] = c_ak
        ccbas.append(c_ccba)
        total_length += len(c_ccba)

    # list to dict then convet to pd.DataFrame
    df_ccbas = pd.DataFrame.from_dict(pd.concat(ccbas))
    df_ccbas = df_ccbas.drop(['byymm'], axis=1)

    assert total_length == len(df_ccbas.index)

    #
    '''
    df_x.columns: 'alert_key', 'date'
    df_y.columns: 'alert_key', 'sar_flag'
    '''
    # bind with label in df_y
    df_xy = None
    if df_y is not None:
        df_xy = pd.merge(df_x, df_y, on='alert_key')
    else:
        df_xy = df_x

    #
    '''
    df_xy.columns: 'alert_key', 'date', 'sar_flag'
    df_ccbas.columns: 'cust_id', 'lupay', 'cycam', 'usgam', 'clamt',
                      'csamt', 'inamt', 'cucsm', 'cucah', 'alert_key'
    '''
    # bind with cust_id in df_custinfo
    df_xy_c = pd.merge(df_xy, df_ccbas, on='alert_key')

    # filter for needed columns
    df_xy_c = df_xy_c.drop(['date', 'cust_id'], axis=1)
    df_xy_c = df_xy_c.dropna()

    assert total_length == len(df_xy_c.index)

    # final process
    ## train data & label
    if df_y is not None:
        rt_y = df_xy_c['sar_flag'].to_numpy()
        rt_ak = df_xy_c['alert_key'].to_numpy()
        rt_x = df_xy_c.drop(['alert_key', 'sar_flag'], axis=1)
        return rt_x, rt_y, rt_ak
    else:
        rt_ak = df_xy_c['alert_key'].to_numpy()
        rt_x = df_xy_c.drop(['alert_key'], axis=1)
        return rt_x, None, rt_ak


def get_cdtx0001_y(df_x: pd.DataFrame,
                   dfs: Tuple[pd.DataFrame],
                   df_y: pd.DataFrame = None,
                   break_id: int = -1):
    df_ccba: pd.DataFrame
    df_cdtx0001: pd.DataFrame
    df_custinfo: pd.DataFrame
    df_dp: pd.DataFrame
    df_remit1: pd.DataFrame
    df_ccba, df_cdtx0001, df_custinfo, df_dp, df_remit1 = dfs

    cdtx0001s = []
    total_length = 0
    for i, c_row in tqdm(df_x.iterrows(),
                         desc="get_cdtx0001",
                         total=df_x.shape[0]):
        if i == break_id:
            break

        # take out value
        c_ak = c_row['alert_key']
        c_date = c_row['date']

        # custinfo
        c_cust_id = df_custinfo[(df_custinfo['alert_key'] == c_ak)]
        c_cust_id = c_cust_id['cust_id'].values[0]

        # ccba
        ## use copy() prevent SettingWithCopyWarning
        c_cdtx0001 = df_cdtx0001[((df_cdtx0001['cust_id'] == c_cust_id) &
                                  (df_cdtx0001['date'] <= c_date) &
                                  (df_cdtx0001['date'] > c_date - 30))].copy()
        c_cdtx0001['alert_key'] = c_ak
        cdtx0001s.append(c_cdtx0001)
        total_length += len(c_cdtx0001)

    # list to dict then convet to pd.DataFrame
    df_cdtx0001s = pd.DataFrame.from_dict(pd.concat(cdtx0001s))
    df_cdtx0001s = df_cdtx0001s.drop(['date'], axis=1)

    assert total_length == len(df_cdtx0001s.index)

    #
    '''
    df_x.columns: 'alert_key', 'date'
    df_y.columns: 'alert_key', 'sar_flag'
    '''
    # bind with label in df_y
    df_xy = None
    if df_y is not None:
        df_xy = pd.merge(df_x, df_y, on='alert_key')
    else:
        df_xy = df_x

    #
    '''
    df_xy.columns: 'alert_key', 'date', 'sar_flag'
    df_cdtx0001s.columns: 'cust_id', 'country', 'cur_type', 'amt', 'alert_key'
    '''
    # bind with cust_id in df_custinfo
    df_xy_c = pd.merge(df_xy, df_cdtx0001s, on='alert_key')

    # filter for needed columns
    df_xy_c = df_xy_c.drop(['date', 'cust_id'], axis=1)
    df_xy_c = df_xy_c.dropna()

    assert total_length == len(df_xy_c.index)

    # final process
    ## train data & label
    if df_y is not None:
        rt_y = df_xy_c['sar_flag'].to_numpy()
        rt_ak = df_xy_c['alert_key'].to_numpy()
        rt_x = df_xy_c.drop(['alert_key', 'sar_flag'], axis=1)
        return rt_x, rt_y, rt_ak
    else:
        rt_ak = df_xy_c['alert_key'].to_numpy()
        rt_x = df_xy_c.drop(['alert_key'], axis=1)
        return rt_x, None, rt_ak


def get_dp_y(df_x: pd.DataFrame,
             dfs: Tuple[pd.DataFrame],
             df_y: pd.DataFrame = None,
             break_id: int = -1):
    df_ccba: pd.DataFrame
    df_cdtx0001: pd.DataFrame
    df_custinfo: pd.DataFrame
    df_dp: pd.DataFrame
    df_remit1: pd.DataFrame
    df_ccba, df_cdtx0001, df_custinfo, df_dp, df_remit1 = dfs

    dps = []
    total_length = 0
    for i, c_row in tqdm(df_x.iterrows(), desc="get_dp", total=df_x.shape[0]):
        if i == break_id:
            break

        # take out value
        c_ak = c_row['alert_key']
        c_date = c_row['date']

        # custinfo
        c_cust_id = df_custinfo[(df_custinfo['alert_key'] == c_ak)]
        c_cust_id = c_cust_id['cust_id'].values[0]

        # ccba
        ## use copy() prevent SettingWithCopyWarning
        c_dp = df_dp[((df_dp['cust_id'] == c_cust_id) &
                      (df_dp['tx_date'] <= c_date) &
                      (df_dp['tx_date'] > c_date - 30))].copy()
        c_dp['alert_key'] = c_ak
        dps.append(c_dp)
        total_length += len(c_dp)

    # list to dict then convet to pd.DataFrame
    df_dps = pd.DataFrame.from_dict(pd.concat(dps))
    df_dps = df_dps.drop(['tx_date', 'tx_time'], axis=1)

    assert total_length == len(df_dps.index)

    #
    '''
    df_x.columns: 'alert_key', 'date'
    df_y.columns: 'alert_key', 'sar_flag'
    '''
    # bind with label in df_y
    df_xy = None
    if df_y is not None:
        df_xy = pd.merge(df_x, df_y, on='alert_key')
    else:
        df_xy = df_x

    #
    '''
    df_xy.columns: 'alert_key', 'date', 'sar_flag'
    df_dps.columns: 'cust_id', 'debit_credit', 'tx_type', 'tx_amt',
                    'exchg_rate', 'info_asset_code', 'fiscTxId',
                    'txbranch', 'cross_bank', 'ATM', 'alert_key'
    '''
    # bind with cust_id in df_custinfo
    df_xy_d = pd.merge(df_xy, df_dps, on='alert_key')

    # filter for needed columns
    df_xy_d = df_xy_d.drop(['date', 'cust_id'], axis=1)
    df_xy_d = df_xy_d.dropna()

    assert total_length == len(df_xy_d.index)

    # final process
    ## train data & label
    if df_y is not None:
        rt_y = df_xy_d['sar_flag'].to_numpy()
        rt_ak = df_xy_d['alert_key'].to_numpy()
        rt_x = df_xy_d.drop(['alert_key', 'sar_flag'], axis=1)
        return rt_x, rt_y, rt_ak
    else:
        rt_ak = df_xy_d['alert_key'].to_numpy()
        rt_x = df_xy_d.drop(['alert_key'], axis=1)
        return rt_x, None, rt_ak


def get_remit1_y(df_x: pd.DataFrame,
                 dfs: Tuple[pd.DataFrame],
                 df_y: pd.DataFrame = None,
                 break_id: int = -1):
    df_ccba: pd.DataFrame
    df_cdtx0001: pd.DataFrame
    df_custinfo: pd.DataFrame
    df_dp: pd.DataFrame
    df_remit1: pd.DataFrame
    df_ccba, df_cdtx0001, df_custinfo, df_dp, df_remit1 = dfs

    dps = []
    total_length = 0
    for i, c_row in tqdm(df_x.iterrows(),
                         desc="get_remit1",
                         total=df_x.shape[0]):
        if i == break_id:
            break

        # take out value
        c_ak = c_row['alert_key']
        c_date = c_row['date']

        # custinfo
        c_cust_id = df_custinfo[(df_custinfo['alert_key'] == c_ak)]
        c_cust_id = c_cust_id['cust_id'].values[0]

        # ccba
        ## use copy() prevent SettingWithCopyWarning
        c_remit1 = df_remit1[((df_remit1['cust_id'] == c_cust_id) &
                              (df_remit1['trans_date'] <= c_date) &
                              (df_remit1['trans_date'] > c_date - 30))].copy()
        c_remit1['alert_key'] = c_ak
        dps.append(c_remit1)
        total_length += len(c_remit1)

    # list to dict then convet to pd.DataFrame
    df_remit1s = pd.DataFrame.from_dict(pd.concat(dps))
    df_remit1s = df_remit1s.drop(['trans_date'], axis=1)

    assert total_length == len(df_remit1s.index)

    #
    '''
    df_x.columns: 'alert_key', 'date'
    df_y.columns: 'alert_key', 'sar_flag'
    '''
    # bind with label in df_y
    df_xy = None
    if df_y is not None:
        df_xy = pd.merge(df_x, df_y, on='alert_key')
    else:
        df_xy = df_x

    #
    '''
    df_xy.columns: 'alert_key', 'date', 'sar_flag'
    df_remit1s.columns: 'cust_id', 'trans_no', 'trade_amount_usd', 'alert_key'
    '''
    # bind with cust_id in df_custinfo
    df_xy_r = pd.merge(df_xy, df_remit1s, on='alert_key')

    # filter for needed columns
    df_xy_r = df_xy_r.drop(['date', 'cust_id'], axis=1)
    df_xy_r = df_xy_r.dropna()

    assert total_length == len(df_xy_r.index)

    # final process
    ## train data & label
    if df_y is not None:
        rt_y = df_xy_r['sar_flag'].to_numpy()
        rt_ak = df_xy_r['alert_key'].to_numpy()
        rt_x = df_xy_r.drop(['alert_key', 'sar_flag'], axis=1)
        return rt_x, rt_y, rt_ak
    else:
        rt_ak = df_xy_r['alert_key'].to_numpy()
        rt_x = df_xy_r.drop(['alert_key'], axis=1)
        return rt_x, None, rt_ak


def _get_data_counter(df_alert: pd.DataFrame,
                      dfs: Tuple[pd.DataFrame],
                      break_id: int = -1):
    df_ccba: pd.DataFrame
    df_cdtx0001: pd.DataFrame
    df_custinfo: pd.DataFrame
    df_dp: pd.DataFrame
    df_remit1: pd.DataFrame
    df_ccba, df_cdtx0001, df_custinfo, df_dp, df_remit1 = dfs

    ids_datasets = []
    for i, c_row in tqdm(df_alert.iterrows(),
                         desc="_get_data_counter",
                         total=df_alert.shape[0]):
        if i == break_id:
            break

        # custinfo
        c_cust_id = df_custinfo.loc[(
            df_custinfo['alert_key'] == c_row['alert_key'])]
        c_cust_id = c_cust_id['cust_id'].values[0]
        c_date = c_row['date']

        # ccba
        c_ccba = ((df_ccba['cust_id'] == c_cust_id) &
                  (df_ccba['byymm'] <= c_date)
                  & (df_ccba['byymm'] > c_date - 30)).sum()
        # c_ccba = df_ccba.loc[((df_ccba['cust_id'] == c_cust_id) &
        #                       (df_ccba['byymm'] <= c_date) &
        #                       (df_ccba['byymm'] > c_date - 30))]

        # cdtx0001
        c_cdtx0001 = ((df_cdtx0001['cust_id'] == c_cust_id) &
                      (df_cdtx0001['date'] <= c_date) &
                      (df_cdtx0001['date'] > c_date - 30)).sum()
        # c_cdtx0001 = df_cdtx0001.loc[((df_cdtx0001['cust_id'] == c_cust_id) &
        #                               (df_cdtx0001['date'] <= c_date) &
        #                               (df_cdtx0001['date'] > c_date - 30))]

        # dp
        c_dp = ((df_dp['cust_id'] == c_cust_id) & (df_dp['tx_date'] <= c_date)
                & (df_dp['tx_date'] > c_date - 30)).sum()
        # c_dp = df_dp.loc[((df_dp['cust_id'] == c_cust_id) &
        #                   (df_dp['tx_date'] <= c_date) &
        #                   (df_dp['tx_date'] > c_date - 30))]

        # remit1
        c_remit1 = ((df_remit1['cust_id'] == c_cust_id) &
                    (df_remit1['trans_date'] <= c_date) &
                    (df_remit1['trans_date'] > c_date - 30)).sum()
        # c_remit1 = df_remit1.loc[((df_remit1['cust_id'] == c_cust_id) &
        #                           (df_remit1['trans_date'] <= c_date) &
        #                           (df_remit1['trans_date'] > c_date - 30))]

        ids_datasets.append({
            # 'cust_id': c_cust_id,
            'n_ccba': c_ccba,
            'n_cdtx0001': c_cdtx0001,
            'n_dp': c_dp,
            'n_remit1': c_remit1,
        })
    df_id = pd.DataFrame.from_dict(ids_datasets)

    df_ac = pd.merge(df_alert, df_custinfo, on='alert_key')
    df_ac_id = pd.concat([df_ac, df_id], axis=1)
    df_ac_id = df_ac_id.drop(['date', 'cust_id'], axis=1)
    df_ac_id = df_ac_id.dropna()

    return df_ac_id


def get_ak_adj_list(y_alert_keys: list, y_pred: list,
                    all_alert_keys: list) -> list:
    # for those in y_alert_keys
    rt_dict = {}
    for ak, y in zip(y_alert_keys, y_pred):
        if ak not in rt_dict.keys() or rt_dict[ak] < y:
            rt_dict[ak] = y

    # adj. the rt_dict to list like w/ seq. as all_alert_keys
    rt_list = []
    for ak in all_alert_keys:
        if ak not in rt_dict.keys():
            rt_list.append(-1)
        else:
            rt_list.append(rt_dict[ak])
    return rt_list


def get_data_counter(df_datasets,
                     df_x_t,
                     df_x_v,
                     df_x_p,
                     df_y,
                     break_id: int = -1):
    # get alert_key, custinfo, counter
    print("train")
    df_x_ac_id_t = _get_data_counter(df_x_t, df_datasets, break_id)
    print("validation")
    df_x_ac_id_v = _get_data_counter(df_x_v, df_datasets, break_id)
    print("public")
    df_x_ac_id_p = _get_data_counter(df_x_p, df_datasets, break_id)

    # merge with label
    df_xy_t = pd.merge(df_x_ac_id_t, df_y, on='alert_key')
    df_xy_v = pd.merge(df_x_ac_id_v, df_y, on='alert_key')

    # final process
    ## train data & label
    rt_y_t = df_xy_t['sar_flag'].to_numpy()
    rt_ak_t = df_xy_t['alert_key'].to_numpy()
    rt_x_t = df_xy_t.drop(['alert_key', 'sar_flag'], axis=1)

    rt_y_v = df_xy_v['sar_flag'].to_numpy()
    rt_ak_v = df_xy_v['alert_key'].to_numpy()
    rt_x_v = df_xy_v.drop(['alert_key', 'sar_flag'], axis=1)

    ## test data
    df_x_all = pd.concat([df_x_ac_id_t, df_x_ac_id_v, df_x_ac_id_p],
                         axis=0,
                         ignore_index=True)
    rt_ak_all = df_x_all['alert_key'].to_numpy()
    rt_x_all = df_x_all.drop(['alert_key'], axis=1)

    return ((rt_x_t, rt_y_t, rt_ak_t), (rt_x_v, rt_y_v, rt_ak_v),
            (rt_x_all, None, rt_ak_all))


def get_datasets(df_datasets,
                 df_x_t,
                 df_x_v,
                 df_x_p,
                 df_y,
                 break_id: int = -1):
    # train: get x, y, alert_key
    print("train")
    ccba_x_t, ccba_y_t, ccba_ak_t = get_ccba_y(df_x_t,
                                               df_datasets,
                                               df_y,
                                               break_id=break_id)
    cdtx_x_t, cdtx_y_t, cdtx_ak_t = get_cdtx0001_y(df_x_t,
                                                   df_datasets,
                                                   df_y,
                                                   break_id=break_id)
    dp_x_t, dp_y_t, dp_ak_t = get_dp_y(df_x_t,
                                       df_datasets,
                                       df_y,
                                       break_id=break_id)
    remit_x_t, remit_y_t, remit_ak_t = get_remit1_y(df_x_t,
                                                    df_datasets,
                                                    df_y,
                                                    break_id=break_id)

    # validation: get x, y, alert_key
    print("validation")
    ccba_x_v, ccba_y_v, ccba_ak_v = get_ccba_y(df_x_v,
                                               df_datasets,
                                               df_y,
                                               break_id=break_id)
    cdtx_x_v, cdtx_y_v, cdtx_ak_v = get_cdtx0001_y(df_x_v,
                                                   df_datasets,
                                                   df_y,
                                                   break_id=break_id)
    dp_x_v, dp_y_v, dp_ak_v = get_dp_y(df_x_v,
                                       df_datasets,
                                       df_y,
                                       break_id=break_id)
    remit_x_v, remit_y_v, remit_ak_v = get_remit1_y(df_x_v,
                                                    df_datasets,
                                                    df_y,
                                                    break_id=break_id)

    # public: get x, y, alert_key
    print("public")
    ccba_x_p, _, ccba_ak_p = get_ccba_y(df_x_p, df_datasets, break_id=break_id)
    cdtx_x_p, _, cdtx_ak_p = get_cdtx0001_y(df_x_p,
                                            df_datasets,
                                            break_id=break_id)
    dp_x_p, _, dp_ak_p = get_dp_y(df_x_p, df_datasets, break_id=break_id)
    remit_x_p, _, remit_ak_p = get_remit1_y(df_x_p,
                                            df_datasets,
                                            break_id=break_id)

    ## test data
    ccba_x_all = pd.concat([ccba_x_t, ccba_x_v, ccba_x_p],
                           axis=0,
                           ignore_index=True)
    ccba_ak_all = np.concatenate([ccba_ak_t, ccba_ak_v, ccba_ak_p])

    cdtx_x_all = pd.concat([cdtx_x_t, cdtx_x_v, cdtx_x_p],
                           axis=0,
                           ignore_index=True)
    cdtx_ak_all = np.concatenate([cdtx_ak_t, cdtx_ak_v, cdtx_ak_p])

    dp_x_all = pd.concat([dp_x_t, dp_x_v, dp_x_p], axis=0, ignore_index=True)
    dp_ak_all = np.concatenate([dp_ak_t, dp_ak_v, dp_ak_p])

    remit_x_all = pd.concat([remit_x_t, remit_x_v, remit_x_p],
                            axis=0,
                            ignore_index=True)
    remit_ak_all = np.concatenate([remit_ak_t, remit_ak_v, remit_ak_p])

    return (((ccba_x_t, ccba_y_t, ccba_ak_t), (cdtx_x_t, cdtx_y_t, cdtx_ak_t),
             (dp_x_t, dp_y_t, dp_ak_t), (remit_x_t, remit_y_t, remit_ak_t)),
            ((ccba_x_v, ccba_y_v, ccba_ak_v), (cdtx_x_v, cdtx_y_v, cdtx_ak_v),
             (dp_x_v, dp_y_v, dp_ak_v), (remit_x_v, remit_y_v, remit_ak_v)),
            ((ccba_x_all, None, ccba_ak_all), (cdtx_x_all, None, cdtx_ak_all),
             (dp_x_all, None, dp_ak_all), (remit_x_all, None, remit_ak_all)))


def do_workhouse(v_split: float = 0.1, break_id: int = -1):
    '''
    validation split; a ratio (0, 1)
    '''

    assert v_split > 0 and v_split < 1, 'validation split need to be flaot in between 0 ~ 1'

    ## read csv ##
    print('csv | dataset')
    df_datasets = read_csv_dataset(base_dir='./data/')

    print('csv | x - train')
    df_x_all = read_csv_x(base_dir='./data/', mode='train')

    n_t_all = len(df_x_all.index)
    n_v = int(n_t_all * v_split)
    n_t = n_t_all - n_v

    df_x_t = df_x_all[:n_t].copy()
    df_x_t = df_x_t.reset_index(drop=True)
    df_x_v = df_x_all[-n_v:].copy()
    df_x_v = df_x_v.reset_index(drop=True)

    assert len(df_x_all.index) == len(df_x_t.index) + len(df_x_v.index)

    print(f'validation split ratio: {v_split} | all: {len(df_x_all.index)},',
          f'train: {len(df_x_t.index)}, validation: {len(df_x_v.index)}.')

    print('csv | x - public')
    df_x_p = read_csv_x(base_dir='./data/', mode='public')

    print('csv | y')
    df_y = read_csv_y(base_dir='./data/')

    ## the getter ##
    print('getter | datasets')
    d = get_datasets(df_datasets, df_x_t, df_x_v, df_x_p, df_y, break_id)

    print('getter | data_counter')
    dc = get_data_counter(df_datasets, df_x_t, df_x_v, df_x_p, df_y, break_id)

    return d, dc


def get_answer_form(alert_keys: list, probability: list):
    df = pd.DataFrame(list(zip(alert_keys, probability)),
                      columns=['alert_key', 'probability'])
    return df


def get_submit(df: pd.DataFrame, save_name: str = None):
    """
    correct from the dataset and pred_list to answer dataframe
    and save
    """
    submit_list = read_csv_submit_list(base_dir='./data/')

    # filter out the alert_key not in submit_list
    df = df[df['alert_key'].isin(submit_list)]

    # get what is left from the submit_list, make it to pd.DataFrame and set probability
    diff_list = list(set(submit_list) - set(df['alert_key'].to_list()))
    df_diff = pd.DataFrame(diff_list, columns=['alert_key'])
    df_diff['probability'] = 0

    # concat the dataframe
    df = pd.concat([df, df_diff], axis=0, ignore_index=True)
    df = df.sort_values(by=['probability'], ascending=False)
    # df = df.sort_values(by=['probability'], ascending=True)

    ## checker ##
    assert len(df.index) == len(df['alert_key'].unique())

    if save_name != None:
        df.to_csv(save_name, index=False)
    return df


def main():
    do_workhouse(100)
    print('Done')
    return


if __name__ == '__main__':
    main()
