from typing import List, Tuple

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
                'country': str,  # 消費地國別 類別型 經過神秘轉換，(130 = 台灣)
                'cur_type': str,  # 消費地幣別 類別型 經過神秘轉換，(47 = 台幣)
                'amt': float,  # 交易金額-台幣 數值型 經過神秘轉換
            }))

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
                'risk_rank': str,  # 風險等級 類別型
                'occupation_code': str,  # 職業 類別型
                'total_asset': float,  # 行內總資產 數值型 經過神秘轉換
                'AGE': str,  # 年齡 類別型
            }))
    df_custinfo_tp['occupation_code'].fillna(value=-1.0, inplace=True)

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
                'tx_type': str,  # 交易類別 類別型
                'tx_amt': float,  # 交易金額 數值型 經過神秘轉換
                'exchg_rate': float,  # 匯率 數值型
                'info_asset_code':
                str,  # 資訊資產代號 類別型 經過神秘轉換，tx_type = 1且info_asset_code = 12時，該交易為臨櫃現金交易
                'fiscTxId': str,  # 交易代碼 類別型 經過神秘轉換
                'txbranch': str,  # 分行代碼 類別型 若為跨行交易，則僅代表交易對手銀行代碼，無分行資訊
                'cross_bank': str,  # 是否為跨行交易 類別型 (0=非跨行；1=跨行)
                'ATM': str,  # 是否為實體ATM交易 類別型 (0=非實體ATM交易；1=實體ATM交易)
            }))

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
                'trans_no': str,  # 交易編號 類別型 經過神秘轉換，代表不同的匯出方式
                'trade_amount_usd': float,  # 交易金額(折合美金) 數值型 經過神秘轉換
            }))
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


def get_cust_id_counter(df):
    # cust_id dict
    ids = {}
    for _, i in df.iterrows():
        # print(i['cust_id'])
        if i['cust_id'] not in ids:
            ids[i['cust_id']] = 1
        else:
            ids[i['cust_id']] += 1

    # get counter
    ids_list = np.array(list(ids.values()))

    # get how many times app. to id count
    unique, counts = np.unique(ids_list, return_counts=True)
    print(dict(zip(unique, counts)))
    print()
    return


def get_data_counter(df_alert: pd.DataFrame,
                     dfs: Tuple[pd.DataFrame],
                     break_id: int = -1):
    df_ccba: pd.DataFrame
    df_cdtx0001: pd.DataFrame
    df_custinfo: pd.DataFrame
    df_dp: pd.DataFrame
    df_remit1: pd.DataFrame
    df_ccba, df_cdtx0001, df_custinfo, df_dp, df_remit1 = dfs

    ids_datasets = []
    for i, c_row in tqdm(df_alert.iterrows(), total=df_alert.shape[0]):
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
            'ccba': c_ccba,
            'cdtx0001': c_cdtx0001,
            'dp': c_dp,
            'remit1': c_remit1,
        })
    df_id = pd.DataFrame.from_dict(ids_datasets)

    df_ac = pd.merge(df_alert, df_custinfo, on='alert_key')
    df_ac_id = pd.concat([df_ac, df_id], axis=1)
    df_ac_id = df_ac_id.drop(['date', 'cust_id'], axis=1)
    df_ac_id = df_ac_id.dropna()

    return df_ac_id


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


def df_workhouse(break_id: int = -1):
    # read csv
    df_datasets = read_csv_dataset(base_dir='./data/')
    df_x_t = read_csv_x(base_dir='./data/', mode='train')
    df_x_p = read_csv_x(base_dir='./data/', mode='public')
    df_y = read_csv_y(base_dir='./data/')

    # get alert_key, custinfo, counter
    df_x_ac_id_t = get_data_counter(df_x_t, df_datasets, break_id)
    df_x_ac_id_p = get_data_counter(df_x_p, df_datasets, break_id)

    # merge with label
    df_xy_t = pd.merge(df_x_ac_id_t, df_y, on='alert_key')

    # final process
    ## train data & label
    rt_y_t = df_xy_t['sar_flag'].to_numpy()
    rt_ak_t = df_xy_t['alert_key'].to_numpy()
    rt_x_t = df_xy_t.drop(['alert_key', 'sar_flag'], axis=1)

    ## test data
    df_x_all = pd.concat([df_x_ac_id_t, df_x_ac_id_p],
                         axis=0,
                         ignore_index=True)
    rt_ak_all = df_x_all['alert_key'].to_numpy()
    rt_x_all = df_x_all.drop(['alert_key'], axis=1)

    return (rt_x_t, rt_y_t, rt_ak_t), (rt_x_all, None, rt_ak_all)


def main():
    (rt_x_t, rt_y_t, rt_ak_t), (rt_x_all, _, rt_ak_all) = df_workhouse(100)

    print(rt_x_t)
    print(rt_y_t)
    print(rt_ak_t)
    print()

    print(rt_x_all)
    print(rt_ak_all)
    print()

    df_pred = get_answer_form(rt_ak_all, [1] * len(rt_ak_all))
    df_submit = get_submit(df_pred, './pred.csv')

    return


if __name__ == '__main__':
    main()
