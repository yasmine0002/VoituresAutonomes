from random import randint
from time import sleep
from tkinter import Canvas, Tk
import platform

from random import choice, randint



from random import randint
from time import sleep
import time
from tkinter import Canvas, Tk
import platform

from random import choice, randint


dark_beige = "#B59D7B"
light_beige = "#F5DEB3"
dark_blue = "#00499F"


def valeur_dans_tableau(tableau, valeur):
    return valeur in tableau

def attribut_dans_tableau(tableau, valeur):
    for case in tableau :
        if(case.priorite == valeur):
            return True
    return False

def est_pair(valeur):
    return valeur%2 ==0

def enleve_valeur(tableau, valeur):
    if valeur in tableau:
        tableau.remove(valeur)

def tri_tableau(tableau):
    tableau.sort(key=lambda voiture: voiture.priorite)


class Cellule:
    def __init__(self, x, y, obstacle=True, est_libre=True):
        self.posx = x
        self.posy = y
        self.obstacle = obstacle
        self.est_libre = est_libre
        
    def isObstacle(self):
        return self.obstacle

    def setObstacle(self, obstacle):
        self.obstacle = obstacle

class Voie:
    def __init__(self, x, y, s, d):
        self.posx = x
        self.posy = y
        self.sens = s
        self.dir = d

    def getPosX(self):
        return self.posx

    def getPosY(self):
        return self.posy

    def getSens(self):
        return self.sens

    def getDir(self):
        return self.dir

class Intersection:
    def __init__(self, x, y):
        self.posx = x
        self.posy = y
        self.droite = Voie(x, y, 1, 1)
        self.gauche = Voie(x, y + 1, 1, -1)
        self.haut = Voie(x + 1, y, -1, 1)
        self.bas = Voie(x, y, -1, -1)
        self.conflit=Conflit(x, y)
        self.tampon=Tampon(x,y)

    def getVoieD(self):
        return self.droite

    def getVoieG(self):
        return self.gauche

    def getVoieH(self):
        return self.haut

    def getVoieB(self):
        return self.bas
    

class Conflit:
    def __init__(self, x, y):
        self.positions_en_conflit = self.initialiser_positions_en_conflit(x, y)

    def initialiser_positions_en_conflit(self, x, y):
        positions = []

        positions.append((x, y)) 
        positions.append((x+1, y))   
        positions.append((x, y+1))
        positions.append((x+1, y+1))
        return positions

    def estDansConflit(self, x, y):
        pos1_x, pos1_y = x, y

        if (pos1_x, pos1_y) in self.positions_en_conflit:
            return True
        return False


class Tampon:
    def __init__(self, x, y):
        self.positionEnTampon=self.initialisation(x,y)

    def initialisation(self, x, y):
        cases=[]
        cases.append((x, y-1))
        cases.append((x+1, y-1))
        cases.append((x-1, y))
        cases.append((x-1, y+1))
        cases.append((x, y+2))
        cases.append((x+1, y+2))
        cases.append((x+2, y))
        cases.append((x+2, y+1))
        return cases

    def estTampon(self, x, y):
        return (x,y) in self.positionEnTampon
    

class Grille:
    def __init__(self, x, y, nb_inter):
        self.largeur = x
        self.hauteur = y
        self.tab = [[Cellule(j, i) for j in range(x)] for i in range(y)]
        self.nb_inter=nb_inter
        self.intersections = []

    def getLargeur(self):
        return self.largeur

    def getHauteur(self):
        return self.hauteur

    def getIntersection(self,n):
        return self.intersections[n]
    
    def attriubueBoolVoie(self, voie):
        if voie.getSens() == 1:
            for a in range(self.largeur):
                if 0 <= voie.getPosY() < self.hauteur and 0 <= a < self.largeur:
                    self.tab[voie.getPosY()][a].setObstacle(False)

        if voie.getSens() == -1:
            for a in range(self.hauteur):
                if 0 <= voie.getPosX() < self.largeur and 0 <= a < self.hauteur:
                    self.tab[a][voie.getPosX()].setObstacle(False)

    def attriubueBoolIntersection(self, inter):
        self.attriubueBoolVoie(inter.getVoieD())
        self.attriubueBoolVoie(inter.getVoieG())
        self.attriubueBoolVoie(inter.getVoieH())
        self.attriubueBoolVoie(inter.getVoieB())

    def attriubueBoolToutesIntersection(self):
        for intersection in self.intersections:
            self.attriubueBoolIntersection(intersection)

    def estPosValide(self, x, y):
        return 0 <= x < self.largeur and 0 <= y < self.hauteur and not self.tab[y][x].isObstacle()

    def addIntersection(self, x, y):
        self.intersections.append(Intersection(x, y))
        self.attriubueBoolIntersection(self.intersections[-1])

    def addTouteIntersections(self):
        ratio_x = int(self.largeur/self.nb_inter)#distance en x entre chaque intersection
        ratio_y = int(self.hauteur/self.nb_inter)#idem y

        if(est_pair(self.nb_inter)):
            for i in range(1,self.nb_inter+1):
                for j in range(1, self.nb_inter+1):
                    self.addIntersection(ratio_x*i-int(ratio_x/2), ratio_y*j-int(ratio_y/2))
                    
        else :
            if(not(est_pair(int(ratio_x/2)))):
                 for i in range(1,self.nb_inter+1):
                    for j in range(1, self.nb_inter+1):
                        self.addIntersection(ratio_x*i-int(ratio_x/2)-1 , ratio_y*j-int(ratio_y/2)-1)

            else:
                 for i in range(1,self.nb_inter+1):
                    for j in range(1, self.nb_inter+1):
                        self.addIntersection(ratio_x*i-int(ratio_x/2), ratio_y*j-int(ratio_y/2))
                

    def est_position_tampon(self, x, y):
        for i in range(0, len(self.intersections)):
            if self.intersections[i].tampon.estTampon(x,y):
                return self.intersections[i].tampon.estTampon(x,y)
        return False

    def est_position_conflit(self, x, y):
        for i in range(0, len(self.intersections)):
            if self.intersections[i].conflit.estDansConflit(x,y):
                return self.intersections[i].conflit.estDansConflit(x,y)
        return False

    def est_position_piste(self, x, y):
        return(not (self.est_position_tampon(x,y) and self.est_position_conflit(x,y)))

    def affichage_precis_intersections(self):
        for i in range(0, len(self.intersections)):
            print("intersection ", i," : ", self.intersections[i].posx, "  ", self.intersections[i].posy)

    def position_dep(self):
        ratio_x = int(self.largeur/self.nb_inter)#distance en x entre chaque intersection
        ratio_y = int(self.hauteur/self.nb_inter)#idem y
        pos_dep = []

        if(not (est_pair(self.nb_inter))):
            if(not(est_pair(int(ratio_x/2)))):
                for i in range(1, self.nb_inter+1):
                    pos_dep.append((0, ratio_y*i-int(ratio_y/2), 2))
                    pos_dep.append((self.largeur-1, ratio_y*i-int(ratio_y/2)-1, 0))
                    pos_dep.append((ratio_x*i-int(ratio_x/2)-1, 0, 1))
                    pos_dep.append((ratio_x*i-int(ratio_x/2), self.hauteur-1, 3))
                return pos_dep
            else:
                for i in range(1, self.nb_inter+1):
                    pos_dep.append((0, ratio_y*i-int(ratio_y/2)+1, 2))
                    pos_dep.append((self.largeur-1, ratio_y*i-int(ratio_y/2), 0))
                    pos_dep.append((ratio_x*i-int(ratio_x/2), 0, 1))
                    pos_dep.append((ratio_x*i-int(ratio_x/2)+1, self.hauteur-1, 3))
                return pos_dep

        else:
                 if(est_pair(self.nb_inter)):
                     for i in range(1, self.nb_inter+1):
                        pos_dep.append((0, ratio_y*i-int(ratio_y/2)+1, 2))
                        pos_dep.append((self.largeur-1, ratio_y*i-int(ratio_y/2), 0))
                        pos_dep.append((ratio_x*i-int(ratio_x/2), 0, 1))
                        pos_dep.append((ratio_x*i-int(ratio_x/2)+1, self.hauteur-1, 3))
                     return pos_dep

    def appartient_grille(self, x, y):
        if(x>=0 and x< self.largeur and y>=0 and y < self.hauteur):
            return True
        return False
            

class Voiture:
    def __init__(self, x, y, ind, g, couleur='black'):
        self.posx = x
        self.posy = y
        self.ind_voie_dep = ind 
        self.priorite = ind 
        self.grille = g
        self.couleur = couleur
        self.a_traverse_conflit = False

    
    def getPosX(self):
        return self.posx

    def getPosY(self):
        return self.posy

    def approach_intersection(self, intersection):
        intersection.enter_intersection(self)

    def cross_intersection(self, intersection):
        intersection.exit_intersection(self)

    def avance(self):
        if(self.prochaine_case().est_libre):
            self.case_voiture().est_libre= True
            if self.ind_voie_dep == 0:
                self.posx -= 1 # vers la gauche
            elif self.ind_voie_dep == 1:
                self.posy += 1 # vers le haut
            elif self.ind_voie_dep == 2:
                self.posx += 1 # vers la droite
            elif self.ind_voie_dep == 3:
                self.posy -= 1  # vers le bas
            if(self.grille.estPosValide(self.posx,self.posy)):
                self.case_voiture().est_libre= False



    def wait(self, grille):
        self.posx =self.posx
        self.posy = self.posy
    
    def commencer_arret_automatique(self):
        self.en_arret_automatique = True

    def attendre_arret_automatique(self):
        if self.en_arret_automatique:
            self.wait(self.grille)
            self.en_arret_automatique = False

    def attribue_pos(self, g, x, y, ind):
        if(ind==0):
            return (g.largeur-1, y, ind)
        if(ind==1):
            return (x, 0, ind)
        if(ind==2):
            return (0, y, ind)
        if(ind==3):
            return (x, g.hauteur-1, ind)

    def case_voiture(self):
        return self.grille.tab[self.posy][self.posx]
        

    def prochaine_case(self):
        if(self.ind_voie_dep == 0):
            if (self.posx > 0):
                return self.grille.tab[self.posy][self.posx-1]
            else :
                return Cellule(-1,-1, True, True)
        if(self.ind_voie_dep == 1):
            if (self.posy < self.grille.hauteur -1):
                return self.grille.tab[self.posy+1][self.posx]
            else :
                return Cellule(-1,-1, True, True)
        if(self.ind_voie_dep == 2):
            if (self.posx < self.grille.largeur-1):
                return self.grille.tab[self.posy][self.posx+1]
            else :
                return Cellule(-1,-1, True, True)
        if(self.ind_voie_dep == 3):
            if (self.posy > 0):
                return self.grille.tab[self.posy-1][self.posx]
            else :
                return Cellule(-1,-1, True, True)


    def preced_case(self):
        if(self.ind_voie_dep == 0):
            if (self.posx > 0):
                return self.grille.tab[self.posy][self.posx+1]
            else :
                return Cellule(-1,-1, True, True)
        if(self.ind_voie_dep == 1):
            if (self.posy < self.grille.hauteur -1):
                return self.grille.tab[self.posy-1][self.posx]
            else :
                return Cellule(-1,-1, True, True)
        if(self.ind_voie_dep == 2):
            if (self.posx < self.grille.largeur-1):
                return self.grille.tab[self.posy][self.posx-1]
            else :
                return Cellule(-1,-1, True, True)
        if(self.ind_voie_dep == 3):
            if (self.posy > 0):
                return self.grille.tab[self.posy+1][self.posx]
            else :
                return Cellule(-1,-1, True, True)

    def quitte_grille(self):
        if(self.posx <0 or self.posx >= self.grille.largeur or self.posy <0 or self.posy >= self.grille.hauteur):
            return True
        return False

    def est_position_tampon(self):
        return self.grille.est_position_tampon(self.posx,self.posy)

    def est_position_conflit(self):
        return self.grille.est_position_conflit(self.posx,self.posy)


   
class Stockage :
    def __init__(self, jeu):
        self.jeu = jeu
        self.tableau = []

    def stock_voitures(self):
        for i in range (0, len(self.jeu.tampon)):
            for k in range (0, len(self.jeu.voitures)) :
                if(not(valeur_dans_tableau(self.tableau, self.jeu.voitures[k]))):
                    if(self.jeu.tampon[i].estTampon(self.jeu.voitures[k].posx, self.jeu.voitures[k].posy) and (not(valeur_dans_tableau(self.tableau, self.jeu.voitures[k]))))and ((self.jeu.voitures[k].grille.est_position_conflit(self.jeu.voitures[k].prochaine_case().posx, self.jeu.voitures[k].prochaine_case().posy)) or self.jeu.grille.intersections[i].conflit.estDansConflit(self.jeu.voitures[k].posx, self.jeu.voitures[k].posy)):
                        if (not self.jeu.voitures[k].a_traverse_conflit):
                            self.tableau.append(self.jeu.voitures[k])

    def quitte_zone_tampon(self, voiture):
        if(valeur_dans_tableau(self.tab, voiture) and (not (voiture.grille.est_position_tampon(voiture.posx, voiture.posy)))):
            self.tab.remove(voiture)
            voiture.a_traverse =False

    def affichage(self) :
        for case in self.tableau:
            print(case.ind_voie_dep,"  ")
        print(" ")



class FeuRouge:
    def __init__(self):
        self.actif = False
    def activer(self):
        self.actif = True
    def desactiver(self):
        self.actif = False     

    
        

class Jeu:
    def __init__(self, x, y, nb_inter):
        self.grille = Grille(x, y, nb_inter)
        self.tampon = []
        self.voitures = []
        self.stock = Stockage(self)
        self.feu_horizontal = FeuRouge()
        self.feu_vertical = FeuRouge()
        self.last_switch_time = time.time()  # Initialise le dernier temps de commutation à l'instant actuel



    def ajouter_voiture(self, x, y, ind, couleur):
        voiture = Voiture(x, y, ind, self.grille, couleur)
        voiture.case_voiture().est_libre= False
        self.voitures.append(voiture)

    def ajouter_tampon(self):
          for intersection in self.grille.intersections :
            self.tampon.append(Tampon(intersection.posx, intersection.posy))

    def occupe_case(self):
            for voiture in self.voitures :
                 if(self.grille.appartient_grille(voiture.posx, voiture.posy)):
                     voiture.case_voiture().est_libre= False

    def nb_cases_libres_dep(self):
        nb_cases=0
        for position in self.grille.position_dep() :
            x, y = position[0], position[1]
            if(self.grille.tab[y][x].est_libre):
                nb_cases=nb_cases+1
        return nb_cases


    def feu_rouge(self, voiture):

        #for intersection in self.grille.intersections:
        if self.feu_horizontal.actif:
                if valeur_dans_tableau(self.stock.tableau, voiture):
                    if voiture.ind_voie_dep==0 or  voiture.ind_voie_dep==2:
                        # if not self.grille.est_position_tampon(voiture.posx, voiture.posy):
                            voiture.avance()
                        #else: 
                        #    print('Oh oh je dois  attendre Horizontal')
        else: 
                if valeur_dans_tableau(self.stock.tableau, voiture):
                    if voiture.ind_voie_dep==1 or  voiture.ind_voie_dep==3:
                        #if not self.grille.est_position_tampon(voiture.posx, voiture.posy):
                            voiture.avance()
                        #else: 
                        #    print('Oh oh je dois  attendre Vertical')
        if(self.grille.est_position_conflit(voiture.posx, voiture.posy)):
            voiture.avance()
            voiture.a_traverse_conflit=True
        if(voiture.a_traverse_conflit==True):
            #je me prepare à faire la meme chose pour une autre intersection
            voiture.a_traverse = False

    def alterner_feux(self):
        current_time = time.time()
        # Vérifie si 5 secondes se sont écoulées depuis la dernière commutation des feux
        if current_time - self.last_switch_time >= 3:
            self.last_switch_time = current_time  # Met à jour le dernier temps de commutation
            if self.feu_horizontal.actif:
                self.feu_horizontal.desactiver()
                self.feu_vertical.activer()
            else:
                self.feu_horizontal.activer()
                self.feu_vertical.desactiver()

    def mouvAutoFeuRouge(self): #ajuster les cond 
        self.occupe_case()
        for voiture in self.voitures:
            if (self.grille.estPosValide(voiture.posx, voiture.posy)):
                #if (not(self.grille.est_position_tampon(voiture.posx,voiture.posy))):  #tant qu'on est pas dans tampon, on avance
                if (not(valeur_dans_tableau(self.stock.tableau, voiture))):####################################
                    if ((voiture.prochaine_case().est_libre) and (not voiture.grille.est_position_conflit(voiture.prochaine_case().posx, voiture.prochaine_case().posy))):
                        voiture.avance()
##
##                #debut du mouv intelligent
                #else:
                #    print("on est la")
                #    if(not voiture.a_traverse) : 
                #        self.mouv_intelligent_une_inter()
                #        return
                #    else :
                #        voiture.avance()

                else:
                    self.alterner_feux()
                    print("Allumer le feu")
                    if( not voiture.a_traverse_conflit) : 
                        self.feu_rouge(voiture)
                    else :
                        voiture.avance()


    def conflit_libre(self):
        for voiture in self.voitures :
            if ((voiture.posx, voiture.posy) in self.tampon):
                return False
        return True


    def parcour_conflit(self):
        voitures_passage = []

        if (self.stock.tableau[0].priorite ==0 or self.stock.tableau[0].priorite ==2):
            for voiture in self.stock.tableau :
                if(voiture.priorite ==0 or voiture.priorite ==2):
                    voitures_passage.append(voiture)
                
            for voiture in voitures_passage:
                if(not voiture.a_traverse_conflit):
                    if(voiture.grille.est_position_tampon(voiture.prochaine_case().posx, voiture.prochaine_case().posy)):
                        voiture.avance()
                    elif(voiture.grille.est_position_conflit(voiture.prochaine_case().posx, voiture.prochaine_case().posy)):
                        voiture.avance()
                        voiture.a_traverse_conflit =False

        elif (self.stock.tableau[0].priorite ==1 or self.stock.tableau[0].priorite ==3):
            for voiture in self.stock.tableau :
                if(voiture.priorite ==1 or voiture.priorite ==3):
                    voitures_passage.append(voiture)
        
            for voiture in voitures_passage:
                if(not voiture.a_traverse_conflit):
                    if(voiture.grille.est_position_tampon(voiture.prochaine_case().posx, voiture.prochaine_case().posy)):
                        voiture.avance()
                    elif(voiture.grille.est_position_conflit(voiture.prochaine_case().posx, voiture.prochaine_case().posy)):
                        voiture.avance()
                        voiture.a_traverse_conflit =False
        for tout in self.voitures:
            if(tout == voiture):
                voiture.a_traverse_conflit =True
                voiture.avance()
            else : 
                if (self.grille.estPosValide(tout.posx, tout.posy)):
                    if (not(valeur_dans_tableau(self.stock.tableau, tout))):
                        if ((tout.prochaine_case().est_libre) and (not tout.grille.est_position_conflit(tout.posx, tout.posy))):
                            tout.avance()
        

    def mouv_intelligent_une_inter(self):
        voitures_passage = []

        if (self.stock.tableau[0].priorite ==0 or self.stock.tableau[0].priorite ==2):
            for voiture in self.stock.tableau :
                if(voiture.priorite ==0 or voiture.priorite ==2):
                    voitures_passage.append(voiture)

        elif (self.stock.tableau[0].priorite ==1 or self.stock.tableau[0].priorite ==3):
            for voiture in self.stock.tableau :
                if(voiture.priorite ==1 or voiture.priorite ==3):
                    voitures_passage.append(voiture)

        self.stock.affichage()
        for voiture0 in voitures_passage :
            if(voiture0.a_traverse_conflit==False):
                if(voiture0.grille.est_position_tampon(voiture0.posx, voiture0.posy) and (not voiture0.grille.est_position_conflit(voiture0.posx, voiture0.posy)) and (not voiture0.a_traverse_conflit) and voiture0.grille.estPosValide(voiture0.posx, voiture0.posy)): #si on est les unique a etre dans tampon
                        voiture0.avance()

                        for voiture in self.voitures:
                            if(voiture == voiture0):
                                continue
                            else : 
                                if (self.grille.estPosValide(voiture.posx, voiture.posy)):
                                    if (not(valeur_dans_tableau(self.stock.tableau, voiture))):
                                        if ((voiture.prochaine_case().est_libre) and (not voiture.grille.est_position_conflit(voiture.posx, voiture.posy))):
                                            voiture.avance()
                        return

                if(voiture0.grille.est_position_conflit(voiture0.posx, voiture0.posy)):
                    if(voiture0.grille.est_position_conflit(voiture0.prochaine_case().posx,voiture0.prochaine_case().posy)):
                        voiture0.avance()
                        for voiture in self.voitures:
                            if(voiture == voiture0):
                                continue
                            else : 
                                if (self.grille.estPosValide(voiture.posx, voiture.posy)):
                                    if (not(valeur_dans_tableau(self.stock.tableau, voiture))):
                                        if ((voiture.prochaine_case().est_libre) and (not voiture.grille.est_position_conflit(voiture.posx, voiture.posy))):
                                            voiture.avance()
                        return
                    if(voiture0.grille.est_position_tampon(voiture0.prochaine_case().posx,voiture0.prochaine_case().posy)):
                        voiture0.a_traverse_conflit= True
                        voiture0.avance()
                        for voiture in self.voitures:
                            if(voiture == voiture0):
                                continue
                            else : 
                                if (self.grille.estPosValide(voiture.posx, voiture.posy)):
                                    if (not(valeur_dans_tableau(self.stock.tableau, voiture))):
                                        if ((voiture.prochaine_case().est_libre) and (not voiture.grille.est_position_conflit(voiture.posx, voiture.posy))):
                                            voiture.avance()
                        
            voiture0.a_traverse_conflit= False
            enleve_valeur(self.stock.tableau, voitures_passage[0])
            enleve_valeur(voitures_passage, voitures_passage[0])


    def voitures_dans_conflit(self):
        voitures_conflit = []
        for case in self.grille.intersections[0].conflit.positions_en_conflit:
            for voiture in self.voitures:
                if voiture.est_position_conflit():
                    voitures_conflit.append(voiture)
        return voitures_conflit
            
            
    def passage_libre(self, voiture):
        if(len(self.voitures_dans_conflit())>0):
            if (voiture.ind_voie_dep ==0 or voiture.ind_voie_dep ==2) :
                return (self.voitures_dans_conflit()[0].ind_voie_dep ==0 or self.voitures_dans_conflit()[0].ind_voie_dep ==2)
            elif (voiture.ind_voie_dep ==1 or voiture.ind_voie_dep ==3) :
                return (self.voitures_dans_conflit()[0].ind_voie_dep ==1 or self.voitures_dans_conflit()[0].ind_voie_dep ==3)
        else :
            return True
        

    def gestion_passage(self):
        passage_voiture02=[]
        passage_voiture13=[]

        for voiture in self.stock.tableau :   #on recupere les voitures en tampon 02
            if (voiture.priorite ==0 or voiture.priorite ==2):
                passage_voiture02.append(voiture)

        for voiture in self.stock.tableau :   #on recupere les voitures en tampon 13
            if (voiture.priorite ==1 or voiture.priorite ==3):
                passage_voiture13.append(voiture)

        if valeur_dans_tableau(passage_voiture02, self.stock.tableau[0]): #si la premiere voiture arrivee dans stock est 02, on fait passer toutes les voitures 02
            for voiture in passage_voiture02:
                if(voiture.a_traverse_conflit == False):
                    if self.passage_libre(voiture):
                        print("on est la")
                        voiture.avance()
                        if (voiture.grille.est_position_tampon(voiture.posx, voiture.posy) and voiture.grille.est_position_conflit(voiture.preced_case().posx, voiture.preced_case().posy)):
                            voiture.a_traverse_conflit =True

        elif valeur_dans_tableau(passage_voiture13, self.stock.tableau[0]): #si la premiere voiture arrivee dans stock est 02, on fait passer toutes les voitures 02
            for voiture in passage_voiture13:
                if(voiture.a_traverse_conflit == False):
                    if self.passage_libre(voiture):
                        voiture.avance()
                        if voiture.grille.est_position_tampon(voiture.posx, voiture.posy) and voiture.grille.est_position_conflit(voiture.preced_case().posx, voiture.preced_case().posy):
                            voiture.a_traverse_conflit =True
                            continue

        for voiture in self.voitures:
            if (valeur_dans_tableau(passage_voiture02, voiture) or valeur_dans_tableau(passage_voiture13, voiture)) and not voiture.a_traverse_conflit:
                enleve_valeur(passage_voiture02, voiture)
                enleve_valeur(passage_voiture13, voiture)
                enleve_valeur(self.stock.tableau, voiture)
                continue
            elif not (valeur_dans_tableau(passage_voiture02, voiture) or valeur_dans_tableau(passage_voiture13, voiture)):
                if self.grille.estPosValide(voiture.posx, voiture.posy):
                    voiture.avance()
        
        

    def mouvAutoIntelligent(self): 
        self.occupe_case()
        for voiture in self.voitures:
            if (self.grille.estPosValide(voiture.posx, voiture.posy)):
                if (not(valeur_dans_tableau(self.stock.tableau, voiture))) and voiture.a_traverse_conflit==False:
                        voiture.avance()
                else:
                    if(not voiture.a_traverse_conflit) and valeur_dans_tableau(self.stock.tableau, voiture) :
                       # tri_tableau(self.stock.tableau)
                        self.gestion_passage()
                        return             
                
    def stock_voitures(self):
        self.stock.stock_voitures()

    def waitAuto(self, voiture, grille): 
        voiture.wait()



#Vue___________________________________________________________________________________________________________
class GUIView:
    def __init__(self, root, grid_width, grid_height, title):
        self.root = root
        self.root.title(title)

        self.canvas = Canvas(root, width=grid_width * 20, height=grid_height * 20)
        self.canvas.pack()

    def draw_grid(self, grid):
        self.canvas.delete("all")

        for i in range(grid.getLargeur()):
            for j in range(grid.getHauteur()):
                if not grid.tab[j][i].isObstacle():
                    self.canvas.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill='white')
                else:
                    self.canvas.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill=dark_blue)

    def draw_cars(self, cars):
        for car in cars:
            self.canvas.create_rectangle(car.getPosX() * 20, car.getPosY() * 20, (car.getPosX() + 1) * 20,
                                         (car.getPosY() + 1) * 20, fill=car.couleur)


class GameController:
    def __init__(self):
        self.jeu = None
        self.view = None
        self.view1 = None
        

    def start_game(self, x, y, nb_inter): 
        self.jeu = Jeu(x, y, nb_inter)

        ratio_x = int(self.jeu.grille.largeur/self.jeu.grille.nb_inter)#distance en x entre chaque intersection
        ratio_y = int(self.jeu.grille.hauteur/self.jeu.grille.nb_inter)#idem y

        self.jeu.grille.addTouteIntersections()
            
        self.jeu.ajouter_tampon()

        self.jeu.stock_voitures()
        tri_tableau(self.jeu.stock.tableau)

        self.jeu.grille.affichage_precis_intersections()
        self.view = GUIView(Tk(), self.jeu.grille.getLargeur(), self.jeu.grille.getHauteur(), "Mirai Traffic Simulation : Feu Rouge")

        self.run_game()



    def run_game(self):
        while True:
            sleep(0.5)
            self.view.draw_grid(self.jeu.grille)
            self.jeu.occupe_case()
            
            #__________Fentre Mouvement Feu Rouge________##COMMENTER SI VOUS VOULEZ MOUVEMENT INTELLIGENT___________________________________________________________________________________________________
            #self.jeu.mouvAutoFeuRouge()
            
            #__________Fentre Mouvement Intelligent______##DECOMMENTER SI VOUS VOULEZ MOUVEMENT INTELLIGENT_____________________________________________________________________________________________________
            self.jeu.mouvAutoIntelligent()

            start_positions=self.jeu.grille.position_dep()

            if(self.jeu.nb_cases_libres_dep()>0):
                couleur_voiture = choice(['grey', 'blue', 'purple', 'brown', 'black'])  #couleur aléatoire
                ajout = choice(['0', '1'])# 50 pourcent de prob d'ajouter une voiture dans ce tour
                nb_voitures_fois = choice(['1', '1', '1', '2', '2', '3', '4'])#nb voiture ajoutees dans ce tour si ajoutees

                while(int(nb_voitures_fois)> self.jeu.nb_cases_libres_dep()):
                    nb_voitures_fois = choice(['1', '2']) #nb voiture ajoutees dans ce tour si ajoutees
                                    
                if(ajout[0]=='0'):            
                    for i in range(0,int(nb_voitures_fois)):
                        x, y, ind = choice(start_positions)
                        for i in range(0,4):#(not (self.jeu.grille.tab[y][x].est_libre)):
                            while(not (self.jeu.grille.tab[y][x].est_libre)): #and self.jeu.nb_cases_libres_dep()> 1):
                                print(self.jeu.nb_cases_libres_dep())
                                x, y, ind = choice(start_positions)
                        couleur_voiture = choice(['grey', 'blue', 'purple', 'brown', 'black'])  #couleur aléatoire
                        self.jeu.ajouter_voiture(x, y, ind, couleur_voiture)  #Ajout une nouvelle voiture à l'une des positions de départ possibles
            
            self.jeu.stock_voitures()

            self.view.draw_cars(self.jeu.voitures)
            
            self.view.root.update_idletasks()
            self.view.root.update()
            
            
            
def main():
    controller = GameController()
    controller.start_game(15,15,1)


    #pair impair -> pair    V   PARFAIT    
    #pair impair -> impair  V   PARFAIT      ---

    #pair pair -> impair  V PARFAIT
    #pair pair -> pair    NON mais ok voitures

if __name__ == "__main__":
    main()
