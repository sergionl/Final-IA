from tkinter import *
from utils import *

root = Tk()
root.title("TF-Cluedo")

Label(root, text="Cluedo").grid(row=0, column=1, columnspan=3)
Label(root, text="1) Hoy a sido asesinado ..."+"\n"+
    "2) Debes encontrar ¿Quién lo hizo? ¿Cón qué arma? ¿Y donde?"+"\n"+
    "3) Se esconderá tres cartas (persona, arma, lugar) sobre el asesinato"+"\n"+
    "4) El resto de cartas se repartiran entre los 2 jugadores"+"\n"+
    "4) Deberás encontrar las cartas escondidas", justify="left").grid(row=1, column=2, rowspan=2, columnspan=2)

#######################################################################
#Modelo
Example = createKb()

#######################################################################

rows = [10, 10]
cols = [2, 3]


def click_Player(txt, i):
    Label(root, text=txt).grid(row=rows[i], column=cols[i])
    rows[i] += rows[i]


player1 = Label(root, text="Jugador 1")
player1.grid(row=4, column=2)

EntryPlayer1 = Entry(root, borderwidth=2)
EntryPlayer1.grid(row=6, column=2)

EnviarPlayer1 = Button(root, text="Enviar", command=lambda: click_Player(EntryPlayer1.get(), 0))
EnviarPlayer1.grid(row=7, column=2)

ConcimientoPlayer1 = Button(root, text="Mostrar conocimiento")
ConcimientoPlayer1.grid(row=8, column=2)

#######################################################################

jugador2 = Label(root, text="Jugador 2")
jugador2.grid(row=4, column=3)

EntryPlayer2 = Entry(root, borderwidth=2)
EntryPlayer2.grid(row=6, column=3)

ButtonPlayer2 = Button(root, text="Enviar", command=lambda: click_Player(EntryPlayer2.get(), 1))
ButtonPlayer2.grid(row=7, column=3)

ConcimientoPlayer2 = Button(root, text="Mostrar conocimiento")
ConcimientoPlayer2.grid(row=8, column=3)

root.mainloop()