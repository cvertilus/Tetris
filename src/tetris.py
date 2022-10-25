ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6
import piezas as piezas
import random


PIEZAS = piezas.cargar_piezas()
ROTACIONES = piezas.cargar_rotaciones(PIEZAS)

def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.

    """
    if pieza == None:
        list = [0,1,2,3,4,5,6]
        numero = random.choice(list)
        return PIEZAS[numero][0]
    return PIEZAS[pieza][0]

def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    nueva_posicion =[]
    for x in range (len(pieza)):
            pos = (pieza[x][0]+ dx , pieza[x][1]+dy) 
            nueva_posicion.append(pos)
    return tuple(nueva_posicion)
    

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """

    grilla=[[ 0 for x in range(ANCHO_JUEGO)] for y in range(ALTO_JUEGO)]
    pieza_centrada = trasladar_pieza(pieza_inicial,ANCHO_JUEGO//2,0)
    return(pieza_centrada,grilla)
                 
def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    juego= (ANCHO_JUEGO,ALTO_JUEGO)
    return juego

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    pieza,_= juego
    return tuple(pieza)

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    _,grilla = juego
    return grilla[y][x] == 1


def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    pieza,grilla = juego
    pieza_movida=trasladar_pieza(pieza,direccion,0)
    juego_nuevo= pieza_movida,grilla
    if not posicion_valida(juego_nuevo) :
            return juego
    return juego_nuevo

def rotar_pieza(juego):
    '''
    la funcionar rotar pieza,nos permite rotar la pieza que esta cayendo que aun no fue consolida por la superficie
    '''
    pieza,grilla=juego
    # ordenamos las piezas de modo que la position1 sera el menor valor de x,y
    pieza_ordenada = ordernar_por_coordenada(pieza)
    primera_pos = pieza_ordenada[0]
    pieza_en_origen=trasladar_pieza(pieza_ordenada,-primera_pos[0],-primera_pos[1])
    siguiente_rotacion = ROTACIONES[pieza_en_origen]
    pieza_ = trasladar_pieza(siguiente_rotacion,primera_pos[0],primera_pos[1])
    juego_nuevo = pieza_,grilla
    #! verifico si se puede rotar la pieza en caso contrario delvolvera la misma pieza
    if posicion_valida(juego_nuevo):
       return juego_nuevo
    return juego

def ordernar_por_coordenada(pieza):
    return sorted(pieza)


def avanzar(juego, siguiente_pieza):
   
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza,score) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie), la tercera es el puntaje.
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Por cada 5 filas eliminadas el puntaje suma 1 punto
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    pieza,grilla =juego
    score=0
    
   
    if not terminado(juego):
        pieza_= trasladar_pieza(pieza,0,1)
        juego_nuevo=pieza_,grilla
        if posicion_valida(juego_nuevo):
            return(juego_nuevo,False,score)
        else:
            grilla_con_pieza_consolida = consolidar_pieza(juego)
            nueva_grilla,score_= eliminar_filas(grilla_con_pieza_consolida,score)
            pieza =trasladar_pieza(siguiente_pieza,ANCHO_JUEGO//2,0)
            juego_n = pieza,nueva_grilla
            return(juego_n,True,score_)
    return(juego,False,score)


def posicion_valida(juego):
    pieza,_=juego
    for x,y in  pieza:
        if y>ALTO_JUEGO-1 or y<0 or x<0 or x>ANCHO_JUEGO-1 or hay_superficie(juego,x,y):
            return False
    return True
    
def consolidar_pieza(juego):
    pieza,grilla=juego
    for x,y in pieza:
        grilla[y][x]=1
    return grilla

def eliminar_filas(grilla,score):  
    for y in range(ALTO_JUEGO):
        count=0
        for x in range(ANCHO_JUEGO):
            if grilla[y][x]==1:
                count+=1
        if count == ANCHO_JUEGO:
            grilla.pop(y)   
            grilla.insert(0,[0]*ANCHO_JUEGO) 
            score+=1
            

    return grilla,score       

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    pieza,grilla=juego
    for x,y in  pieza:
        if grilla[y][x]!= 0:
            return True
    return False


