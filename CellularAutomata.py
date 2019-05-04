from tkinter import *
from time import sleep


class LangtonAnt(Canvas):
    """Classe qui permet de simuler la fourmis de Langton"""

    def __init__(self, boss =None, cote =200):
        """Constructeur de la classe
        Initialisation du canvas et des variables"""

        Canvas.__init__(self)   # héritage de Canvas

        # Initialisation des variables
        self.cote =cote                         #nombre de cellule par coté
        self.cellSize =2                        # taille des cellules
        self.canSize =self.cellSize*self.cote   # taille du canvas    
        self.config(bg ='black')

        # configuration du canvas
        self.config(width =self.canSize, height =self.canSize)
        self.bind('<Button>', self.switchColor)

        self.passer =[]

        # Initialisation des direction dans lesquelles la fourmis peut regarder
        self.vhaut =0
        self.vdroite =1
        self.vbas =2
        self.vgauche =3

        # Initialisation des directions dans lesquelles la fourmis peut tourné
        self.ddroite =0
        self.dgauche =1

        # Définitions des fonctions de mouvement
        # Configuration: self.mouvement[direction tourné (ddroite ou dgauche][regard (vhaut, vbas, vdroite, vgauche)]
        # Voire la photo incluse dans le dossier pour plus de détails
        self.mouvement =[ 
                        
                        [ [self.vdroite, 'self.Antx+1, self.Anty'], [self.vbas, 'self.Antx, self.Anty+1'], 
                            [self.vgauche, 'self.Antx-1, self.Anty'], [self.vhaut, 'self.Antx, self.Anty-1'] ],
                                
                            [ [self.vgauche, 'self.Antx-1, self.Anty'], [self.vhaut, 'self.Antx, self.Anty-1'],
                            [self.vdroite, 'self.Antx+1, self.Anty'], [self.vbas, 'self.Antx, self.Anty+1'] ]
                             
                        ]
        
        # Initialisation des règles de déplacement
        self.direction =[ ['white', self.ddroite], ['black', self.dgauche]]

        #Initialisation des variables d'état

        self.regard =self.vhaut # la fourmis regarde en haut
        self.Antx =self.cote//2 # position initiale en x de la fourmis
        self.Anty =self.cote//2 # position initiale en y de la fourmis

        self.outFlag =False # flag de sortie du canvas

        # Initialisation des listes de stockage de données
        self.cell =[ [0 for row in range(self.cote)] for col in range(self.cote) ]   #stockage des cellules
        self.etat =[ [0 for row in range(self.cote)] for col in range(self.cote)] #stockage des états des cellules à l'état t

        # Initialisation de l'état de la position initiale de la fourmis
        self.etat[self.cote//2][self.cote//2] =0

        # On dessine et on configure les cellules et leurs état
        for x in range(self.cote):
            for y in range(self.cote):
                self.cell[x][y] =self.create_rectangle((x*self.cellSize, y*self.cellSize, (x+1)*self.cellSize, (y+1)*self.cellSize), 
                                                        outline ='#5d5d5d', fill ='#5d5d5d')
                self.etat[x][y] =0


    def switchColor(self, event):
        """Fonction qui permet de changer l'éat d'une cellule après un clic"""
        
        # on récupère la position de la cellule cliqué
        x =event.x//self.cellSize   
        y =event.y//self.cellSize

        # On passe l'état de la cellule a l'état suivant
        self.etat[x][y] =(self.etat[x][y]+1)%len(self.direction)

        # On récupère la couleur
        color =self.direction[self.etat[x][y]][0]
         
        # on configure la cellule en changeant sa couleur
        self.itemconfig(self.cell[x][y], outline =color, fill =color)


    def calcul(self):
        """Fonction qui permet de calculer l'étape suivante"""

        if self.outFlag == True:    # on vérifie si on est pas sortie du canvas
            return
        else:
            None

        # Position des données couleur et direction dans les règles
        couleur =0
        direction =1

        if [self.Antx, self.Anty] in self.passer:
            pass
        else:
            self.passer.append([self.Antx, self.Anty] )

        # mise à jour de l'état de la cellule actuelle
        self.etat[self.Antx][self.Anty] =(self.etat[self.Antx][self.Anty]+1)%len(self.direction)

        # on récupère la couleur qui correspont a cet état
        coul =self.direction[self.etat[self.Antx][self.Anty]][couleur]

        # On configure la cellule en changeant sa couleur"""
        self.itemconfig(self.cell[self.Antx][self.Anty], outline =coul, fill =coul)


        # On récupère les règles qui correspondent à la prochaine étape en fonction de l'état de la cellule et du regard
        rule =self.mouvement[ self.direction[self.etat[self.Antx][self.Anty]][direction] ] [self.regard]

        # On recalcul les position x y de la fourmis
        self.Antx, self.Anty =eval(rule[1])

        # On met à jour le regard
        self.regard =rule[0]

        # On vérifie qu'on sort pas du canvas
        if self.Antx<0 or self.Antx>self.cote-1 or self.Anty<0 or self.Anty>self.cote-1:
            self.outFlag =True
        else: 
            self.itemconfig(self.cell[self.Antx][self.Anty], fill='red')
