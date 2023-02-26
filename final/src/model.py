from sklearn import ensemble


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
    # c_ensemble = ensemble.ExtraTreesRegressor(n_estimators=200)

    # GOOD ??? #
    c_ensemble = ensemble.RandomForestRegressor(n_estimators=200)

    # GOOD ??? #
    # c_ensemble = ensemble.BaggingRegressor(n_estimators=200)

    # GOOD ??? #
    # but output between -1 or 1
    # c_ensemble = ensemble.GradientBoostingRegressor(n_estimators=200,
    #                                                 learning_rate=1)
    return c_ensemble
