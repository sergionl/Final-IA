from typing import AsyncIterable
import numpy as np
import random
def cartas():
    """
    Define las cartas del juego y las guarda en una matriz de 6x3.
    """
    cartasCulpable=['Mora','Blanco','Amapola','Prado','Rubio','Celeste']
    cartasLugar=['Patio','Estudio','Comedor','Garaje','Salon','Dormitorio']
    cartasMotivo=['Racismo','Homofobia','Transfobia','Xenofobia','Sexismo','Discriminacion por discapacidad']

    cartas = [cartasCulpable,cartasLugar,cartasMotivo]
    return cartas

def createKb():
    """
    Se crea una base de conocimiento, esta tiene forma de una matriz de 3x6, ya que esa son la cantidad de cartas en el juego.

    La base de conocimiento tiene datos iniciales en -1, ya que este representa falta de informacion.
    """
    kb = np.zeros((3,6))
    for i in range(18):
        kb.itemset(i,-1)
    return kb

def changeValue(kb, card, info):
    """
    Cambia los valores a la base de conocimiento.

    0 representa que esa carta no es la respuesta.

    1 representa que esa carta es parte de la respuesta.
    """

    if info:
        kb.itemset(card, 1)
    else:
        kb.itemset(card, 0)
    return kb

def seeSecurity(kb,cardType,cartas):
    """
    Muestra si nuestra base de conocimiento tiene certeza sobre algun tipo de cartas.
    Se basa en la regla solo una carta de cada tipo es la respuesta correcta, esto se puede entender como:

    -Solo existe una carta de culpables que es el culpable:  ∃x. (CartaCulpable(x) ∧ Culpable(x))

    -Solo existe una carta de lugares que es el lugar:  ∃x. (CartaLugar(x) ∧ Lugar(x))

    -Solo existe una carta de motivos que es el motivo:  ∃x. (CartaMotivo(x) ∧ Motivo(x))
    
    """
    count0 = 0
    for i in range(6):
        if kb[cardType,i] == 0:
            count0 +=1
        if kb[cardType,i] == 1:
            mensaje="Carta {0} es parte de la respuesta".format(cartas[cardType][i])
            return kb,mensaje
    if count0 == 5:
        for i in range(6):
            if kb[cardType,i] == -1:
                kb = changeValue(kb,(cardType,i),True)
                mensaje="Carta {0} es parte de la respuesta".format(cartas[cardType][i])
                return kb,mensaje
    mensaje="La base de conocimiento no tiene informacion suficiente sobre "
    if cardType==0:
        mensaje+="Los culpables"
    elif cardType==1:
        mensaje+="El lugar"
    else:
        mensaje+="El motivo" 
    return kb,mensaje

def nameToNumber(name):
    """
    Recive la carta seleccionada por el usuario y devuelve 
    la posicion de la matriz que representa esa carta.
    """
    name = name.lower()
    cardType,card = -1,-1
    if name == "mora":
        cardType,card = 0,0
        return cardType,card
    elif name == "blanco":
        cardType,card = 0,1
        return cardType,card
    elif name == "amapola":
        cardType,card = 0,2
        return cardType,card
    elif name == "prado":
        cardType,card = 0,3
        return cardType,card
    elif name == "rubio":
        cardType,card = 0,4
        return cardType,card
    elif name == "celeste":
        cardType,card = 0,5
        return cardType,card
    elif name == "racismo":
        cardType,card = 2,0
        return cardType,card
    elif name == "homofobia":
        cardType,card = 2,1
        return cardType,card
    elif name == "transfobia":
        cardType,card = 2,2
        return cardType,card
    elif name == "xenofobia":
        cardType,card = 2,3
        return cardType,card
    elif name == "sexismo":
        cardType,card = 2,4
        return cardType,card
    elif name == "discriminacion por discapacidad":
        cardType,card = 2,5
        return cardType,card
    elif name == "patio":
        cardType,card = 1,0
        return cardType,card
    elif name == "estudio":
        cardType,card = 1,1
        return cardType,card
    elif name == "comedor":
        cardType,card = 1,2
        return cardType,card
    elif name == "garaje":
        cardType,card = 1,3
        return cardType,card
    elif name == "salon":
        cardType,card = 1,4
        return cardType,card
    elif name == "dormitorio":
        cardType,card = 1,5
        return cardType,card
    else:
        return -1,-1

def helpSecurity(kb,cartas):
    """
    Función auxiliar

    LLama 3 veces a la función seeSecurity para revisar si se tiene certeza de algun tipo de cartas
    """
    mensajes=""
    for i in range(3):
        kb,aux = seeSecurity(kb,i,cartas)
        mensajes+=aux+"\n"
    return kb, mensajes

def selectedCartasGanador():
    """
    Selecciona aleatoriamente las cartas del ganador
    """
    number1=random.randint(0,5)
    number2=random.randint(0,5)
    number3=random.randint(0,5)
    return [(0, number1), (1, number2), (2, number3)]

def selectCartasIniciales(ganador, otrojugador, kb):
    """
    Para iniciar el juego se reparte cartas, la funcion se encarga de seleccionar cartas aleatoriamente a 
    los jugadores y seleccionar aleatoriamente las cartas ganadore(culpable, motivo y lugar)
    """
    selected = []
    
    for i in range(3):
        while True:
            number = random.randint(0,5)
            if number == ganador[i][1]:
                continue

            if (number == otrojugador[i][1]):
                continue
            
            card = (i, number)
            selected.append(card)
            kb=changeValue(kb, card, False)

            break

    return selected, kb

def selectCarta(availablecards):
    """
    Selecciona la carta que solicita
    """
    ans = (-1, -1)
    if len(availablecards) == 0:
        return ans

    return random.choice(availablecards)

def initial_available_cards():
    """
    Se crea la lista inicial de cartas
    """
    lista = list()
    for i in range(3):
        for j in range(6):
            lista.append((i, j))
    
    return lista

def quit_some_availablecards(available: list, group: list):
    """
    Quita la carta que el jugador robo en su turno de la lista de cartas que aun no roba
    """
    for element in group:
        if element in available:
            available.remove(element)
    
    return available

def question(kb,cardType,card,otroJugador):
    """
    Revisa si el jugador y tiene la respuesta a la pregunta de jugador x, y llama a la funcion changeValue

    """
    
    if (cardType,card) in otroJugador:
        mensaje="Base de conocimiento actualizada"
        kb = changeValue(kb,(cardType,card),False)
    else:
        mensaje="No se obtiene respuesta"
    return kb,mensaje

def verification(numeroPersona,numeroMotivo,numeroLugar,cartasganadoras):
    """
    Revisa si la acusacion de un jugador es correcta.

    Esta solo es correcta si el jugador acierta el culpable, el motivo y el lugar.

    ∀x. (Culpable(x) ∧ Lugar(y) ∧ Motivo (z) →RespuestaCorrecta(x,y,z))
    """
    if numeroPersona not in cartasganadoras:
        mensaje="Perdiste"
        return mensaje
    if numeroMotivo not in cartasganadoras:
        mensaje="Perdiste"
        return mensaje
    if numeroLugar not in cartasganadoras:
        mensaje="Perdiste"
        return mensaje
    mensaje="Ganaste"
    return mensaje
    
def getNoticas():
    aux=[
        ["Casos de racismo","./img/racismo.png","""
        El 29% de ciudadanos cusqueños fue víctima de discriminación en los últimos 12 meses, según la 
        primera encuesta nacional “Percepciones Sobre Diversidad Cultural y Discriminación Étnico-Racial”, 
        realizado por el Ministerio de Cultura.
        De acuerdo a la percepción de los cusqueños, un 26% se siente discriminado por el color de piel, 
        mientras que el 21% por el lugar de procedencia, el 19% por su forma de hablar y el 18% por el nivel 
        de ingresos económicos.""",
        "https://rpp.pe/peru/cusco/color-de-piel-y-nivel-de-ingresos-son-algunos-factores-de-discriminacion-en-cusco-noticia-1125800"],
        
        ["Casos de homofobia","./img/homofobia.webp","""
        Enrique Alberto Li Gonzales (27) denunció el último domingo haber sido agredido por un sujeto que,
        tras insultarlo por su orientación sexual, le desfiguró el rostro en pleno centro de Miraflores.
        Según relató la víctima, transitaba por la avenida Larco acompañado de un amigo cuando su atacante 
        identificado como Juan Carlos Marchena Iparraguirre (24) comenzó a lanzarle insultos homofóbicos.
        Afectado por la agresión verbal, Li Gonzáles encaró al sujeto y este respondió violentamente causándole
        un corte en el pómulo izquierdo para posteriormente huir del lugar con un acompañante.""",
        "https://peru21.pe/lima/caso-de-homofobia-en-miraflores-le-desfiguran-rostro-a-joven-y-acusa-a-los-policias-de-liberar-a-su-atacante-video-noticia/"
        ],
        
        ["Casos de transfobia","./img/transfobia.jpg","""
         No es un secreto que la comunidad trans en el país es constantemente discriminada y vulnerada en más
         de un aspecto de sus vidas. La transfobia, el odio y rechazo se suma a la larga lista de vulneraciones 
         contra sus derechos, bajo la falta de políticas públicas para proteger a esta población.
         El último 8 de enero, la serie De Vuelta al Barrio, una producción de América Televisión, proyectó una 
         escena violenta en la que el personaje principal del sketch hacía referencia a mujer trans. Una escena 
         que posiblemente hubiera pasado desapercibida si no fuera por Gianna Camacho, activista e integrante 
         del Proyecto Únicxs de la UPCH, quien denunció —a través de sus redes sociales— la transfobia contenida 
         en el episodio de la serie.""",
         "https://larepublica.pe/sociedad/2021/01/19/transfobia-en-la-television-peruana-violencia-contra-personas-trans-sigue-presente-atmp/"
        ],
        
        ["Casos de xenofobia","./img/xenofobia.jpg","""
         A fines de mayo del 2021 aparecieron en algunos sectores de Lima unos afiches con mensajes de odio 
         que se han convertido en la evidencia más extrema del discurso de la xenofobia en el país. Las láminas 
         de papel llevaban como titular: ‘Bicentenario sin venecos’, en referencia ofensiva a los migrantes 
         venezolanos. A eso se sumaban frases de rechazo a una supuesta invasión e incluso abiertas amenazas 
         de muerte contra los migrantes, a quienes se acusaba de una serie de delitos. “No al robo de nuestros 
         empleos”, “Soberanía e identidad nacional”, eran algunas de las expresiones colocadas en hilera. 
        Los mensajes iban acompañados de dos imágenes: a un lado y en posición preponderante, el retrato del 
        héroe nacional Andrés A. Cáceres; al costado, y algo más abajo, la foto de Silvano Cántaro, un joven 
        músico peruano que murió tras ser arrojado de un puente en Colombia por supuestos venezolanos, un 
        crimen que conmocionó a la opinión pública peruana en febrero de este año. 
         ""","https://ojo-publico.com/2774/mensajes-de-odio-hacia-venezolanos-aumentaron-nueve-veces-en-campana"],
        
        ["Casos de sexismo","./img/sexismo.jpg","""
         En su discurso, el presidente del Consejo de Ministros, Guido Bellido, asegura que este gobierno y 
         su persona han llegado al poder para traer la igualdad, una frase vacía y falsa pues sus comentarios 
         machistas y misóginos han puesto en evidencia su verdadero perfil. Antes de asumir el cargo, algunas 
         frases del premier ya eran conocidas. En Facebook nunca escondió su posición frente a las minorías, 
         especialmente contra la comunidad LGTB+. Ahora, luego de que la congresista Patricia Chirinos lo 
         denunciara públicamente por agresión verbal, ha quedado expuesto también su desprecio hacia las 
         mujeres.
         El pasaje que fue dado a conocer por la tercera vicepresidenta del Congreso el último lunes, ya 
         había sido adelantado hace un mes por El Comercio, antes de que Bellido fuera designado como titular 
         de la PCM. El entonces congresista de Perú Libre le dijo a su par: “Anda, cásate (...), solo falta 
         que te violen”, cuando esta solicitaba que le asignen la oficina que había pertenecido a su padre 
         (Enrique Chirinos Soto).
         ""","https://peru21.pe/politica/gobierno-de-peru-libre-escalada-misogina-y-machista-del-premier-bellido-bajo-la-lupa-noticia/"],
        
        ["Casos de discriminacion por discapacidad","./img/discriminacion por discapacidad.jpg","""
         Un supuesto caso de discriminación denunció madre de familia quien contó que a su niño de tres años 
         le negaron la matrícula en el Centro Educativo Santa Rosa de Surco.
         El niño sufre de una malformación de la columna que no le permite caminar con normalidad y lo tiene 
         que hacer con ayuda de unas muletas.

         Soledad Rocha, madre del menor, dijo que en la referida escuela los responsables le dieron diferentes excusas 
         para no inscribirlo en el presente año escolar.

         “No es la primera vez que me niegan la inscripción de mi niño. La directora de la institución me recibió al 
         principio muy cordialmente y me informó que sí tenían vacantes para niños de cinco años, pero al ver las 
         muletas empezó a titubear", contó a RPP Noticias.
         ""","https://rpp.pe/lima/actualidad/madre-denuncia-discriminacion-de-su-hijo-discapacitado-en-surco-noticia-772853"]
    ]
    
    return aux