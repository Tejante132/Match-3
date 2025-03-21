# -*- coding: utf-8 -*-
"""
GUILBERT Eva
GUYARD-GILLES Clotilde

                    MINI POO : Jeu Match-3
                    

couleurs des cases dispo: jaune, rouge, vert, bleu, rose

EVA ATTENDS QUE JE MODIFIE 2-3 TRUCS AVANT D'AVANCER STP


"""


import random #pour random.choice(liste)
import xml.etree.ElementTree as ET
arbreXML = ET.parse("C:\\Users\\Clotilde\\OneDrive - ensam.eu\\MINI POO\\Données test (XML)\\NIveau6 V1.2 - Flux complexe et téléportation.xml")
tronc = arbreXML.getroot()

liste_couleurs= ['jaune','rouge','vert','bleu','rose']
orientations= ['haut','bas','gauche','droite']



#----------------------------------Classe Map--------------------------------------

class Map():
    def __init__(self, ma_liste_couleurs, mes_dimensions, mon_titre):
        self._liste_couleurs= ma_liste_couleurs
        self._dimensions= list(mes_dimensions)
        self._titre=str(mon_titre)
        self._objectifs = []       #liste qui recevra les objectifs
        
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

#----------------------------------Chargement XML de la classe Map------------------------

les_couleurs = tronc.get('couleurs')[2:-2].split("', '")
les_dimensions = [int(tronc.get('nb_lignes')),int(tronc.get('nb_colonnes'))]
le_titre = str(tronc.get('titre'))
le_nb_coups = int(tronc.get("nb_coup"))
la_map = Map(les_couleurs,les_dimensions,le_titre)


#----------------------------------Classe Objectifs---------------------------------------
##instanciation
class Objectif():
    def __init__(self,ma_cible,ma_quantite):
        self._cible = ma_cible
        self._quantite = ma_quantite
        
    def _get_cible(self):
        return self._cible
    sa_cible = property(_get_cible)
    
    def _get_quantite(self):
        return self._quantite
    sa_quantite = property(_get_quantite)
        
    def __repr__(self):
        if self._cible in la_map.sa_liste_couleurs:
            return "Objectif : détruire {} éléments de couleur {}.".format(self.sa_quantite,self.sa_cible)
        else:
            return "Objectif : détruire {} éléments {}.".format(self.sa_quantite,self.sa_cible)
        
#Chargement des objectifs depuis le XML
for objectif_xml in tronc[1]:
    la_cible = objectif_xml.get("Cible")
    la_quantite = objectif_xml.get("Nombre")
    objectif_poo = Objectif(la_cible,la_quantite)
    la_map.add_objectif(objectif_poo)



#----------------------------------Classe Grille----------------------------------------

class Grille():
    def __init__(self):
        self._dico_cases = {}       #dico qui contiendra en clé une postion sous le forme "[i,j]"
                                    #et en argument une case
                                    
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
        case= self[str(localisation)]
        if isinstance(case, Normale):
            case.exploser_classique()
        elif isinstance(case, Gelee):
            case.degelage()
            
            
    def exploser_bonus(self, localisation):
        """
        Parameters
        localisation de la case contenant l'element bonus'
        localisation : list
            fait exploser le bonus en detruisant les elements des cases voisines

        Returns
        -------
        None.

        """
        case=self[str(localisation)]
        bonus=case.son_element
        ib, jb=localisation[0], localisation[1]
        list
        if isinstance(bonus,Bonus):
            #bombe
            if isinstance(bonus, Bombe):
                cases_explosees=[[ib, jb-2],[ib, jb-1],[ib, jb+1],[ib, jb+1],[ib-2, jb],[ib-1, jb],[ib+1, jb],[ib+2, jb],[ib-1, jb-1],[ib-1, jb+1],[ib+1, jb-1],[ib+1, jb+1]]
                for case in cases_explosees:
                    #la case contient un element normal/gelé
                    if not isinstance(self[str(case)].son_element, Bonus):
                        self.activation(case)
                    else:
                        self.exploser_bonus(case)
                        
        if isinstance(bonus, Roquette):
            #roquette
            if bonus.sa_direction=='H':
                pass
            pass
        
    
    #tester la validité et les effets dun swap, exploser des cases, creer des bonus...
    def test_swap_classique(self, case):
        """
        argument: self, case contenant un element classique où vient d'atterir l'element swapé
        ---
        teste si un pattern a ete formé
        (delfagrateur, bombe, missile, avion, combinaison classique)
        si oui, detruit les cases et rajoute le bonus, renvoie True
        si non, renvoie False
        """
        
        if isinstance(case, Normale):
            [ie, je]= case.sa_position
            couleur= case.son_element.sa_couleur 
            bonus= False
            
            
            #test deflagrateur
            #horizontal
            defl_h=0
        
            liste_voisins=[[ie, je-2], [ie, je-1],[ie, je+1],[ie, je+2]]
            for voisin in liste_voisins:
                if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
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
                    if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
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
                    if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            bombe_v+=1
                if bombe_v==2:
                    #bombe en T vertical, a voir si elle est à lendroit ou a lenvers
                    #testons si elle est en T inversé
                    bombe_vv=0
                    liste_voisins2=[[ie+1, je],[ie+2, je]]
                    for voisin in liste_voisins2:
                        if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
                            if self[str(voisin)].son_element.sa_couleur==couleur:
                                bombe_vv+=1
                    if bombe_vv==2:
                        #bombe en T inversé 
                        for voisin in liste_voisins+liste_voisins2:
                            self.activation(voisin)
                            self[str([ie, je])]=Bombe
                            bonus=True
                    
                    else:
                        #testons si elle est en T à l'endroit
                        bombe_vv=0
                        liste_voisins2=[[ie-1, je],[ie-2, je]]
                        for voisin in liste_voisins2:
                            if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
                                if self[str(voisin)].son_element.sa_couleur==couleur:
                                    bombe_vv+=1
                        if bombe_vv==2:
                            #bombe en T à l'endroit
                            for voisin in liste_voisins+liste_voisins2:
                                self.activation(voisin)
                                self[str([ie, je])]=Bombe
                                bonus=True
                                
            if not bonus:
                #test bombe
                #horizontal
                bombe_h=0
                liste_voisins=[[ie-1, je],[ie+1, je]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            bombe_h+=1
                if bombe_h==2:
                    #bombe en T horizontale, a voir si elle est à droite ou à gauche
                    #testons si elle est à droite
                    bombe_hh=0
                    liste_voisins2=[[ie, je+1],[ie, je+2]]
                    for voisin in liste_voisins2:
                        if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
                            if self[str(voisin)].son_element.sa_couleur==couleur:
                                bombe_hh+=1
                    if bombe_hh==2:
                        #bombe horizontale à droite 
                        for voisin in liste_voisins+liste_voisins2:
                            self.activation(voisin)
                            self[str([ie, je])]=Bombe
                            Bonus=True
                    
                    else:
                        #testons si elle est à gauche 
                        bombe_hh=0
                        liste_voisins2=[[ie, je-1],[ie, je-2]]
                        for voisin in liste_voisins2:
                            if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
                                if self[str(voisin)].son_element.sa_couleur==couleur:
                                    bombe_hh+=1
                        if bombe_hh==2:
                            #bombe horizontale à gauche
                            for voisin in liste_voisins+liste_voisins2:
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
                    if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
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
                    if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
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
                    if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
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
                    if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            missile_v+=1
                if missile_v==3:
                    #missile horizontal à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.activation([ie, je])
                        self[str([ie-1,je])]=Roquette('V')
                        bonus=True
                        
            #test avion
            #case en haut à gauche
            if not bonus:
                avion_hg=0
                liste_voisins=[[ie+1, je],[ie+1, je+1],[ie, je+1]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            avion_hg+=1
                if avion_hg==3:
                    #avion en haut à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self[str([ie,je])]=Avion
                        bonus=True
                        
            #case en bas à gauche
            if not bonus:
                avion_bg=0
                liste_voisins=[[ie-1, je],[ie-1, je+1],[ie, je+1]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            avion_bg+=1
                if avion_bg==3:
                    #avion en haut à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.activation([ie, je])
                        self[str([ie-1,je])]=Avion
                        bonus=True
                        
            #case en haut à droite        
            if not bonus:     
                avion_hd=0
                liste_voisins=[[ie, je-1],[ie+1, je-1],[ie+1, je]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            avion_hd+=1
                if avion_hd==3:
                    #avion en haut à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.activation([ie, je])
                        self[str([ie,je-1])]=Avion
                        bonus=True

            #case en bas à droite        
            if not bonus:     
                avion_bd=0
                liste_voisins=[[ie-1, je],[ie-1, je-1],[ie, je-1]]
                for voisin in liste_voisins:
                    if isinstance(voisin, Normale) or isinstance(voisin, Gelee):
                        if self[str(voisin)].son_element.sa_couleur==couleur:
                            avion_bd+=1
                if avion_bd==3:
                    #avion en haut à gauche
                    for voisin in liste_voisins:
                        self.activation(voisin)
                        self.activation([ie, je])
                        self[str([ie-1,je-1])]=Avion
                        bonus=True
                        
            #test match3
            #si dans la liste, 2 cases d'affilées sont de la mm couleur, alors il ya match
            if not bonus:
                liste_cases=[[ie, je+1],[ie, je+2],[ie, je-1],[ie, je+1],[ie, je-2],[ie, je-1],[ie+1, je],[ie+2, je],[ie-1, je],[ie+1, je],[ie-2, je],[ie-1, je]]
                for k in [0,12,2]:
                    if (isinstance(liste_cases[k], Normale)or isinstance(liste_cases[k], Gelee)) and (isinstance(liste_cases[k+1], Normale)or isinstance(liste_cases[k+1], Gelee)):
                        if self[str(liste_cases[k])].son_element.sa_couleur==couleur and self[str(liste_cases[k+1])].son_element.sa_couleur==couleur:
                            #presence match3
                            match=[[ie, je], [liste_cases[k]], liste_cases[k+1]]
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
            self.exploser_bonus(case1)
        elif isinstance(case2.son_element, Bonus) and isinstance(case1.son_element, Classique):
            ok1= self.test_swap_classique(case1)
            self.exploser_bonus(case2)
        return (ok1 or ok2)      

                    
        

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
        self._element= str(element_case)
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
        if self.est_une_source and self.son_element==None:
            couleur= random.choice(la_map.sa_liste_couleurs)
            self.son_element=Classique(self,couleur)
               
    def exploser_classique(self):
        if self.son_element!=None:
            self.son_element=None
    
    def donner_element(self):
        """
        enlève l'élement de la case courante et le met dans la case qui la suit
        dans le sens du flux (prend en compte la téléportation)
        """
        #trouver les coordonnées de la case alimentée
        if self.son_flux_tp:
            coord_case_alimentee = self.son_flux_tp()
        else:
            if self.get_orientation()=='Haut':
                coord_case_alimentee= [self.sa_position[0] -1, self.sa_position[1]]
            elif self.get_orientation()=='Bas':
                coord_case_alimentee= [self.sa_position[0] +1, self.sa_position[1]]
            elif self.get_orientation()=='Droite':
                coord_case_alimentee= [self.sa_position[0], self.sa_position[1] +1]
            elif self.get_orientation()=='Gauche':
                coord_case_alimentee= [self.sa_position[0], self.sa_position[1] -1]
        print('ok orientation')
        #retrouver cette case dans la grille
        assert isinstance(grille, Grille)
        #On obtient la case alimentée
        case_alimentee=grille.retourner_case(coord_case_alimentee)
        #donner l'element à la case alimentée. 
        if isinstance(case_alimentee, Normale) and case_alimentee.son_element==None:
            case_alimentee.son_element=self.son_element
            #dire que la case est vide
            self.son_element=None

    def echanger_elements(self, case2):
        if isinstance(case2, Normale):
            if not isinstance(self.son_element, Etoile) and not isinstance(case2.son_element, Etoile):
                elt1=self.son_element       #ça marche même si l'élement est None
                elt2=case2.son_element
                self.son_element=elt2
                elt2.sa_case = self         #il faut aussi changer les cases des éléments
                case2.son_element=elt1
                elt1.sa_case = case2
    
    
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
            grille[str(self.sa_position)]=new_case    
    
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


#----------------------------------Classe Etoile (Element)------------------------------------------ 
class Etoile(Element):
    def __init__(self):
        super().__init__()
        self._dans_puits = False
        
    def set_dans_puits(self):
        self._dans_puits = True         #on ne peut que mettre une étoile dans un puits
                                        #après on ne l'en sort pas
    def affichage(self):
         return 'element étoile'
    def __repr__(self):
         return self.affichage()
    def __str__(self):
         return self.affichage()
     
        

#----------------------------------Classe Bonus----------------------------------------------------- 

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


     
            
#-------------------Chargement des cases dans la grille à partir du XML--------------------
grille = Grille()
    
    #Instanciation des cases
for case_xml in tronc[0]:
    la_position = [int(case_xml.get("ligne")),int(case_xml.get('colonne'))]
    
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
    
    grille.add_case(case_poo)
    
    
    


