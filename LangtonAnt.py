from tkinter import*
from tkinter.colorchooser import *
import tkinter.ttk as ttk
from CellularAutomata import LangtonAnt
from tkinter import filedialog
from tkinter.messagebox import *
from tkinter import tix
import Image, ImageDraw



class RuleWidget(Frame):
    """Widget qui permet de configuré un ensemble de règle"""

    def __init__(self, boss =None, r =1, lb =None):
        """Constructeur"""

        Frame.__init__(self)    #héritage de la classe Frame

        self.labl =lb
        self.config(bg ='#5d5d5d')

        val =tix.Balloon()

        #liste des couleurs d'initialisation
        col =['white', 'black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']

        #on récupère la couleur en fonction du nombre de bouton appelé
        self.color =col[r%8]

        # On cré le widget permettant de saisir la direction de la fourmis
        self.direction =ttk.Combobox(boss, values =['->', '<-'], width =10)
        self.direction.current(r%2)
        val.bind_widget(widget =self.direction, msg="Sélectionner une direction")
        self.direction.grid(row =r, column =2, padx =2, pady =5)

        # bouton pour sélectionner la couleur
        self.b =Button(boss, text ='color', command =self.getColor, bg =self.color, activebackground =self.color)
        val.bind_widget(widget =self.b, msg="Sélectionner une couleur")

        # si la couleur est noir on affiche le texte en blanc
        if self.color == 'black' or self.color == '#000000':
            self.b.config(fg ='white')
        else:
            self.b.config(fg ='black')

        self.b.grid(row =r, column =1, padx =2, pady =5)

    def getColor(self):
        """ Fonction qui permet de saisir une couleur en cliquant sur le bouton"""

        # on cré un widgt de demande de couleur
        self.color =askcolor()[-1]

        # on change la couleur du bouton
        self.b.config(bg =self.color, activebackground =self.color)
        
        # si la couleur choisis est noire on met le texte en blanc
        if self.color == 'black' or self.color == '#000000':
            self.b.config(fg ='white')
        else:
            self.b.config(fg ='black')

        if self.labl != None:
            self.labl.config(text ='Rules are changed', fg ='#FF0000')

        
    def getParam(self):
        """Fonction qui permet de retourné les paramètres utiles a la fourmis"""

        return self.color, self.direction.current()
        


class GUI(tix.Tk):

    def __init__(self):
        """Configuration de l'interface graphique et initialisation des variables"""

        bgColor ='#5d5d5d'
        textColor ='#0000FF'

        # Initialisation de l'interface graphique
        tix.Tk.__init__(self) 
        self.title("Universal Langton Ant")
        self.config(bg =bgColor)

        val =tix.Balloon()


        menuBar =Menu(self)
        self['menu'] = menuBar
        sousMenu =Menu(menuBar)
        menuBar.add_cascade(label='File', menu=sousMenu)
        sousMenu.add_command(label='Open rule', command=self.chargeData)
        sousMenu.add_command(label='Save rule', command=self.saveRule)
        sousMenu.add_command(label='Export to png', command=self.export)


        # bouton de remise à zéros de la fourmis
        self.btRAZ =Button(self, text ='R.A.Z', width =10, command =self.RAZ, bg =bgColor, fg =textColor)
        val.bind_widget(widget =self.btRAZ, msg="Remise à zéros de la grille")
        self.btRAZ.grid(row =1, column =3, pady =5)

        # Création du label pour conter les étapes
        self.stepCounter =0
        self.LBstepCounter =Label(self, text ='Step: 0', bg =bgColor, fg =textColor)
        self.LBstepCounter.grid(row =1, column =1, columnspan =2)

        # Varialbes utiles a la gestion du programme
        self.runFlag =False

        # Création de la fourmis 
        self.antCanvas =LangtonAnt()
        self.antCanvas.grid(row =2, column =1, rowspan =8, columnspan =7, padx =5)
        
        # Création du bouton de démarrage de la fourmis
        self.BtStart =Button(self, text ='Start', command =self.start, width =10, bg =bgColor, fg =textColor)
        val.bind_widget(widget =self.BtStart, msg="Lancer l'algorithme")
        self.BtStart.grid(row =10, column =2, pady =5)

        #Création du bouton d'arrêt de la fourmis
        self.BtStop =Button(self, text ='Stop', command =self.stop, width =10, bg =bgColor, fg =textColor)
        self.BtStop.grid(row =10, column =3, pady =5)

        # Création du check button pour passer en mode pas à pas
        self.stepFlag =IntVar()
        self.CkStep =Checkbutton(self, variable =self.stepFlag, command =self.changeStepParam, width =3,
                                 bg =bgColor, fg =textColor)
        val.bind_widget(widget =self.CkStep, msg="Activer le mode pas à pas")
        self.CkStep.grid(row =10, column =4, pady =5)

        # Création du bouton pour le mode pas à pas
        self.BtStep =Button(self, text ="Step", state =DISABLED, command =self.move, width =10, bg =bgColor, fg =textColor)
        val.bind_widget(widget =self.BtStep, msg="Avancer d'une étape")
        self.BtStep.grid(row =10, column =5, pady =5)

        # Partie de la configuration des règles
        Label(self, text ="Rule configuration", bg =bgColor, fg =textColor).grid(row =1, column =7, columnspan =3)

        # Création pour enlever une règles
        self.BtLess =Button(self, text ='-', command =self.suppRule, bg =bgColor, fg =textColor)
        val.bind_widget(widget =self.BtLess, msg="Supprimer une règle")
        self.BtLess.grid(row =2, column =8)

        # Création de d'une zone de saisie pour modifier le nombre de règles
        self.LbNumberRule =Label(self, text ='2', width =10, bg =bgColor, fg =textColor)
        self.LbNumberRule.grid(row =2, column =9, padx =5)

        # Création du bouton pour ajouter une règle
        self.BtPlus =Button(self, text ='+', command =self.addRule, bg =bgColor, fg =textColor)
        val.bind_widget(widget =self.BtPlus, msg="Ajouter une règle")
        self.BtPlus.grid(row =2, column =10)

        # Bouton pour généré les boutons pour définir les règles
        self.BtGenerate =Button(self, text ='Generate', width =13, command =self.generateRule, bg =bgColor, fg =textColor)
        val.bind_widget(widget =self.BtGenerate, msg="Générer les règles")
        self.BtGenerate.grid(row =3, column =8, columnspan =3, padx =5, pady =5)

        # Création d'un label pour informé l'utilisateur de la mise à jour des règles
        self.LbRule =Label(self, text ='You can start', fg ='#3FFF00', bg =bgColor)
        self.LbRule.grid(row =10, column =8, columnspan =4, pady =5)

        # Scroll barre pour les widgets RuleWidget
        vsb = Scrollbar(self, orient=VERTICAL)
        vsb.grid(row=4, column=11, rowspan =5, sticky=N+S)

        # Canvas pour les widgets RuleWidget
        self.ruleCan =Canvas(self, yscrollcommand=vsb.set, width =130, height =300, bg =bgColor)
        self.ruleCan.grid(row =4, column =8, columnspan =3, rowspan =5)
        vsb.config(command=self.ruleCan.yview)

        # Frame pour les widgets RuleWidget
        self.ruleFrame =Frame(self.ruleCan)

        self.ruleList=[]    #liste pour contenir les paramètres des règles

        # Création de 2 RuleWidgets
        for i in range(0, 2):

            widget =RuleWidget(boss =self.ruleFrame, r =i, lb =self.LbRule)
            self.ruleList.append(widget)
        
        # Configuration du canvas
        self.ruleCan.create_window(0, 0,  window=self.ruleFrame)
        self.ruleFrame.update_idletasks()
        self.ruleCan.config(scrollregion=self.ruleCan.bbox("all"))

    def export(self):
        """Fonction qui ermet d'exporter l'image sur le canvas dans une image jpg"""

        # on demande a l'utilisateur l'emplacement du futur fichier
        filename =filedialog.asksaveasfilename(initialdir = "/",title = "Select file",
                                   filetypes = (("JPG Files","*.jpg"),("all files","*.*")))

        
        try:
            ext =filename.split('.')[1] # on récupère l'extension

            if ext != 'jpg':            # pour vérifier que c'est la bonne
                showerror('File extension error', 'Error file extension\nFile extension must be .jpg')
                return

        except: #si le fichier n'a pas d'extension on rajoute le jpg
            filename+='.jpg'

        try:
            t =self.antCanvas.canSize   # on récupère la taille du canvas

            image1 = Image.new("RGB", (t, t), '#5d5d5d')    # on crée une image RGB de la même taille du canvas avec une fond de couleur grise
            draw = ImageDraw.Draw(image1)   # on cré un dessin référencé a cette image

            t =self.antCanvas.cellSize  # on récupère la taille des cellules de lla fourmis

            # on parcours tous les points 
            for pts in self.antCanvas.passer:

                # on récupère les coordonées des points
                x =pts[0]
                y =pts[1]

                # on récupère la couleur de la cellule
                color =self.antCanvas.direction[self.antCanvas.etat[x][y]][0]

                # et on dessine la cellule
                draw.rectangle([x*t, y*t, (x+1)*t, (y+1)*t],
                                outline =color, fill =color)
            
            # on enregistre l'image dans le fdossier de destination
            image1.save(filename)

        except:
            showerror('File cannot open', 'Error file cannot open') # si le dossier ne peut pas être ouvert on l'indique
            return

        


    def saveRule(self):
        """Fonction qui permet de sauvegarder des règles de déplacement"""

        dir =[self.antCanvas.ddroite, self.antCanvas.dgauche]

        rule =[] #liste qui contient les règles
        
        # on parcours les RuleWidget
        for widget in self.ruleList:
            c, d =widget.getParam()     # on récupère la couleur et la direction
            l =[c, dir[d]]              # on insère dans une liste la couleur et la direction en fonction des variables de la foumris
            rule.append(l)              # on ajoute cette règles a la liste des règles


        # on demande à l'utilisateur le dossier de sauvegarde
        filename =filedialog.asksaveasfilename(initialdir = "/",title = "Select file",
                                   filetypes = (("Langton Ant files","*.ant"),("all files","*.*")))

        try:
            ext =filename.split('.')[1] # on récupère l'extension du fichier
                
            if ext != 'ant':    # pour vérifier si c'est la bonne extension
                showerror('File extension error', 'Error file extension\nFile extension must be .ant')
                return

        except:
            filename+='.ant'    # s'il n'y a pas d'extension on la rajoute

        try:
            # on écrit lezs règles dans le fichier
            file =open(filename, 'w')
            file.write(str(rule))
            file.close()

        except:
            # si on ne peut pas ouvrir on le signal
            showerror('File cannot open', 'Error file cannot open')
            return




    def chargeData(self):
        """ Fonction qui permet de charger des règles de déplacement"""
        
        # on demande le fichier de règles a charger à l'utilisateur
        filename =filedialog.askopenfilename(initialdir = "/",title = "Select file",
                                   filetypes = (("Langton Ant files","*.ant"),("all files","*.*")))

        try:
            ext =filename.split('.')[1] # on récupère l'extension

            if ext != 'ant':    # pour vérifier si c'est la bonne
                showerror('File extension error', 'Error file extension\nFile extension must be .ant')
                return
        except: # si le fichier n'a pas d'extension on ne peut rien faire
            showerror('File extension error', 'Error file extension\nFile extension must be .ant')
            return

        try:
            # on récupère les règles écrite dans le fichier
            file =open(filename, 'r')
            rule =eval(file.read())

            n =len(rule)    # on récupère le nombre de règles stocké

            l =self.ruleFrame.grid_slaves() # On récupère les widgets contenue dans ruleFrame
            for wi in l:
                wi.destroy()    # puis on les détruit

            self.ruleList =[]   # on remet à 0 la liste des règles

            for i in range(0, n):   # on parcours les règles récupérées dans le fichier pour créé les widget assosicés
                widget =RuleWidget(boss =self.ruleFrame, r =i, lb =self.LbRule) 
                self.ruleList.append(widget)

            for i in range(0, n):   # on paramètres les boutons et les combobox pour avoir les bonnes valeurs dedans
                # on change la couleur du bouton
                color =rule[i][0]

                self.ruleList[i].b.config(bg =color, activebackground =color)
        
                # si la couleur choisis est noire on met le texte en blanc
                if color == 'black' or color == '#000000':
                    self.ruleList[i].b.config(fg ='white')
                else:
                    self.ruleList[i].b.config(fg ='black')

                self.ruleList[i].direction.current(rule[i][1])
                self.ruleList[i].color =color



            self.LbNumberRule.config(text =str(len(self.ruleList))) # on met kle compteur de règles à jour

            self.generateRule() # puis on génère les règles





            # On met à jour le canvas
            self.ruleCan.create_window(0, 0,  window=self.ruleFrame)
            self.ruleFrame.update_idletasks()
            self.ruleCan.config(scrollregion=self.ruleCan.bbox("all"))
                

        except:
            showerror('File cannot open', 'Error file cannot open')
            return
        

    def changeStepParam(self):
        """Fonction qui permet de passer en mode pas à pas"""
        
        if self.stepFlag.get() == 1:
            self.BtStep.configure(state ='normal')
        else:
            self.BtStep.configure(state ='disabled')
            

    def RAZ(self):
        """Fonction qui permet de remettre le canvas de la fourmis a 0"""

        cellSize =self.antCanvas.cellSize
        self.stepCounter =0
        self.LBstepCounter.config(text ='Step: 0')

        self.antCanvas.Antx =self.antCanvas.cote//2
        self.antCanvas.Anty =self.antCanvas.cote//2

        for x in range(self.antCanvas.cote):
                for y in range(self.antCanvas.cote):
                    self.antCanvas.cell[x][y] =self.antCanvas.create_rectangle((x*cellSize, y*cellSize, (x+1)*cellSize, (y+1)*cellSize), 
                                                          outline ="#5d5d5d", fill ='#5d5d5d')
                    self.antCanvas.etat[x][y] =0

        

    def start(self):
        """Fonction qui permet de lancer la fourmis"""

        self.runFlag =True
        self.move()

    def move(self):
        """Fonction qui permet de calculer et d'afficher la prochaine étape de la fourmis"""

        self.antCanvas.calcul()                                           #on détermine la prochaine étape de la fourmis
        self.stepCounter +=1                                        #on incrémente de 1 le compteur d'étape
        self.LBstepCounter.config(text ='Step: '+str(self.stepCounter))   #on l'affiche

        if self.runFlag == True or self.antCanvas.outFlag == True:                    
            self.after(1, self.move)    #on continue la simulation
        else:
            None

    def stop(self):
        """Fonction qui permet d'arrêter la simulation"""

        self.runFlag =False
        self.move()


    def generateRule(self):
        """Génère les règle de déplacement de la fourmis"""

        dir =[self.antCanvas.ddroite, self.antCanvas.dgauche]

        rule =[] #liste qui contient les règles
        
        # on parcours les RuleWidget
        for widget in self.ruleList:
            c, d =widget.getParam()     # on récupère la couleur et la direction
            l =[c, dir[d]]              # on insère dans une liste la couleur et la direction en fonction des variables de la foumris
            rule.append(l)              # on ajoute cette règles a la liste des règles

        # on envoie la configuration dans la fourmis
        self.antCanvas.direction =rule
        
        self.LbRule.config(text ='You can start', fg ='#3FFF00')

        self.stop()
            

    def addRule(self):
        """Fonction qui permet d'ajouter un RuleWidget"""

        # Création d'un widget RuleWidget
        widget =RuleWidget(boss =self.ruleFrame, r =len(self.ruleList), lb =self.LbRule)
        self.ruleList.append(widget)
        
        # On met à jour le canvas
        self.ruleCan.create_window(0, 0,  window=self.ruleFrame)
        self.ruleFrame.update_idletasks()
        self.ruleCan.config(scrollregion=self.ruleCan.bbox("all"))

        # On met à jour le texte dans le zone de saisie
        n =len(self.ruleList)
        self.LbNumberRule.config(text =str(n))

        self.LbRule.config(text ='Rule are changed', fg ='#FF0000')


    def suppRule(self):
        """Fonction qui permet de supprimer un RuleWidget"""

        # On met à jour le texte dans le zone de saisie
        n =len(self.ruleList)

        if n == 2:  # On emp^che à l'utilisateur de descendre en dessous de 2 règles
            return 

        l =self.ruleFrame.grid_slaves() # On récupère les widgets contenue dans ruleFrame

        # On détruit le bouton et la combobox
        l[0].destroy()
        l[1].destroy()

        # On enlève le widget de la liste
        del(self.ruleList[-1])

        self.LbNumberRule.config(text =str(len(self.ruleList)))

        # On met à jour le Canvas
        self.ruleCan.create_window(0, 0,  window=self.ruleFrame)
        self.ruleFrame.update_idletasks()
        self.ruleCan.config(scrollregion=self.ruleCan.bbox("all"))

        self.LbRule.config(text ='Rule are changed', fg ='#FF0000')

        

if __name__ == '__main__':
    GUI().mainloop()