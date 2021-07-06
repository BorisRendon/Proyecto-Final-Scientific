from datetime import datetime, timedelta
from cli_menu import MenuDisplay
from utils import read_file
from analysis import analysis_range, graphs, razon_de_cambio
import numpy as np


def funxx():
    x = input("numero")
    print(x)
    return x

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
        print(len(SAMPLE)==0)
        try:
            opcion = int(input("""Selecciones una opcion (ingrese el numero):
            1. Rango de análisis
            2. Gráficas
            3. Tabla de metabolización
            4. Aceleración metabólica de la glucosa
            5. Glucosa Promedio
            6. Glucosa-Meta
            7. Tendencia
            8. Salir
            """))

            if opcion == 1:
                SAMPLE = analysis_range(df)
                #print(SAMPLE['Diferencia Horas'])
            elif(len(SAMPLE)==0):
                raise Exception("Tiene que seleccionar un rango de fechas para seleccionar cualquier otra opcion")

            elif opcion == 2:
                graphs(SAMPLE)

            elif opcion ==3:
                xy=SAMPLE.to_numpy()
                mgdL=xy[:,1]#mg
                condicion=xy[:,3]#condicion
                diferencia_horas=xy[:,4]#dif horas
                


                r=razon_de_cambio(diferencia_horas,mgdL)
                r
                #tabla_razon_cambio= pd.DataFrame(r,columns=['Razon de cambio'])
                #tabla_razon_cambio
                #faltaria agregarle a este df(tabla razon cambio) la condicion (ayuno, desayuno, almuerzo etc)
                
            


            else:
                print("Opcion invalida, intente de nuevo")
                raise Exception

        except Exception:
            print("Ocurrio un error, intente de nuevo")




