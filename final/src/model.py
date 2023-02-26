from sklearn import ensemble


def ensemble_workhouse():
    c_ensemble = ensemble.ExtraTreesRegressor(n_estimators=200)

    # c_ensemble = ensemble.RandomForestRegressor(n_estimators=200)

    # c_ensemble = ensemble.BaggingRegressor(n_estimators=200)

    # but output between -1 or 1
    # c_ensemble = ensemble.GradientBoostingRegressor(n_estimators=200, learning_rate=1)

    # can not map well on distribution
    # c_ensemble = ensemble.AdaBoostRegressor(n_estimators=200, learning_rate=1)

    # but output between -1 or 1
    # c_ensemble = ensemble.HistGradientBoostingRegressor(learning_rate=1)
    return c_ensemble
