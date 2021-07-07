from datetime import datetime
import matplotlib.pyplot as plt
from utils import lagrange, select_sample
import numpy as np
import sympy as sp
import pandas as pd
import math


def analysis_range(df):
    
    ff = df.sort_values(by=["Fecha"])
            
    min_start_date = ff["Fecha"].iloc[0]
    max_end_date = ff["Fecha"].iloc[-1]
    

    print(min_start_date)
    print(max_end_date)
    while True:
        try:
        
            start_date = datetime.strptime(input("ingrese fecha de inicio (formato: dd-mm-YYYY ej: 31-05-2020): "), '%d-%m-%Y')
            
            if(start_date<min_start_date or start_date>max_end_date):
                print(f"La fecha seleccionada no es valida, escoja una fecha entre {min_start_date} y {max_end_date}")
                raise Exception

            end_date = datetime.strptime(input("ingrese fecha de fin (formato: dd-mm-YYYY ej: 31-05-2020): "), '%d-%m-%Y')
            
            if(end_date<min_start_date or end_date>max_end_date or start_date>end_date):
                print(f"La fecha seleccionada no es valida, escoja una fecha entre {min_start_date} y {max_end_date} que sea mayor a {start_date}")
                raise Exception
            
            if(start_date>end_date):
                print("Fecha de inicio es despues de la fecha de fin")
                raise Exception      
                

            mask = (df['Fecha'] > start_date) & (df['Fecha'] <= end_date)

            sample = select_sample(df.loc[mask])

            if len(sample)<=0:
                print("no hay datos en ese rango de fechas")
                raise Exception()

            break

        except Exception:
            print("Fechas mal ingresadas, intente de nuevo")
            
    return sample


def graphs(df):

    while(True):
        try:
            option = int(input("""Seleccione una opcion:
            1. Puntos
            2. Polinomio
            """))

            if(option>2 or option<1):
                raise Exception
            
            break

        except:
            print("opcion invalida intente de nuevo")

    
    if option==1:
        plt.figure(figsize = (15, 10))
        df = df.sort_values(by=['Diferencia Horas'])
        plt.plot(df["Diferencia Horas"],df["mg/dL"])
        
        plt.xlabel("Tiempo desde Medicamento (hrs)")
        plt.ylabel("Glucosa en Sangre (mg/dL)")
        plt.title('Glucosa en Sangre vs Tiempo desde Medicamento')
        plt.grid()
        plt.legend()

        plt.show()
    
    elif option ==2:
        x = sp.symbols('x')
        polinomio = lagrange(df["Diferencia Horas"],df["mg/dL"])
       

        fx = sp.lambdify(x,polinomio)
        plt.figure(figsize = (15, 10))

        xx = np.linspace(min(df["Diferencia Horas"]),max(df["Diferencia Horas"]),1000)
        yy = [fx(xxi) for xxi in xx]

        plt.plot(xx,yy)
        plt.plot(df["Diferencia Horas"],df["mg/dL"],'ro')# plotea solo los puntos

        plt.xlabel("Tiempo desde Medicamento (hrs)")
        plt.ylabel("Glucosa en Sangre (mg/dL)")
        plt.title('Glucosa en Sangre vs Tiempo desde Medicamento')
        plt.grid()
        plt.legend()

        plt.show()


    
def razon_de_cambio(x,y):

    
    r = np.empty((len(y)))
    r[0] = (y[1]-y[0])/(x[1]-x[0])
    
    for i in range(1,len(y)-1):
        r[i]=(y[i+1]-y[i-1])/(x[i+1]-x[i-1])
    
    r[-1]=(y[-1]-y[-2])/(x[-1]-x[-2])
    
    return r



def trapecio(x,y):
    h = (x[-1]-x[0]) / ((len(x)) - 1)
    return (h/2)* (y[0] + 2 * sum(y[1:-1]) + y[-1])

#############
def lin_reg(x,y):
    sum_x = x.sum()
    sum_y = y.sum()
    sum_x_y = x@y
    sum_x_squared = (x**2).sum()
    n = len(x)
    
    m = ( (n*sum_x_y) - (sum_x*sum_y) ) / ( (n*sum_x_squared) - sum_x**2 )
    b = ( (sum_y*sum_x_squared) - (sum_x)(sum_x_y) ) / ( (n*sum_x_squared) - sum_x*2 )
    
    return lambda x: m*x + b

def r_squared(f,x,y):
    y_predicted = f(x)
    
    sum_of_squares_of_residuals = ((y_predicted - y)**2).sum()
    total_sum_of_squares = ((y - y.mean())**2).sum()
    
    print(sum_of_squares_of_residuals)
    print(total_sum_of_squares)
    return 1 - (sum_of_squares_of_residuals/total_sum_of_squares)




#########

def estimate_coef(x, y):
    n = np.size(x)#obtenemos el numero de observaciones
 
    m_x = np.mean(x)#media de x
    m_y = np.mean(y)#media de y
 
    SS_xy = np.sum(y*x) - n*m_y*m_x #hacemos el calculo de desviacion
    SS_xx = np.sum(x*x) - n*m_x*m_x
 
    b_1 = SS_xy / SS_xx#calculamos los coeficientes de regresion
    b_0 = m_y - b_1*m_x
 
    return (b_0, b_1)
 
def plot_regression_line(x, y, b):
    plt.scatter(x, y, color = "m",
               marker = "o", s = 30)#plot de los puntos
 
    y_pred = b[0] + b[1]*x #obtenemos la recta de la regresion
 
    plt.plot(x, y_pred, color = "g")#grafica de la regresion
    plt.xlabel('Diferencia de Horas')
    plt.ylabel('mg/dL')
    plt.grid()
    plt.title("Diferencia de horas vs mg/dL")
    plt.show()
 
def prueba1(x1,y1,op):
    
    b = estimate_coef(x1, y1)
    x = sp.symbols('x')
    
    


    print("La funcion de regresion lineal es: \n y= {} {} + ({})".format(b[1],x,b[0]))
    
    prueba1.variable1=b[1]
    prueba1.variable2=b[0]
    if op == 6:
        pass
    else:

        plot_regression_line(x1, y1, b)
        

def reg_lin(y):
    #y=mx+b
    #return prueba1.variable1 * x + (prueba1.variable2)
    return (y-prueba1.variable2)/prueba1.variable1
    
    

    