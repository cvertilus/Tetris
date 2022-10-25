import csv
import tetris as tetris
import gamelib as gamelib
import random
import time 
VENTANA_LARGO = 400
VENTANA_ANCHO= 450
ESPERA_DESCENDER = 8
PIEZA_SIZE = 20
POS_INICIO_X=30
POS_INICIO_Y=20


COLOR=('RED','BLUE','Green','YELLOW','WHITE')

def verificar_cambios():
  '''
  La funcion verifica si algunos de los componentes globales fueron cambiados
  si es asi devolvera true en caso contrario False
  '''
  if VENTANA_LARGO != 400 or VENTANA_ANCHO!= 450 or PIEZA_SIZE!= 20 or POS_INICIO_X!=30 or POS_INICIO_Y!=20:
    gamelib.say("PORQUE CAMBIASTE LAS COSAS , PELIGRO")
    return True
  return False

def mostrar_hud(puntaje,pieza_siguiente,color_siguiente,juego,color_act,color_piezas_consolidas):
  ''' 
  La funcion recibe todos los elementos del juego y se le  
  mostrara en la mostrar_hud

  '''
  gamelib.draw_text('TETRIS',200,420,20,fill='Yellow')
  gamelib.draw_text('Puntaje',300,190,18,fill='Yellow')
  gamelib.draw_text(puntaje,306,230,30,fill='Green')
  gamelib.draw_text('Siguiente',300,20,18,fill='Yellow')

  dibujar_siguiente_pieza(pieza_siguiente,color_siguiente)
  dibujar_grilla(juego,color_act,color_piezas_consolidas)

def juego_a_dibujar(pieza):
  '''la funcion  recibe una pieza que esta al inicio , y cear un juego con esta pieza
  '''
  juego = tetris.crear_juego(pieza)
  return juego

def dibujar_grilla(juego,color_act,color_piezas_consolidas):
  ''' 
  la funcion recibe un juego, un color para la pieza que se esta moviendo en la grilla 
  -un color para las piezas que fueron consolodias en la grilla 
  -y la funcion dibuja los componentes grilla y pieza
  
  '''
  pieza,grilla = juego
  
  #*a dibujamos la grilla con tetris.ALTO_JUEGO,tetris.ANCHO_JUEGO,PIEZA_SIZE
  
  #! este for dibuja las lineas horizontales 
  for x in range(PIEZA_SIZE,PIEZA_SIZE*(tetris.ALTO_JUEGO),PIEZA_SIZE):
    gamelib.draw_line(POS_INICIO_X,x+POS_INICIO_Y,tetris.ALTO_JUEGO*10+POS_INICIO_X,x+POS_INICIO_Y,fill="Grey",width=0.05)
  
  ## este for dibuja las lineas verticales
  for y in range(PIEZA_SIZE,PIEZA_SIZE*(tetris.ANCHO_JUEGO),PIEZA_SIZE):
    gamelib.draw_line(y+POS_INICIO_X,POS_INICIO_Y,y+POS_INICIO_X,380,fill='Grey',width=0.05)

  
  ## verificamos si hay superficie en la grilla y la dibujamos 
  for x in range(len(grilla)):
    for y in range(len(grilla[x])):
      if tetris.hay_superficie(juego,y,x):
        gamelib.draw_rectangle((POS_INICIO_X+1)+(y*PIEZA_SIZE),(POS_INICIO_Y)+(x*PIEZA_SIZE),((PIEZA_SIZE*2)+10+(y*PIEZA_SIZE))-1,((PIEZA_SIZE*2)+(x*PIEZA_SIZE)),fill=color_piezas_consolidas,width=0.1)
  
  
  #!dibujamos los bordes
  gamelib.draw_line(POS_INICIO_X,POS_INICIO_Y,(PIEZA_SIZE*(PIEZA_SIZE/2))+10,POS_INICIO_Y,fill="Red",width=0.5)
  gamelib.draw_line(POS_INICIO_X,380,(PIEZA_SIZE*(PIEZA_SIZE/2))+10,380,fill="Red",width=0.5)
  gamelib.draw_line(POS_INICIO_X,POS_INICIO_Y,POS_INICIO_X,380,fill="Red",width=0.5)
  gamelib.draw_line((PIEZA_SIZE*(PIEZA_SIZE/2))+10,POS_INICIO_Y,(PIEZA_SIZE*(PIEZA_SIZE/2))+10,380,fill="Red",width=0.5)
 
  ## se dibuja la pieza que no fue consolida 
  dibujar_pieza(pieza,color_act)  

def dibujar_pieza(pieza,c):
  '''
  La funcion recibe una pieza , y un color    
  -se dibuja la pieza , con el color recibido  en la grilla 
  ''' 
  for pos in pieza:
    x,y = pos
    gamelib.draw_rectangle((POS_INICIO_X+1)+(x*PIEZA_SIZE),(POS_INICIO_Y)+(y*PIEZA_SIZE),((PIEZA_SIZE*2)+10+(x*PIEZA_SIZE))-1,((PIEZA_SIZE*2)+(y*PIEZA_SIZE)),fill=c,width=0.1)

def dibujar_siguiente_pieza(siguiente_pieza,color):
  '''
  La funcion recibe una pieza y un color 
  la pieza es la siguiente pieza que saldra despues de consolidar la pieza actual
  se dibuja la pieza con elcolor que recibe la funcion 

  '''
  for pos in siguiente_pieza:
    x,y=pos
    gamelib.draw_rectangle((POS_INICIO_X*8)+(x*PIEZA_SIZE)+30,(70)+(y*PIEZA_SIZE),((PIEZA_SIZE*2)+(x*PIEZA_SIZE))+250,((PIEZA_SIZE*2)+(50)+(y*PIEZA_SIZE))-1,fill=color,width=0.1)
 
def cargar_teclas():
  ''' 
  Esta funcion abre un archivo de texto que contiene teclas y acciones de forma
  <tecla>,=,<accion>
  se crea un diccionario cuyo clave sera la tecla , y accion como valor 
  retorna el diccionario

  '''
  teclas={}
  with open('archivo/teclas.txt')as f:
    linea = csv.reader(f,delimiter=' ')
    for line in linea:
      if len(line) == 0:
        continue
      teclas[line[0]]=line[2]
  return teclas

def guardar_juego(estado_juego):
  '''
  La funcion recibe un estado de juego que contiene
  -juego
  -puntaje
  -la pieza_siguiente
  se guarda el estado en un archivo de texto en una foema accesible
  '''
  with open('archivo/guardar.txt','w',newline='') as f:
    juego,puntaje,pieza_siguiente=estado_juego
    pieza_actual,grilla=juego

    name = ['pieza_siguiente','pieza_actual','Grilla','puntaje']
    write = csv.DictWriter(f,fieldnames=name)
    write.writeheader()
    write.writerow({"pieza_siguiente":tuple(pieza_siguiente),'pieza_actual':tuple(pieza_actual),'Grilla':grilla,'puntaje':puntaje})
  
def cargar_partido():
  """
  La funcion nos permite cargar_puntuaciones  del juego 
  en la forma que que estaba antes de guardarlo en  un 
  la funcion devuelve el juego en el estado que se guardo 
  """
  with open('archivo/guardar.txt') as f:
    reader = csv.DictReader(f)
    for columna in reader:
      pieza_siguiente = convertir_pieza_guardada_en_tupla(columna['pieza_siguiente'])
      pieza_actual = convertir_pieza_guardada_en_tupla(columna['pieza_actual'])
      grilla =convertir_la_grilla_en_lista(columna['Grilla'])
      puntaje= int(columna['puntaje'])

      return pieza_siguiente,pieza_actual,grilla,puntaje

def convertir_pieza_guardada_en_tupla(pieza):
  ''' 
  La funcion recibe una pieza en formato string y lo convierta en formato tupla de tupla
  '''
  list=['(',')']
  #!creamos una cadena con los valores interos
  piez_=''
  for x in range(len(pieza)):
    if pieza[x] not in list:
      piez_+=pieza[x]
  #! creamos una lista
  lista=piez_.split(',')
  #*creamos una lista de tupla con los valores y al final lo devolvemos en tupla de tupla
  pos_pieza=[]
  for x in range(0,len(lista),2):
    pos=(int(lista[x]),int(lista[x+1]))
    pos_pieza.append(pos)

  return tuple(pos_pieza)

def convertir_la_grilla_en_lista(grilla):
  ''' La funcion recibe una grilla en formato de cadena y lo convertira en una lista de lista'''

  #aca transformamos la grilla en un lista 
  grilla = grilla.split(']')

  grilla_=[]
  #este for recore toda la grilla 
  for x in range(len(grilla)):
    lista_aux=[]
    #este for nos permite recorer elementos de la grilla
    for y in range(len(grilla[x])):
      if grilla[x][y].isdigit():
        lista_aux.append(int(grilla[x][y]))
    #antes de agregar la lista auxiliar en nuestar grilla verificamos si es igual al ancho de juego 
    if len(lista_aux)== tetris.ANCHO_JUEGO:
      grilla_.append(lista_aux)
  return grilla_

def obtener_lista_de_puntuaciones():
  '''
  devuelve una lista de tupla de forma (puntaje,nombre) con la informacion del archivo puntuaciones.txt
  '''
  lista_puntuaciones=[]
  with open('archivo/puntuaciones.txt','r')as f:
    csv_reader = csv.DictReader(f)
    for linea in csv_reader:
      lista_puntuaciones.append((int(linea['SCORE']),linea['NOMBRE']))
  lista_puntuaciones.sort()
  return lista_puntuaciones

def guardar_puntuaciones(puntaje,lista):
    '''
    guardar las puntuaciones en el archivo de puntuaciones.txt, en forma <score>,<nombre>
    '''
 
    with open('archivo/puntuaciones.txt','w',newline='') as f:
      cabeza=['SCORE','NOMBRE']
      csv_writer = csv.DictWriter(f,fieldnames=cabeza)
      csv_writer.writeheader()
    
      if len(lista) < 10:
        nombre = gamelib.input('ingrese su nombre:')
        if not nombre:
          return
        lista.append((int(puntaje),nombre))
        if len(lista)>1:
          lista.sort()
        for score, persona in lista:
         csv_writer.writerow({'SCORE':score,'NOMBRE':persona})
        return
      
      if len(lista)== 10:
        if lista[0][0]< puntaje:
          nombre = gamelib.input('ingrese su nombre: ')
          lista.pop(0)
          lista.append((int(puntaje),nombre))
          lista.sort()
        for score, persona in lista:
         csv_writer.writerow({'SCORE':score,'NOMBRE':persona})
        return

def mostrar_puntaje_mas_alto(lista):
  '''
  al terminar el juego mostaremos el puntaje mas que tenia el juego
  '''
  if len(lista)==0:
    gamelib.say("El puntaje mas alto es 0")
    return
  #gamelib.draw_text(f'{lista[len(lista)-1][0]}',255,260,30,fill='Green')
  gamelib.say(f"El puntaje mas alto era: {lista[len(lista)-1][0]} ")

def main():
    # Inicializar el estado del juego
    puntaje=0
    cambios = verificar_cambios()

    color_actual= random.choice(COLOR)
    color_siguiente = random.choice(COLOR)
    color_piezas_consolidas=random.choice(COLOR)
    pieza= tetris.generar_pieza()
    pieza_siguiente=tetris.generar_pieza()
    juego = juego_a_dibujar(pieza)
    teclas = cargar_teclas()
    lista_de_puntuaciones = obtener_lista_de_puntuaciones()
    
    gamelib.resize(VENTANA_LARGO, VENTANA_ANCHO)
    timer_bajar = ESPERA_DESCENDER
  
    while gamelib.loop(fps=POS_INICIO_X):
        gamelib.draw_begin()
        # Dibujar la mostrar_hud
        if not cambios:
         mostrar_hud(puntaje,pieza_siguiente,color_siguiente,juego,color_actual,color_piezas_consolidas)
        gamelib.draw_end()

        for event in gamelib.get_events():
          if not event:
             break
          if event.type == gamelib.EventType.KeyPress:
              tecla = event.key
              #Actualizar el juego, según la tecla presionada
              if tecla not in teclas.keys():
                continue
              
              if teclas[tecla] == 'IZQUIERDA':
                juego = tetris.mover(juego,tetris.IZQUIERDA)

              if teclas[tecla] == 'DERECHA':
                juego = tetris.mover(juego,tetris.DERECHA)

              if teclas[tecla] == 'DESCENDER':
                juego,siguiente_pieza,puntaje_n=tetris.avanzar(juego,pieza_siguiente)
                puntaje+=puntaje_n
                #verificamos el estado de la sguiente pieza
                if siguiente_pieza == True:
                  pieza=pieza_siguiente
                  pieza_siguiente=tetris.generar_pieza()
                  color_actual= random.choice(COLOR)
                  color_siguiente = random.choice(COLOR)

              if teclas[tecla] == 'GUARDAR':
                estado_juego =juego,puntaje,pieza_siguiente
                guardar_juego(estado_juego)
                return
      
              if teclas[tecla] == 'cargar_puntuaciones':
                pieza_siguiente,pieza_actual,grilla,puntaje=cargar_partido()
                juego = pieza_actual,grilla
                
              
              if teclas[tecla]=='ROTAR':
                juego=tetris.rotar_pieza(juego)
                
              if teclas[tecla] == 'SALIR':
                return

        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER

             #Descender la pieza automáticamente
            juego,siguiente_pieza,puntaje_=tetris.avanzar(juego,pieza_siguiente)
            puntaje+=puntaje_
            if siguiente_pieza == True:
             pieza=pieza_siguiente
             pieza_siguiente=tetris.generar_pieza()
             color_actual= random.choice(COLOR)
             color_siguiente = random.choice(COLOR)

        if tetris.terminado(juego):
              mostrar_puntaje_mas_alto(lista_de_puntuaciones)
              guardar_puntuaciones(puntaje,lista_de_puntuaciones)
              #time.sleep(3)
              break  

gamelib.init(main)