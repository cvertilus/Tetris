import csv

def cargar_piezas():
    piezas = []
    with open('archivo/piezas.txt') as f:
        linea = csv.reader(f, delimiter=" ")
        #*nos permite reccorer el archivo 
        for Pos in linea :
           pieza =[]
           #! para cambiar el formato de las piezas en el archivo
           for x in Pos:
               pos = x.split(';')
               if len(pos)!=4:
                   continue
               pieza_=[]
               ## para convertir los datos en forma de tupla 
               for p in pos:
                   pos= tuple(p.split(','))
                   pos_x_y = (int(pos[0]), int(pos[1]))
                   pieza_.append(pos_x_y)
               pieza.append(tuple(pieza_))
           piezas.append(tuple(pieza))
    return tuple(piezas)

def cargar_rotaciones(piezas):
    dict_piezas ={}
    #* pieza cubo
    dict_piezas[piezas[0][0]]=piezas[0][0]
    #* piezas (Z,S,I)
    for x in range(1,4):
         dict_piezas[piezas[x][0]]= piezas[x][1]
         dict_piezas[piezas[x][1]]=piezas[x][0]
    #*piezas (L,-L,T)
    for x in range(4,7):
        dict_piezas[piezas[x][0]]=piezas[x][1]
        dict_piezas[piezas[x][3]]=piezas[x][0]
        dict_piezas[piezas[x][1]]=piezas[x][2]
        dict_piezas[piezas[x][2]]=piezas[x][3]
    return dict_piezas


