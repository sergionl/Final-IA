from tkinter import *
from PIL import ImageTk, Image
from utils import *
from tkinter import messagebox
import webbrowser
root = Tk()
kbs=[createKb(),createKb()]
lcards = cartas() #list cards
wcards = selectedCartasGanador() #winner cards
noticias= getNoticas()

available_cards = list()
available_cards = initial_available_cards()

class Player():
    def __init__(self, txt,i):
        self.window = Toplevel()
        self.window.geometry("600x300")
        self.title = txt
        self.i=i
        self.perdiste=False
        self.cards = [(-1, -1) for _ in range(3)]
        self.checked = IntVar()
        self.button=Button()
        self.nextPlayer=Button()
        Label(self.window, text=self.title).pack()
        self.entry = Entry(self.window, borderwidth=2)
        self.show = Checkbutton(self.window, text="Mostrar cartas", variable=self.checked, command=self.showcards)
        self.buttonknowledge= Button(self.window, text="Mostrar conocimiento",command= self.showknowledge)
        self.buttonpick = Button(self.window, text="Tomar una carta",command= self.pickCard)
        self.buttonAcusar=Button(self.window,text="Acusar",command= self.acusar)
        self.fcards = LabelFrame()

        self.entry.pack()
        self.show.pack()
        self.buttonknowledge.pack()
        self.buttonpick.pack()
        self.buttonAcusar.pack()
    
    def selectInitialCards(self, AnotherPlayerCards, i):
        self.cards, kbs[i] = selectCartasIniciales(wcards, AnotherPlayerCards, kbs[i])
        return 

    def showknowledge(self):
        kbs[self.i],mensajes=helpSecurity(kbs[self.i],lcards)
        messagebox.showinfo("Respuestas",mensajes)
        return
        
    def showcards(self):
        
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
        
        self.cards.append(card)
        kbs[self.i] = changeValue(kbs[self.i],card,False)
        
        available_cards = quit_some_availablecards(available_cards, [card])
        self.showcards()
        setPickCard(self.i)

    def acusar(self):
        global new_img
        ventanaAcusar=Toplevel()
        ventanaAcusar.title("Acusar")
        ventanaAcusar.geometry("300x400")
        Label(ventanaAcusar,text="Acusar "+str(self.i+1)).pack()
        
        canva = Canvas(ventanaAcusar, width=150, height=200)
        canva.pack()
        my_img = (Image.open("./img/acusar.jpg"))
        resized_img = my_img.resize((150, 200), Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(resized_img)
        canva.create_image(10, 10, anchor=NW, image=new_img)
        
        Label(ventanaAcusar,text="Persona: ").pack()
        entryPersona=Entry(ventanaAcusar)
        entryPersona.pack()
        
        Label(ventanaAcusar,text="Lugar: ").pack()
        entryLugar=Entry(ventanaAcusar)
        entryLugar.pack()
        
        Label(ventanaAcusar,text="Motivo: ").pack()
        entryMotivo=Entry(ventanaAcusar)
        entryMotivo.pack()
        def boton(state : bool):
            
            return
        def acusacion():
            numeroPersona=nameToNumber(entryPersona.get())
            numeroMotivo=nameToNumber(entryMotivo.get())
            numeroLugar=nameToNumber(entryLugar.get())
            if numeroPersona == (-1,-1):
                messagebox.showwarning("Error","No existe esta persona")
                return
            if numeroMotivo == (-1,-1):
                messagebox.showwarning("Error","No hemos tomado en cuenta este motivo para el juego")
                return
            if numeroLugar == (-1,-1):
                messagebox.showwarning("Error","No existe este lugar")
                return
            mensaje=verification(numeroPersona,numeroLugar,numeroMotivo,wcards)
            
            messagebox.showinfo("anuncio",mensaje)
            if mensaje== "Ganaste":
                i=numeroMotivo[1]
                noticia(i)

            else:
                self.perdiste=True
                ventanaAcusar.destroy()
                fin_del_juego(False)
                nextPlayer(self.i)
                
            return
            
        Button(ventanaAcusar, text="Enviar",command=acusacion).pack()
        Button(ventanaAcusar, text="Retroceder",command=ventanaAcusar.destroy).pack()

        Button()
        return

def setPickCard(i):
    global player0,player1
    if i==0:
        if player1.perdiste==True:
            player0.buttonpick['state']=NORMAL
            return
        else:
            player0.buttonpick['state']=DISABLED
    elif i==1:
        if player0.perdiste==True:
            player1.buttonpick['state']=NORMAL
            return
        else:
            player1.buttonpick['state']=DISABLED
            
    
def nextPlayer(i):
    global player0,player1
    
    if i==0:
        if player0.perdiste==True:
            player1.nextPlayer['state']=DISABLED
        if player1.perdiste==True:
            player1.window.withdraw()
            player0.window.deiconify()
            return    
        player1.window.deiconify()
        player0.window.withdraw()
    else:
        if player1.perdiste==True:
            player0.nextPlayer['state']=DISABLED
        if player0.perdiste==True:
            player0.window.withdraw()
            player1.window.deiconify()
            return
        player0.window.deiconify()
        player1.window.withdraw()
    
        
def noticia(i):
    titulo=noticias[i][0]
    img=noticias[i][1]
    descripcion=noticias[i][2]
    link=noticias[i][3]
    
    ventananoticia=Toplevel()
    ventananoticia.title("Noticia")
    ventananoticia.geometry("600x500")
    Label(ventananoticia,text=titulo).pack()
    
    global new_img
    canva = Canvas(ventananoticia, width=400, height=200)
    canva.pack()
    my_img = (Image.open(img))
    resized_img = my_img.resize((400, 200), Image.ANTIALIAS)
    new_img = ImageTk.PhotoImage(resized_img)
    canva.create_image(10, 10, anchor=NW, image=new_img)
    
    Label(ventananoticia,text=descripcion).pack()
    def callback(url):
        webbrowser.open_new(url)
            
    link1 = Label(ventananoticia, text="Link a la noticia", fg="blue", cursor="hand2")
    link1.pack()
    link1.bind("<Button-1>", lambda e: callback(link))
    clickButton=Button(ventananoticia,text="cerrar juego",command=lambda:fin_del_juego(True))  
    clickButton.pack() 
    return

def fin_del_juego(var):
    global player0, player1
    if var==True:
        root.destroy()
    elif player0.perdiste==True and player1.perdiste==True:
        messagebox.showinfo("Fin del juego","Nadie gano")
        root.destroy()
    
def play(pregunta:Player,respuesta:Player,i):
    texto=pregunta.entry.get()
    numero=nameToNumber(texto)
    if numero == (-1,-1):
        messagebox.showwarning("Error","Debes ingresar una carta correcta")
        
        return
    kbs[i],mensaje=question(kbs[i],numero[0],numero[1],respuesta.cards)
    if respuesta.perdiste==True:
        pregunta.button['state'] = NORMAL
    else:
        pregunta.button['state'] = DISABLED
    messagebox.showinfo("Base de conocimiento",mensaje)       
    return 
def showAnotherplayer(window1: Toplevel, window2: Toplevel, player: Player,anotherplayer: Player):
    if anotherplayer.perdiste==True:return
    nextPlayer(player.i)

    player.buttonpick['state'] = NORMAL
    player.button['state'] = NORMAL

def start():
    global root, available_cards, wcards,player0,player1
    root.withdraw()
    player0 = Player("Jugador 1",0)
    player1 = Player("Jugador 2",1)    

    player0.selectInitialCards(player1.cards, 0)
    player1.selectInitialCards(player0.cards, 1)

    player0.button=Button(player0.window, text="Enviar", command= lambda:play(player0,player1,0))
    player0.button.pack()
    player0.nextPlayer=Button(player0.window, text="El siguiente jugador", 
    command=lambda: showAnotherplayer(player0.window, player1.window, player0,player1))
    player0.nextPlayer.pack()
    player1.button=Button(player1.window, text="Enviar", command= lambda:play(player1,player0,1))
    player1.button.pack()
    player1.nextPlayer=Button(player1.window, text="El siguiente jugador", 
    command=lambda: showAnotherplayer(player1.window, player0.window, player1,player0))
    player1.nextPlayer.pack()
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