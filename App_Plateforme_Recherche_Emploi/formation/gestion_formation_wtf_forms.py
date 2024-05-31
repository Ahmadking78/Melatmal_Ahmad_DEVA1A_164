"""
    Fichier : gestion_formation_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""

from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *


class FormWTFAjouterformation(FlaskForm):
    """
        Form for adding a new formation.
    """
    ID_Formation = StringField("ID Formation")
    FK_Candidat = StringField("FK Candidat")
    Etablissement = StringField("Etablissement")
    Diplome = StringField("Diplome")
    Domaine = StringField("Domaine")
    Date_Debut = DateField("Date Début")
    Date_Fin = DateField("Date Fin")
    Description = TextAreaField("Description")
    submit = SubmitField("Enregistrer formation")



class FormWTFUpdateformation(FlaskForm):
    """
    Dans le formulaire "formation_update_wtf.html" on impose que le champ soit rempli.
    Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    ID_Formation = IntegerField("ID Formation")
    FK_Candidat = IntegerField("FK Candidat")
    Etablissement = StringField("Etablissement", validators=[InputRequired("Etablissement obligatoire")])
    Diplome = StringField("Diplome", validators=[InputRequired("Diplome obligatoire")])
    Domaine = StringField("Domaine", validators=[InputRequired("Domaine obligatoire")])
    Date_Debut = DateField("Date Debut", validators=[InputRequired("Date Debut obligatoire")])
    Date_Fin = DateField("Date Fin", validators=[InputRequired("Date Fin obligatoire")])
    Description = TextAreaField("Description", validators=[InputRequired("Description obligatoire")])
    submit = SubmitField("Update formation")



class FormWTFDeleteformation(FlaskForm):
    """
        Dans le formulaire "formation_delete_wtf.html"

        nom_formation_delete_wtf : Champ qui reçoit la valeur du formation, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "formation".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_formation".
    """
    nom_formation_delete_wtf = StringField("Effacer ce formation")
    submit_btn_del = SubmitField("Effacer formation")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
