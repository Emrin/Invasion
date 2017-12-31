# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 18:32:06 2015

@author: Emrin
"""

from tkinter import *
import random as random
from time import *
import threading
import pickle
from operator import itemgetter

#Etat du jeux
Startup = 1
Vies = 3
Lazer_Ready=1

#Etat des Fenetres
Start = 1
Game_On = 0
Score = 0

#classe heritant de Tk pour mettre le tout ensemble
class Link(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        container = Frame(self) #on va tout mettre dans le container
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for Frames in (StartFrame, GameFrame, ScoreFrame):
            frame = Frames(container, self)
            self.frames[Frames] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartFrame)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() # cela met en avant le frame choisie
    

class StartFrame(Frame):
    def __init__(self, parent, controller):
        global Start, Game_On, Score, Enemy_Fire
        global UserName, Startup, EntryEnterName
        global Set_GameFrame, Set_GameFrame_Event, Set_ScoreFrame, Set_ScoreFrame_Event, Edit_Name, Start_Once
        Frame.__init__(self, parent, bg="gray21")
        
        Start_Once = 1
        
        def Set_GameFrame(event=None): #debute les mechanismes du jeux
            global Game_On, Start, Start_Once
            controller.show_frame(GameFrame)
            EntryEnterName.configure(state='disabled')
            self.ButtonEditName.configure(state='normal')
            Start = 0
            Game_On = 1
            if Start_Once == 1:
                Start_Once = 0
                Autopilot_Right()
                Autopilot_Right2()
                Autopilot_Right3()
                Autopilot_Right4()
                Autopilot_Right5()
                Autopilot_Right6()
                Autopilot_Right7()
                Enemy_Fire()
                Enemy_Fire2()
                Enemy_Fire3()
                Enemy_Fire4()
                Enemy_Fire5()
                Enemy_Fire6()
                Enemy_Fire7()
        
        def Set_ScoreFrame(event=None):
            global Start, Score
            controller.show_frame(ScoreFrame)
            EntryEnterName.configure(state='disabled')
            self.ButtonEditName.configure(state='normal')
            Start = 0
            Score = 1
        
        def Edit_Name():
            EntryEnterName.configure(state='normal')
            self.after(5000, Set_ScoreName)
        
        self.LabelWelcome = Label(self, text="BIENVENU DANS INVASION", font=("System", 20), fg="RoyalBlue1", bg="gray21") #invasion graphic #compound option
        self.LabelWelcome.pack(padx=15, pady=15)
        
        self.LabelEnterName = Label(self, text="Entrer Nom :", font=("System", 10), fg="chartreuse", bg="gray21")
        self.LabelEnterName.pack()
        
        UserName = StringVar()
        EntryEnterName = Entry(self, textvariable = UserName)
        EntryEnterName.focus_set()
        EntryEnterName.pack()
        
        self.ButtonEditName = Button(self, text="Editer Nom", font=("System", 10), command = Edit_Name)
        self.ButtonEditName.pack(padx=3, pady=3)
        
        self.ButtonGameFrame = Button(self, text="Debuter le Jeux! [enter]", font=("System", 10), fg="white", bg="Green3", command = Set_GameFrame)
        self.ButtonGameFrame.pack(padx=5, pady=5)
        
        self.ButtonScoreFrame = Button(self, text="Tableau de Bord [ins]", font=("System", 10), bg="goldenrod", command = Set_ScoreFrame)
        self.ButtonScoreFrame.pack(padx=5, pady=5)
        
        self.ButtonQuit = Button(self, text="Quitter [alt+f4]", font=("System", 10), fg="red", bg="black", command=None) #NOPE
        self.ButtonQuit.pack(padx=5, pady=5)
        
        self.Tips = Label(self, text="Utiliser W,A,S,D ou les Flèches pour bouger", fon=("System", 20), fg="white", bg="gray21").pack(pady=30)
        self.Tips2 = Label(self, text="Et espace pour tirer\n(vous pouvez tirer toutes les 1.4 sec)", fon=("System", 20), fg="white", bg="gray21").pack()
        
        self.Tips2 = Label(self, text="Conseil 1:  Les Aliens peuvent utiliser des manoeuvres spéciales après la 1ère vague. \n Conseil 2: Si vous ne laissez pas 1.4sec à votre Lazer pour se recharger,\n il risque d'y avoir une dysfonctionnement.\n Pour réparer cela vous devrez bouger votre vaisceau.", fon=("System", 10), fg="white", bg="gray21").pack(pady=30)
        
        if Startup == 1:
            Startup = 0
            EntryEnterName.insert(0, 'Doge')
            self.ButtonEditName.configure(state='disabled')
        
        #Clefs
        self.bind_all("<Return>", Set_GameFrame)
        self.bind_all("<Insert>", Set_ScoreFrame)
        
#Ici se deroule l'action
class GameFrame(Frame):
    def __init__(self, parent, controller):
        global UserName, Vies, Start, Game_On, Score, CanvasGame, Shots_Fired, Lazer_Ready, EnemyShip1, Player_Score, Set_ScoreFrame, Enemy_Fire, Ship
        global UserName, EntryEnterName, Vies, Startup, Start, Game_On, CanvasGame, Shots_Fired, Lazer_Ready, EnemyShip1, Player_Score, Score, Set_GameFrame, Set_ScoreFrame, Edit_Name, Set_GameFrame_Event, Set_GameFrame_Event, MyShipCoords, Atmosphere
        global Set_StartFrame, Left, Right, Up, Below, Random_Lazer, Score_Animation, Obliterate, Enemy_Hitbox, Lazer_Trajectory, Reload, Fire, Create_Enemy_Lazer, Enemy_Lazer, Set_StartFrame_Event, Player_Lives, EnemyShip1, EnemyShip2, EnemyShip3, EnemyShip4, EnemyShip5, EnemyShip6, EnemyShip7, EnemyShips
        Frame.__init__(self, parent, bg="gray14")
        
        def Set_StartFrame(event=None):
            global Game_On, Start
            controller.show_frame(StartFrame)
            Game_On = 0
            Start = 1
        
        self.LabelPlayer = Label(self, text="Joueur: ", font=("System", 10), fg="white", bg="gray14")
        self.LabelPlayer.grid(row=0, column=0, sticky=W)
        
        self.LabelUserName = Label(self, textvariable=UserName, font=("System", 15), fg="white", bg="gray14")
        self.LabelUserName.grid(row=0, column=1, sticky=W)
        
        self.LabelScore = Label(self, text="Score :", font=("System", 10), fg="yellow", bg="gray14")
        self.LabelScore.grid(row=0, column=2, sticky=E)
        
        Player_Score = IntVar()
        Player_Score.set(0)
        self.LabelScoreValue = Label(self, textvariable=Player_Score, font=("System", 15), fg="yellow", bg="gray14")
        self.LabelScoreValue.grid(row=0, column=3, sticky=E)
        
        self.LabelLives = Label(self, text="Vies: ", font=("System", 10), fg="SeaGreen1", bg="gray14").grid(row=1, column=0, sticky=W)
        
        
        Player_Lives = IntVar()
        Player_Lives.set(5)
        
        self.LabelLivesValue = Label(self, textvariable=Player_Lives, font=("System", 15), fg="SeaGreen1", bg="gray14").grid(row=1, column=1, sticky=W)
        
        self.ButtonHome = Button(self, text="Accueil [esc]", font=("System", 10), fg="white", bg="steel blue",command =Set_StartFrame)
        self.ButtonHome.grid(row=2, column=0, columnspan=2, sticky=W)
        
        self.ButtonScoreboard = Button(self, text="Scoreboard [ins]", font=("System", 10), bg="goldenrod",command = Set_ScoreFrame)
        self.ButtonScoreboard.grid(row=1, column=2, columnspan = 2, sticky=E)
        
        self.ButtonQuit = Button(self, text="Quitter [alt+f4]", font=("System", 10), fg="red", bg="black", command=self.quit)
        self.ButtonQuit.grid(row=2, column=2, columnspan=2, sticky=E)
        
        CanvasGame = Canvas(self, width=700, height=500, bg="midnight blue")
        
        Atmosphere = CanvasGame.create_line(0, 500, 710, 500, width=20, fill="SkyBlue2")
        
        #Vaisceaux
        MyShipCoords=[335, 470, 365, 440]
        Ship = CanvasGame.create_rectangle(MyShipCoords[0], MyShipCoords[1], MyShipCoords[2], MyShipCoords[3], outline="lavender", fill="limegreen")
        
        
        EnemyShip1 = CanvasGame.create_oval(30, 30, 100, 70, outline="light cyan", fill="firebrick", dash=(10,10))
        EnemyShip2 = CanvasGame.create_oval(120, 30, 190, 70, outline="light cyan", fill="firebrick", dash=(10,10))
        EnemyShip3 = CanvasGame.create_oval(210, 30, 280, 70, outline="light cyan", fill="firebrick", dash=(10,10))
        EnemyShip4 = CanvasGame.create_oval(300, 30, 370, 70, outline="light cyan", fill="firebrick", dash=(10,10))
        
        EnemyShip5 = CanvasGame.create_oval(70, 90, 140, 130, outline="light cyan", fill="firebrick", dash=(10,10))
        EnemyShip6 = CanvasGame.create_oval(160, 90, 230, 130, outline="light cyan", fill="firebrick", dash=(10,10))
        EnemyShip7 = CanvasGame.create_oval(250, 90, 320, 130, outline="light cyan", fill="firebrick", dash=(10,10))
        
        EnemyShips = [EnemyShip1, EnemyShip2, EnemyShip3, EnemyShip4, EnemyShip5, EnemyShip6, EnemyShip7]
        
        # EnemyShips.append(CanvasGame.create_oval(120, 150, 190, 190, outline="light cyan", fill="firebrick", dash=(10,10)))
        # EnemyShips.append(CanvasGame.create_oval(210, 150, 280, 190, outline="light cyan", fill="firebrick", dash=(10,10)))
        # 
        # EnemyShips.append(CanvasGame.create_oval(170, 210, 240, 250, outline="light cyan", fill="firebrick", dash=(10,10)))
        
        CanvasGame.grid(row=3, column=0, rowspan=3, columnspan=4)
        
        #Encore quelques clefs
        self.bind_all("<Escape>", Set_StartFrame)
        self.bind_all("<a>", Left)
        self.bind_all("<Left>", Left)
        self.bind_all("<d>", Right)
        self.bind_all("<Right>", Right)
        self.bind_all("<w>", Up)
        self.bind_all("<Up>", Up)
        self.bind_all("<s>", Below)
        self.bind_all("<Down>", Below)
        self.bind_all("<space>", Fire)
        
        
# la fenetre des scores
class ScoreFrame(Frame):
    
    def __init__(self, parent, controller):
        global UserName, Player_Score, CanvasScores, Text_Score, Text_Name
        Frame.__init__(self, parent, bg="dark slate blue")
        
        #objets du fenetre Score
        self.LabelScoreboard = Label(self, text="LE SCOREBOARD", font=("System", 40), fg="gold", bg="dark slate blue").grid(row=0, column=1, rowspan=3, sticky=W)

        self.ButtonHome = Button(self, text="Revenir en Accueil [esc]", font=("System", 10), bg="steel blue", command=lambda: controller.show_frame(StartFrame))
        self.ButtonHome.grid(row=0, column=0, sticky=W)
        
        self.ButtonGame = Button(self, text="Revenir au Jeux [enter]", font=("System", 10), bg="Green3", command=lambda: controller.show_frame(GameFrame))
        self.ButtonGame.grid(row=1, column=0, sticky=W)
        
        self.ButtonQuit = Button(self, text="Quitter [alt+f4]", font=("System", 10), fg="red", bg="black", command=None) #heh
        self.ButtonQuit.grid(row=2, column=0, sticky=W)
        
        CanvasScores = Canvas(self, width=700, height=500, bg="goldenrod")
        
        #Mon score dans le Scoreboard
        Text_Name = CanvasScores.create_text(100, 30, text=UserName.get(), font=("System",30), fill="spring green")
        Text_Score = CanvasScores.create_text(600, 30, text=Player_Score.get(), font=("System",30), fill="spring green")
        
        File_Exists()

        Display_Scores()

        CanvasScores.grid(row=3, column=0,rowspan=3, columnspan=2)
        

#Mouvement
def Left(event):
    Coords_Ship = []
    Coords_Ship = CanvasGame.coords(Ship)
    if Coords_Ship != []:
        if Coords_Ship[0] > 0:
            CanvasGame.move(Ship,-10,0)

def Right(event):
    Coords_Ship = []
    Coords_Ship = CanvasGame.coords(Ship)
    if Coords_Ship != []:
        if Coords_Ship[2] < 700:
            CanvasGame.move(Ship,10,0)

def Up(event):
    Coords_Ship = []
    Coords_Ship = CanvasGame.coords(Ship)
    if Coords_Ship != []:
        if Coords_Ship[1] > 370:
            CanvasGame.move(Ship,0,-5)

def Below(event):
    Coords_Ship = []
    Coords_Ship = CanvasGame.coords(Ship)
    if Coords_Ship != []:
        if Coords_Ship[3] <500 : # x0,y0 haut ,x1,y1 bas
            CanvasGame.move(Ship,0,5)

#Animations & Mechanismes

def Next_Wave(event=None):
    global EnemyShips, EnemyShip1, EnemyShip2, EnemyShip3, EnemyShip4, EnemyShip5, EnemyShip6, EnemyShip7
    
    Gz_Text = CanvasGame.create_text(350, 250, text="La prochaine vague arrive!", font=("System", 30), fill="white")
    CanvasGame.after(2000, lambda: CanvasGame.delete(Gz_Text))
    
    EnemyShip1 = CanvasGame.create_oval(30, 30, 100, 70, outline="light cyan", fill="firebrick", dash=(10,10))
    EnemyShip2 = CanvasGame.create_oval(120, 30, 190, 70, outline="light cyan", fill="firebrick", dash=(10,10))
    EnemyShip3 = CanvasGame.create_oval(210, 30, 280, 70, outline="light cyan", fill="firebrick", dash=(10,10))
    EnemyShip4 = CanvasGame.create_oval(300, 30, 370, 70, outline="light cyan", fill="firebrick", dash=(10,10))
    
    EnemyShip5 = CanvasGame.create_oval(70, 90, 140, 130, outline="light cyan", fill="firebrick", dash=(10,10))
    EnemyShip6 = CanvasGame.create_oval(160, 90, 230, 130, outline="light cyan", fill="firebrick", dash=(10,10))
    EnemyShip7 = CanvasGame.create_oval(250, 90, 320, 130, outline="light cyan", fill="firebrick", dash=(10,10))
    
    EnemyShips = [EnemyShip1, EnemyShip2, EnemyShip3, EnemyShip4, EnemyShip5, EnemyShip6, EnemyShip7]
    
    Autopilot_Right()
    Autopilot_Right2()
    Autopilot_Right3()
    Autopilot_Right4()
    Autopilot_Right5()
    Autopilot_Right6()
    Autopilot_Right7()
    Enemy_Fire()
    Enemy_Fire2()
    Enemy_Fire3()
    Enemy_Fire4()
    Enemy_Fire5()
    Enemy_Fire6()
    Enemy_Fire7()

def Check_Progress(event=None): # Si les enemis sont tous morts alors aux prochains!
    if list(CanvasGame.coords(EnemyShip1)) == []:
        if list(CanvasGame.coords(EnemyShip2)) == []:
            if list(CanvasGame.coords(EnemyShip3)) == []:
                if list(CanvasGame.coords(EnemyShip4)) == []:
                    if list(CanvasGame.coords(EnemyShip5)) == []:
                        if list(CanvasGame.coords(EnemyShip6)) == []:
                            if list(CanvasGame.coords(EnemyShip7)) == []:
                                Next_Wave()

def Score_Animation(event=None):
    Score_Popup = CanvasGame.create_text(Coords_EnemyShip1_Anim[2]-15, Coords_EnemyShip1_Anim[3]+-15, text="360", font=("System",30), fill="yellow")
    CanvasGame.after(1000, lambda: CanvasGame.delete(Score_Popup))

def Score_Animation2(event=None):
    Score_Popup = CanvasGame.create_text(Coords_EnemyShip2_Anim[2]-15, Coords_EnemyShip2_Anim[3]+-15, text="360", font=("System",30), fill="yellow")
    CanvasGame.after(1000, lambda: CanvasGame.delete(Score_Popup))

def Score_Animation3(event=None):
    Score_Popup = CanvasGame.create_text(Coords_EnemyShip3_Anim[2]-15, Coords_EnemyShip3_Anim[3]+-15, text="360", font=("System",30), fill="yellow")
    CanvasGame.after(1000, lambda: CanvasGame.delete(Score_Popup))

def Score_Animation4(event=None):
    Score_Popup = CanvasGame.create_text(Coords_EnemyShip4_Anim[2]-15, Coords_EnemyShip4_Anim[3]+-15, text="360", font=("System",30), fill="yellow")
    CanvasGame.after(1000, lambda: CanvasGame.delete(Score_Popup))

def Score_Animation5(event=None):
    Score_Popup = CanvasGame.create_text(Coords_EnemyShip5_Anim[2]-15, Coords_EnemyShip5_Anim[3]+-15, text="360", font=("System",30), fill="yellow")
    CanvasGame.after(1000, lambda: CanvasGame.delete(Score_Popup))

def Score_Animation6(event=None):
    Score_Popup = CanvasGame.create_text(Coords_EnemyShip6_Anim[2]-15, Coords_EnemyShip6_Anim[3]+-15, text="360", font=("System",30), fill="yellow")
    CanvasGame.after(1000, lambda: CanvasGame.delete(Score_Popup))

def Score_Animation7(event=None):
    Score_Popup = CanvasGame.create_text(Coords_EnemyShip7_Anim[2]-15, Coords_EnemyShip7_Anim[3]+-15, text="360", font=("System",30), fill="yellow")
    CanvasGame.after(1000, lambda: CanvasGame.delete(Score_Popup))

# def Obliterate(enemy):
#     global EnemyShips, Coords_EnemyShip_Anim
#     
#     Coords_EnemyShip_Anim = list(CanvasGame.coords(enemy))
#     CanvasGame.delete(enemy)
#     
#     Player_Score_got = Player_Score.get()
#     Player_Score.set(Player_Score_got + 360)
#     CanvasScores.itemconfig(Text_Score, text=Player_Score.get())
#     Score_Animation()
#     Reload()
# 

def Obliterate(event=None): #cela efface L'ennemi touche, et regle les scores
    global EnemyShip1, Coords_EnemyShip1_Anim, EnemyShips
    Coords_EnemyShip1_Anim = list(CanvasGame.coords(EnemyShip1))
    CanvasGame.delete(EnemyShip1)
    Player_Score_got = Player_Score.get()
    Player_Score.set(Player_Score_got + 360)
    CanvasScores.itemconfig(Text_Score, text=Player_Score.get())
    Score_Animation()
    Reload()
    Check_Progress()

def Obliterate2(event=None):
    global EnemyShip2, Coords_EnemyShip2_Anim, EnemyShips
    Coords_EnemyShip2_Anim = list(CanvasGame.coords(EnemyShip2))
    CanvasGame.delete(EnemyShip2)
    Player_Score_got = Player_Score.get()
    Player_Score.set(Player_Score_got + 360)
    CanvasScores.itemconfig(Text_Score, text=Player_Score.get())
    Score_Animation2()
    Reload()
    Check_Progress()

def Obliterate3(event=None):
    global EnemyShip3, Coords_EnemyShip3_Anim, EnemyShips
    Coords_EnemyShip3_Anim = list(CanvasGame.coords(EnemyShip3))
    CanvasGame.delete(EnemyShip3)
    Player_Score_got = Player_Score.get()
    Player_Score.set(Player_Score_got + 360)
    CanvasScores.itemconfig(Text_Score, text=Player_Score.get())
    Score_Animation3()
    Reload()
    Check_Progress()

def Obliterate4(event=None):
    global EnemyShip4, Coords_EnemyShip4_Anim, EnemyShips
    Coords_EnemyShip4_Anim = list(CanvasGame.coords(EnemyShip4))
    CanvasGame.delete(EnemyShip4)
    Player_Score_got = Player_Score.get()
    Player_Score.set(Player_Score_got + 360)
    CanvasScores.itemconfig(Text_Score, text=Player_Score.get())
    Score_Animation4()
    Reload()
    Check_Progress()

def Obliterate5(event=None):
    global EnemyShip5, Coords_EnemyShip5_Anim, EnemyShips
    Coords_EnemyShip5_Anim = list(CanvasGame.coords(EnemyShip5))
    CanvasGame.delete(EnemyShip5)
    Player_Score_got = Player_Score.get()
    Player_Score.set(Player_Score_got + 360)
    CanvasScores.itemconfig(Text_Score, text=Player_Score.get())
    Score_Animation5()
    Reload()
    Check_Progress()

def Obliterate6(event=None):
    global EnemyShip6, Coords_EnemyShip6_Anim, EnemyShips
    Coords_EnemyShip6_Anim = list(CanvasGame.coords(EnemyShip6))
    CanvasGame.delete(EnemyShip6)
    Player_Score_got = Player_Score.get()
    Player_Score.set(Player_Score_got + 360)
    CanvasScores.itemconfig(Text_Score, text=Player_Score.get())
    Score_Animation6()
    Reload()
    Check_Progress()

def Obliterate7(event=None):
    global EnemyShip7, Coords_EnemyShip7_Anim, EnemyShips
    Coords_EnemyShip7_Anim = list(CanvasGame.coords(EnemyShip7))
    CanvasGame.delete(EnemyShip7)
    Player_Score_got = Player_Score.get()
    Player_Score.set(Player_Score_got + 360)
    CanvasScores.itemconfig(Text_Score, text=Player_Score.get())
    Score_Animation7()
    Reload()
    Check_Progress()

def Enemy_Hitbox(event=None):
    global Coords_Lazer
    Coords_EnemyShip1 = list(CanvasGame.coords(EnemyShip1))
    if Coords_EnemyShip1 != []:
        if Coords_Lazer[0] > Coords_EnemyShip1[0]:
            if Coords_Lazer[2] < Coords_EnemyShip1[2]:
                if Coords_Lazer[1] < Coords_EnemyShip1[3]:
                    # if Coords_Lazer[0] < Coords_EnemyShip1[3]:
                    Obliterate()

def Enemy_Hitbox2(event=None):
    global Coords_Lazer
    Coords_EnemyShip2 = list(CanvasGame.coords(EnemyShip2))
    if Coords_EnemyShip2 != []:
        if Coords_Lazer[0] > Coords_EnemyShip2[0]:
            if Coords_Lazer[2] < Coords_EnemyShip2[2]:
                if Coords_Lazer[1] < Coords_EnemyShip2[3]:
                    # if Coords_Lazer[0] < Coords_EnemyShip1[3]:
                    Obliterate2()

def Enemy_Hitbox3(event=None):
    global Coords_Lazer
    Coords_EnemyShip3 = list(CanvasGame.coords(EnemyShip3))
    if Coords_EnemyShip3 != []:
        if Coords_Lazer[0] > Coords_EnemyShip3[0]:
            if Coords_Lazer[2] < Coords_EnemyShip3[2]:
                if Coords_Lazer[1] < Coords_EnemyShip3[3]:
                    # if Coords_Lazer[0] < Coords_EnemyShip1[3]:
                    Obliterate3()

def Enemy_Hitbox4(event=None):
    global Coords_Lazer
    Coords_EnemyShip4 = list(CanvasGame.coords(EnemyShip4))
    if Coords_EnemyShip4 != []:
        if Coords_Lazer[0] > Coords_EnemyShip4[0]:
            if Coords_Lazer[2] < Coords_EnemyShip4[2]:
                if Coords_Lazer[1] < Coords_EnemyShip4[3]:
                    # if Coords_Lazer[0] < Coords_EnemyShip1[3]:
                    Obliterate4()

def Enemy_Hitbox5(event=None):
    global Coords_Lazer
    Coords_EnemyShip5 = list(CanvasGame.coords(EnemyShip5))
    if Coords_EnemyShip5 != []:
        if Coords_Lazer[0] > Coords_EnemyShip5[0]:
            if Coords_Lazer[2] < Coords_EnemyShip5[2]:
                if Coords_Lazer[1] < Coords_EnemyShip5[3]:
                    # if Coords_Lazer[0] < Coords_EnemyShip1[3]:
                    Obliterate5()

def Enemy_Hitbox6(event=None):
    global Coords_Lazer
    Coords_EnemyShip6 = list(CanvasGame.coords(EnemyShip6))
    if Coords_EnemyShip6 != []:
        if Coords_Lazer[0] > Coords_EnemyShip6[0]:
            if Coords_Lazer[2] < Coords_EnemyShip6[2]:
                if Coords_Lazer[1] < Coords_EnemyShip6[3]:
                    # if Coords_Lazer[0] < Coords_EnemyShip1[3]:
                    Obliterate6()

def Enemy_Hitbox7(event=None):
    global Coords_Lazer
    Coords_EnemyShip7 = list(CanvasGame.coords(EnemyShip7))
    if Coords_EnemyShip7 != []:
        if Coords_Lazer[0] > Coords_EnemyShip7[0]:
            if Coords_Lazer[2] < Coords_EnemyShip7[2]:
                if Coords_Lazer[1] < Coords_EnemyShip7[3]:
                    # if Coords_Lazer[0] < Coords_EnemyShip1[3]:
                    Obliterate7()

# def Enemy_Hitbox(event=None):
#     global Coords_Lazer
#     Coords_EnemyShips = []
#     for Enemy in EnemyShips:
#         Coords_EnemyShips.append(CanvasGame.coords(Enemy))
#     if EnemyShips != []:
#         for i in range(len(EnemyShips)):
#             if Coords_Lazer[0] > Coords_EnemyShips[i][0]:
#                 if Coords_Lazer[2] < Coords_EnemyShips[i][2]:
#                     if Coords_Lazer[1] < Coords_EnemyShips[i][3]:
#                         # if Coords_Lazer[0] < Coords_EnemyShip[i][3]:
#                         Obliterate(EnemyShips[i])

def Lazer_Trajectory(event=None):
    global Lazer, Coords_Lazer
    Coords_Lazer = list(CanvasGame.coords(Lazer))
    if Coords_Lazer != []:
        CanvasGame.move(Lazer,0,-20)
        Enemy_Hitbox()
        Enemy_Hitbox2()
        Enemy_Hitbox3()
        Enemy_Hitbox4()
        Enemy_Hitbox5()
        Enemy_Hitbox6()
        Enemy_Hitbox7()
        threading.Timer(0.05, Lazer_Trajectory).start()

def Reload(event=None): # Recharger le lazer
    global Lazer_Ready, Lazer
    if Lazer in CanvasGame.find_all():
        CanvasGame.delete(Lazer)
    Lazer_Ready = 1
    # Tk.bind_all("<space>", Fire)
    EnemyShips = [EnemyShip1, EnemyShip2, EnemyShip3, EnemyShip4, EnemyShip5, EnemyShip6, EnemyShip7]
    if EnemyShips == []:
        Next_Weave()

def Random_Lazer(event=None): # couleur aleatoire
    Colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]
    return random.choice(Colors)

def Fire(event):
    global Lazer, Lazer_Ready
    if Ship in CanvasGame.find_all():
        if Lazer_Ready == 1:
            Lazer_Ready = 0
            # Tk.unbind_all("<space>", Fire)
            Coords_Ship = list(CanvasGame.coords(Ship))
            Lazer = CanvasGame.create_line(Coords_Ship[0]+15,Coords_Ship[1],Coords_Ship[2]-15,Coords_Ship[3], width=3, fill=Random_Lazer())
            Lazer_Trajectory()
            CanvasGame.after(1400, Reload)

def Display_Scores(event=None): #affiche les scores en les classant
    global high_scores, Text_Player_Names, Text_Player_Scores
    File = open('High_Scores', 'rb')
    high_scores = pickle.load(File)
    File.close()
    
    Player_Names = []
    Player_Scores = []
    
    for pair in high_scores:
        Player_Names.append(pair[0])
        Player_Scores.append(pair[1])
    
    for i in range(len(Player_Names)):
        Text_Player_Names = CanvasScores.create_text(100, 100 + i*42, text=Player_Names[i], font=("System",17), fill="white")
        
    for i in range(len(Player_Scores)):
        Text_Player_Scores = CanvasScores.create_text(600, 100 + i*42, text=Player_Scores[i], font=("System",17), fill="white")

def Erase_Scores(event=None): # effacer anciens textes
    CanvasScores.delete(ALL)
    Text_Name = CanvasScores.create_text(100, 30, text=UserName.get(), font=("System",30), fill="spring green")
    Text_Score = CanvasScores.create_text(600, 30, text=Player_Score.get(), font=("System",30), fill="spring green")

def Update_File(event=None): #mettre à jour le fichier
    File = open('High_Scores', 'wb')
    pickle.dump(high_scores, File)
    File.close()

def Update_Scores(event=None): #ajouter le score du joueur à la liste high_scores, et retenir les 10 1ers
    global high_scores
    high_scores.append((UserName.get(), Player_Score.get()))
    high_scores = sorted(high_scores, key=itemgetter(1), reverse=True)[:10]
    Update_File()
    Erase_Scores()
    Display_Scores()

def GameOver(event=None):
    CanvasGame.create_text(350, 250, text="---=Game Over=---", font=("System", 30), fill="white")
    CanvasGame.itemconfig(Atmosphere, fill="firebrick")
    CanvasGame.delete(Ship)
    Update_Scores()

def Resurrect(event=None): # reaparaitre au milieu
    CanvasGame.coords(Ship, MyShipCoords[0], MyShipCoords[1], MyShipCoords[2], MyShipCoords[3])

def Wreck_Animation(event=None):
    Coords_Ship = list(CanvasGame.coords(Ship))
    Wrecked_Text = CanvasGame.create_text(350, 200, text="Vous êtes touché", font=("System", 30), fill="white")
    Boom_Text = CanvasGame.create_text(Coords_Ship[0]+15, Coords_Ship[1]+15, text="boom", font=("System", 15), fill="white")
    CanvasGame.after(1000, lambda: CanvasGame.delete(Wrecked_Text))
    CanvasGame.after(1000, lambda: CanvasGame.delete(Boom_Text))

def Wreck(event=None): #si on est touché, on regle les vies
    global Ship, Coords_Ship_Anim, Player_Lives
    Coords_Ship_Anim = list(CanvasGame.coords(Ship))
    Player_Lives_got = Player_Lives.get()
    Player_Lives.set(Player_Lives_got -1)
    Wreck_Animation()
    if Player_Lives.get() >= 1:
        Resurrect()
    else:
        GameOver()

def Player_Hitbox(event=None):
    Coords_Ship = list(CanvasGame.coords(Ship))
    if Coords_Ship != []:
        if Coords_Enemy_Lazer[0] > Coords_Ship[0]:
            if Coords_Enemy_Lazer[0] < Coords_Ship[2]:
                if Coords_Enemy_Lazer[3] > Coords_Ship[1]:
                    if Coords_Enemy_Lazer[1] < Coords_Ship[3]:
                        Wreck()

def Enemy_Lazer_Trajectory(event=None):
    global Enemy_Lazer, Coords_Enemy_Lazer
    Coords_Enemy_Lazer = list(CanvasGame.coords(Enemy_Lazer))
    if Coords_Enemy_Lazer[3] < 550:
        CanvasGame.move(Enemy_Lazer,0,20)
        threading.Timer(0.05, Enemy_Lazer_Trajectory).start()
        Player_Hitbox()

def Create_Enemy_Lazer(event=None):
    global Enemy_Lazer
    Coords_EnemyShip1 = list(CanvasGame.coords(EnemyShip1))
    Enemy_Lazer = CanvasGame.create_line(Coords_EnemyShip1[0]+35, Coords_EnemyShip1[1], Coords_EnemyShip1[0]+35, Coords_EnemyShip1[3], width=3, fill=Random_Lazer())
    Enemy_Lazer_Trajectory()
    
first_time_shooting = 1
def Enemy_Fire(event=None):
    global first_time_shooting
    if EnemyShip1 in CanvasGame.find_all():
        if first_time_shooting != 1:
            # if Enemy_Lazer in CanvasGame.find_all(): #
            CanvasGame.delete(Enemy_Lazer)
        first_time_shooting = 0
        Create_Enemy_Lazer()
        t = random.randrange(2, 10, 1)
        threading.Timer(t, Enemy_Fire).start()

def Player_Hitbox2(event=None):
    Coords_Ship = list(CanvasGame.coords(Ship))
    if Coords_Ship != []:
        if Coords_Enemy_Lazer2[0] > Coords_Ship[0]:
            if Coords_Enemy_Lazer2[0] < Coords_Ship[2]:
                if Coords_Enemy_Lazer2[3] > Coords_Ship[1]:
                    if Coords_Enemy_Lazer2[1] < Coords_Ship[3]:
                        Wreck()

def Enemy_Lazer_Trajectory2(event=None):
    global Enemy_Lazer2, Coords_Enemy_Lazer2
    Coords_Enemy_Lazer2 = list(CanvasGame.coords(Enemy_Lazer2))
    if Coords_Enemy_Lazer2[3] < 550:
        CanvasGame.move(Enemy_Lazer2,0,20)
        threading.Timer(0.05, Enemy_Lazer_Trajectory2).start()
        Player_Hitbox2()

def Create_Enemy_Lazer2(event=None):
    global Enemy_Lazer2
    Coords_EnemyShip2 = list(CanvasGame.coords(EnemyShip2))
    Enemy_Lazer2 = CanvasGame.create_line(Coords_EnemyShip2[0]+35, Coords_EnemyShip2[1], Coords_EnemyShip2[0]+35, Coords_EnemyShip2[3], width=3, fill=Random_Lazer())
    Enemy_Lazer_Trajectory2()

first_time_shooting2 = 1
def Enemy_Fire2(event=None):
    global first_time_shooting2
    if EnemyShip2 in CanvasGame.find_all():
        if first_time_shooting2 != 1:
        # if Enemy_Lazer2 in CanvasGame.find_all(): #
            CanvasGame.delete(Enemy_Lazer2)
        first_time_shooting2 = 0
        Create_Enemy_Lazer2()
        t = random.randrange(2, 10, 1)
        threading.Timer(t, Enemy_Fire2).start()

def Player_Hitbox3(event=None):
    Coords_Ship = list(CanvasGame.coords(Ship))
    if Coords_Ship != []:
        if Coords_Enemy_Lazer3[0] > Coords_Ship[0]:
            if Coords_Enemy_Lazer3[0] < Coords_Ship[2]:
                if Coords_Enemy_Lazer3[3] > Coords_Ship[1]:
                    if Coords_Enemy_Lazer3[1] < Coords_Ship[3]:
                        Wreck()

def Enemy_Lazer_Trajectory3(event=None):
    global Enemy_Lazer3, Coords_Enemy_Lazer3
    Coords_Enemy_Lazer3 = list(CanvasGame.coords(Enemy_Lazer3))
    if Coords_Enemy_Lazer3[3] < 550:
        CanvasGame.move(Enemy_Lazer3,0,20)
        threading.Timer(0.05, Enemy_Lazer_Trajectory3).start()
        Player_Hitbox3()

def Create_Enemy_Lazer3(event=None):
    global Enemy_Lazer3
    Coords_EnemyShip3 = list(CanvasGame.coords(EnemyShip3))
    Enemy_Lazer3 = CanvasGame.create_line(Coords_EnemyShip3[0]+35, Coords_EnemyShip3[1], Coords_EnemyShip3[0]+35, Coords_EnemyShip3[3], width=3, fill=Random_Lazer())
    Enemy_Lazer_Trajectory3()

first_time_shooting3 = 1
def Enemy_Fire3(event=None):
    global first_time_shooting3
    if EnemyShip3 in CanvasGame.find_all():
        if first_time_shooting3 != 1:
        # if Enemy_Lazer3 in CanvasGame.find_all(): #
            CanvasGame.delete(Enemy_Lazer3)
        first_time_shooting3 = 0
        Create_Enemy_Lazer3()
        t = random.randrange(2, 10, 1)
        threading.Timer(t, Enemy_Fire3).start()

def Player_Hitbox4(event=None):
    Coords_Ship = list(CanvasGame.coords(Ship))
    if Coords_Ship != []:
        if Coords_Enemy_Lazer4[0] > Coords_Ship[0]:
            if Coords_Enemy_Lazer4[0] < Coords_Ship[2]:
                if Coords_Enemy_Lazer4[3] > Coords_Ship[1]:
                    if Coords_Enemy_Lazer4[1] < Coords_Ship[3]:
                        Wreck()

def Enemy_Lazer_Trajectory4(event=None):
    global Enemy_Lazer4, Coords_Enemy_Lazer4
    Coords_Enemy_Lazer4 = list(CanvasGame.coords(Enemy_Lazer4))
    if Coords_Enemy_Lazer4[3] < 550:
        CanvasGame.move(Enemy_Lazer4,0,20)
        threading.Timer(0.05, Enemy_Lazer_Trajectory4).start()
        Player_Hitbox4()

def Create_Enemy_Lazer4(event=None):
    global Enemy_Lazer4
    Coords_EnemyShip4 = list(CanvasGame.coords(EnemyShip4))
    Enemy_Lazer4 = CanvasGame.create_line(Coords_EnemyShip4[0]+35, Coords_EnemyShip4[1], Coords_EnemyShip4[0]+35, Coords_EnemyShip4[3], width=3, fill=Random_Lazer())
    Enemy_Lazer_Trajectory4()

first_time_shooting4 = 1
def Enemy_Fire4(event=None):
    global first_time_shooting4
    if EnemyShip4 in CanvasGame.find_all():
        if first_time_shooting4 != 1:
        # if Enemy_Lazer4 in CanvasGame.find_all(): #
            CanvasGame.delete(Enemy_Lazer4)
        first_time_shooting4 = 0
        Create_Enemy_Lazer4()
        t = random.randrange(2, 10, 1)
        threading.Timer(t, Enemy_Fire4).start()

def Player_Hitbox5(event=None):
    Coords_Ship = list(CanvasGame.coords(Ship))
    if Coords_Ship != []:
        if Coords_Enemy_Lazer5[0] > Coords_Ship[0]:
            if Coords_Enemy_Lazer5[0] < Coords_Ship[2]:
                if Coords_Enemy_Lazer5[3] > Coords_Ship[1]:
                    if Coords_Enemy_Lazer5[1] < Coords_Ship[3]:
                        Wreck()

def Enemy_Lazer_Trajectory5(event=None):
    global Enemy_Lazer5, Coords_Enemy_Lazer5
    Coords_Enemy_Lazer5 = list(CanvasGame.coords(Enemy_Lazer5))
    if Coords_Enemy_Lazer5[3] < 550:
        CanvasGame.move(Enemy_Lazer5,0,20)
        threading.Timer(0.05, Enemy_Lazer_Trajectory5).start()
        Player_Hitbox5()

def Create_Enemy_Lazer5(event=None):
    global Enemy_Lazer5
    Coords_EnemyShip5 = list(CanvasGame.coords(EnemyShip5))
    Enemy_Lazer5 = CanvasGame.create_line(Coords_EnemyShip5[0]+35, Coords_EnemyShip5[1], Coords_EnemyShip5[0]+35, Coords_EnemyShip5[3], width=3, fill=Random_Lazer())
    Enemy_Lazer_Trajectory5()

first_time_shooting5 = 1
def Enemy_Fire5(event=None):
    global first_time_shooting5
    if EnemyShip5 in CanvasGame.find_all():
        if first_time_shooting5 != 1:
        # if Enemy_Lazer5 in CanvasGame.find_all(): #
            CanvasGame.delete(Enemy_Lazer5)
        first_time_shooting5 = 0
        Create_Enemy_Lazer5()
        t = random.randrange(2, 10, 1)
        threading.Timer(t, Enemy_Fire5).start()

def Player_Hitbox6(event=None):
    Coords_Ship = list(CanvasGame.coords(Ship))
    if Coords_Ship != []:
        if Coords_Enemy_Lazer6[0] > Coords_Ship[0]:
            if Coords_Enemy_Lazer6[0] < Coords_Ship[2]:
                if Coords_Enemy_Lazer6[3] > Coords_Ship[1]:
                    if Coords_Enemy_Lazer6[1] < Coords_Ship[3]:
                        Wreck()

def Enemy_Lazer_Trajectory6(event=None):
    global Enemy_Lazer6, Coords_Enemy_Lazer6
    Coords_Enemy_Lazer6 = list(CanvasGame.coords(Enemy_Lazer6))
    if Coords_Enemy_Lazer6[3] < 550:
        CanvasGame.move(Enemy_Lazer6,0,20)
        threading.Timer(0.05, Enemy_Lazer_Trajectory6).start()
        Player_Hitbox6()

def Create_Enemy_Lazer6(event=None):
    global Enemy_Lazer6
    Coords_EnemyShip6 = list(CanvasGame.coords(EnemyShip6))
    Enemy_Lazer6 = CanvasGame.create_line(Coords_EnemyShip6[0]+35, Coords_EnemyShip6[1], Coords_EnemyShip6[0]+35, Coords_EnemyShip6[3], width=3, fill=Random_Lazer())
    Enemy_Lazer_Trajectory6()

first_time_shooting6 = 1
def Enemy_Fire6(event=None):
    global first_time_shooting6
    if EnemyShip6 in CanvasGame.find_all():
        if first_time_shooting6 != 1:
        # if Enemy_Lazer6 in CanvasGame.find_all(): #
            CanvasGame.delete(Enemy_Lazer6)
        first_time_shooting6 = 0
        Create_Enemy_Lazer6()
        t = random.randrange(2, 10, 1)
        threading.Timer(t, Enemy_Fire6).start()

def Player_Hitbox7(event=None):
    Coords_Ship = list(CanvasGame.coords(Ship))
    if Coords_Ship != []:
        if Coords_Enemy_Lazer7[0] > Coords_Ship[0]:
            if Coords_Enemy_Lazer7[0] < Coords_Ship[2]:
                if Coords_Enemy_Lazer7[3] > Coords_Ship[1]:
                    if Coords_Enemy_Lazer7[1] < Coords_Ship[3]:
                        Wreck()

def Enemy_Lazer_Trajectory7(event=None):
    global Enemy_Lazer7, Coords_Enemy_Lazer7
    Coords_Enemy_Lazer7 = list(CanvasGame.coords(Enemy_Lazer7))
    if Coords_Enemy_Lazer7[3] < 550:
        CanvasGame.move(Enemy_Lazer7,0,20)
        threading.Timer(0.05, Enemy_Lazer_Trajectory7).start()
        Player_Hitbox7()

def Create_Enemy_Lazer7(event=None):
    global Enemy_Lazer7
    Coords_EnemyShip7 = list(CanvasGame.coords(EnemyShip7))
    Enemy_Lazer7 = CanvasGame.create_line(Coords_EnemyShip7[0]+35, Coords_EnemyShip7[1], Coords_EnemyShip7[0]+35, Coords_EnemyShip7[3], width=3, fill=Random_Lazer())
    Enemy_Lazer_Trajectory7()

first_time_shooting7 = 1
def Enemy_Fire7(event=None):
    global first_time_shooting7
    if EnemyShip7 in CanvasGame.find_all():
        if first_time_shooting7 != 1:
            CanvasGame.delete(Enemy_Lazer7)
        first_time_shooting7 = 0
        Create_Enemy_Lazer7()
        t = random.randrange(2, 10, 1)
        threading.Timer(t, Enemy_Fire7).start()

def Autopilot_Left(event=None): # Ennemi bouge vers la gauche automatiquement
    Coords_EnemyShip1 = list(CanvasGame.coords(EnemyShip1))
    if Coords_EnemyShip1 != []:
        if Coords_EnemyShip1[0] > 30:
            CanvasGame.move(EnemyShip1,-5,0)
            threading.Timer(0.1, Autopilot_Left).start()
        if Coords_EnemyShip1[0] <= 30:
            CanvasGame.move(EnemyShip1,0,50)
            Autopilot_Right()
            if Coords_EnemyShip1[3] >= 400:
                GameOver()

def Autopilot_Left2(event=None):
    Coords_EnemyShip2 = list(CanvasGame.coords(EnemyShip2))
    if Coords_EnemyShip2 != []:
        if Coords_EnemyShip2[0] > 30:
            CanvasGame.move(EnemyShip2,-5,0)
            threading.Timer(0.1, Autopilot_Left2).start()
        if Coords_EnemyShip2[0] <= 30:
            CanvasGame.move(EnemyShip2,0,50)
            Autopilot_Right2()
            if Coords_EnemyShip2[3] >= 400:
                GameOver()

def Autopilot_Left3(event=None):
    Coords_EnemyShip3 = list(CanvasGame.coords(EnemyShip3))
    if Coords_EnemyShip3 != []:
        if Coords_EnemyShip3[0] > 30:
            CanvasGame.move(EnemyShip3,-5,0)
            threading.Timer(0.1, Autopilot_Left3).start()
        if Coords_EnemyShip3[0] <= 30:
            CanvasGame.move(EnemyShip3,0,50)
            Autopilot_Right3()
            if Coords_EnemyShip3[3] >= 400:
                GameOver()

def Autopilot_Left4(event=None):
    Coords_EnemyShip4 = list(CanvasGame.coords(EnemyShip4))
    if Coords_EnemyShip4 != []:
        if Coords_EnemyShip4[0] > 30:
            CanvasGame.move(EnemyShip4,-5,0)
            threading.Timer(0.1, Autopilot_Left4).start()
        if Coords_EnemyShip4[0] <= 30:
            CanvasGame.move(EnemyShip4,0,50)
            Autopilot_Right4()
            if Coords_EnemyShip4[3] >= 400:
                GameOver()

def Autopilot_Left5(event=None):
    Coords_EnemyShip5 = list(CanvasGame.coords(EnemyShip5))
    if Coords_EnemyShip5 != []:
        if Coords_EnemyShip5[0] > 30:
            CanvasGame.move(EnemyShip5,-5,0)
            threading.Timer(0.1, Autopilot_Left5).start()
        if Coords_EnemyShip5[0] <= 30:
            CanvasGame.move(EnemyShip5,0,50)
            Autopilot_Right5()
            if Coords_EnemyShip5[3] >= 400:
                GameOver()

def Autopilot_Left6(event=None):
    Coords_EnemyShip6 = list(CanvasGame.coords(EnemyShip6))
    if Coords_EnemyShip6 != []:
        if Coords_EnemyShip6[0] > 30:
            CanvasGame.move(EnemyShip6,-5,0)
            threading.Timer(0.1, Autopilot_Left6).start()
        if Coords_EnemyShip6[0] <= 30:
            CanvasGame.move(EnemyShip6,0,50)
            Autopilot_Right6()
            if Coords_EnemyShip6[3] >= 400:
                GameOver()

def Autopilot_Left7(event=None):
    Coords_EnemyShip7 = list(CanvasGame.coords(EnemyShip7))
    if Coords_EnemyShip7 != []:
        if Coords_EnemyShip7[0] > 30:
            CanvasGame.move(EnemyShip7,-5,0)
            threading.Timer(0.1, Autopilot_Left7).start()
        if Coords_EnemyShip7[0] <= 30:
            CanvasGame.move(EnemyShip7,0,50)
            Autopilot_Right7()
            if Coords_EnemyShip7[3] >= 400:
                GameOver()

def Autopilot_Right(event=None):
    Coords_EnemyShip1 = list(CanvasGame.coords(EnemyShip1))
    if Coords_EnemyShip1 != []:
        if Coords_EnemyShip1[2] < 670:
            CanvasGame.move(EnemyShip1,5,0)
            threading.Timer(0.1, Autopilot_Right).start()
        if Coords_EnemyShip1[2] >= 670:
            CanvasGame.move(EnemyShip1,0,50)
            Autopilot_Left()
            if Coords_EnemyShip1[3] >= 400:
                GameOver()

def Autopilot_Right2(event=None):
    Coords_EnemyShip2 = list(CanvasGame.coords(EnemyShip2))
    if Coords_EnemyShip2 != []:
        if Coords_EnemyShip2[2] < 670:
            CanvasGame.move(EnemyShip2,5,0)
            threading.Timer(0.1, Autopilot_Right2).start()
        if Coords_EnemyShip2[2] >= 670:
            CanvasGame.move(EnemyShip2,0,50)
            Autopilot_Left2()
            if Coords_EnemyShip2[3] >= 400:
                GameOver()

def Autopilot_Right3(event=None):
    Coords_EnemyShip3 = list(CanvasGame.coords(EnemyShip3))
    if Coords_EnemyShip3 != []:
        if Coords_EnemyShip3[2] < 670:
            CanvasGame.move(EnemyShip3,5,0)
            threading.Timer(0.1, Autopilot_Right3).start()
        if Coords_EnemyShip3[2] >= 670:
            CanvasGame.move(EnemyShip3,0,50)
            Autopilot_Left3()
            if Coords_EnemyShip3[3] >= 400:
                GameOver()

def Autopilot_Right4(event=None):
    Coords_EnemyShip4 = list(CanvasGame.coords(EnemyShip4))
    if Coords_EnemyShip4 != []:
        if Coords_EnemyShip4[2] < 670:
            CanvasGame.move(EnemyShip4,5,0)
            threading.Timer(0.1, Autopilot_Right4).start()
        if Coords_EnemyShip4[2] >= 670:
            CanvasGame.move(EnemyShip4,0,50)
            Autopilot_Left4()
            if Coords_EnemyShip4[3] >= 400:
                GameOver()

def Autopilot_Right5(event=None):
    Coords_EnemyShip5 = list(CanvasGame.coords(EnemyShip5))
    if Coords_EnemyShip5 != []:
        if Coords_EnemyShip5[2] < 670:
            CanvasGame.move(EnemyShip5,5,0)
            threading.Timer(0.1, Autopilot_Right5).start()
        if Coords_EnemyShip5[2] >= 670:
            CanvasGame.move(EnemyShip5,0,50)
            Autopilot_Left5()
            if Coords_EnemyShip5[3] >= 400:
                GameOver()

def Autopilot_Right6(event=None):
    Coords_EnemyShip6 = list(CanvasGame.coords(EnemyShip6))
    if Coords_EnemyShip6 != []:
        if Coords_EnemyShip6[2] < 670:
            CanvasGame.move(EnemyShip6,5,0)
            threading.Timer(0.1, Autopilot_Right6).start()
        if Coords_EnemyShip6[2] >= 670:
            CanvasGame.move(EnemyShip6,0,50)
            Autopilot_Left6()
            if Coords_EnemyShip6[3] >= 400:
                GameOver()

def Autopilot_Right7(event=None):
    Coords_EnemyShip7 = list(CanvasGame.coords(EnemyShip7))
    if Coords_EnemyShip7 != []:
        if Coords_EnemyShip7[2] < 670:
            CanvasGame.move(EnemyShip7,5,0)
            threading.Timer(0.1, Autopilot_Right7).start()
        if Coords_EnemyShip7[2] >= 670:
            CanvasGame.move(EnemyShip7,0,50)
            Autopilot_Left7()
            if Coords_EnemyShip7[3] >= 400:
                GameOver()

def Set_ScoreName(event=None): # met à jour le nom du joueur dans le scoreboard
    CanvasScores.itemconfig(Text_Name, text=UserName.get())

def File_Exists(): # verifie si un fichier scores existe, sinon il le crée
    try:
        File = open('High_Scores', 'rb')
        File.close()
        print("HighScore file exists")
    except:
        File = open('High_Scores', 'wb')
        high_scores=[('Bot',0)]
        pickle.dump(high_scores, File)
        File.close()
        print("HighScore file did not exist and was created")
        # Inform = tkinter.Message('Yes','HighScore file did not exist and was created')
        




#import ctypes 4 user coords



game = Link()
game.title("Invasion")
"""game.maxsize(width=1000, height=1000)
game.minsize(width=1000, height=1000)"""
game.mainloop() # on lance la boucle