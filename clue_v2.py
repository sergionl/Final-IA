from tkinter import *
from PIL import ImageTk, Image
from utils_v2 import *
from tkinter import messagebox
root = Tk()
kbs=[createKb(),createKb()]
lcards = cartas() #list cards
wcards = selectedCartasGanador() #winner cards
available_cards = list()
available_cards = initial_available_cards()

class Player():
    def __init__(self, txt,i):
        self.window = Toplevel()
        self.window.geometry("600x300")
        self.title = txt
        self.i=i
        self.cards = [(-1, -1) for _ in range(3)]
        self.checked = IntVar()
        self.button=Button()
        Label(self.window, text=self.title).pack()
        self.entry = Entry(self.window, borderwidth=2)
        self.show = Checkbutton(self.window, text="Mostrar cartas", variable=self.checked, command=self.showcards)
        self.buttonknowledge= Button(self.window, text="Mostrar conocimiento",command= self.showknowledge)
        self.buttonpick = Button(self.window, text="Tomar una carta",command= self.pickCard)
        self.fcards = LabelFrame()

        self.entry.pack()
        self.show.pack()
        self.buttonknowledge.pack()
        self.buttonpick.pack()
    
    def selectInitialCards(self, AnotherPlayerCards, i):
        self.cards, kbs[i] = selectCartasIniciales(wcards, AnotherPlayerCards, kbs[i])
        return 

    def showknowledge(self):
        kbs[self.i],mensajes=helpSecurity(kbs[self.i],lcards)
        messagebox.showinfo("Respuestas",mensajes)
        return
        
    def showcards(self):
        print(self.checked.get())
        if(self.checked.get() == 1):
            self.fcards.pack_forget()
            self.canshow = False

            self.fcards = LabelFrame(self.window, text="Cards " + self.title)
            self.fcards.pack(padx=10, pady=10)
            
            for i,j in self.cards:
                Label(self.fcards, text=lcards[i][j]).pack()
        else:
            self.fcards.pack_forget()

    def pickCard(self):
        global available_cards
        if len(available_cards)==0:
            messagebox.showerror("Error","No hay mas cartas")
            return
        card = selectCarta(available_cards)
        print(available_cards)
        self.cards.append(card)
        available_cards = quit_some_availablecards(available_cards, [card])
        self.showcards()

        print('state: ', self.buttonpick['state'])        
        #self.buttonpick['state'] = DISABLED

def play(pregunta:Player,respuesta:Player,i):
    texto=pregunta.entry.get()
    numero=nameToNumber(texto)
    if numero == (-1,-1):
        messagebox.showwarning("Error","Debes ingresar una carta correcta")
        return
    kbs[i]=question(kbs[i],numero[0],numero[1],respuesta.cards)
    pregunta.button['state'] = DISABLED        
    print(kbs[i],numero)
    return 
def showAnotherplayer(window1: Toplevel, window2: Toplevel, player: Player):
    #window1.withdraw()
    #window2.deiconify()

    print('state: ', player.buttonpick['state'])        
    player.buttonpick['state'] = NORMAL
    player.button['state'] = NORMAL

def start():
    global root, available_cards, wcards
    root.withdraw()
    player0 = Player("Jugador 1",0)
    player1 = Player("Jugador 2",1)    
    
    player0.selectInitialCards(player1.cards, 0)
    player1.selectInitialCards(player0.cards, 1)
    print(kbs[0])
    print(kbs[1])
    Button(player0.window, text="Enviar", command= lambda:play(player0,player1,0)).pack()
    Button(player0.window, text="El siguiente jugador", 
    command=lambda: showAnotherplayer(player0.window, player1.window, player0)).pack()
    Button(player1.window, text="Enviar", command= lambda:play(player1,player0,1)).pack()
    Button(player1.window, text="El siguiente jugador", 
    command=lambda: showAnotherplayer(player1.window, player0.window, player1)).pack()
    print(wcards)
    #player1.window.withdraw()
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