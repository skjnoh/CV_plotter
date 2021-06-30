from numpy import abs
from numpy import array
import numpy as np
import pandas as pd

#Behaviors: 1. Take all files in the given folder and then analyze them to get the ECSA number and plot
# Return a two dimensional array with the scan rate vs i_diff
def ECSA_Analysis(df_ECSA):
    ScanRates = []
    Cur_diff = []
    ColNum = len(df_ECSA.columns)

    for i in list(range(ColNum)):
        if i == ColNum-1:
            ScanRates = np.float64(df_ECSA['Text'][0].split())
        elif i%2 == 1:  # current get current difference
            #print('debug1')

            Cur_diff.append(
                abs(df_ECSA.iloc[df_ECSA.iloc[:,i].dropna().size-1,i] - df_ECSA.iloc[int(df_ECSA.iloc[:,i].dropna().size/2-1),i])/2
                    )

    if len(ScanRates) != len(Cur_diff):
        print("error: Scan rate list length different from i_diff list length")
    #print(Cur_diff)
    Cap_array = [array(ScanRates), array(Cur_diff)]
    return Cap_array


def CValigner(df_CV1, df_CV2):
    #as written, this function assumes that scan direction is negative, with same scan rate and lower vertex potential.
    min_start_pot = min(df_CV1["Potential applied (V)"][0], df_CV2["Potential applied (V)"][0])
    df_CV1_sub = df_CV1[df_CV1["Potential applied (V)"] < min_start_pot].reset_index()
    df_CV2_sub = df_CV2[df_CV2["Potential applied (V)"] < min_start_pot].reset_index()
    new_cur_series = df_CV1_sub['WE(1).Current (A)'] - df_CV2_sub['WE(1).Current (A)']
    frame = {"Potential applied (V)":df_CV1_sub["Potential applied (V)"], 'WE(1).Current (A)':new_cur_series}
    return pd.DataFrame(frame)

