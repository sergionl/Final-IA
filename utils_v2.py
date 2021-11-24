from typing import AsyncIterable
import numpy as np
import random
def cartas():
    cartasCulpable=['Mora','Blanco','Amapola','Prado','Rubio','Celeste']
    cartasLugar=['Patio','Estudio','Comedor','Garaje','Salon','Dormitorio']
    cartasMotivo=['Racismo','Homofobia','Transfobia','Xenofobia','Sexismo','Discriminacion por discapacidad']

    cartas = [cartasCulpable,cartasLugar,cartasMotivo]
    return cartas

def createKb():
    kb = np.zeros((3,6))
    for i in range(18):
        kb.itemset(i,-1)
    return kb

def changeValue(kb, card, info):
    if info:
        kb.itemset(card, 1)
    else:
        kb.itemset(card, 0)
    return kb

def seeSecurity(kb,cardType,cartas):
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
    mensajes=""
    for i in range(3):
        kb,aux = seeSecurity(kb,i,cartas)
        mensajes+=aux+"\n"
    return kb, mensajes

def selectedCartasGanador():
    number1=random.randint(0,5)
    number2=random.randint(0,5)
    number3=random.randint(0,5)
    return [(0, number1), (1, number2), (2, number3)]

def selectCartasIniciales(ganador, otrojugador, kb):
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
    ans = (-1, -1)
    if len(availablecards) == 0:
        return ans

    return random.choice(availablecards)

def initial_available_cards():
    lista = list()
    for i in range(3):
        for j in range(5):
            lista.append((i, j))
    
    return lista

def quit_some_availablecards(available: list, group: list):
    for element in group:
        if element in available:
            available.remove(element)
    
    return available

def question(kb,cardType,card,otroJugador):
    
    if (cardType,card) in otroJugador:
        mensaje="Base de conocimiento actualizada"
        kb = changeValue(kb,(cardType,card),False)
    else:
        mensaje="No se obtiene respuesta"
    return kb,mensaje

def verification(numeroPersona,numeroMotivo,numeroLugar,cartasganadoras):
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
    