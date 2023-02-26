from sklearn import ensemble
from xgboost import XGBRegressor, XGBRFRegressor


def model_workhouse():
    random_state = 5487  # aka. the seed

    #### sklearn.ensemble ####

    ## rp ##
    # train: 1.0
    # validation: 0.005434782608695652
    # public: 0.006218905472636816
    # c_model = ensemble.ExtraTreesRegressor(n_estimators=200)

    ## rp ##
    # train: 0.010565684899485742
    # validation: 0.005429864253393665
    # public: 0.006218905472636816
    # c_model = ensemble.RandomForestRegressor(n_estimators=200)

    # c_model = ensemble.BaggingRegressor(n_estimators=200)

    # can not map well on distribution
    # c_model = ensemble.AdaBoostRegressor(n_estimators=200, learning_rate=1)

    # strange outcome
    # c_model = ensemble.GradientBoostingRegressor(n_estimators=200, learning_rate=1)

    # strange outcome
    # c_model = ensemble.HistGradientBoostingRegressor(learning_rate=1)

    #### xgboost ####

    c_model = XGBRFRegressor(random_state=random_state)

    # c_model = XGBRegressor(random_state=random_state)

    return c_model
