"""
    Fichier : gestion_employeur_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""

from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *


class FormWTFAjouteremployeur(FlaskForm):
    """
        Dans le formulaire "employeur_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_employeur_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    ID_Employeur = StringField("ID Employeur")
    Nom_Entreprise = StringField("Nom de l'entreprise")
    Secteur = StringField("Secteur")
    Email = StringField("Email")
    Telephone = StringField("Téléphone")
    Adresse = StringField("Adresse")
    Description = TextAreaField("Description")
    submit = SubmitField("Enregistrer employeur")




class FormWTFUpdateemployeur(FlaskForm):
    """
        Dans le formulaire "employeur_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_employeur_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_employeur_update_wtf = StringField("Clavier le employeur ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_employeur_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    ID_Employeur = StringField("ID de l'employeur", validators=[Length(min=1, max=10, message="min 1 max 10")])
    Nom_Entreprise = StringField("Nom de l'entreprise", validators=[Length(min=2, max=50, message="min 2 max 50")])
    Secteur = StringField("Secteur", validators=[Length(min=2, max=50, message="min 2 max 50")])
    Email = StringField("Email", validators=[Length(min=6, max=50), Email(message="Adresse email invalide")])
    Telephone = StringField("Téléphone", validators=[Length(min=8, max=15, message="min 8 max 15")])
    Adresse = StringField("Adresse", validators=[Length(min=2, max=100, message="min 2 max 100")])
    Description = StringField("Description")
    submit = SubmitField("Update employeur")




class FormWTFDeleteemployeur(FlaskForm):
    """
        Dans le formulaire "employeur_delete_wtf.html"

        nom_employeur_delete_wtf : Champ qui reçoit la valeur du employeur, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "employeur".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_employeur".
    """
    nom_employeur_delete_wtf = StringField("Effacer ce employeur")
    submit_btn_del = SubmitField("Effacer employeur")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
