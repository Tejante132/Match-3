# -*- coding: utf-8 -*-
"""
Chargement du .XML contenant des infos sur la Map
traduction des appellations de M. Etienne vers nos appellations

et instanciation des classes au fur et à mesure

"""

import random #pour random.choice(liste)
import xml.etree.ElementTree as ET
arbreXML = ET.parse("C:\\Users\\Clotilde\\OneDrive - ensam.eu\\MINI POO\\Données test (XML)\\Niveau1.1 - Activation des bonus.xml")
tronc = arbreXML.getroot()


#----------------------------------Classe Map--------------------------------------
##Instanciation
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


#Chargement de la map 
les_couleurs = tronc.get('couleurs')[2:-2].split("', '")
les_dimensions = [int(tronc.get('nb_lignes')),int(tronc.get('nb_colonnes'))]
le_titre = str(tronc.get('titre'))
le_nb_coups = int(tronc.get("nb_coup"))
la_map = Map(les_couleurs,les_dimensions,le_titre)


#----------------------------------Classe Objectifs--------------------------------------
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
    

#----------------------------------Classe Grille--------------------------------------
##instanciation
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


#----------------------------------Classe Case et ses filles--------------------------------------

##Instanciation des Cases (ou Cellules)
class Case():
    def __init__(self,ma_position):
        self._position = ma_position      
        #position est une liste (vient du chargement des cases)
        
    def _get_position(self):
        return self._position
    sa_position = property(_get_position)           #lecture seule : une case ne bouge pas
                                                    #liste de forme [i,j]                                            
    def __repr__(self):
        return "Je suis une case située en {}, orientée vers le/la {}.".format(self.sa_position, self.son_orientation)


#----------------------------------Classe Vide (cases vides)--------------------------------------
##instanciation
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
##instanciation
class Element():
    def __init__(self):
        pass
    


#----------------------------------Classe Classique------------------------------------------
##instanciation
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
    
    
    


