# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"""
couleurs des cases dispo: jaune, rouge, vert, bleu, rose
"""


import random #pour random.choice(liste)


class Grille():
    def __init__(self, taille_grille, niveau_grille, contenu_grille, objectifs_grille, nb_coups_grille):
        self._taille= list(taille_grille)
        self._niveau= int(niveau_grille)
        self._contenu=list(contenu_grille)
        self._objectifs= str(objectifs_grille)
        self._nb_coups_max= int(nb_coups_grille)
        self._nb_coups_restants= int()
        
        
    #tous les get des attributs de la grille   
    def get_taille(self):
        return self._taille.get()
    def get_niveau(self):
        return self._niveau.get()
    def get_contenu(self):
        return self._contenu.get()
    def get_objetcifs(self):
        return self._objectifs.get()
    def get_nb_coups_max(self):
        return self._nb_coups_max.get()
    def get_nb_coups_restants(self):
        return self._nb_coups_restants.get()
        
        
    #definition REPR et STR    
    def affichage_grille(self):
        return "grille niveau {}, contenu:{}, objectifs: {}, nb de coups: {}".format( self.get_niveau(), self.get_contenu(), self.get_objetcifs(), self.get_nb_coups_max())
    def __repr__(self):
        return self.affichage_grille()
    def __str__(self):
        return self.affichage_grille()
        
        
        
        
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
    
    
    
class Vide(Case):
    def __init__(self, position_case):
        super().__init__(position_case) 

    
    
    def affichage_vide(self):
        return 'case vide, position{}'.format(self.sa_position)
    def __repr__(self):
        return self.affichage_vide()
    def __str__(self):
        return self.affichage_vide()
    
    
    
    
class Gelee(Case):
    def __init__(self, niveau_gel, element_case, position_case):
        super().__init__(position_case)
        self._niveau_gel=int(niveau_gel)
        self._element= str(element_case)
        
    #property niveau gel   
    def get_niveau_gel(self):
        return self._niveau_gel.get()   #ca marche pas, jsp, help
    def set_niveau_gel(self, new_niveau_gel):
        if new_niveau_gel in [0,1,2,3]:
            self._niveau_gel=new_niveau_gel
    
    son_niveau=property(get_niveau_gel, set_niveau_gel)
        
        
       
    def degelage(self):
        if self.son_niveau>1:
            ancien_niveau=self.son_niveau
            self.son_niveau=(ancien_niveau -1)
        elif self.son_niveau==1:
            #detruire l'element gelee et le remplacer par normale, au mm endroit.
            #obtenir l'orientation de la case
            pass
       
    # propriete element
    def get_element(self):
        return self._element.get()  
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
    
    
        
       
        
        
        
        
        
class Normale(Case):
    def __init__(self, orientation_case, position_case, element_case, est_une_source_case, est_un_puit_case):
        super()._init__(position_case)
        self._orientation=str(orientation_case) #coordonnées de la case vers qui le flux va 
        self._element= element_case
        self._est_une_source= bool
        self._est_un_puit=bool
        self._est_vide= False
      
    #property element
    def get_element(self):
        return self._element.get()
    def set_element(self, new_element):
        if isinstance(new_element, Element):
            self._element=new_element       
    son_element=property(get_element, set_element)
    

    def get_orientation(self):
        return self._orientation.get()
    def get_est_une_source(self):
        return self._est_une_source.get()
    def get_est_un_puit(self):
        return self._est_un_puit.get()
    def get_est_vide(self):
        return self._est_vide()
    
    
    #affichage
    def affichage_normale(self):
        return 'case normale, position:{}, element contenu:{}, orientation:{}'.format(self.get_position(), self.get_element(), self.get_orientation())
    def __repr__(self):
        return self.affichage_normale()
    def __str__(self):
        return self.affichage_normale()
    
    
    
    def donner_element(self):
        pass
        
    
    
    
    
class Element():
    pass

liste_couleurs= ['jaune','rouge','vert','bleu','rose']

class Classique(Element):
    def __init__(self, couleur):
        self._couleur= str(couleur)
    
    #property
    def get_couleur(self):
        return self._couleur.get()
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
     
        
    def generer_classique(case_source):
         assert isinstance(case_source, Normale())
         assert case_source.get_est_une_source()
         assert case_source.get_est_vide()
         couleur= random.choice(liste_couleurs)
         case_source.son_element(Classique(couleur))
         
    
        



    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
