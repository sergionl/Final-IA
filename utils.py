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
    #print(kb)
    return kb

def changeValue(kb,cardType,card,info):
    if info:
        kb.itemset((cardType,card),1)
    else:
        kb.itemset((cardType,card),0)
    return kb

def seeSecurity(kb,cardType):
    count0 = 0
    for i in range(6):
        if kb[cardType,i] == 0:
            count0 +=1
        if kb[cardType,i] == 1:
            print("Carta {0} es parte de la respuesta".format(cartas[cardType][i]))
            return kb
    if count0 == 5:
        for i in range(6):
            if kb[cardType,i] == -1:
                print("Carta {0} es parte de la respuesta".format(cartas[cardType][i]))
                kb = changeValue(kb,cardType,i,True)
                return kb
    print("La base de conocimiento no tiene informacion suficiente")

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
        cardType,card = 1,0
        return cardType,card
    elif name == "homofobia":
        cardType,card = 1,1
        return cardType,card
    elif name == "transfobia":
        cardType,card = 1,2
        return cardType,card
    elif name == "xenofobia":
        cardType,card = 1,3
        return cardType,card
    elif name == "sexismo":
        cardType,card = 1,4
        return cardType,card
    elif name == "discriminacion por discapacidad":
        cardType,card = 1,5
        return cardType,card
    elif name == "patio":
        cardType,card = 2,0
        return cardType,card
    elif name == "estudio":
        cardType,card = 2,1
        return cardType,card
    elif name == "comedor":
        cardType,card = 2,2
        return cardType,card
    elif name == "garaje":
        cardType,card = 2,3
        return cardType,card
    elif name == "salon":
        cardType,card = 2,4
        return cardType,card
    elif name == "dormitorio":
        cardType,card = 2,5
        return cardType,card
    else:
        print("Ingrese una carta existente")

def helpSecurity(kb):
    for i in range(3):
        kb = seeSecurity(kb,i)
    return kb

def selectedCartasGanador(cartas):
    carta1=random.randint(0,5)
    carta2=random.randint(0,5)
    carta3=random.randint(0,5)
    print(carta1,carta2,carta3)
    return [carta1,carta2,carta3]

def selectCartasJugador(cartas,ganador,otrojugador,kb):
    while True:
        carta1= random.randint(0,5)
        if carta1== ganador[0]:
            continue
        if carta1==otrojugador[0]:
            continue
        kb=changeValue(kb,0,carta1,False)
        break
    while True:
        carta2= random.randint(0,5)
        if carta2== ganador[1]:
            continue
        if carta2==otrojugador[1]:
            continue
        kb=changeValue(kb,1,carta2,False)
        break
    while True:
        carta3= random.randint(0,5)
        if carta3== ganador[2]:
            continue
        if carta3==otrojugador[2]:
            continue
        kb=changeValue(kb,2,carta3,False)
        break
    return [carta1, carta2, carta3], kb

def question(kb,cardType,card,otroJugador):
    if otroJugador[cardType] == card:
        kb = changeValue(kb,cardType,card,False)
    else:
        print("No se obtiene respuesta")
    return kb
