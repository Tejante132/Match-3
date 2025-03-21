# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"""
couleurs des cases dispo: jaune, rouge, vert, bleu, rose
"""


import random #pour random.choice(liste)

liste_couleurs= ['jaune','rouge','vert','bleu','rose']
orientation= ['haut','bas','gauche','droite']
grille= {"[0,0]":"case1", "[0,1]":"case2"}

"""
----------------------------------Classe Map--------------------------------------
"""
class Map():
    def __init__(self, liste_couleurs, dimensions, titre):
        self._liste_couleurs= list(liste_couleurs)
        self._dimensions= list(dimensions)
        self._titre=str(titre)
        
        



"""
----------------------------------Classe Grille--------------------------------------
"""

class Grille():
    def __init__(self, taille_grille, niveau_grille, dico_cases):
        self._taille= list(taille_grille)
        self._niveau= int(niveau_grille)
        self._contenu=dict(dico_cases) #dic: clé = [ligne, colonne], valeur= case
        
        
    #tous les get des attributs de la grille   
    def get_taille(self):
        return self._taille
    def get_niveau(self):
        return self._niveau
    def get_contenu(self):
        return self._contenu
         
        
    #definition REPR et STR    
    def affichage_grille(self):
        return "grille niveau {}, contenu:{}".format( self.get_niveau(), self.get_contenu())
    def __repr__(self):
        return self.affichage_grille()
    def __str__(self):
        return self.affichage_grille()
    
    
    
    
    
        
    #fonction qui detruit les cases normales, degele les cases gelees, juste avec leur position
    def activation(self, localisation):
        """
        argument: localisation d'une case sous forme [i,j]
        ---
        si case de classe Normale: l'explose
        si case de classe Gelee: la degele
        ---
        return: None
        """
        case= self[str(localisation)]
        if isinstance(case, Normale()):
            case.exploser_classique()
        elif isinstnace(case, Gelee()):
            case.degelage()
        
            
        
    
    
    
    #tester la validité et les effets dun swap, exploser des cases, creer des bonus...
    def test_swap(self, case):
        """
        argument: self, case où vient d'atterir l'element swapé
        ---
        teste si un pattern a ete formé
        (delfagrateur, bombe, missile, avion, combinaison classique)
        si oui, detruit les cases et rajoute le bonus
        si non, renvoie False
        """
        
        if isinstance(case, Normale()):
            [ie, je]= case.sa_position
            couleur= case.son_element.sa_couleur 
            swap_ok=False
            
            bonus= False
            
            
            #test deflagrateur
            #horizontal
            defl_h=0
        
            liste_voisins=[[ie, je-2], [ie, je-1],[ie, je+1],[ie, je+2]]
            for voisin in liste_voisins:
                if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                    if self[str(voisin)].son_element.sa_couleur==couleur:
                        defl_h+=1
            if defl_h==4:
                #exploser les 4 cases, placer un deflagrateur
                for voisin in liste_voisins:
                    self.activation(voisin)
                    self[str([ie,je])]=Deflagrateur
                    bonus=True
            
            if not bonus:
                
                #test deflagrateur
                #vertical
                defl_v=0
                liste_voisins=[[ie -2, je], [ie -1, je],[ie +1, je],[ie+2, je]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            defl_v+=1
                if defl_v==4:
                    #exploser les 4 cases, placer un deflagrateur
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self[str([ie,je])]=Deflagrateur    
                        bonus=True
                        
            if not bonus:        
                #test bombe
                #vertical
                bombe_v=0
                liste_voisins=[[ie, je-1],[ie, je+1]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            bombe_v+=1
                if bombe_v==2:
                    #bombe en T vertical, a voir si elle est à lendroit ou a lenvers
                    #testons si elle est en T inversé
                    bombe_vv=0
                    liste_voisins2=[[ie+1, je],[ie+2, je]]
                    for voisin in liste_voisins2:
                        if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                            if self[str(voisin)].son_element.sa_couleur==couleur:
                                bombe_vv+=1
                    if bombe_vv==2:
                        #bombe en T inversé 
                        for voisin in liste_voisins+liste_voisin2:
                            self.activation(voisin)
                            self[str([ie, je])]=Bombe
                            bonus=True
                    
                    else:
                        #testons si elle est en T à l'endroit
                        bombe_vv=0
                        liste_voisins2=[[ie-1, je],[ie-2, je]]
                        for voisin in liste_voisins2:
                            if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                                if self[str(voisin)].son_element.sa_couleur==couleur:
                                    bombe_vv+=1
                        if bombe_vv==2:
                            #bombe en T à l'endroit
                            for voisin in liste_voisins+liste_voisin2:
                                self.activation(voisin)
                                self[str([ie, je])]=Bombe
                                bonus=True
                                
            if not bonus:
                #test bombe
                #horizontal
                bombe_h=0
                liste_voisins=[[ie-1, je],[ie+1, je]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            bombe_h+=1
                if bombe_h==2:
                    #bombe en T horizontale, a voir si elle est à droite ou à gauche
                    #testons si elle est à droite
                    bombe_hh=0
                    liste_voisins2=[[ie, je+1],[ie, je+2]]
                    for voisin in liste_voisins2:
                        if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                            if self[str(voisin)].son_element.sa_couleur==couleur:
                                bombe_hh+=1
                    if bombe_hh==2:
                        #bombe horizontale à droite 
                        for voisin in liste_voisins+liste_voisin2:
                            self.activation(voisin)
                            self[str([ie, je])]=Bombe
                            Bonus=True
                    
                    else:
                        #testons si elle est à gauche 
                        bombe_hh=0
                        liste_voisins2=[[ie, je-1],[ie, je-2]]
                        for voisin in liste_voisins2:
                            if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                                if self[str(voisin)].son_element.sa_couleur==couleur:
                                    bombe_hh+=1
                        if bombe_hh==2:
                            #bombe horizontale à gauche
                            for voisin in liste_voisins+liste_voisin2:
                                self.activation(voisin)
                                self[str([ie, je])]=Bombe
                                Bonus=True
                                
            if not bonus:
                #Test missile 
                #horizontal
                # à droite
                missile_h=0
                liste_voisins=[[ie, je-1], [ie, je+1],[ie, je+2]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            missile_h+=1
                if missile_h==3:
                    #missile horizontal à droite
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self[str([ie,je])]=Roquette('H')
                        bonus=True
                #à gauche
            if not bonus:
                missile_h=0
                liste_voisins=[[ie, je-1], [ie, je+1],[ie, je-2]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            missile_h+=1
                if missile_h==3:
                    #missile horizontal à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.activation([ie, je])
                        self[str([ie,je-1])]=Roquette('H')
                        bonus=True
                        
                #vertical
                # en haut
            if not Bonus:
                missile_v=0
                liste_voisins=[[ie-1, je], [ie+1, je],[ie-2, je]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            missile_v+=1
                if missile_v==3:
                    #missile vertical en haut
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self[str([ie,je])]=Roquette('V')
                        bonus=True
                #en bas
            if not Bonus:
                missile_v=0
                liste_voisins=[[ie-2, je], [ie-1, je],[ie+1, je]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale()) or isinstance(voisin, Gelee()):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            missile_v+=1
                if missile_v==3:
                    #missile horizontal à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.activation([ie, je])
                        self[str([ie-1,je])]=Roquette('V')
                        bonus=True
                        
                    #finir code avion et 3-swap



            


            

                    
              

                    
        
"""
----------------------------------Classe Case et ses filles----------------------------
"""  
        
        
class Case():
    def __init__(self, position_case):
        self._position= list(position_case)
        
    def get_position(self):
        return self._position
    
    sa_position= property(get_position)
    
    #affichage
    def affichage_case(self):
        return 'case, position: {}'.format(self._position)
    def __repr__(self):
        return self.affichage_case()
    def __str__(self):
        return self.affichage_case()
    
            
    
"""
----------------------------------Classe Vide---------
"""
    
class Vide(Case):
    def __init__(self, position_case):
        super().__init__(position_case) 

    
    
    def affichage_vide(self):
        return 'case vide, position{}'.format(self.sa_position)
    def __repr__(self):
        return self.affichage_vide()
    def __str__(self):
        return self.affichage_vide()
    
"""
----------------------------------Classe Gelee---------
"""
    
    
class Gelee(Case):
    def __init__(self, niveau_gel, element_case, position_case, orientation_case):
        super().__init__(position_case)
        self._niveau_gel=int(niveau_gel)
        self._element= str(element_case)
        self._orientation= str(orientation_case)
        
    #property niveau gel   
    def get_niveau_gel(self):
        return self._niveau_gel   
    def set_niveau_gel(self, new_niveau_gel):
        if new_niveau_gel in [0,1,2,3]:
            self._niveau_gel=new_niveau_gel
            
    son_niveau=property(get_niveau_gel, set_niveau_gel)     
            
    #property orientation
    def get_orientation(self):
        return self._orientation
    son_orientation=property(get_orientation)
     
        
       
    def degelage(self):
        """
        argument:self
        ---
        enleve 1 niveau de gel à une case gelée,
        si la case gelée atteint le niveau 0, la detruit et met une case Normale à la place
        ---
        return: None
        """
        if self.son_niveau>1:
            ancien_niveau=self.son_niveau
            self.son_niveau=ancien_niveau -1
        elif self.son_niveau==1:
            #detruire l'element gelee et le remplacer par normale, au mm endroit.
            new_case= Normale(self.son_orientation, self.sa_position, self.son_element, False, False)
            grille[str(self.sa_position)]=new_case
            
       
    # propriete element
    def get_element(self):
        return self._element  
    def set_element(self, new_element):
        if isinstance(new_element, Element):
            self._element=new_element            
    son_element=property(get_element, set_element)
    
    #affichage
    def affichage_gelee(self):
        return 'case gelee, niveau: {}, position: {}, element contenu:{}'.format(self.get_niveau_gel(), self.get_position(), self.get_element())
    def __repr__(self):
        return self.affichage_gelee()
    def __str__(self):
        return self.affichage_gelee()
    
    
        
"""
----------------------------------Classe Normale---------
"""       
        
        
        
        
        
class Normale(Case):
    def __init__(self, orientation_case, position_case, element_case, est_une_source_case, est_un_puits_case):
        super().__init__(position_case)
        self._orientation=str(orientation_case) #coordonnées de la case vers qui le flux va 
        self._element= element_case
        self._est_une_source= bool
        self._est_un_puits=bool
        self._est_vide= False
      
    #property element
    def get_element(self):
        return self._element
    def set_element(self, new_element):
        if isinstance(new_element, Element):
            self._element=new_element       
    son_element=property(get_element, set_element)
    

    def get_orientation(self):
        return self._orientation
    def get_est_une_source(self):
        return self._est_une_source
    def get_est_un_puit(self):
        return self._est_un_puit
    
    #property est_vide
    def get_est_vide(self):
        return self._est_vide()
    def set_est_vide(self, arg):
        if isinstance(arg, bool):
            self._est_vide=arg
    son_est_vide= property(get_est_vide, set_est_vide)
    
    
    #affichage
    def affichage_normale(self):
        return 'case normale, position:{}, element contenu:{}, orientation:{}'.format(self.get_position(), self.get_element(), self.get_orientation())
    def __repr__(self):
        return self.affichage_normale()
    def __str__(self):
        return self.affichage_normale()
    
    
    def generer_classique(self):
         assert self.get_est_une_source()
         assert self.get_est_vide()
         couleur= random.choice(liste_couleurs)
         self.son_element=Classique(couleur)
         
    def exploser_classique(self):
        assert not (self.get_est_vide())
        self.son_element=None
        self.son_est_vide= True 
        
    
    def donner_element(self, grille):
        #trouver les coordonnees de la case alimentée
        if self.get_orientation()=='haut':
            case_alimentee= [self.sa_position[0] -1, self.sa_position[1]]
        elif self.get_orientation()=='bas':
            case_alimentee= [self.sa_position[0] +1, self.sa_position[1]]
        elif self.get_orientation()=='droite':
            case_alimentee= [self.sa_position[0], self.sa_position[1] +1]
        elif self.get_orientation()=='haut':
            case_alimentee= [self.sa_position[0], self.sa_position[1] -1]
        #retrouver cette case dans la grille
        assert isinstance(grille, Grille())
        #donner l'element
        case_alimentee=grille.get_contenu[case_alimentee] #on obtient la case alimentée
        assert isinstance(case_alimentee, Normale())
        assert case_alimentee.get_est_vide()
        case_alimentee.son_element=self.son_element
        case_alimentee.son_est_vide=False
        #dire que la case est vide
        self.son_element=None
        self.son_est_vide=True
        
        
            
    
        
"""
----------------------------------Classe Element et ses filles----------------------------
"""  
    
    
class Element():
    pass


"""
----------------------------------Classe Classique---------
"""



class Classique(Element):
    def __init__(self, couleur):
        self._couleur= str(couleur)
    
    #property
    def get_couleur(self):
        return self._couleur
    def set_couleur(self, new_couleur):
        if new_couleur in liste_couleurs:
            self._couleur=new_couleur
            
    sa_couleur=property(get_couleur, set_couleur)
    
     #affichage  
    def affichage_classique(self):
         return 'element classique {}'.format(self.get_couleur())
    def __repr__(self):
         return self.affichage_classique()
    def __str__(self):
         return self.affichage_classique()
     
        
     
     
#----------------------------------Classe Bonus---------   

class Bonus(Element):
    
    
    def __repr__(self):
        return "Bonus"
    def __str__(self):
        return "Bonus"

class Bombe(Bonus):
    
    def __repr__(self):
        return "Bombe"
    def __str__(self):
        return "Bombe"
    
    

class Roquette(Bonus):
    def __init__(self, direction):
        self.__direction= str(direction)
        
    def __repr__(self):
        return "Roquette {}".format(self.__direction)
    def __str__(self):
        return "Roquette {}".format(self.__direction)

class Avion(Bonus):
    
    def __repr__(self):
        return "Avion"
    def __str__(self):
        return "Avion"


class Deflagrateur(Bonus):

    def __repr__(self):
        return "Deflagrateur"
    def __str__(self):
        return "Deflagrateur"




    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
