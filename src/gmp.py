from datetime import datetime, timedelta
from cli_menu import MenuDisplay
from utils import read_file
from analysis import analysis_range, graphs


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
            2. Tabla de metabolización
            3. Aceleración metabólica de la glucosa
            4. Glucosa Promedio
            5. Glucosa-Meta
            6. Tendencia
            7. Salir
            """))

            if opcion == 1:
                SAMPLE = analysis_range(df)
            elif(len(SAMPLE)==0):
                raise Exception("Tiene que seleccionar un rango de fechas para seleccionar cualquier otra opcion")

            elif opcion == 2:
                graphs(SAMPLE)
            else:
                print("Opcion invalida, intente de nuevo")
                raise Exception

        except Exception:
            print("Ocurrio un error, intente de nuevo")




