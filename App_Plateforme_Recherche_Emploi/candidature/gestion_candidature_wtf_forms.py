"""
    Fichier : gestion_candidature_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""

from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *


class FormWTFAjoutercandidature(FlaskForm):
    """
        Dans le formulaire "candidature_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    ID_Candidature = IntegerField("ID de la candidature")
    FK_Candidat = IntegerField("FK du candidat")
    FK_Offre = IntegerField("FK de l'offre")
    Date_Candidature = DateField("Date de la candidature")
    Lettre_Motivation = TextAreaField("Lettre de motivation")
    Statut = StringField("Statut")
    submit = SubmitField("Enregistrer candidature")





class FormWTFUpdatecandidature(FlaskForm):
    ID_Candidature = StringField("ID Candidature")
    FK_Candidat = StringField("FK Candidat")
    FK_Offre = StringField("FK Offre")
    Date_Candidature = DateField("Date Candidature")
    Lettre_Motivation = StringField("Lettre Motivation")
    Statut = StringField("Statut")
    submit = SubmitField("Update candidature")





class FormWTFDeletecandidature(FlaskForm):
    """
        Dans le formulaire "candidature_delete_wtf.html"

        nom_candidature_delete_wtf : Champ qui reçoit la valeur du candidature, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "candidature".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_candidature".
    """
    nom_candidature_delete_wtf = StringField("Effacer ce candidature")
    submit_btn_del = SubmitField("Effacer candidature")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
