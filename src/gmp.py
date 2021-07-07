from datetime import datetime, timedelta
from cli_menu import MenuDisplay
from utils import read_file
from analysis import analysis_range, graphs, razon_de_cambio,trapecio,lin_reg,r_squared,estimate_coef,plot_regression_line,prueba1,reg_lin
import numpy as np
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt

if __name__ == "__main__":

    SAMPLE = []

    
    df = read_file("../Glucosa-Project.xlsx")

    while True:
        try:
            GLUCOSE_INTAKE_HOUR = input("ingrese la hora en la que toma su primera dosis del meidcamento (fomato 24 hrs): ")
            hours, minutes = GLUCOSE_INTAKE_HOUR.split(':')

            if(int(hours)>23 or int(minutes)>59):
                raise Exception
            break

        except:
            print("Hora invalida, intente de nuevo")
            pass

    df['Diferencia Horas'] = [time.hour - int(hours) for time in df["Hora"]]

    salir = False

    while not salir:
        try:
            opcion = int(input("""Selecciones una opcion (ingrese el numero):
            1. Rango de análisis
            2. Gráficas
            3. Tabla de metabolización
            4. Aceleración metabólica de la glucosa
            5. Glucosa Promedio
            6. Glucosa-Meta
            7. Tendencia
            8. Resumen Estadistico
            9. Salir
            """))

            if opcion == 1:
                SAMPLE = analysis_range(df)
                #print(SAMPLE['Diferencia Horas'])
                SAMPLE=SAMPLE.sort_values(by=['Diferencia Horas'])

            elif(len(SAMPLE)==0):
                raise Exception("Tiene que seleccionar un rango de fechas para seleccionar cualquier otra opcion")

            elif opcion == 2:
                graphs(SAMPLE)

            elif opcion ==3:
                xy=SAMPLE.to_numpy()
                mgdL=xy[:,1]#mg
                fecha=xy[:,0]#fecha
                condicion=xy[:,3]#condicion
                diferencia_horas=xy[:,4]#dif horas
                


                r=razon_de_cambio(diferencia_horas,mgdL)
                tabla_razon_cambio= pd.DataFrame(r,columns=['Razon de cambio'])
                tabla_razon_cambio["Condicion"]=condicion
                tabla_razon_cambio["Fecha"]=fecha
                print(tabla_razon_cambio)
                #faltaria agregarle a este df(tabla razon cambio) la condicion (ayuno, desayuno, almuerzo etc)
                
            elif opcion ==4:
                #aceleracion metabolica
                xy=SAMPLE.to_numpy()
                mgdL=xy[:,1]#mg
                fecha=xy[:,2]#fecha
                condicion=xy[:,3]#condicion
                diferencia_horas=xy[:,4]#dif horas
                r=razon_de_cambio(diferencia_horas,mgdL)
                r2=razon_de_cambio(diferencia_horas,r)
                tabla_razon_cambio_r2= pd.DataFrame(r2,columns=['Aceleracion'])
                aceleracion=tabla_razon_cambio_r2["Aceleracion"]
                max_value = aceleracion.max()
                print("Aceleracion de glucosa maxima en la sangre: " , max_value)
                print("\n")
                min_value = aceleracion.min()
                print("Aceleracion de glucosa minima en la sangre:" , min_value)

            elif opcion ==5:
                #Glucosa promedio
                xy=SAMPLE.to_numpy()
                mgdL=xy[:,1]#mg
                diferencia_horas=xy[:,4]#dif horas


                glucosa_promedio = trapecio(diferencia_horas,mgdL)
                b=diferencia_horas[-1]
                a=diferencia_horas[0]
                print(a)
                glucosa = glucosa_promedio/(b-a)
                print("La glucosa promedio en la sangre para el intervalo de fechas seleecionado es: \n: ", glucosa)

            elif opcion==6:
                #Glucosa-meta
                x=sp.symbols('x')
                xy=SAMPLE.to_numpy()
                mgdL=xy[:,1]#mg
                diferencia_horas=xy[:,4]#dif horas
                prueba1(diferencia_horas,mgdL,op=6)
                glucosa_input= float(input("Ingrese un valor especifico de glucosa:  "))
                glucosa_meta=reg_lin(glucosa_input)
                print("La glucosa meta en sangre se alcanzará en:", glucosa_meta)

            elif opcion==7:
                x=sp.symbols('x')
                xy=SAMPLE.to_numpy()
                mgdL=xy[:,1]#mg
                diferencia_horas=xy[:,4]#dif horas
                regression = lin_reg(diferencia_horas,mgdL)
                print(str(regression(x)))
                print("r cuadrado: ",r_squared(regression,diferencia_horas,mgdL))

                plt.figure(figsize = (15, 10))
                plt.xlabel("Diferencia Horas")
                plt.ylabel("Glucosa")
                plt.title('Regresion linear')
                plt.grid()
                plt.plot(diferencia_horas,regression(diferencia_horas),'r')
                plt.plot(diferencia_horas,mgdL, 'bo')
                plt.show()


            elif opcion==8:
                #resumen estadistico
                print(df['mg/dL'].describe())
                plt.figure(figsize = (15, 10))
                plt.title('Histograma Glucosa')
                plt.grid()
                plt.hist(df["mg/dL"])
                plt.show()

            elif opcion ==9:
                exit()
            else:
                print("Opcion invalida, intente de nuevo")
                raise Exception

        except Exception:
            print("Ocurrio un error, intente de nuevo")




