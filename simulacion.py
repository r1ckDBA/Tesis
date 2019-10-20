# Programa para simular donaciones en la ciudad de Guadalajara
# Autor: Ricardo E Acosta V    A01301931
# ITESM MCC      8/Ago/2019
import json
import os
from tkinter import *
from tkinter import ttk
import random
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


global df 
global data


def resultados (dict_total):
    tab_num = len(tabs) 
    print("Creando tab:" , tab_num)
    tabs.append(ttk.Frame(note))
    note.add(tabs[tab_num],text = str(tab_num) + " - Resultados" )
    note.pack()
 
    print("Imprimeidno resultados")
    df = pd.DataFrame(dict_total)
    Label(tabs[tab_num], text = df.tail(20), bg ='white', borderwidth= 3, relief="raised", font = "Verdana 10" ).grid(row = 1, column = 1 )
    Label(tabs[tab_num], text = df["Distancia"].describe(), bg ='white', borderwidth=3, relief="raised" , font = "Verdana 10" ).grid(row =1, column = 2) 
    Label(tabs[tab_num], text = df["Utilidad"].describe(), bg ='white', borderwidth=3, relief="raised", font = "Verdana 10").grid(row = 1, column = 3) 
    Label(tabs[tab_num], text = df["ONG"].value_counts() , bg ='white', borderwidth=3, relief="raised", font = "Verdana 10").grid(row = 2, column = 3) 
    Label(tabs[tab_num], text = df["ONG"].value_counts().describe() , bg ='white', borderwidth=3, relief="raised", font = "Verdana 10").grid(row = 2, column = 4) 


    df2 = pd.DataFrame(df, columns=['dias','Distancia','Utilidad'])
    df2 = df2 [['dias','Distancia','Utilidad']].groupby('dias' ).mean()
    Label(tabs[tab_num], text = df2.head(20), bg ='white', borderwidth=3, relief="raised", font = "Verdana 10").grid(row = 2, column = 2) 


    figure1 = plt.Figure(figsize=(7,4), dpi=100)
    ax2 = figure1.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure1, tabs[tab_num])
    line2.get_tk_widget().grid( row = 2 , column = 1)
    df2.plot(kind='line', legend=True, ax=ax2, color=['c','b'] ,marker='o', fontsize=10)
    ax2.set_title('Promedios por dia')    
    


def generar_donacion():
	 nueva_donacion = {
	 "x" : random.randint(150, 900),
	 "y" : random.randint(50, 600),
	 "tipo" : random.randint(1,10) }
	 return nueva_donacion

def asignacion_simple (donacion):
    distancia = 1000
    v_utilidad =0
    utilidad_nueva = 0
    ong_elegida="None"

    for ong in data["ONGs"]:

       if donacion["tipo"] == ong["prioridad1"]: v_utilidad=100
       if donacion["tipo"] == ong["prioridad2"]: v_utilidad=66
       if donacion["tipo"] == ong["prioridad3"]: v_utilidad=33
    
    #Si la nueva donacion tiene alguna utilidad
       if v_utilidad > 0 :
          distancia_nueva=math.sqrt( ( ong["x"] - donacion["x"] ) ** 2 + ( ong["y"] - donacion["y"] ) ** 2 )
          if distancia_nueva < distancia:
             distancia = distancia_nueva
             utilidad_nueva = v_utilidad             
             ong_elegida = str(ong["Etiqueta"] )
             x_elegida = ong["x"]
             y_elegida = ong["y"]   
    print("ONG elegida:", ong_elegida , " a una distancia de ",distancia )
     
    asignacion = { 
       "Etiqueta" : ong_elegida , 
       "ONG_X" :  x_elegida ,
       "ONG_Y" :  y_elegida ,
       "Distancia" : distancia ,
       "Donacion_x" : donacion["x"] ,
       "Donacion_y" : donacion["y"] ,
       "Tipo" : donacion["tipo"] , 
       "Utilidad" : utilidad_nueva
	 }
    
    return asignacion

def asignacion_utilidad (donacion):
    distancia = 1000
    v_utilidad =0
    utilidad_nueva = 33
    ong_elegida="None"
    for ong in data["ONGs"]:
       #Asigna utilidad
       if donacion["tipo"] == ong["prioridad1"]: v_utilidad=100
       if donacion["tipo"] == ong["prioridad2"]: v_utilidad=66
       if donacion["tipo"] == ong["prioridad3"]: v_utilidad=33

       #Si la donacion tiene una mejor utilidad
       if v_utilidad >= utilidad_nueva:
             distancia_nueva=math.sqrt( ( ong["x"] - donacion["x"] ) ** 2 + ( ong["y"] - donacion["y"] ) ** 2 )
             if distancia_nueva < distancia:
                utilidad_nueva = v_utilidad
                distancia = distancia_nueva
                ong_elegida = str(ong["Etiqueta"] )
                x_elegida = ong["x"]
                y_elegida = ong["y"]   
    print("ONG elegida:", ong_elegida , " a una distancia de ",distancia )
     
    asignacion = { 
       "Etiqueta" : ong_elegida , 
       "ONG_X" :  x_elegida ,
       "ONG_Y" :  y_elegida ,
       "Distancia" : distancia ,
       "Donacion_x" : donacion["x"] ,
       "Donacion_y" : donacion["y"] ,
       "Tipo" : donacion["tipo"] , 
       "Utilidad" : utilidad_nueva
	 }
    
    return asignacion


def asignacion_3ra (donacion):
    distancia = 1000
    v_utilidad =0
    utilidad_nueva = 0
    ong_elegida="None"
    matriz_donaciones=[]

    for ong in data["ONGs"]:

       if donacion["tipo"] == ong["prioridad1"]: v_utilidad=100
       if donacion["tipo"] == ong["prioridad2"]: v_utilidad=66
       if donacion["tipo"] == ong["prioridad3"]: v_utilidad=33
    
       #Si la nueva donacion tiene alguna utilidad
       if v_utilidad > 0 :
          distancia_nueva=math.sqrt( ( ong["x"] - donacion["x"] ) ** 2 + ( ong["y"] - donacion["y"] ) ** 2 )
          matriz_donaciones.append([distancia_nueva,v_utilidad,str(ong["Etiqueta"]),ong["x"],ong["y"] ] )

    d_panda = pd.DataFrame(matriz_donaciones, columns = ['distancia','utilidad','Etiqueta','ONG_X','ONG_Y'])
    
    #Evaluacion de Utilidad / distancia
    d_panda["Dist_100"] = d_panda["distancia"] * 100 / d_panda["distancia"].max()
    d_panda["EVAL"] = d_panda["utilidad"] /  d_panda["Dist_100"]
    sort_by_eval = d_panda.sort_values('EVAL',ascending=False)
    print (sort_by_eval)
    ong_row = sort_by_eval.head(1)
    #print(ong_row)

    ong_elegida = ong_row["Etiqueta"].values[0]
    x_elegida = ong_row["ONG_X"].values[0]
    y_elegida = ong_row["ONG_Y"].values[0] 
    print("ONG elegida:", ong_elegida , " a una distancia de ",ong_row["distancia"].values[0],"\n")
     
    asignacion = { 
       "Etiqueta" : ong_elegida , 
       "ONG_X" :  x_elegida ,
       "ONG_Y" :  y_elegida ,
       "Distancia" : ong_row["distancia"].values[0] ,
       "Donacion_x" : donacion["x"] ,
       "Donacion_y" : donacion["y"] ,
       "Tipo" : donacion["tipo"] , 
       "Utilidad" : ong_row["utilidad"].values[0]
	 }
    
    return asignacion

def asignacion_4ta (donacion, my_DF):
    distancia = 1000
    v_utilidad =0
    utilidad_nueva = 0
    ong_elegida="None"
    matriz_donaciones=[]

    for ong in data["ONGs"]:

       if donacion["tipo"] == ong["prioridad1"]: v_utilidad=100
       if donacion["tipo"] == ong["prioridad2"]: v_utilidad=66
       if donacion["tipo"] == ong["prioridad3"]: v_utilidad=33
    
       #Si la nueva donacion tiene alguna utilidad
       if v_utilidad > 0 :
          distancia_nueva=math.sqrt( ( ong["x"] - donacion["x"] ) ** 2 + ( ong["y"] - donacion["y"] ) ** 2 )
          matriz_donaciones.append([distancia_nueva,v_utilidad,str(ong["Etiqueta"]),ong["x"],ong["y"] ] )

    d_panda = pd.DataFrame(matriz_donaciones, columns = ['distancia','utilidad','Etiqueta','ONG_X','ONG_Y'])
    

    #Evaluacion de Utilidad / distancia
    d_panda["Dist_100"] = d_panda["distancia"] * 100 / d_panda["distancia"].max()
    d_panda["EVAL"] = d_panda["utilidad"] /  d_panda["Dist_100"]

    #Evaluacion de Sesgo
    if len(my_DF) > 0 : 
       #df = pd.DataFrame([df],columns = ["id","information"])
       df5= pd.DataFrame(my_DF)
       #print(df5)
       df5.index.names = ['Idx1']
       #print("Idx \n",df5)
       #print("Uniendo \n", d_panda,"Con ..... \n", df5)
       d_panda = pd.merge(d_panda, df5, how='left', left_on = ['Etiqueta'], right_on= ['Idx1'] )
       d_panda.replace(np.nan , 0 , regex=True ) 
       d_panda["EVAL2"] = d_panda["EVAL"] * d_panda["ONG"].max() / d_panda["ONG"] 
       sort_by_eval = d_panda.sort_values('EVAL2',ascending=False)
       print(sort_by_eval)
       ong_row = sort_by_eval.head(1)
    
    else: 
       sort_by_eval = d_panda.sort_values('EVAL',ascending=False)
       ong_row = sort_by_eval.head(1)
    #print(ong_row)

    ong_elegida = ong_row["Etiqueta"].values[0]
    x_elegida = ong_row["ONG_X"].values[0]
    y_elegida = ong_row["ONG_Y"].values[0] 
    print("ONG elegida:", ong_elegida , " a una distancia de ",ong_row["distancia"].values[0],"\n")
     
    asignacion = { 
       "Etiqueta" : ong_elegida , 
       "ONG_X" :  x_elegida ,
       "ONG_Y" :  y_elegida ,
       "Distancia" : ong_row["distancia"].values[0] ,
       "Donacion_x" : donacion["x"] ,
       "Donacion_y" : donacion["y"] ,
       "Tipo" : donacion["tipo"] , 
       "Utilidad" : ong_row["utilidad"].values[0]
	 }
    
    return asignacion



def simulacion():
     dict_total=[]
     funcion = fun_obj.get()
     no_dias = dias.get() 
     if len( funcion ) > 1 :
          print(funcion)
          print(no_dias)

          i=0
          while i < int(no_dias):
             i=i+1		   	   
             print ("Simulando dia ",i)

             if i > 1:
                #print ("Calculando coeficientes de ONGs")
                df3 = pd.DataFrame(dict_total)
                df3 = pd.DataFrame(df3, columns=['ONG'])
                #df4 = df3.groupby('ONG')['ONG'].value_counts()
                df4 = df3.ONG.value_counts()
                #print(df4) 
                #print(df4.describe()) 
             else: 
                df4 = []


             j=0 
             while j < 100:
                j=j+1
                donacion = generar_donacion()
                ##print(donacion) 
                if funcion == 'simple':
                   if i==1:
                      ttk.Label(frame1, text = ".", background = 'blue').place(x = donacion["x"], y = donacion["y"], width =5, height = 5)

                   registro = asignacion_simple (donacion)
                   registro_armado = {
                      "dias" : i ,
                      "ONG"  : registro["Etiqueta"],
                      "ONG_X" : registro["ONG_X"] ,
                      "ONG_Y" : registro["ONG_Y"] ,
                      "Distancia"  : registro ["Distancia"] ,
                      "Donacion_x" : registro ["Donacion_x"] ,
                      "Donacion_y" : registro ["Donacion_y"] ,
                      "Tipo"       : registro ["Tipo"] ,
                     "Utilidad"    : registro ["Utilidad"]
                   }
                   dict_total.append(registro_armado)


                if funcion == 'utilidad':
                   if i==1:
                      ttk.Label(frame1, text = ".", background = 'blue').place(x = donacion["x"], y = donacion["y"], width =5, height = 5)

                   registro = asignacion_utilidad (donacion)
                   registro_armado = {
                      "dias" : i ,
                      "ONG"  : registro["Etiqueta"],
                      "ONG_X" : registro["ONG_X"] ,
                      "ONG_Y" : registro["ONG_Y"] ,
                      "Distancia"  : registro ["Distancia"] ,
                      "Donacion_x" : registro ["Donacion_x"] ,
                      "Donacion_y" : registro ["Donacion_y"] ,
                      "Tipo"       : registro ["Tipo"] ,
                     "Utilidad"    : registro ["Utilidad"]
                   }
                   dict_total.append(registro_armado)

                if funcion == '3ra':
                   if i==1:
                      ttk.Label(frame1, text = ".", background = 'blue').place(x = donacion["x"], y = donacion["y"], width =5, height = 5)

                   registro = asignacion_3ra (donacion)
                   registro_armado = {
                      "dias" : i ,
                      "ONG"  : registro["Etiqueta"],
                      "ONG_X" : registro["ONG_X"] ,
                      "ONG_Y" : registro["ONG_Y"] ,
                      "Distancia"  : registro ["Distancia"] ,
                      "Donacion_x" : registro ["Donacion_x"] ,
                      "Donacion_y" : registro ["Donacion_y"] ,
                      "Tipo"       : registro ["Tipo"] ,
                     "Utilidad"    : registro ["Utilidad"]
                   }
                   dict_total.append(registro_armado)

                if funcion == '4ta':
                   if i==1:
                      ttk.Label(frame1, text = ".", background = 'blue').place(x = donacion["x"], y = donacion["y"], width =5, height = 5)

                   registro = asignacion_4ta (donacion, df4)
                   registro_armado = {
                      "dias" : i ,
                      "ONG"  : registro["Etiqueta"],
                      "ONG_X" : registro["ONG_X"] ,
                      "ONG_Y" : registro["ONG_Y"] ,
                      "Distancia"  : registro ["Distancia"] ,
                      "Donacion_x" : registro ["Donacion_x"] ,
                      "Donacion_y" : registro ["Donacion_y"] ,
                      "Tipo"       : registro ["Tipo"] ,
                     "Utilidad"    : registro ["Utilidad"]
                   }
                   dict_total.append(registro_armado)

          resultados (dict_total)             

root = Tk()
root.title('Simulacion de donaciones')
root.geometry("1400x850")

note = ttk.Notebook(root)
tabs = []
no_tab=0
tabs.append(ttk.Frame(note))
note.add(tabs[no_tab],text = "1 -Principal")

#Titulo
label_titulo = ttk.Label(tabs[0], text=" Bienvenido a la aplicacion de simulacion de donaciones")
label_titulo.config(justify = CENTER)
label_titulo.config(foreground = 'black', background = 'white')
label_titulo.config(font = ('Courier', 18, 'bold'))
label_titulo.grid(row = 1, column = 1, columnspan = 2)

#Carga mapa
frame1 = ttk.Frame(tabs[0])
frame1.config(height = 790, width = 1135)
frame1.config(relief = RIDGE)
frame1.grid(row = 2, column = 1, sticky = 'w', rowspan = 50)

label_map = ttk.Label(frame1, text = "Hello, Tkinter!")
logo = PhotoImage(file = 'D:\\mapa.PNG') 
label_map.config(image = logo)
label_map.place(x = 1, y = 1)

#cargar texto y botones
label_insert = ttk.Label(tabs[0], text=" Introduce el numero de dias a simular: ")
label_insert.grid(row = 2, column = 3)

dias = ttk.Entry(tabs[0], width = 5)
dias.insert(0,"1")
dias.grid(row = 2, column = 4)

### OPCIONES
label_opcion = ttk.Label(tabs[0], text="\n\n Elige la funcion objetivo: ")
label_opcion.grid(row = 3, column = 3)
fun_obj = StringVar()
ttk.Radiobutton(tabs[0], text = 'Asignacion minimizando distancia', variable = fun_obj,
		value = 'simple').grid(row = 4, column = 3, columnspan = 2)
ttk.Radiobutton(tabs[0], text = 'Asignacion maximizando utilidad', variable = fun_obj,
		value = 'utilidad').grid(row = 5, column = 3, columnspan = 2)
ttk.Radiobutton(tabs[0], text = 'Asignacion maximizando utilidad + \n minimizando distancia', variable = fun_obj,
		value = '3ra').grid(row = 6, column = 3, columnspan = 2)
ttk.Radiobutton(tabs[0], text = 'Asignacion maximizando utilidad + \n minimizando distancia + balanceo \n equitativo y disminucion de sesgo', variable = fun_obj,
		value = '4ta').grid(row = 7, column = 3, columnspan = 2)
print(fun_obj.get())

boton = ttk.Button(tabs[0], text = "Iniciar")
boton.config(command = simulacion)
boton.grid(row = 8, column = 3)
boton.invoke()

#Cargar ONGs
with open('D:\BD_ONGs.json') as f:
  data = json.load(f)

for ong in data["ONGs"]:
	ttk.Label(frame1, text = ong["Etiqueta"], background = 'yellow').place(x = ong["x"], y = ong["y"], width =20, height = 20)


##### TAB RESULTADOS ######
tabs.append(ttk.Frame(note))
note.add(tabs[1],text = "Resultados")
note.pack()

note.hide(tabs[1])
root.mainloop()
