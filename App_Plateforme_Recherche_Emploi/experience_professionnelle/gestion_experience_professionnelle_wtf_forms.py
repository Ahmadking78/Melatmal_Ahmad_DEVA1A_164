"""
    Fichier : gestion_experience_professionnelle_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""

from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *




class FormWTFAjouterexperience_professionnelle(FlaskForm):
    """
        Dans le formulaire "experience_professionnelle_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    ID_Experience = StringField("ID de l'expérience")
    FK_Candidat = StringField("FK du candidat")
    Entreprise = StringField("Nom de l'entreprise")
    Titre_Poste = StringField("Titre du poste")
    Date_Debut = DateField("Date de début")
    Date_Fin = DateField("Date de fin")
    Description = StringField("Description")
    submit = SubmitField("Enregistrer l'expérience professionnelle")




class FormWTFUpdateexperience_professionnelle(FlaskForm):
    """
    Form for updating professional experience information.
    """

    ID_Experience = StringField("ID Experience")
    FK_Candidat = StringField("FK Candidat")
    Entreprise = StringField("Entreprise")
    Titre_Poste = StringField("Titre Poste")
    Date_Debut = DateField("Date Debut")
    Date_Fin = DateField("Date Fin")
    Description = StringField("Description")

    submit = SubmitField("Update experience_professionnelle")



class FormWTFDeleteexperience_professionnelle(FlaskForm):
    """
        Dans le formulaire "experience_professionnelle_delete_wtf.html"

        nom_experience_professionnelle_delete_wtf : Champ qui reçoit la valeur du experience_professionnelle, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "experience_professionnelle".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_experience_professionnelle".
    """
    nom_experience_professionnelle_delete_wtf = StringField("Effacer ce experience_professionnelle")
    submit_btn_del = SubmitField("Effacer experience_professionnelle")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
