# -*- coding: utf-8 -*-
"""
GUILBERT Eva
GUYARD-GILLES Clotilde

                    MINI POO : Jeu Match-3
                    

couleurs des cases dispo: jaune, rouge, vert, bleu, rose

EVA ATTENDS QUE JE MODIFIE 2-3 TRUCS AVANT D'AVANCER STP


"""


import tkinter as TK
import tkinter.ttk as TTK
import tkinter.filedialog as TKFD

import random #pour random.choice(liste)
import xml.etree.ElementTree as ET


#arbreXML = ET.parse("//Users//Eva//Desktop//Niveau1 - Reconnaissance de bonus.xml")
#arbreXML = ET.parse("C:\\Users\\strel\\OneDrive\\Desktop\Arts et Métiers\\1ère Année\\GIE 1\\Projet POO\\Niveaux\\Niveau1.1 - Activation des bonus.xml")

#arbreXML = ET.parse("//Users//Eva//Desktop//Niveau1 - Reconnaissance de bonus.xml")

#ArbreXML selon le niveau
#arbreXML = ET.parse("C:\\Users\\Clotilde\\OneDrive - ensam.eu\\MINI POO\\Données test (XML)\\Niveaux\\Niveau1 - Reconnaissance de bonus.xml")
#arbreXML = ET.parse("C:\\Users\\Clotilde\\OneDrive - ensam.eu\\MINI POO\\Données test (XML)\\Niveaux\\Niveau1.1 - Activation des bonus.xml")
arbreXML = ET.parse("C:\\Users\\Clotilde\\OneDrive - ensam.eu\\MINI POO\\Données test (XML)\\Niveaux\\Niveau2 - Introduction des cellules gelees.xml")
#arbreXML = ET.parse("C:\\Users\\Clotilde\\OneDrive - ensam.eu\\MINI POO\\Données test (XML)\\Niveaux\\Niveau3 - Introduction des cellules vides.xml")
#arbreXML = ET.parse("C:\\Users\\Clotilde\\OneDrive - ensam.eu\\MINI POO\\Données test (XML)\\Niveaux\\Niveau4 V1.3 - Carte non convexe + introduction des étoiles.xml")

tronc = arbreXML.getroot()

liste_couleurs= ["green", "red", "yellow", "blue", "magenta"]

orientations= ['Haut','Bas','Gauche','Droite']


#----------------------------Instanciation de compteurs--------------------------------
#pour le suivi des objectifs

#nombres d'éléments détruits de chaque couleur
#nombre de bonus activés
#nombre d'étoiles dans des puits
compteur = {"green" : 0, "magenta" : 0, "red" : 0, "yellow" : 0, "blue" : 0, "Etoiles" : 0, "Bonus" : 0, "coups" : 0}
#les clés correspondent à l'attribut "cible" des objectifs



#----------------------------------Classe Map--------------------------------------

class Map():
    def __init__(self, ma_liste_couleurs, mes_dimensions, mon_titre, mon_nb_coups):
        self._liste_couleurs= ma_liste_couleurs
        self._dimensions= list(mes_dimensions)
        self._titre=str(mon_titre)
        self._objectifs = []       #liste qui recevra les objectifs
        self._nb_coups = int(mon_nb_coups)
        self._grille = Grille()
        self._coups_restants = int(mon_nb_coups)
        
    def _get_grille(self):
        return self._grille
    sa_grille = property(_get_grille)
        
    def _get_nb_coups(self):
        return self._nb_coups
    son_nb_coups = property(_get_nb_coups)
    
    
    def _get_coups_restants(self):
        return self._coups_restants
    def _set_coups_restants(self,new_quantite):
        assert type(new_quantite) == int or type(new_quantite) == float
        self._coups_restants = int(new_quantite)
    ses_coups_restants = property(_get_coups_restants, _set_coups_restants)
    
    def maj_coups_restants(self):
        self.ses_coups_restants = self.son_nb_coups - compteur.get("coups")
        
    def add_objectif(self,objectif):
        if isinstance(objectif,Objectif):
            self._objectifs += [objectif]
            
    def _get_objectifs(self):
        return self._objectifs
    ses_objectifs = property(_get_objectifs)
    
    def _get_liste_couleurs(self):
        return self._liste_couleurs
    sa_liste_couleurs = property(_get_liste_couleurs)
    
    def _get_titre(self):
        return self._titre
    son_titre = property(_get_titre)
    
    def _get_dimensions(self):
        return self._dimensions
    ses_dimensions = property(_get_dimensions)
        
    def __repr__(self):
        return "Map \"{}\", de dimensions {}, contenant les couleurs {}".format(self.son_titre,self.ses_dimensions,str(self.sa_liste_couleurs))



#----------------------------------Classe Objectifs---------------------------------------
#à la fin de chaque tour de jeu, il faut mettre à jour les quantites restantes de tous les objectifs


##instanciation
class Objectif():
    def __init__(self,ma_cible,ma_quantite):
        self._cible = str(ma_cible)
        self._quantite = int(ma_quantite)
        self._quantite_restante = int(ma_quantite)
        
    def _get_cible(self):
        return self._cible
    sa_cible = property(_get_cible)
    
    def _get_quantite(self):
        return self._quantite
    sa_quantite = property(_get_quantite)
    
    def _get_quantite_restante(self):
        return self._quantite_restante
    def _set_quantite_restante(self,new_quantite):
        assert type(new_quantite) == int or type(new_quantite) == float
        self._quantite_restante = int(new_quantite)
    sa_quantite_restante = property(_get_quantite_restante, _set_quantite_restante)
    
    def maj_quantite_restante(self):
        self.sa_quantite_restante = self.sa_quantite - compteur.get(self.sa_cible)
    
        
    def affichage(self):
        if self._cible in la_map.sa_liste_couleurs:
            return "Eléments de couleur {} à détruire:".format(self.sa_cible)
        elif self._cible == "Bonus":
            return "Bonus à détruire :"
        else:
            return "Etoiles à détruire :"
    def __repr__(self):
        return self.affichage()
    def __str__(self):
        return self.affichage()
    



#----------------------------------Classe Grille----------------------------------------

class Grille():
    def __init__(self):
        self._dico_cases = {}       #dico qui contiendra en clé une postion sous le forme "[i,j]"
                                    #et en argument une case
                                    
    def _get_cases(self):
        return self._dico_cases.values()
    ses_cases = property(_get_cases)
                                    
    def add_case(self,ma_case):
        if isinstance(ma_case,Case):
            self._dico_cases[str(ma_case.sa_position)]=ma_case
            
    def retourner_case(self,coordonnees):
        """
        entrée : coordonnées d'une case au format [i,j] avec i la ligne et j la colonne
        sortie : case se trouvant aux coordonnées [i,j] dans la grille
        """
        assert type(coordonnees)==list, "Donner la localisation de la case sous format [i,j] avec i la ligne et j la colonne"
        return self._dico_cases.get(str(coordonnees))
    
    def ajouter_bonus(self, coordonnees, bonus):
        """
        arguments: self, position de la case dont l'element va etre changé, nouveau bonus
        ----------
        coordonnees : [i,j] avec i la ligne et j la colonne
        bonus: type Bonus

        return: none
        -------
        met un bonus dans la case
        """
        if isinstance(self.retourner_case(coordonnees), Normale) or isinstance(self.retourner_case(coordonnees), Gelee):
            if isinstance(bonus, Bonus):
                self.retourner_case(coordonnees).son_element=bonus
         
    #definition REPR et STR    
    def affichage_grille(self):
        return "grille"
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
        case= self.retourner_case(localisation)
        if isinstance(case, Normale):
            case.exploser_classique()
        elif isinstance(case, Gelee):
            case.degelage()
                   
    def exploser_bonus(self, localisation):
        """
        Parameters
        localisation de la case contenant l'element bonus'
        localisation : list
            fait exploser le bonus selon son type, en detruisant les elements des cases voisines
        si le bonus est un deflagrateur et qu'on l'a activé en le swappant, NE PAS UTILISER CETTE FONCTION
        UTILISER exploser_deflagrateur(self, localisation, case_swappee)
        Returns
        -------
        None.

        """
        case=self.retourner_case(localisation)
        bonus=case.son_element
        ib, jb=localisation[0], localisation[1]
        im, jm=la_map.ses_dimensions[0], la_map.ses_dimensions[1]
        
        if isinstance(bonus,Bonus):
            #bombe
            cases_explosees=[[ib, jb-2],[ib, jb-1],[ib, jb+1],[ib, jb+1],[ib-2, jb],[ib-1, jb],[ib+1, jb],[ib+2, jb],[ib-1, jb-1],[ib-1, jb+1],[ib+1, jb-1],[ib+1, jb+1]]
            for case in cases_explosees:
                #on explose les cases, si elles ne sont pas de classe Vide
                if isinstance(self.retourner_case(case), Non_Vide):
                    if isinstance(self.retourner_case(case).son_element, Classique):
                        self.activation(case)
                    elif isinstance(self.retourner_case(case).son_element, Bonus):
                        self.exploser_bonus(case)       #un bonus peut en faire exploser d'autres
                            
        if isinstance(bonus, Roquette):
            #roquette
            if bonus.sa_direction=='H':
                #detruire toute sa ligne
                cases_explosees=[]
                for j in range (0,jm):
                    cases_explosees.append([ib,j])
                for case in cases_explosees:
                    #on explose les cases, si elles ne sont pas de classe Vide
                    if isinstance(self.retourner_case(case), Non_Vide):
                        if isinstance(self.retourner_case(case).son_element, Classique):
                            self.activation(case)
                        elif isinstance(self.retourner_case(case).son_element, Bonus):
                            self.exploser_bonus(case)
            #roquette
            if bonus.sa_direction=='V':
                #detruire toute sa colonne
                cases_explosees=[]
                for i in range (0,im):
                    cases_explosees.append([i, jb])
                for case in cases_explosees:
                    #on explose les cases, si elles ne sont pas de classe Vide
                    if isinstance(self.retourner_case(case), Non_Vide):
                        if isinstance(self.retourner_case(case).son_element, Classique):
                            self.activation(case)
                        elif isinstance(self.retourner_case(case).son_element, Bonus):
                            self.exploser_bonus(case)
         
        if isinstance(bonus, Avion):
            #avion
            #detruire 4 cases adjacentes
            cases_explosees=[[ib, jb-2],[ib, jb-1],[ib, jb+1],[ib, jb+2]]
            for case in cases_explosees:
                #on explose les cases, si elles ne sont pas de classe Vide
                if isinstance(self.retourner_case(case), Non_Vide):
                    if isinstance(self.retourner_case(case).son_element, Classique):
                        self.activation(case)
                    elif isinstance(self.retourner_case(case).son_element, Bonus):
                        self.exploser_bonus(case)
            #detruire un objectif 
            "jsp comment faire"
            #detruire une case au hasard
            """jsp comment faire, genre...
            ir, jr=randint(0,im), randint(0, jm)
            if isinstance(self.retourner_case([ir,jr]), Non_Vide):
                while not isinstance(self.retourner_case([ir, jr]).son_element, Classique):
                    ir, jr=randint(0,im), randint(0, jm)
            self.activation([ir, jr])
            """
            
        if isinstance(bonus, Deflagrateur):     #si le deflagrateur à ete activé en le swappant,NE PAS UTILISER CETTE FONCTION
            #deflagrateur
            #trouver une couleur dans les cases adjacentes
            cases_adjacentes=[[ib+1,jb+1],[ib+1,jb-1],[ib-1,jb-1],[ib-1,jb+1]] 
            couleurs_adjacentes=[]
            for case in cases_adjacentes:
                if isinstance(self.retourner_case(case), Non_Vide) and isinstance(self.retourner_case(case).son_element, Classique):
                    couleurs_adjacentes.append(self.retourner_case(case).son_element)
            if couleurs_adjacentes!=[]:
                couleur=random.choice(couleurs_adjacentes)
            else: 
                couleur=random.choice(liste_couleurs)
            #exploser toutes les cases de cette couleur
            for i in range (0,im):
                for j in range (0,jm):
                    if isinstance(self.retourner_case([i,j]), Non_Vide):
                        if self.retourner_case([i,j]).son_element==str(couleur):
                            self.activation([i,j])
                            
        self.retourner_case([ib,jb]).son_element=Element_None()
                            
    
    def exploser_deflagrateur(self, localisation_deflag, localisation_case):
        """

        Parameters
        ----------
        localisation_deflag :  [i,j]
            localisation du deflagrateur apres qu'il ait été swappé
        localisation_case : [i,j]
            localisation de la case avec laquelle le deflagrateur a été swappé
        fonction à utiliser lorsque le deflagrateur est swappé
        explose le deflagrateur et explose tous les éléments de la meme couleur que l'élément swappé        

        Returns
        -------
        None.

        """
        case_deflag=self.retourner_case(localisation_deflag)
        case_swap=self.retourner_case(localisation_case)
        im, jm= la_map.ses_dimensions[0], la_map.ses_dimensions[1]
        if isinstance(case_deflag.son_element, Deflagrateur) and isinstance(case_swap.son_element, Classique):
            compteur["Bonus"] += 1      #activation d'un bonus supplémentaire
            #deflagrateur
            #trouver une couleur dans les cases adjacentes
            couleur=case_swap.son_element
            #exploser toutes les cases de cette couleur
            for i in range (0,im):
                for j in range (0,jm):
                    if isinstance(self.retourner_case([i,j]), Non_Vide):
                        if self.retourner_case([i,j]).son_element==couleur:
                            self.activation([i,j])

                    
                      
                
        
    
    #tester la validité et les effets dun swap, exploser des cases, creer des bonus...
    def test_swap_classique(self, case):
        """
        argument: self, case contenant un element classique où vient d'atterir l'element swapé
        ---
        teste si un pattern a ete formé
        (delfagrateur, bombe, missile, avion, combinaison classique)
        si oui, detruit les cases et rajoute le bonus, renvoie True
        si non, renvoie False
        la variable booleenne bonus est False à l'origine, passe à True si il y a un pattern(meme un match3)
        si bonus ==True: on arrive quasi-direct à la fin
        """
        
        if isinstance(case, Normale):
            [ie, je]= case.sa_position 
            bonus= False
            
            
            #test deflagrateur
            #horizontal
        
            liste_voisins=[[ie, je],[ie, je-2], [ie, je-1],[ie, je+1],[ie, je+2]]
            if self.test_meme_couleur(liste_voisins):                #exploser les 4 cases, placer un deflagrateur
                for voisin in liste_voisins:        #coordonnées dans list de coord
                    self.activation(voisin)         #explose les cases Normales, degele les cases Gelees
                    self.ajouter_bonus([ie, je], Deflagrateur())    
                    bonus=True
            
            if not bonus:
                
                #test deflagrateur
                #vertical
                liste_voisins=[[ie ,je],[ie -2, je], [ie -1, je],[ie +1, je],[ie+2, je]]
                if self.test_meme_couleur(liste_voisins):               #exploser les 4 cases, placer un deflagrateur
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.ajouter_bonus([ie, je], Deflagrateur())
                        bonus=True
                        
            if not bonus:        
                #test bombe
                #vertical
                liste_voisins=[[ie, je],[ie, je-1],[ie, je+1]]
                if self.test_meme_couleur(liste_voisins):               #bombe en T vertical, a voir si elle est à lendroit ou a lenvers
                    #testons si elle est en T inversé
                    liste_voisins2=[[ie+1, je],[ie+2, je]]
                    if self.test_meme_couleur(liste_voisins2):                     #bombe en T inversé 
                        for voisin in liste_voisins+liste_voisins2:
                            self.activation(voisin)
                            self.ajouter_bonus([ie, je], Bombe())
                            bonus=True
                    
                    else:
                        #testons si elle est en T à l'endroit
                        liste_voisins2=[[ie, je],[ie-1, je],[ie-2, je]]
                        if self.test_meme_couleur(liste_voisins2):                 #bombe en T à l'endroit
                            for voisin in liste_voisins+liste_voisins2:
                                self.activation(voisin)
                                self.ajouter_bonus([ie, je], Bombe())
                                bonus=True
                                
            if not bonus:
                #test bombe
                #horizontal
                liste_voisins=[[ie, je],[ie-1, je],[ie+1, je]]
                if self.test_meme_couleur(liste_voisins):                  #bombe en T horizontale, a voir si elle est à droite ou à gauche
                    #testons si elle est à droite
                    liste_voisins2=[[ie, je],[ie, je+1],[ie, je+2]]
                    if self.test_meme_couleur(liste_voisins2):                    #bombe horizontale à droite 
                        for voisin in liste_voisins+liste_voisins2:
                            self.activation(voisin)
                            self.ajouter_bonus([ie, je], Bombe())
                            bonus=True
                    
                    else:
                        #testons si elle est à gauche 
                        liste_voisins2=[[ie, je],[ie, je-1],[ie, je-2]]
                        if self.test_meme_couleur(liste_voisins2):               #bombe horizontale à gauche
                            for voisin in liste_voisins+liste_voisins2:
                                self.activation(voisin)
                                self.ajouter_bonus([ie, je], Bombe())
                                bonus=True
                                
            if not bonus:
                #Test missile 
                #horizontal
                # à droite
                liste_voisins=[[ie, je],[ie, je-1], [ie, je+1],[ie, je+2]]
                if self.test_meme_couleur(liste_voisins):                    #missile horizontal à droite
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.ajouter_bonus([ie,je], Roquette('V'))
                        bonus=True
                #à gauche
            if not bonus:
                liste_voisins=[[ie, je],[ie, je-1], [ie, je+1],[ie, je-2]]
                if self.test_meme_couleur(liste_voisins):                    #missile horizontal à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.ajouter_bonus([ie,je-1], Roquette('V'))
                        bonus=True
                        
                #vertical
                # en haut
            if not bonus:
                liste_voisins=[[ie, je],[ie-1, je], [ie+1, je],[ie-2, je]]
                if self.test_meme_couleur(liste_voisins):                  #missile vertical en haut
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.ajouter_bonus([ie, je], Roquette('H'))
                        bonus=True
                #en bas
            if not bonus:
                liste_voisins=[[ie, je],[ie-2, je], [ie-1, je],[ie+1, je]]
                if self.test_meme_couleur(liste_voisins):                #missile horizontal à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.ajouter_bonus([ie-1 ,je], Roquette('V'))
                        bonus=True
                        
            #test avion
            #case en haut à gauche
            if not bonus:
                liste_voisins=[[ie, je],[ie+1, je],[ie+1, je+1],[ie, je+1]]
                if self.test_meme_couleur(liste_voisins):                #avion en haut à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.ajouter_bonus([ie, je], Avion())
                        bonus=True
                        
            #case en bas à gauche
            if not bonus:
                liste_voisins=[[ie, je],[ie-1, je],[ie-1, je+1],[ie, je+1]]
                if self.test_meme_couleur(liste_voisins):        #avion en haut à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.ajouter_bonus([ie-1, je], Avion())
                        bonus=True
                        
            #case en haut à droite        
            if not bonus:     
                liste_voisins=[[ie, je],[ie, je-1],[ie+1, je-1],[ie+1, je]]
                if self.test_meme_couleur(liste_voisins):     #avion en haut à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.ajouter_bonus([ie, je-1], Avion())
                        bonus=True

            #case en bas à droite        
            if not bonus:     
                liste_voisins=[[ie, je],[ie-1, je],[ie-1, je-1],[ie, je-1]]
                if self.test_meme_couleur(liste_voisins):    #avion en haut à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.ajouter_bonus([ie-1, je-1], Avion())
                        bonus=True
                        
            #test match3
            #si dans la liste, 2 cases d'affilées sont de la mm couleur, alors il ya match
            if not bonus:
                liste_cases=[[ie, je+1],[ie, je+2],[ie, je-1],[ie, je+1],[ie, je-2],[ie, je-1],[ie+1, je],[ie+2, je],[ie-1, je],[ie+1, je],[ie-2, je],[ie-1, je]]
                for k in range (0,11,2):
                    if self.test_meme_couleur([[ie, je], liste_cases[k], liste_cases[k+1]]):
                            #presence match3
                            print(k)
                            match=[[ie, je], liste_cases[k], liste_cases[k+1]]
                            for case in match:
                                self.activation(case)
                            bonus=True
        
            return bonus
                


          
    def test_swap(self, case1, case2):
        
        """
        argument: self, case1 et case2: les cases dont les elements viennent d'etre echangés
        ---
        effectue les differents test sur la presence de pattern, fait exploser case1/2 s'ils sont des bonus
        ---
        return: True si le swap est reussi, False sinon
        """
        
        if isinstance(case1.son_element, Classique) and isinstance(case2.son_element, Classique):
            ok1=self.test_swap_classique(case1)
            ok2=self.test_swap_classique(case2)
        elif isinstance(case1.son_element, Bonus) and isinstance(case2.son_element, Classique):
            ok2= self.test_swap_classique( case2)
            if isinstance(case1.son_element, Deflagrateur):
                self.exploser_deflagrateur(case1.sa_position, case2.sa_position)
            else:
                self.exploser_bonus(case1.sa_position)
        elif isinstance(case2.son_element, Bonus) and isinstance(case1.son_element, Classique):
            ok1= self.test_swap_classique(case1)
            if isinstance(case2.son_element, Deflagrateur):
                self.exploser_deflagrateur(case2.sa_position, case1.sa_position)
            else:
                self.exploser_bonus(case2.sa_position)
                
                
        if not ok1 and not ok2:
            case1.echanger_elements(case2)
            

        return (ok1 or ok2)      



    def test_meme_couleur(self, cases_potentielles):
        """

        Parameters
        ----------
        cases_potentielles : list
            contient les coordonnées [i,j] des cases devant etre de la meme couleur

        Returns
        -------
        bool
            renvoie True si les cases sont de la meme couleur, False sinon
        """
        k=0
        if isinstance(self.retourner_case(cases_potentielles[0]), Non_Vide):
            if isinstance(self.retourner_case(cases_potentielles[0]).son_element, Classique):
                    couleur=self.retourner_case(cases_potentielles[0]).son_element.sa_couleur
                    for case in cases_potentielles:
                        if isinstance(self.retourner_case(case), Non_Vide):
                            if isinstance(self.retourner_case(case).son_element, Classique):
                                if self.retourner_case(case).son_element.sa_couleur==couleur:
                                    k+=1
                    if k==len(cases_potentielles):
                        return True
                    else: 
                        return False




    def test_grille(self):
        im, jm= la_map.ses_dimensions[0], la_map.ses_dimensions[1]
        
        #parcours 1: deflagrateur
        
        #5 cases horizontales
        #dans une meme ligne, on cherche 5 cases de la mm couleur. Si il y en a, on les detruit, 
        #on place un deflagrateur et on poursuit 5 cases à droite
        i=0
        while i<im:
            j=0
            while j<jm-4:
                #deflagrateur, horizontal
                cases_potentielles=[[i,j],[i, j+1],[i, j+2],[i, j+3],[i, j+4]]
                if self.test_meme_couleur(cases_potentielles):
                    for case in cases_potentielles:
                        self.activation(case)
                        self.ajouter_bonus([i,j+2], Deflagrateur())
                        j+=5
        
                else: j+=1
            i+=1
        #5 cases verticales
        #dans une meme colonne, on cherche 5 cases de la mm couleur. Si il y en a , on les
        #detruit, on place un deflagrateur et on poursuite 5 cases en dessous
        j=0
        while j<jm:
            i=0
            while i<im-4:
                #deflagrateur, vertical
                cases_potentielles=[[i,j],[i+1, j],[i+2, j],[i+3, j],[i+4, j]]
                if self.test_meme_couleur(cases_potentielles):
                    for case in cases_potentielles:
                        self.activation(case)
                        self.ajouter_bonus([i+2,j], Deflagrateur())
                        i+=5
        
                else: i+=1
            j+=1
        
    
        """        
        #parcourt 2: Bombe
        
        #3 cases horizontales
        #dans une meme ligne, on cherche 3 cases de la mm couleur. Si il y en a, on cherche pour 2 cases autour
        #si il y en a, on exploser, pose une bombe, avance de 3 cases
        i=0
        while i<im-1:
            j=0
            while j<jm-2:
                #bombe, horizontal
                cases_potentielles=[[i,j],[i, j+1],[i, j+2]]
                if self.test_meme_couleur(cases_potentielles):
                    cases_pot2=[[i,j],[i-1,j],[i+1,j]]
                    cases_pot3=[[i,j],[i-1,j+2],[i+1,j+2]]
                    #à gauche
                    if self.test_meme_couleur(cases_pot2):
                        for case in cases_potentielles+cases_pot2:
                            self.activation(case)
                            self.ajouter_bonus([i,j], Bombe)
                            j+=3
                     #à droite
                    if self.test_meme_couleur(cases_pot3):
                         for case in cases_potentielles+cases_pot3:
                             self.activation(case)
                             self.ajouter_bonus([i,j+2], Bombe)
                             j+=3
                else: j+=1
            i+=1
                             
        #3 cases verticales
        #dans une meme colonne, on cherche 3 cases de la mm couleur. Si il y en a, on cherche pour 2 cases autour
        #si il y en a, on exploser, pose une bombe, descend de 3 cases
        j=0
        while j<jm-2:
            i=0
            while i<im-2:
                #bombe, verticale
                cases_potentielles=[[i,j],[i+1, j],[i+2, j]]
                if self.test_meme_couleur(cases_potentielles):
                    cases_pot2=[[i,j],[i,j-1],[i,j+1]]
                    cases_pot3=[[i,j],[i+2,j-1],[i+2,j+1]]
                    #en haut
                    if self.test_meme_couleur(cases_pot2):
                        for case in cases_potentielles+cases_pot2:
                            self.activation(case)
                            self.ajouter_bonus([i,j], Bombe)
                            i+=3
                     #en bas
                    if self.test_meme_couleur(cases_pot3):
                         for case in cases_potentielles+cases_pot3:
                             self.activation(case)
                             self.ajouter_bonus([i+2,j], Bombe)
                             i+=3
                else: i+=3
            j+=1
        """  
        #parcourt 3: Roquette
        #4 cases horizontales
        #dans une meme ligne, on cherche 4 cases de la mm couleur. Si il y en a, on les detruit, 
        #on place une roquette verticale et on poursuit 4 cases à droite
        i=0
        while i<im:
            j=0
            while j<jm-3:
                #roquette, horizontale
                cases_potentielles=[[i,j],[i, j+1],[i, j+2],[i, j+3]]
                if self.test_meme_couleur(cases_potentielles):
                    for case in cases_potentielles:
                        self.activation(case)
                        self.ajouter_bonus([i,j+1], Roquette('V'))
                        j+=4
        
                else: j+=1
            i+=1
        #4 cases verticales
        #dans une meme colonne, on cherche 4 cases de la mm couleur. Si il y en a , on les
        #detruit, on place une roquette horizontale et on poursuite 4 cases en dessous
        j=0
        while j<jm:
            i=0
            while i<im-3:
                #Roquettes, verticale
                cases_potentielles=[[i,j],[i+1, j],[i+2, j],[i+3, j]]
                if self.test_meme_couleur(cases_potentielles):
                    for case in cases_potentielles:
                        self.activation(case)
                        self.ajouter_bonus([i+1,j], Roquette('H'))
                        i+=4
        
                else: i+=1
            j+=1
                
        #parcourt 4: Avion
        #on cherche des carrés, sachant que notre case se situe forcément en haut à droite du carré
        #on detruit, place un avion, poursuit 2 cases à droite
        i=0
        while i<im-1:
            j=0
            while j<jm-1:
                #roquette, horizontale
                cases_potentielles=[[i,j],[i+1, j],[i, j+1],[i+1, j+1]]
                if self.test_meme_couleur(cases_potentielles):
                    for case in cases_potentielles:
                        self.activation(case)
                        self.ajouter_bonus([i,j], Avion())
                        j+=2
        
                else: j+=1
            i+=1
                
        #parcourt 5: match 3
        #3 cases horizontales 
        #on cherche 3 cases de la meme couleur. Si il y en a , on les explose et on poursuit 3 cases à droite
        i=0
        while i<im:
            j=0
            while j<jm-2:
                #deflagrateur, horizontal
                cases_potentielles=[[i,j],[i, j+1],[i, j+2]]
                if self.test_meme_couleur(cases_potentielles):
                    for case in cases_potentielles:
                        self.activation(case)
                        j+=3
                else: j+=1
            i+=1
        #3 cases verticales 
        #on cherche 3 cases de la meme couleur. Si il y en a , on les explose et on poursuit 3 cases en dessous
        j=0
        while j<jm:
            i=0
            while i<im-2:
                #deflagrateur, vertical
                cases_potentielles=[[i,j],[i+1, j],[i+2, j]]
                if self.test_meme_couleur(cases_potentielles):
                    for case in cases_potentielles:
                        self.activation(case)
                        i+=3
        
                else: i+=1
            j+=1

                   
                    
    def grille_pleine(self):
        for case in self.ses_cases:
            if isinstance(case.son_element, Element_None):
                return False
        return True
      
    def renouveler_grille(self):
        """

        lorsque la grille contient des elements vides, effectue les flux d'elements, en crée, et recheck'
        -------
        None.

        """
      
        self.test_grille()
        while not self.grille_pleine():
            for case in self.ses_cases:
                if isinstance(case, Normale):
                    case.donner_element()
                    if case.est_une_source:
                        case.generer_classique()
                   # self.test_grille()
            self.test_grille()
                                               
                                    


#----------------------------------Classe Case et ses filles----------------------------

class Case():
    def __init__(self,ma_position):
        assert type(ma_position) == list , "Entrer les coordonnées sour format [ligne, colonne]"
        self._position = ma_position      
        #position est une liste (vient du chargement des cases)
        
    def _get_position(self):
        return self._position
    sa_position = property(_get_position)           #lecture seule : une case ne bouge pas
                                                    #liste de forme [i,j]                                            
    def affichage_case(self):
        return "Je suis une case située en {}, orientée vers le/la {}.".format(self.sa_position, self.son_orientation)
    def __repr__(self):
        return self.affichage_case()
    def __str__(self):
        return self.affichage_case()
    
    
#----------------------------------Classe Vide (cases vides)--------------------------------------

class Vide(Case):
    def __init__(self, position_case):
        super().__init__(position_case) 
    
    def affichage_vide(self):
        return 'case vide, position{}'.format(self.sa_position)
    def __repr__(self):
        return self.affichage_vide()
    def __str__(self):
        return self.affichage_vide()

    

#----------------------------------Classe Non-Vide (mère de Normale et Gelée)--------------------------------------

class Non_Vide(Case):
    def __init__(self, position_case, element_case, orientation_case, le_flux_tp_vers=None):
        super().__init__(position_case)
        self._element= element_case
        self._orientation= str(orientation_case)    #"Haut", "Bas", "Gauche" ou "Droite"
        assert type(le_flux_tp_vers) == list or le_flux_tp_vers == None, "Donner la direction de téléportation sous forme de coordonnées [i,j]"
        self._flux_tp_vers = le_flux_tp_vers 
            
    #property orientation
    def _get_orientation(self):
        return self._orientation
    son_orientation=property(_get_orientation)
     
    def _get_flux_tp_vers(self):
        return self._flux_tp_vers
    son_flux_tp = property(_get_flux_tp_vers)
       
    # propriété element
    def _get_element(self):
        return self._element  
    def _set_element(self, new_element):
        if isinstance(new_element, Element):
            self._element=new_element            
    son_element=property(_get_element, _set_element)


#----------------------------------Classe Normale (case normale)--------------------------------------

    #Instanciation des cases normales
class Normale(Non_Vide):        #classe fille de la classe Case
    def __init__(self, orientation_case, position_case, element_case, est_une_source_case, est_un_puits_case, le_flux_tp_vers=None):
        super().__init__(position_case, element_case, orientation_case, le_flux_tp_vers)
        self._est_une_source= est_une_source_case
        self._est_un_puits=est_un_puits_case

    def _get_est_une_source(self):
        return self._est_une_source
    est_une_source = property(_get_est_une_source)
    def _get_est_un_puits(self):
        return self._est_un_puits
    est_un_puits = property(_get_est_un_puits)

    #affichage
    def affichage_normal(self):
        return 'case normale, position:{}, element contenu:{}, orientation:{}'.format(self.sa_position, self.son_element, self.son_orientation)
    def __repr__(self):
        return self.affichage_normal()
    def __str__(self):
        return self.affichage_normal()
    
    def generer_classique(self):
        if self.est_une_source and isinstance(self.son_element, Element_None):
            couleur= random.choice(la_map.sa_liste_couleurs)
            self.son_element=Classique(str(couleur))
            
    def exploser_classique(self):
        if isinstance(self.son_element, Classique):
            compteur[self.son_element.sa_couleur] += 1  #on va péter un élément de cette couleur en +
            self.son_element=Element_None()
    
    
    
    
    def donner_element(self):
        """
        enlève l'élement de la case courante et le met dans la case qui la suit
        dans le sens du flux (prend en compte la téléportation)
        """
        #trouver les coordonnées de la case alimentée
        coord_case_alimentee=2
        if isinstance(self, Normale):
            if not isinstance(self.son_element, Element_None):
                if self.son_flux_tp:
                    coord_case_alimentee = self.son_flux_tp()
                else:
                    if self.son_orientation=='Haut':
                        coord_case_alimentee= [self.sa_position[0] -1, self.sa_position[1]]
                    elif self.son_orientation=='Bas':
                        coord_case_alimentee= [self.sa_position[0] +1, self.sa_position[1]]
                    elif self.son_orientation=='Droite':
                        coord_case_alimentee= [self.sa_position[0], self.sa_position[1] +1]
                    elif self.son_orientation=='Gauche':
                        coord_case_alimentee= [self.sa_position[0], self.sa_position[1] -1]
                if coord_case_alimentee!=2:
                    print(coord_case_alimentee)
                    #retrouver cette case dans la grille
                    #On obtient la case alimentée
                    print(la_map.sa_grille.retourner_case(coord_case_alimentee))
                    if isinstance(la_map.sa_grille.retourner_case(coord_case_alimentee), Normale):
                        print(la_map.sa_grille.retourner_case(coord_case_alimentee).son_element)
                        if isinstance(la_map.sa_grille.retourner_case(coord_case_alimentee).son_element, Element_None):
                            print('ok')
                            #donner l'element à la case alimentée. 
                            self.echanger_elements(la_map.sa_grille.retourner_case(coord_case_alimentee))
                        

    def echanger_elements(self, case2):
        if isinstance(case2, Normale):
            if not isinstance(self.son_element, Etoile) and not isinstance(case2.son_element, Etoile):
                elt1=self.son_element       #ça marche même si l'élement est None
                elt2=case2.son_element
                self.son_element=elt2
                case2.son_element=elt1
    
    
    
#----------------------------------Classe Gelée (cases gelées)--------------------------------------
#instanciation
class Gelee(Non_Vide):
    def __init__(self, niveau_gel, element_case, position_case, orientation_case, le_flux_tp_vers=None):
        super().__init__(position_case, element_case, orientation_case, le_flux_tp_vers)
        self._niveau_gel=int(niveau_gel)
        
    #property niveau gel   
    def _get_niveau_gel(self):
        return self._niveau_gel   
    def _set_niveau_gel(self, new_niveau_gel):
        if new_niveau_gel in [0,1,2,3]:
            self._niveau_gel=new_niveau_gel
    son_niveau_gel=property(_get_niveau_gel, _set_niveau_gel)     
        
    def degelage(self):
        """
        argument:self
        ---
        enleve 1 niveau de gel à une case gelée,
        si la case gelée atteint le niveau 0, la detruit et met une case Normale à la place
        ---
        return: None
        """
        if self.son_niveau_gel>1:
            ancien_niveau=self.son_niveau_gel
            self.son_niveau_gel=ancien_niveau -1
        elif self.son_niveau_gel==1:
            #detruire l'element gelee et le remplacer par normale, au mm endroit.
            new_case= Normale(self.son_orientation, self.sa_position, self.son_element, False, False)
            la_map.sa_grille[str(self.sa_position)]=new_case    
    
    #affichage
    def affichage_gelee(self):
        return 'case gelee, niveau: {}, position: {}, element contenu:{}'.format(self.son_niveau_gel, self.sa_position, self.son_element)
    def __repr__(self):
        return self.affichage_gelee()
    def __str__(self):
        return self.affichage_gelee()


#----------------------------------Classe Element et ses filles----------------------------

class Element():
    def __init__(self):
        pass
    


#----------------------------------Classe Classique------------------------------------------

class Classique(Element):
    def __init__(self, ma_couleur):
        super().__init__()
        self._couleur= str(ma_couleur)
    
    #property
    def _get_couleur(self):
        return self._couleur
    def _set_couleur(self, new_couleur):        #on ne change pas la couleur d'un élément, si ?
                                                #je crois qu'on en crée juste un novueau...?
        if new_couleur in la_map.sa_liste_couleurs:
            self._couleur=new_couleur
    sa_couleur=property(_get_couleur, _set_couleur)
    
     #affichage  
    def affichage_classique(self):
         return 'element classique {}'.format(self.sa_couleur)
    def __repr__(self):
         return self.affichage_classique()
    def __str__(self):
         return self.affichage_classique()
#----------------------------------Classe Element_None (Element)------------------------------------------

class Element_None(Element):
    def __init__(self):
        super().__init__()

     #affichage  
    def affichage_none(self):
         return 'element  none'
    def __repr__(self):
         return self.affichage_none()
    def __str__(self):
         return self.affichage_none()
    




#----------------------------------Classe Etoile (Element)------------------------------------------ 
class Etoile(Element):
    def __init__(self):
        super().__init__()
        self._dans_puits = False
        
    def set_dans_puits(self):
        if self._dans_puits == False:
            compteur["Etoiles"] += 1        #on n'incrémente que si l'étoile n'était pas déjà dans un puits
        self._dans_puits = True         #on ne peut que mettre une étoile dans un puits
                                        #après on ne l'en sort pas
    def affichage(self):
         return 'element étoile'
    def __repr__(self):
         return self.affichage()
    def __str__(self):
         return self.affichage()
    
        

#----------------------------------Classe Bonus-------------------------------------------------- 

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
    def __init__(self, ma_direction):
        self._direction= str(ma_direction)      #sous la forme "H" pour horizontal
                                                #               "V" pour vertical
        
    def __repr__(self):
        return "Roquette {}".format(self._direction)
    def __str__(self):
        return "Roquette {}".format(self._direction)
    
    def _get_direction(self):
        return self._direction
    sa_direction=property(_get_direction)
        

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



#----------------------------------------Chargement XML-------------------------------
         
    
def chargement_XML():       #plus tard, on pourra mettre en argument le niveau, qu'on choisira dans l'interface de jeu...
    pass
if 1:
#Chargement de la Map

    les_couleurs = tronc.get('couleurs')[2:-2].split("', '")
    les_dimensions = [int(tronc.get('nb_lignes')),int(tronc.get('nb_colonnes'))]
    le_titre = str(tronc.get('titre'))
    le_nb_coups = int(tronc.get("nb_coup"))
    la_map = Map(les_couleurs,les_dimensions,le_titre,le_nb_coups)


    #Chargement des objectifs depuis le XML
    for objectif_xml in tronc[1]:
        la_cible = objectif_xml.get("Cible")[1:]
        la_quantite = objectif_xml.get("Nombre")
        objectif_poo = Objectif(la_cible,la_quantite)
        la_map.add_objectif(objectif_poo)
        
        
       
    #Chargement des cases dans la grille à partir du XML
    #grille = Grille()
        
        #Instanciation des cases
    for case_xml in tronc[0]:
        la_position = [int(case_xml.get("ligne")), int(case_xml.get('colonne'))]
        #on a numéroté nos cases avec un axe vertical descendant comme dans une table Python
        #donc on prend pour le numéro de ligne le complément par rapport au nb de lignes
        
            #Instanciation des cases vides
        if case_xml.tag == "Cellule_Vide":
            case_poo = Vide(la_position) 
        else:
            
            #Instanciation des cases normales et gelées 
            l_orientation = case_xml.get('orientation')
            le_flux_tp_vers = None
            contenu_xml = case_xml.get('contenu')
            if case_xml.get("flux_tp_vers") :   #case qui peut téléporter
                le_flux_tp_vers = [int(i) for i in case_xml.get("flux_tp_vers")[1:-1].split(",")]
            if contenu_xml in la_map.sa_liste_couleurs:     #contient un élément classique
                l_element = Classique(contenu_xml)
            elif contenu_xml == "Etoile":
                l_element = Etoile()
                
            else:   #le reste c'est forcément des boni
                if contenu_xml == "Bombe":
                    l_element = Bombe()
                elif contenu_xml == "Avion":
                    l_element = Avion()
                elif contenu_xml == "Deflagrateur":
                    l_element = Deflagrateur()
                else:       #forcémeent une roquette H ou V
                    la_direction = contenu_xml.split(" ")[1][0].upper()   #initiale de Horizontale ou Verticale (majuscule)
                    l_element = Roquette(la_direction)
            
                #Instanciation des cellules gelées
            if case_xml.tag == "Cellule_Gelee":
                le_niveau_gel = int(case_xml.get('niveau_gel'))
                case_poo = Gelee(le_niveau_gel,l_element,la_position,l_orientation,le_flux_tp_vers)
            
                 #Instanciation des cellules normales
            elif case_xml.tag == "Cellule":
                le_est_un_puits,le_est_une_source = 0,0
                if case_xml.get('flux') == "Puits":
                    le_est_un_puits = 1
                elif case_xml.get('flux') == "Source":
                    le_est_une_source = 1
                case_poo = Normale(l_orientation,la_position,l_element,le_est_une_source,le_est_un_puits,le_flux_tp_vers)
        
        la_map.sa_grille.add_case(case_poo)
        
#chargement_XML()
    
#----------------------------------Chargement XML------------------------

    
    
    
##TODO : ajouts (jusqu'à la fin)

class Partie():
    #-------------------------------Chargement de la grille--------------------------------
    #chargement_XML()
    pass






    #-------------------------------Tours de jeu-------------------------------------------
    #jusqu'à ce que les objectifs soient atteints ou que le joueur n'ait plus de coups

def action_joueur(mon_action):
    """
    entrée : mon_action, de type str, de la forme "[i1,j1] [i2,j2]" ou "[i,j]"
    
    action:
    dans le premier cas, teste le swap des cases en [i1,j1] et [i2,j2], et l'effectue s'il est valide
    dans le second cas, teste si la case [i,j] contient un bonus, et l'explose le cas échéant
    """
    print("mon action", mon_action)
    coord_str = mon_action.split(" ")   #liste de forme ["[i1,j1]","[i2,j2]"]
    print("coord str", coord_str)
    #tester la forme de l'entrée ?
    assert len(coord_str)==1 or len(coord_str) ==2 , "Entrez une commande valide, sous la forme : \"[i1,j1] [i2,j2]\" (swap) ou \"[i,j]\" (activation bonus)"
    if len(coord_str) == 2:     #swap
        coord1 = [int(nb_str) for nb_str in coord_str[0][1:-1].split(",")]
        print("coord1", coord1, type(coord1))
        coord2 = [int(nb_str) for nb_str in coord_str[1][1:-1].split(",")]
        print("coord2", coord2)
        case1 = la_map.sa_grille.retourner_case(coord1)
        case2 = la_map.sa_grille.retourner_case(coord2)
        case1.echanger_elements(case2)
        la_map.sa_grille.test_swap(case1,case2)        #si le swap ne servait à rien, les éléments seront sont ré-échangés
        
    elif len(coord_str)==1:     #activation d'un bonus
        coord = [int(nb_str) for nb_str in coord_str[0][1:-1].split(",")]
        case = la_map.sa_grille.retourner_case(coord)
        assert isinstance(case,Bonus), "Veuillez entrer une commande valide, sous la forme : \"[i1,j1] [i2,j2]\" (swap) ou \"[i,j]\" (activation bonus)"
        la_map.sa_grille.exploser_bonus(case)
        
    la_map.sa_grille.test_grille()
    #la_map.sa_grille.renouveler_grille()       #màj jusqu'à complétion et stabilité de la grille
    
    #refresh la grille affichée
    

    #-------------------------------Donner l'issue de la partie-------------------------------

    








#-------------------------Affichage des cases et élements---------------------------


couleurs_cases = {Vide : "#999", Gelee : "#99f", Normale : "#fff"}

def couleur_case(case):
    if isinstance(case, Normale) :
        if case.est_un_puits :
            return "#fcc"       #rouge
        elif case.est_une_source :
            return "#cfc"       #vert
    return couleurs_cases.get(type(case))
    
liste_couleurs      = ["green", "red", "yellow", "blue", "magenta"]
couleurs_classique = {"green" : "#0f0", "red" : "#f00", "yellow" : "#ff0", "blue" : "#00f", "magenta" : "#f0f"}

def couleur_element(case):
    if isinstance(case,Vide):
        return "#000"
    if isinstance(case.son_element,Classique):
        return couleurs_classique.get(case.son_element.sa_couleur)
    else:
        return "#000"       #noir

icones = {Classique : "🍬", Deflagrateur: "💥", Avion : "✈", Roquette : "🚀", Bombe : "💣", Etoile : "★"}    

def icone_element(case):
    if isinstance(case, Vide):
        #print("c'est vide !")
        return ""
    else:
        #print("c'est pas vide")
        return icones.get(type(case.son_element))
    
    
    
    
    



#-----------------------------------Interface--------------------------------------

class Interface():
    def __init__(self,ma_map):        
        self.fenetre = TK.Tk()
        self.fenetre.title("Jeu Match-3")
        l = 0
         
        #Création affichage du nom du niveau
        TK.Label(self.fenetre, text="Niveau :").grid(row=l, column=0, columnspan=2, sticky = 'w e n s', padx = 5, pady = 5)
        TK.Label(self.fenetre, text=ma_map.son_titre.upper(), fg="#f00").grid(row=l, column=2, columnspan=4, sticky = 'w e n s', padx = 5, pady = 5)
        
        #Bouton options (pour reset la partie)
        #pour ça il faut que le chargement XML soit dans une fonction
        #comme ça on relance le chargement XML quand on veut reset la partie
        TK.Button(self.fenetre, text="RESET").grid(row=l, column=6, rowspan=2, columnspan = ma_map.ses_dimensions[1]+1-6, sticky = 'w e n s', padx = 5, pady = 5)
        l+=1    #ligne
        
        #Affichage de l'avancement en nb de coups
        TK.Label(self.fenetre, text="Coups restants :").grid(row=l, column=0, columnspan=3, sticky = 'w n s', padx = 5, pady = 5)
        TK.Label(self.fenetre, text=str(ma_map.ses_coups_restants) + "/" + str(ma_map.son_nb_coups) ).grid(row=l, column=3, columnspan=3, sticky = 'w e n s', padx = 5, pady = 5)
        l+=1
        
        #Affichage de la grille
        action = []
        
        def ajouter_clic(ma_case,mon_action):
            assert isinstance(ma_case,Case)
            mon_action += [ma_case.sa_position]
            print(mon_action)
        #ça marche pas..... toujours celui de la dernière case créée
        
        def remplissage_grille():
            for case in ma_map.sa_grille.ses_cases:
                row_case = case.sa_position[0] +2        #on affiche à la ligne 2
                column_case = case.sa_position[1] +1    #on affiche à la colonne 1
                label = TK.Button(self.fenetre, text=icone_element(case), command=lambda : ajouter_clic(case,action),
                         bg=couleur_case(case),fg=couleur_element(case),pady=10, padx=10, font=20)
                label.grid(row=row_case, column=column_case, sticky = 'w e n s', padx = 1, pady = 1)
        remplissage_grille()
        #ma_map.sa_grille.test_grille()         #tester au début, mais ne parche pas pour le moment...
            
        l+=ma_map.ses_dimensions[0]
        
        #Affichage des coordonnées des cases (pour le joueur)
        for i in range(ma_map.ses_dimensions[0]):
            label = TK.Label(self.fenetre, text=str(i),
                     bg="#fff" ,fg="#000",pady=10, padx=10, font=20)
            label.grid(row=i+2, column=0, sticky = 'w e n s', padx = 1, pady = 1)
        for j in range(ma_map.ses_dimensions[1]):
            label = TK.Label(self.fenetre, text=str(j), 
                             bg="#fff" ,fg="#000",pady=10, padx=10, font=20)
            label.grid(row=l, column=j+1, sticky = 'w e n s', padx = 1, pady = 1)
        l+=1
    
            # def coucou(event):
            #     print("Souris en {} {}".format(event.x, event.y))
            # label.bind('<Button-1>', coucou)

        #Fenêtre d'action
        VarAction = TK.StringVar()
        TK.Entry(self.fenetre, textvariable = VarAction).grid(row=l, column=0, columnspan = ma_map.ses_dimensions[1]-1, sticky = 'w e n s', padx = 5, pady = 5)   
        TK.Button(self.fenetre,text="Valider Action", command=lambda : action_joueur(VarAction.get())).grid(row=l, column=6, columnspan = 2, sticky = 'w e n s', padx = 5, pady = 5) 
        l+=1
        remplissage_grille()
        
        
        

        
        
        #Affichage de l'avancement des objectifs (faire qqch de dynamique qui s'adapte au xobjectifs de ma_map)
        for objectif in ma_map.ses_objectifs:
            
            TK.Label(self.fenetre, text=objectif).grid(row=l, column=0, columnspan=ma_map.ses_dimensions[1]-2, sticky = 'w n s', padx = 5, pady = 5)
            TK.Label(self.fenetre, text=str(objectif.sa_quantite_restante)+"/"+str(objectif.sa_quantite)).grid(row=l, column=5, columnspan=3, sticky = 'w e n s', padx = 5, pady = 5)
            l+=1
        
        
        self.fenetre.mainloop()
    
            
    
Interface(la_map)
   
    # # bg is to change background, fg is to change foreground (technically the text color)
    # label = TK.Label(Fenetre, text=icone_bombe,
    #                  bg=couleur_gelee, fg=couleur_bonus, pady=10, padx=10, font=10) # You can use use color names instead of color codes.
    # label.pack()
    # click_here = TK.Button(Fenetre, text="click here to find out",
    #                        bg='#000', fg='#ff0', padx = 10, pady = 5)
    
    # click_here.pack()
   
#case1 = la_map.sa_grille.retourner_case([2,0])
#case2 = la_map.sa_grille.retourner_case([1,2])