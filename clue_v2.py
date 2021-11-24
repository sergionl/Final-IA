from tkinter import *
from PIL import ImageTk, Image
from utils import *

root = Tk()
kbs=[createKb(),createKb()]
lcards = cartas() #list cards
wcards = selectedCartasGanador() #winner cards
available_cards = list()
available_cards = initial_available_cards()

class Player():
    def __init__(self, txt):
        self.window = Toplevel()
        self.window.geometry("600x300")
        self.title = txt
        self.cards = [(-1, -1) for _ in range(3)]
        self.checked = IntVar()

        Label(self.window, text=self.title).pack()
        self.entry = Entry(self.window, borderwidth=2)
        self.button = Button(self.window, text="Enviar", command= self.play)
        self.show = Checkbutton(self.window, text="Mostrar cartas", variable=self.checked, command=self.showcards)
        self.buttonpick = Button(self.window, text="Tomar una carta",command= self.pickCard)
        self.fcards = LabelFrame()

        self.entry.pack()
        self.button.pack()
        self.show.pack()
        self.buttonpick.pack()
    
    def selectInitialCards(self, AnotherPlayerCards, AnotherPlayerkb):
        self.cards, auxkb = selectCartasIniciales(wcards, AnotherPlayerCards, AnotherPlayerkb)
        return auxkb

    def play(self):
        
        self.button['state'] = DISABLED        
        return

    def showcards(self):
        print(self.checked.get())
        if(self.checked.get() == 1):
            self.fcards.pack_forget()
            self.canshow = False

            self.fcards = LabelFrame(self.window, text="Cards " + self.title)
            self.fcards.pack(padx=10, pady=10)
            
            for i in self.cards:
                Label(self.fcards, text=str(i)).pack()
        else:
            self.fcards.pack_forget()

    def pickCard(self):
        global available_cards
        card = selectCarta(available_cards)

        self.cards.append(card)
        available_cards = quit_some_availablecards(available_cards, [card])
        self.showcards()

        print('state: ', self.buttonpick['state'])        
        self.buttonpick['state'] = DISABLED


def showAnotherplayer(window1: Toplevel, window2: Toplevel, player: Player):
    window1.withdraw()
    window2.deiconify()

    print('state: ', player.buttonpick['state'])        
    player.buttonpick['state'] = NORMAL
    player.button['state'] = NORMAL

def start():
    global root, available_cards, wcards
    root.withdraw()
    player0 = Player("Jugador 1")
    player1 = Player("Jugador 2")    
    
    kbs[0] = player0.selectInitialCards(player1.cards, kbs[1])
    kbs[1] = player1.selectInitialCards(player0.cards, kbs[0])

    Button(player0.window, text="El siguiente jugador", 
    command=lambda: showAnotherplayer(player0.window, player1.window, player0)).pack()
    Button(player1.window, text="El siguiente jugador", 
    command=lambda: showAnotherplayer(player1.window, player0.window, player1)).pack()

    player1.window.withdraw()
    available_cards = quit_some_availablecards(available_cards, player0.cards)
    available_cards = quit_some_availablecards(available_cards, player1.cards)
    available_cards = quit_some_availablecards(available_cards, wcards)

def instructions():
    global new_img

    root.title("TF-Cluedo")
    lbl = Label(root, text="Cluedo", border=3, padx=5, pady=5)
    lbl.pack(anchor=CENTER)
    lbl.config(fg="white",
               bg="black",
               font=("Verdana", 24, "bold"))
    
    canva = Canvas(root, width=150, height=200)
    canva.pack()
    my_img = (Image.open("./img/cluedo.jpg"))
    resized_img = my_img.resize((150, 200), Image.ANTIALIAS)
    new_img = ImageTk.PhotoImage(resized_img)
    canva.create_image(10, 10, anchor=NW, image=new_img)

    
    lbl = Label(root, text="1) Hoy a sido asesinado ..."+"\n"+
    "2) Debes encontrar ¿Quién lo hizo? ¿Cual fue el motivo? ¿Y donde?"+"\n"+
    "3) Se esconderá tres cartas (persona, motivo, lugar) sobre el asesinato"+"\n"+
    "4) El resto de cartas se repartiran entre los 2 jugadores"+"\n"+
    "4) Deberás encontrar las cartas escondidas", justify="left", padx=10, pady=5)
    lbl.pack()
    lbl.config(font=("Verdana", 10))

    Button(root, text="Comenzar (>)", bg="green", fg="black", pady=10, command=start).pack()


instructions()
root.mainloop()