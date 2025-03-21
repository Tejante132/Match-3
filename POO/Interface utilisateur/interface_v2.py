# -*- coding: utf-8 -*-
"""
Interface utilisateur
MINI POO Jeu Match-3

Clotilde
"""




import tkinter as TK
import tkinter.ttk as TTK
import tkinter.filedialog as TKFD

import random #pour random.choice(liste)
import xml.etree.ElementTree as ET


#arbreXML = ET.parse("//Users//Eva//Desktop//Niveau1 - Reconnaissance de bonus.xml")
arbreXML = ET.parse("C:\\Users\\Clotilde\\OneDrive - ensam.eu\\MINI POO\\Données test (XML)\\Niveaux\\Niveau1 - Reconnaissance de bonus.xml")


tronc = arbreXML.getroot()




























liste_couleurs= ["green", "red", "yellow", "blue", "magenta"]
couleur_green       = "#0f0"
couleur_red         = "#f00"
couleur_yellow      = "#ff0"
couleur_blue        = "#00f"
couleur_magenta     = "#f0f"

#Element
icone_classique     = "🍬"
liste_couleurs      = ["green", "red", "yellow", "blue", "magenta"]
couleur_green       = "#0f0"
couleur_red         = "#f00"
couleur_yellow      = "#ff0"
couleur_blue        = "#00f"
couleur_magenta     = "#f0f"

icone_deflagrateur  = "💥"
icone_avion         = "✈"
icone_roquette      = "🚀"
icone_bombe         = "💣"
couleur_bonus       = "#000"

icone_etoile        = "★"
couleur_etoile      = "#ff0"

#Case
couleur_vide        = "#999"            #grisé
couleur_gelee       = "#99f"            #bleu clair
couleur_normale     = "#fff"            #blanc



class Interface():
    def __init__(self,ma_map):        
        self.fenetre = TK.Tk()
        self.fenetre.title("Jeu Match-3")
        
        #Création affichage du nom du niveau
        TK.Label(self.fenetre, text="Niveau :").grid(row=0, column=0, columnspan=2, sticky = 'w e n s', padx = 5, pady = 5)
        TK.Label(self.fenetre, text=la_map.son_titre).grid(row=0, column=2, columnspan=4, sticky = 'w e n s', padx = 5, pady = 5)
        
        #Bouton options (pour reset la partie)
        #pour ça il faut que le chargement XML soit dans une fonction
        #comme ça on relance le chargement XML quand on veut reset la partie
        
        #Affichage de l'avancement
        TK.Label(self.fenetre, text="Coups restants :").grid(row=1, column=0, columnspan=3, sticky = 'w e n s', padx = 5, pady = 5)
        TK.Label(self.fenetre, text=str(ma_map.coups_restants) + "/" + str(ma_map.son_nb_coups) ).grid(row=1, column=3, columnspan=3, sticky = 'w e n s', padx = 5, pady = 5)
        
        TK.Label(self.fenetre, text="Elements détruits:").grid(row=8, column=0, columnspan=3, sticky = 'w e n s', padx = 5, pady = 5)
        TK.Label(self.fenetre, text=str("objectifs d'éléments").grid(row=8, column=3, columnspan=3, sticky = 'w e n s', padx = 5, pady = 5)
        
        # TK.Label(self.fenetre, text="Boni activés:").grid(row=9, column=0, columnspan=3, sticky = 'w e n s', padx = 5, pady = 5)
        # TK.Label(self.fenetre, text="Boni activés").grid(row=9, column=3, columnspan=3, sticky = 'w e n s', padx = 5, pady = 5)
        
        # TK.Label(self.fenetre, text=("Etoiles dans un puits:").grid(row=10, column=0, columnspan=3, sticky = 'w e n s', padx = 5, pady = 5)
        # TK.Label(self.fenetre, text=str("objectifs d'étoiles").grid(row=10, column=3, columnspan=3, sticky = 'w e n s', padx = 5, pady = 5)
        
    
    
    

   
    # # bg is to change background, fg is to change foreground (technically the text color)
    # label = TK.Label(Fenetre, text=icone_bombe,
    #                  bg=couleur_gelee, fg=couleur_bonus, pady=10, padx=10, font=10) # You can use use color names instead of color codes.
    # label.pack()
    # click_here = TK.Button(Fenetre, text="click here to find out",
    #                        bg='#000', fg='#ff0', padx = 10, pady = 5)
    
    # click_here.pack()
   
