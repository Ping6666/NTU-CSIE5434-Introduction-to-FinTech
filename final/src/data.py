import pandas as pd


def get_custinfo(f_name):
    """
    f_name: './data/public_train_x_custinfo_full_hashed.csv'
    """

    df_custinfo = pd.DataFrame(pd.read_csv(f_name))

    # occupation_code number range 0~20
    df_custinfo['occupation_code'].fillna(value=-1.0, inplace=True)

    # clear out string (which can not be parse by the sklearn)
    df_custinfo = df_custinfo.drop('cust_id', axis=1)
    return df_custinfo


def get_x_alert_date(f_name):
    """
    f_name: './data/train_x_alert_date.csv' or './data/public_x_alert_date.csv'
    """

    df_x = pd.DataFrame(pd.read_csv(f_name))

    return df_x


def get_y_sar_flag(f_name):
    """
    f_name: './data/train_y_answer.csv'
    """
    df_y = pd.DataFrame(pd.read_csv(f_name))
    return df_y


def get_pred_list(f_name):
    """
    f_name: './data/all_x_alert.csv'
    """

    df_all = pd.DataFrame(pd.read_csv(f_name))

    # get col alert_key
    pred_list = df_all['alert_key'].to_list()
    return pred_list


def get_answer(df_x: pd.DataFrame, y_pred: list):
    """
    correct from the dataset and pred_list to answer dataframe
    """
    pred_list = get_pred_list('./data/all_x_alert.csv')

    # add col: probability
    df_x['probability'] = y_pred
    # only take cols: ['alert_key', 'probability']
    df_xy = df_x[['alert_key', 'probability']]

    # filter out the alert_key not in pred_list
    df_xy = df_xy[df_xy['alert_key'].isin(pred_list)]

    # get what is left from the pred_list, make it to pd.DataFrame and set probability
    diff_list = list(set(pred_list) - set(df_xy['alert_key'].to_list()))
    df_diff = pd.DataFrame(diff_list, columns=['alert_key'])
    df_diff['probability'] = 0

    # concat the dataframe
    df_xy = pd.concat([df_xy, df_diff], axis=0, ignore_index=True)
    # df_xy = df_xy.sort_values(by=['probability'], ascending=False)
    df_xy = df_xy.sort_values(by=['probability'], ascending=True)

    ## checker ##
    assert len(df_xy.index) == len(df_xy['alert_key'].unique())

    return df_xy


def df_workhouse():
    ## get all needed df ##
    # custinfo
    df_custinfo = get_custinfo(
        './data/public_train_x_custinfo_full_hashed.csv')

    # train alert_date & sar_flag
    df_train_x = get_x_alert_date('./data/train_x_alert_date.csv')
    df_train_y = get_y_sar_flag('./data/train_y_answer.csv')

    # public alert_date
    df_public_x = get_x_alert_date('./data/public_x_alert_date.csv')

    # get dataset with col in:
    # ['alert_key', 'date', 'alert_key', 'cust_id', 'risk_rank',
    # 'occupation_code', 'total_asset', 'AGE', 'sar_flag']
    df_train_x_custinfo = pd.merge(df_train_x, df_custinfo, on='alert_key')
    df_train_xy = pd.merge(df_train_x_custinfo, df_train_y, on='alert_key')

    # get all alert_date (the pred data)
    df_all_x = pd.concat([df_train_x, df_public_x], axis=0, ignore_index=True)

    # get dataset with col in:
    # ['alert_key', 'date', 'alert_key', 'cust_id', 'risk_rank',
    # 'occupation_code', 'total_asset', 'AGE']
    df_all_x_custinfo = pd.merge(df_all_x, df_custinfo, on='alert_key')

    # final process
    train_y = df_train_xy['sar_flag'].to_numpy()
    df_train_x = df_train_xy.drop('sar_flag', axis=1)
    return (df_train_x, train_y), df_all_x_custinfo
