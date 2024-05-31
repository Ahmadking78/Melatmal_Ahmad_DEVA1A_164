"""
    Fichier : gestion_competence_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""

from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *


class FormWTFAjoutercompetence(FlaskForm):
    """
    Form for adding a competence.
    """
    nom_competence_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    ID_Competence = StringField("ID Competence")
    nom_competence_wtf = StringField("Nom du competence", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                     Regexp(nom_competence_regexp,
                                                                            message="Pas de chiffres, de caractères "
                                                                                    "spéciaux, "
                                                                                    "d'espace à double, de double "
                                                                                    "apostrophe, de double trait union")
                                                                     ])
    description_competence = TextAreaField("Description")
    submit = SubmitField("Enregistrer competence")
    


class FormWTFUpdatecompetence(FlaskForm):
    ID_Competence_update_wtf = IntegerField("ID du competence")
    nom_competence_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    Nom_Competence_update_wtf = StringField("Clavier le competence", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                             Regexp(nom_competence_update_regexp,
                                                                                    message="Pas de chiffres, de caractères "
                                                                                            "spéciaux, "
                                                                                            "d'espaces à double, de double "
                                                                                            "apostrophe, de double trait "
                                                                                            "d'union")
                                                                             ])
    Description_competence_update_wtf = TextAreaField("Description du competence")
    submit = SubmitField("Update competence")




class FormWTFDeletecompetence(FlaskForm):
    """
        Dans le formulaire "competence_delete_wtf.html"

        nom_competence_delete_wtf : Champ qui reçoit la valeur du competence, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "competence".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_competence".
    """
    nom_competence_delete_wtf = StringField("Effacer ce competence")
    submit_btn_del = SubmitField("Effacer competence")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
