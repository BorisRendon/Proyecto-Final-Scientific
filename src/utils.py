import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import pandas as pd
import math


read_file = lambda file_path: pd.read_excel(file_path, header=1, index_col=0, parse_dates=[1,3]).dropna()



numerical_non_nmerical = lambda df: {"numerical": df.select_dtypes(include='number').columns,
                                     "non_numerical":df.select_dtypes(exclude='number').columns}


def select_sample(df):
    selected =set()
    indexes = []
    n=0

    print(len(df))

    if(len(df)<=10):
        return df

    while n < 10:
        index = np.random.randint(len(df))
        x_val = df["Diferencia Horas"].iloc[index]
        if(x_val not in selected):
            selected.add(x_val)
            indexes.append(index)
            n = n+1
            print(n)
        else:
            pass
    return df.iloc[indexes]

def multiplicativo(x_, i):
    x = sp.symbols('x')

    multiplicativo = 1
    for j in range(len(x_)):
        if j != i:
            multiplicativo = multiplicativo* (x - x_.iloc[j])/(x_.iloc[i]-x_.iloc[j])
    return multiplicativo

def lagrange(x_,y_):
    result = 0
    for i in range(len(x_)):
        mult = multiplicativo(x_,i)
        result += y_.iloc[i]*mult
    return sp.simplify(result)