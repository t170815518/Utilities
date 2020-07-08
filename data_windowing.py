# windowing the dataset 
def windowing(df,target,win_size=96,feature_win_size=96,lag=96):
    '''
    Generate windowing DataFrame for df
    
    arguments: 
        df: target pandas.DataFrame
        target: the name of predictor
        win_size: the size of windows to feed in models as orignal data
        feature_win_size: the size of windows to analyze, but the original data is not feed into models. feature_win_size > win_size. 
    
    return: the new dataframe after windowing.'''
    from numpy.fft import fft 
    
    def get_outliers_rows(S):
        compare = (S-S.mean()).abs() > 2*S.std()
        windows_stat['outlier_max'] = S[compare].max()
        windows_stat['outlier_min'] = S[compare].min()
        windows_stat['outlier_distance'] = windows_stat['outlier_max'] - windows_stat['outlier_min']
        windows_stat['outlier_numbers'] = compare.sum()
        windows_stat.fillna(0,inplace=True)
        
    def entropy(series):
        import scipy.stats
        p_data = series.value_counts()
        entropy = scipy.stats.entropy(p_data)
        return entropy
    
    def negative_turning(series):
        point_num = 0
        last = 0
        for i,value in series.iteritems():
            if i==0:
                last = value
                continue 
            if value < last:
                point_num += 1 
            last = value 
        return point_num 
    
    def positive_turning(series):
        point_num = 0
        last = 0
        for i,value in series.iteritems():
            if i==0:
                last = value
                continue 
            if value > last:
                point_num += 1 
            last = value 
        return point_num 
        
    def get_slope(signal):
        """
        copy from tsfel 
        Computes the slope of the signal.
        Slope is computed by fitting a linear equation to the observed data.
        Feature computational cost: 1
        Parameters
        ----------
        signal : nd-array
            Input from which linear equation is computed
        Returns
        -------
        float
            Slope
        """
        t = np.linspace(0, len(signal) - 1, len(signal))
        return np.polyfit(t, signal, 1)[0]
    
    windows = pd.DataFrame()
    for i in range(0,feature_win_size):
        windows[str(i)] = df[target].shift(lag+i)
    windows = windows[lag+feature_win_size-1:] # Remove rows with NaN 
    
    windows_stat = pd.DataFrame()
    windows_stat['Mean'] = windows.mean(axis=1)
    windows_stat['Median'] = windows.median(axis=1)
    windows_stat['std'] = windows.std(axis=1)
#     windows.apply(get_outliers_rows,axis=1)
    windows_stat['skewness'] = windows.skew(axis=1)
    windows_stat['kurtosis'] = windows.kurtosis(axis=1)
    windows_stat['entropy'] = windows.apply(entropy,axis=1)
    windows_stat['25quantile'] = windows.quantile(0.25,axis=1)
    windows_stat['75quantile'] = windows.quantile(0.75,axis=1)
    windows_stat['InterquartileRange'] = windows_stat['75quantile'] - windows_stat['25quantile']
    windows_stat['mad'] = windows.mad(axis=1)
    windows_stat['RMS'] = windows_stat['Mean']**(1/2)
    windows_stat['Var'] = windows.var(axis=1)
#     windows_stat['NegativeTurning'] = windows.apply(negative_turning, axis=1)
#     windows_stat['PositiveTurning'] = windows.apply(negative_turning, axis=1)
    windows_stat['mean_abs_diff'] = windows.apply(lambda x: np.mean(np.abs(np.diff(x))),axis=1)
    windows_stat['mean_diff'] = windows.apply(lambda x: np.mean(np.diff(x)),axis=1)
    windows_stat['median_abs_diff'] = windows.apply(lambda x: np.median(np.abs(np.diff(x))),axis=1)
    windows_stat['sum_abs_diff'] = windows.apply(lambda x: np.sum(np.abs(np.diff(x))),axis=1)
    windows_stat['abs_energy'] = windows.apply(lambda x: np.sum(np.array(x) ** 2),axis=1)
    windows_stat['slope'] = windows.apply(get_slope,axis=1)
    windows_stat.fillna(0,inplace=True)
    
    windows_stat['96'] = df[target].shift(96)
    windows_stat['96'].fillna(windows_stat['96'].mean(),inplace=True)
    windows_stat['192'] = df[target].shift(192)
    windows_stat['192'].fillna(windows_stat['192'].mean(),inplace=True)
    windows_stat['288'] = df[target].shift(288)
    windows_stat['288'].fillna(windows_stat['288'].mean(),inplace=True)
    windows_stat['momentum'] = pd.DataFrame(windows_stat['96'] - windows_stat['192'])
    windows_stat['force'] = pd.DataFrame(windows_stat['96']- 2*windows_stat['192']+windows_stat['288'])
    windows_stat.drop(['96','192','288'],axis=1,inplace=True)
    
    
    windows_origin = pd.DataFrame()
    for i in range(0,win_size):
        windows_origin[str(i)] = df[target].shift(lag+i)
    windows_origin = windows_origin[lag+feature_win_size-1:] # Remove rows with NaN 

    return pd.concat([df[lag+feature_win_size-1:],windows_origin,windows_stat],axis=1)
